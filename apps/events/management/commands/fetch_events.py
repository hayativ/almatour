# -*- coding: utf-8 -*-
"""
Management command to fetch event data from sxodim.com
and populate the Event / EventTranslation tables.

Usage:
    python manage.py fetch_events            # fetch from all categories
    python manage.py fetch_events --limit 10 # fetch at most 10 events
    python manage.py fetch_events --dry-run  # preview without saving

Designed to be run periodically (e.g. via cron every 6 hours):
    0 */6 * * * cd /path/to/project && python manage.py fetch_events
"""

from __future__ import annotations

import logging
import re
import time
from datetime import date, time as dtime
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup, Tag
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from apps.events.models import Event, EventTranslation

logger = logging.getLogger(__name__)

BASE_URL = "https://sxodim.com"
ALMATY_URL = f"{BASE_URL}/almaty"

# Category mapping: sxodim URL slug -> Event.Category int
CATEGORY_MAP: dict[str, int] = {
    "kontserty": 1,              # concerts
    "koncerty-v-everjazz": 1,    # EverJazz concerts
    "concerty-dvorec-respubliki": 1,  # Palace of Republic concerts
    "vystavki": 2,               # exhibitions
    "screening": 2,              # movie screenings
    "standup": 1,                # stand-up shows
    "vecherinki": 1,             # parties
    "teatr": 2,                  # theatre
    "razvlecheniya": 3,          # entertainment
    "detskie-meropriyatiya": 3,  # kids events
}

# Listing pages to scrape (most relevant categories)
LISTING_SLUGS = [
    "kontserty",
    "koncerty-v-everjazz",
    "concerty-dvorec-respubliki",
    "vystavki",
    "standup",
    "vecherinki",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
}

# Translation language IDs matching EventTranslation.Language choices
LANG_EN = 1
LANG_RU = 2
LANG_KZ = 3


