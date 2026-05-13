from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view

from apps.info.models import Souvenir, App, Advertisement
from apps.info.serializers import (
    SouvenirSerializer,
    AppSerializer,
    AdvertisementSerializer,
)


@extend_schema_view(
    list=extend_schema(
        tags=['Souvenirs'],
        summary='List souvenir shops',
        description='Returns all souvenir shops/items available in Almaty.',
    ),
    retrieve=extend_schema(
        tags=['Souvenirs'],
        summary='Get souvenir details',
        description='Returns full details of a single souvenir entry.',
    ),
)
class SouvenirViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for souvenir shops and items."""

    queryset = Souvenir.objects.all()
    serializer_class = SouvenirSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    list=extend_schema(
        tags=['Apps'],
        summary='List useful apps',
        description='Returns all useful mobile apps and services recommended for tourists.',
    ),
    retrieve=extend_schema(
        tags=['Apps'],
        summary='Get app details',
        description='Returns full details of a single app/service listing.',
    ),
)
class AppViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for useful mobile apps and services."""

    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    list=extend_schema(
        tags=['Advertisements'],
        summary='List active advertisements',
        description=(
            'Returns all active advertisements/banners, '
            'ordered by priority (highest first).'
        ),
    ),
    retrieve=extend_schema(
        tags=['Advertisements'],
        summary='Get advertisement details',
        description='Returns full details of a single advertisement, including translations.',
    ),
)
class AdvertisementViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset for active promotional advertisements."""

    serializer_class = AdvertisementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Advertisement.objects.filter(is_active=True).prefetch_related(
            'translations'
        ).order_by('-priority')


# ── Translator proxy ──────────────────────────────────────────────

import logging
import requests as http_requests
from decouple import config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import extend_schema, inline_serializer

logger = logging.getLogger(__name__)

GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"
MAX_TEXT_LENGTH = 2000


class TranslateView(APIView):
    """Proxy endpoint for Google Cloud Translation API v2."""

    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "translate"

    @extend_schema(
        tags=["Translator"],
        summary="Translate text",
        description=(
            "Proxies a translation request to the Google Cloud Translation API. "
            "Text is limited to 2 000 characters."
        ),
        request=inline_serializer(
            name="TranslateRequest",
            fields={
                "text": serializers.CharField(help_text="Text to translate (max 2000 chars)"),
                "source": serializers.CharField(
                    required=False,
                    default="auto",
                    help_text="Source language code or 'auto'",
                ),
                "target": serializers.CharField(help_text="Target language code, e.g. 'ru'"),
            },
        ),
        responses={
            200: inline_serializer(
                name="TranslateResponse",
                fields={
                    "translatedText": serializers.CharField(),
                    "detectedSourceLanguage": serializers.CharField(required=False),
                },
            ),
        },
    )
    def post(self, request):
        text = (request.data.get("text") or "").strip()
        source = (request.data.get("source") or "auto").strip()
        target = (request.data.get("target") or "").strip()

        # --- validation ---
        if not text:
            return Response(
                {"error": "Text is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(text) > MAX_TEXT_LENGTH:
            return Response(
                {"error": f"Text must be at most {MAX_TEXT_LENGTH} characters."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not target:
            return Response(
                {"error": "Target language is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        api_key = config("GOOGLE_TRANSLATE_API_KEY", default="")
        if not api_key:
            logger.error("GOOGLE_TRANSLATE_API_KEY is not configured.")
            return Response(
                {"error": "Translation service is not configured."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        # --- call Google API ---
        params = {
            "q": text,
            "target": target,
            "format": "text",
            "key": api_key,
        }
        if source and source != "auto":
            params["source"] = source

        try:
            resp = http_requests.post(GOOGLE_TRANSLATE_URL, data=params, timeout=10)
            resp.raise_for_status()
        except http_requests.RequestException as exc:
            logger.exception("Google Translate API error")
            error_detail = "Translation service unavailable."
            if hasattr(exc, "response") and exc.response is not None:
                try:
                    error_detail = exc.response.json().get("error", {}).get(
                        "message", error_detail
                    )
                except Exception:
                    pass
            return Response(
                {"error": error_detail},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        data = resp.json()
        translation = data["data"]["translations"][0]
        return Response(
            {
                "translatedText": translation["translatedText"],
                "detectedSourceLanguage": translation.get(
                    "detectedSourceLanguage", source
                ),
            },
            status=status.HTTP_200_OK,
        )