class Command(BaseCommand):
    help = "Fetch events from sxodim.com and populate Event/EventTranslation tables"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Maximum number of events to fetch (0 = no limit)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview what would be fetched without saving to DB",
        )
        parser.add_argument(
            "--delay",
            type=float,
            default=1.0,
            help="Delay between HTTP requests in seconds (default: 1.0)",
        )

    def handle(self, *args: Any, **kwargs: Any) -> None:
        limit = kwargs["limit"]
        dry_run = kwargs["dry_run"]
        delay = kwargs["delay"]

        self.stdout.write(self.style.NOTICE("Fetching events from sxodim.com..."))

        session = requests.Session()
        session.headers.update(HEADERS)

        # Step 1: Collect event links from listing pages
        event_links: dict[str, int] = {}  # url -> category
        for slug in LISTING_SLUGS:
            category = CATEGORY_MAP.get(slug, 1)
            listing_url = f"{ALMATY_URL}/events/{slug}"
            self.stdout.write(f"  Scraping listing: {listing_url}")
            try:
                links = self._scrape_listing(session, listing_url)
                for link in links:
                    if link not in event_links:
                        event_links[link] = category
                self.stdout.write(f"    Found {len(links)} event links")
            except Exception as e:
                self.stderr.write(f"    Error scraping listing {listing_url}: {e}")
            time.sleep(delay)

        if limit > 0:
            # Limit the total number of events
            items = list(event_links.items())[:limit]
            event_links = dict(items)

        self.stdout.write(
            self.style.NOTICE(
                f"Total unique event links to process: {len(event_links)}"
            )
        )

        # Step 2: Scrape each event detail page
        created_count = 0
        updated_count = 0
        error_count = 0

        for event_url, category in event_links.items():
            try:
                event_data = self._scrape_event_detail(session, event_url, category)
                if event_data is None:
                    error_count += 1
                    continue

                if dry_run:
                    self.stdout.write(
                        f"  [DRY RUN] {event_data['artist']} | "
                        f"{event_data['date']} | {event_data['cost']} KZT"
                    )
                else:
                    was_created = self._save_event(event_data)
                    if was_created:
                        created_count += 1
                        self.stdout.write(
                            f"  [CREATED] {event_data['artist']}"
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            f"  [UPDATED] {event_data['artist']}"
                        )
            except Exception as e:
                error_count += 1
                self.stderr.write(
                    self.style.ERROR(f"  Error processing {event_url}: {e}")
                )
            time.sleep(delay)

        # Summary
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n[DRY RUN] Would process {len(event_links)} events "
                    f"({error_count} errors)"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nDone! Created: {created_count}, Updated: {updated_count}, "
                    f"Errors: {error_count}"
                )
            )

    # ------------------------------------------------------------------
    # Scraping helpers
    # ------------------------------------------------------------------

    def _fetch_page(self, session: requests.Session, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page and return parsed BeautifulSoup, or None on error."""
        try:
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except requests.RequestException as e:
            self.stderr.write(f"    HTTP error fetching {url}: {e}")
            return None

    def _scrape_listing(
        self, session: requests.Session, listing_url: str
    ) -> list[str]:
        """Extract event detail page URLs from a listing page."""
        soup = self._fetch_page(session, listing_url)
        if soup is None:
            return []

        event_links: list[str] = []

        # Strategy 1: Find links matching the event detail URL pattern
        # sxodim.com event detail URLs look like: /almaty/event/{slug}
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # Match event detail links: /almaty/event/some-slug
            if re.match(r"^(/almaty/event/[\w-]+)$", href):
                full_url = f"{BASE_URL}{href}"
                if full_url not in event_links:
                    event_links.append(full_url)
            elif re.match(
                r"^https?://sxodim\.com/almaty/event/[\w-]+$", href
            ):
                if href not in event_links:
                    event_links.append(href)

        return event_links

    def _scrape_event_detail(
        self,
        session: requests.Session,
        event_url: str,
        category: int,
    ) -> Optional[dict[str, Any]]:
        """Scrape an individual event detail page."""
        soup = self._fetch_page(session, event_url)
        if soup is None:
            return None

        # --- Extract event title ---
        title = self._extract_title(soup)
        if not title:
            self.stderr.write(f"    No title found for {event_url}")
            return None

        # --- Extract image ---
        image = self._extract_image(soup)

        # --- Extract date ---
        event_date = self._extract_date(soup)

        # --- Extract start time ---
        start_time = self._extract_time(soup)

        # --- Extract cost/price ---
        cost = self._extract_cost(soup)

        # --- Extract address ---
        address = self._extract_address(soup)

        # --- Extract description ---
        description = self._extract_description(soup, title)

        return {
            "image": image or "",
            "date": event_date or date.today(),
            "start_time": start_time or dtime(19, 0),
            "duration": 120,  # default, rarely available on the page
            "artist": title,
            "cost": cost,
            "currency": "KZT",
            "category": category,
            "address": address or "Алматы",
            "link": event_url,
            "name_ru": title,
            "description_ru": description or f"Мероприятие в Алматы. {title}.",
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract event title from the page."""
        # Try <h1>
        h1 = soup.find("h1")
        if h1:
            text = h1.get_text(strip=True)
            if text:
                return text

        # Try og:title meta tag
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()

        # Try <title> tag
        title_tag = soup.find("title")
        if title_tag:
            text = title_tag.get_text(strip=True)
            # Remove site name suffix
            text = re.sub(r"\s*\|\s*Давай Сходим!?\s*$", "", text)
            text = re.sub(r"\s*-\s*купить билеты.*$", "", text)
            if text:
                return text.strip()

        return ""

    def _extract_image(self, soup: BeautifulSoup) -> str:
        """Extract the main event image URL."""
        # Try og:image meta tag (most reliable)
        og_img = soup.find("meta", property="og:image")
        if og_img and og_img.get("content"):
            return og_img["content"]

        # Try finding image in the main content area
        # Look for large images (event banners)
        for img in soup.find_all("img"):
            src = img.get("src", "") or img.get("data-src", "")
            if src and ("uploads/posts" in src or "optimized" in src):
                if not src.startswith("http"):
                    src = f"{BASE_URL}{src}"
                return src

        return ""

    def _extract_date(self, soup: BeautifulSoup) -> Optional[date]:
        """Extract event date from the page."""
        text = soup.get_text()

        # Russian month names
        months_ru = {
            "января": 1, "февраля": 2, "марта": 3, "апреля": 4,
            "мая": 5, "июня": 6, "июля": 7, "августа": 8,
            "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12,
            "январь": 1, "февраль": 2, "март": 3, "апрель": 4,
            "май": 5, "июнь": 6, "июль": 7, "август": 8,
            "сентябрь": 9, "октябрь": 10, "ноябрь": 11, "декабрь": 12,
        }

        # Pattern: "20 февраля" or "20 февраля 2026"
        for month_name, month_num in months_ru.items():
            pattern = rf"(\d{{1,2}})\s+{re.escape(month_name)}(?:\s+(\d{{4}}))?[\s,.]"
            match = re.search(pattern, text)
            if match:
                day = int(match.group(1))
                year = int(match.group(2)) if match.group(2) else timezone.now().year
                try:
                    return date(year, month_num, day)
                except ValueError:
                    continue

        # Pattern: DD.MM.YYYY or DD.MM
        match = re.search(r"(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?", text)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3)) if match.group(3) else timezone.now().year
            try:
                return date(year, month, day)
            except ValueError:
                pass

        return None

    def _extract_time(self, soup: BeautifulSoup) -> Optional[dtime]:
        """Extract event start time from the page."""
        text = soup.get_text()

        # Pattern: "в 19:00" or "начало в 20:00" or just "19:00"
        match = re.search(r"(?:в|начало|время|старт)\s*:?\s*(\d{1,2})[:\.](\d{2})", text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            if 0 <= hour < 24 and 0 <= minute < 60:
                return dtime(hour, minute)

        # Standalone time pattern in typical event time range (15:00 - 23:00)
        times = re.findall(r"\b(\d{1,2})[:\.](\d{2})\b", text)
        for h_str, m_str in times:
            h, m = int(h_str), int(m_str)
            if 10 <= h <= 23 and 0 <= m < 60:
                return dtime(h, m)

        return None

    def _extract_cost(self, soup: BeautifulSoup) -> int:
        """Extract ticket price from the page."""
        text = soup.get_text()

        # Patterns: "от 5000 ₸", "5 000 тг", "от 3000", "5000 KZT"
        # Also handles space-separated thousands: "10 000"
        patterns = [
            r"(?:от|from|цена|стоимость|price)\s*:?\s*([\d\s]+)\s*(?:₸|тг|тенге|KZT|kzt)",
            r"([\d\s]+)\s*(?:₸|тг|тенге|KZT|kzt)",
            r"(?:от|from)\s+([\d\s]+)\b",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                price_str = match.group(1).replace(" ", "").strip()
                try:
                    price = int(price_str)
                    # Sanity check: event tickets are typically 500 - 500000 KZT
                    if 100 <= price <= 500000:
                        return price
                except ValueError:
                    continue

        return 0

    def _extract_address(self, soup: BeautifulSoup) -> str:
        """Extract venue / address from the page."""
        # Try common patterns in the page text
        text = soup.get_text()

        # Look for address patterns: "Место:", "Адрес:", "Площадка:", "Venue:"
        patterns = [
            r"(?:Место|Адрес|Площадка|Venue|Орын)\s*:?\s*(.+?)(?:\n|$)",
            r"(?:ул\.|пр\.|проспект|улица|Достык|Гоголя)[^,\n]{3,60}",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                addr = match.group(1) if match.lastindex else match.group(0)
                addr = addr.strip()
                if len(addr) > 5:
                    return addr[:200]  # cap length

        return ""

    def _extract_description(self, soup: BeautifulSoup, title: str) -> str:
        """Extract event description from the page."""
        # Try og:description
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            desc = og_desc["content"].strip()
            if len(desc) > 20:
                return desc

        # Try meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            desc = meta_desc["content"].strip()
            if len(desc) > 20:
                return desc

        return ""

    # ------------------------------------------------------------------
    # Database helpers
    # ------------------------------------------------------------------

    @transaction.atomic
    def _save_event(self, data: dict[str, Any]) -> bool:
        """
        Save or update an Event and its translations.
        Returns True if created, False if updated.
        """
        event, created = Event.objects.update_or_create(
            link=data["link"],
            defaults={
                "image": data["image"],
                "date": data["date"],
                "start_time": data["start_time"],
                "duration": data["duration"],
                "artist": data["artist"],
                "cost": data["cost"],
                "currency": data["currency"],
                "category": data["category"],
                "address": data["address"],
                "updated_at": timezone.now(),
                "deleted_at": None,
            },
        )

        # Create / update translations for all 3 languages
        name_ru = data["name_ru"]
        desc_ru = data["description_ru"]

        # Russian is the primary source; English and Kazakh get the same text
        # as baseline (can be enhanced with a translation API later)
        translations = [
            {
                "language_id": LANG_EN,
                "name": name_ru,      # baseline: Russian text
                "description": desc_ru,
            },
            {
                "language_id": LANG_RU,
                "name": name_ru,
                "description": desc_ru,
            },
            {
                "language_id": LANG_KZ,
                "name": name_ru,      # baseline: Russian text
                "description": desc_ru,
            },
        ]

        for tr in translations:
            EventTranslation.objects.update_or_create(
                event=event,
                language_id=tr["language_id"],
                defaults={
                    "name": tr["name"],
                    "description": tr["description"],
                },
            )

        return created
