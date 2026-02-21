import { Injectable, signal } from '@angular/core';

export type Language = 'en' | 'ru' ;

export interface Translations {
  // Navbar
  nav: {
    home: string;
    paintings: string;
    favorites: string;
    about: string;
    login: string;
    profile: string;
    title: string;
  };
  // Home page
  home: {
    title: string;
    subtitle: string;
    exploreButton: string;
    featuredArtworks: string;
    loadingFeatured: string;
    aboutMuseum: string;
    aboutDescription: string;
    learnMore: string;
  };
  // About page
  about: {
    title: string;
    founded: string;
    artworks: string;
    whatMakesUsSpecial: string;
    planYourVisit: string;
    weekdays: string;
    weekends: string;
    ourMission: string;
    missionText: string;
    facts: {
      worldClass: { title: string; description: string };
      historic: { title: string; description: string };
      diverse: { title: string; description: string };
      educational: { title: string; description: string };
    };
  };
  // Login page
  login: {
    title: string;
    subtitle: string;
    email: string;
    emailPlaceholder: string;
    password: string;
    passwordPlaceholder: string;
    signIn: string;
    signingIn: string;
    noAccount: string;
    signUp: string;
  };
  // Signup page
  signup: {
    title: string;
    subtitle: string;
    email: string;
    emailPlaceholder: string;
    password: string;
    passwordPlaceholder: string;
    confirmPassword: string;
    confirmPasswordPlaceholder: string;
    passwordHint: string;
    signUp: string;
    creatingAccount: string;
    haveAccount: string;
    signIn: string;
    errors: {
      emailInvalid: string;
      passwordLength: string;
      passwordNumber: string;
      passwordSpecial: string;
      passwordMismatch: string;
    };
  };
  // Profile page
  profile: {
    title: string;
    changePhoto: string;
    uploading: string;
    memberSince: string;
    lastSignIn: string;
    emailVerified: string;
    emailNotVerified: string;
    signOut: string;
    browsePaintings: string;
    viewFavorites: string;
    userId: string;
  };
  // Paintings list
  paintings: {
    searchPlaceholder: string;
    viewCollection: string;
    itemsPerPage: string;
    loading: string;
    noData: string;
    showing: string;
    of: string;
    results: string;
    page: string;
    previous: string;
    next: string;
  };
  // Painting details
  paintingDetails: {
    backToList: string;
    loading: string;
    notFound: string;
    artist: string;
    date: string;
    medium: string;
    dimensions: string;
    department: string;
    origin: string;
    creditLine: string;
    viewOnArtic: string;
    addToFavorites: string;
    removeFromFavorites: string;
  };
  // Favorites page
  favorites: {
    title: string;
    loading: string;
    empty: string;
    emptyMessage: string;
    browsePaintings: string;
    count: string;
    remove: string;
    mergeSuccess: string;
  };
  // Footer
  footer: {
    ticketMessage: string;
    ticketButton: string;
    visitors: string;
    buyButton: string;
    paymentMessage: string;
  };
  // Offline page
  offline: {
    title: string;
    message: string;
    subtitle: string;
    cachedArtworks: string;
    cachedArtworksDesc: string;
    yourFavorites: string;
    yourFavoritesDesc: string;
    autoReconnect: string;
    autoReconnectDesc: string;
    tryAgain: string;
    viewFavorites: string;
    waitingConnection: string;
  };
  // Common
  common: {
    loading: string;
    error: string;
    save: string;
    cancel: string;
    delete: string;
    edit: string;
    close: string;
  };
}

const translations: Record<Language, Translations> = {
  en: {
    nav: {
      home: 'Home',
      paintings: 'Paintings',
      favorites: 'Favorites',
      about: 'About',
      login: 'Login',
      profile: 'Profile',
      title: 'Art Institute'
    },
    home: {
      title: 'Art Institute of Chicago',
      subtitle: 'Discover World-Class Art',
      exploreButton: 'Explore Collection',
      featuredArtworks: 'Featured Artworks',
      loadingFeatured: 'Loading featured artworks...',
      aboutMuseum: 'About the Museum',
      aboutDescription: 'The Art Institute of Chicago is one of the oldest and largest art museums in the United States, housing a collection of over 300,000 works of art.',
      learnMore: 'Learn More →'
    },
    about: {
      title: 'About the Art Institute of Chicago',
      founded: 'Founded',
      artworks: 'Artworks',
      whatMakesUsSpecial: 'What Makes Us Special',
      planYourVisit: 'Plan Your Visit',
      weekdays: 'Weekdays',
      weekends: 'Weekends',
      ourMission: 'Our Mission',
      missionText: 'The Art Institute of Chicago collects, preserves, and interprets works of art of the highest quality, representing the world\'s diverse artistic traditions, for the inspiration and education of the public and in accordance with our profession\'s highest ethical standards and practices.',
      facts: {
        worldClass: { title: 'World-Class Collection', description: 'Home to iconic works including Grant Wood\'s "American Gothic" and Georges Seurat\'s "A Sunday on La Grande Jatte"' },
        historic: { title: 'Historic Institution', description: 'Founded in 1879, the museum is one of the oldest and largest art museums in the United States' },
        diverse: { title: 'Diverse Exhibits', description: 'Features art spanning 5,000 years from cultures around the world, including paintings, sculptures, textiles, and more' },
        educational: { title: 'Educational Mission', description: 'Committed to inspiring curiosity and fostering understanding through art and education programs' }
      }
    },
    login: {
      title: 'Login',
      subtitle: 'Access your account',
      email: 'Email',
      emailPlaceholder: 'Enter your email',
      password: 'Password',
      passwordPlaceholder: 'Enter your password',
      signIn: 'Sign In',
      signingIn: 'Signing in...',
      noAccount: 'Don\'t have an account?',
      signUp: 'Sign up'
    },
    signup: {
      title: 'Sign Up',
      subtitle: 'Create your account',
      email: 'Email',
      emailPlaceholder: 'Enter your email',
      password: 'Password',
      passwordPlaceholder: 'Enter your password',
      confirmPassword: 'Confirm Password',
      confirmPasswordPlaceholder: 'Confirm your password',
      passwordHint: 'Must be at least 8 characters with 1 number and 1 special character',
      signUp: 'Sign Up',
      creatingAccount: 'Creating account...',
      haveAccount: 'Already have an account?',
      signIn: 'Sign in',
      errors: {
        emailInvalid: 'Please enter a valid email address',
        passwordLength: 'Password must be at least 8 characters',
        passwordNumber: 'Password must contain at least one number',
        passwordSpecial: 'Password must contain at least one special character',
        passwordMismatch: 'Passwords do not match'
      }
    },
    profile: {
      title: 'Profile',
      changePhoto: 'Change Photo',
      uploading: 'Uploading...',
      memberSince: 'Member since',
      lastSignIn: 'Last sign in',
      emailVerified: '✓ Email Verified',
      emailNotVerified: 'Email not verified',
      signOut: 'Sign Out',
      browsePaintings: 'Browse Paintings',
      viewFavorites: 'View Favorites',
      userId: 'User ID'
    },
    paintings: {
      searchPlaceholder: 'Search...',
      viewCollection: 'View collection',
      itemsPerPage: 'Items per page:',
      loading: 'Loading paintings...',
      noData: 'No data yet. Click the button',
      showing: 'Showing',
      of: 'of',
      results: 'results',
      page: 'Page',
      previous: '« Previous',
      next: 'Next »'
    },
    paintingDetails: {
      backToList: '← Back to list',
      loading: 'Loading painting details...',
      notFound: 'Painting not found',
      artist: 'Artist',
      date: 'Date',
      medium: 'Medium',
      dimensions: 'Dimensions',
      department: 'Department',
      origin: 'Place of Origin',
      creditLine: 'Credit Line',
      viewOnArtic: 'View on Art Institute Website',
      addToFavorites: 'Add to Favorites',
      removeFromFavorites: 'Remove from Favorites'
    },
    favorites: {
      title: 'My Favorites',
      loading: 'Loading your favorites...',
      empty: 'No favorites yet',
      emptyMessage: 'Start exploring paintings and add some to your favorites!',
      browsePaintings: 'Browse Paintings',
      count: 'painting(s) saved',
      remove: '♥ Remove',
      mergeSuccess: 'Your local favorites have been merged with your account!'
    },
    footer: {
      ticketMessage: 'Click to add ticket',
      ticketButton: 'Add',
      visitors: 'Visitors',
      buyButton: 'Buy tickets',
      paymentMessage: 'We\'ll send payment to your email'
    },
    offline: {
      title: 'You\'re Offline',
      message: 'It looks like you\'ve lost your internet connection.',
      subtitle: 'Don\'t worry, you can still browse cached content!',
      cachedArtworks: 'Cached Artworks',
      cachedArtworksDesc: 'Previously viewed paintings are still available',
      yourFavorites: 'Your Favorites',
      yourFavoritesDesc: 'Access your saved favorites offline',
      autoReconnect: 'Auto-Reconnect',
      autoReconnectDesc: 'We\'ll restore full access when you\'re back online',
      tryAgain: 'Try Again',
      viewFavorites: 'View Favorites',
      waitingConnection: 'Waiting for connection...'
    },
    common: {
      loading: 'Loading...',
      error: 'An error occurred',
      save: 'Save',
      cancel: 'Cancel',
      delete: 'Delete',
      edit: 'Edit',
      close: 'Close'
    }
  },
  ru: {
    nav: {
      home: 'Главная',
      paintings: 'Картины',
      favorites: 'Избранное',
      about: 'О музее',
      login: 'Войти',
      profile: 'Профиль',
      title: 'Институт Искусств'
    },
    home: {
      title: 'Институт Искусств Чикаго',
      subtitle: 'Откройте для себя мировое искусство',
      exploreButton: 'Исследовать коллекцию',
      featuredArtworks: 'Избранные произведения',
      loadingFeatured: 'Загрузка избранных произведений...',
      aboutMuseum: 'О музее',
      aboutDescription: 'Институт Искусств Чикаго — один из старейших и крупнейших художественных музеев США, коллекция которого насчитывает более 300 000 произведений искусства.',
      learnMore: 'Узнать больше →'
    },
    about: {
      title: 'Об Институте Искусств Чикаго',
      founded: 'Основан',
      artworks: 'Экспонатов',
      whatMakesUsSpecial: 'Что делает нас особенными',
      planYourVisit: 'Планируйте визит',
      weekdays: 'Будние дни',
      weekends: 'Выходные',
      ourMission: 'Наша миссия',
      missionText: 'Институт Искусств Чикаго собирает, сохраняет и интерпретирует произведения искусства высочайшего качества, представляющие разнообразные художественные традиции мира, для вдохновения и образования публики в соответствии с высочайшими этическими стандартами и практиками нашей профессии.',
      facts: {
        worldClass: { title: 'Мировая коллекция', description: 'Здесь хранятся знаковые работы, включая «Американскую готику» Гранта Вуда и «Воскресный день на острове Гранд-Жатт» Жоржа Сёра' },
        historic: { title: 'Историческое учреждение', description: 'Основанный в 1879 году, музей является одним из старейших и крупнейших художественных музеев США' },
        diverse: { title: 'Разнообразные выставки', description: 'Представлено искусство 5000 лет из культур со всего мира, включая картины, скульптуры, текстиль и многое другое' },
        educational: { title: 'Образовательная миссия', description: 'Стремимся вдохновлять любознательность и способствовать пониманию через искусство и образовательные программы' }
      }
    },
    login: {
      title: 'Вход',
      subtitle: 'Войдите в свой аккаунт',
      email: 'Эл. почта',
      emailPlaceholder: 'Введите эл. почту',
      password: 'Пароль',
      passwordPlaceholder: 'Введите пароль',
      signIn: 'Войти',
      signingIn: 'Выполняется вход...',
      noAccount: 'Нет аккаунта?',
      signUp: 'Зарегистрироваться'
    },
    signup: {
      title: 'Регистрация',
      subtitle: 'Создайте аккаунт',
      email: 'Эл. почта',
      emailPlaceholder: 'Введите эл. почту',
      password: 'Пароль',
      passwordPlaceholder: 'Введите пароль',
      confirmPassword: 'Подтвердите пароль',
      confirmPasswordPlaceholder: 'Подтвердите пароль',
      passwordHint: 'Минимум 8 символов, 1 цифра и 1 спецсимвол',
      signUp: 'Зарегистрироваться',
      creatingAccount: 'Создание аккаунта...',
      haveAccount: 'Уже есть аккаунт?',
      signIn: 'Войти',
      errors: {
        emailInvalid: 'Введите корректный адрес эл. почты',
        passwordLength: 'Пароль должен содержать минимум 8 символов',
        passwordNumber: 'Пароль должен содержать хотя бы одну цифру',
        passwordSpecial: 'Пароль должен содержать хотя бы один спецсимвол',
        passwordMismatch: 'Пароли не совпадают'
      }
    },
    profile: {
      title: 'Профиль',
      changePhoto: 'Изменить фото',
      uploading: 'Загрузка...',
      memberSince: 'Участник с',
      lastSignIn: 'Последний вход',
      emailVerified: '✓ Почта подтверждена',
      emailNotVerified: 'Почта не подтверждена',
      signOut: 'Выйти',
      browsePaintings: 'Смотреть картины',
      viewFavorites: 'Избранное',
      userId: 'ID пользователя'
    },
    paintings: {
      searchPlaceholder: 'Поиск...',
      viewCollection: 'Смотреть коллекцию',
      itemsPerPage: 'На странице:',
      loading: 'Загрузка картин...',
      noData: 'Данных пока нет. Нажмите кнопку',
      showing: 'Показано',
      of: 'из',
      results: 'результатов',
      page: 'Страница',
      previous: '« Назад',
      next: 'Далее »'
    },
    paintingDetails: {
      backToList: '← Вернуться к списку',
      loading: 'Загрузка информации о картине...',
      notFound: 'Картина не найдена',
      artist: 'Художник',
      date: 'Дата',
      medium: 'Техника',
      dimensions: 'Размеры',
      department: 'Отдел',
      origin: 'Место происхождения',
      creditLine: 'Источник',
      viewOnArtic: 'Смотреть на сайте музея',
      addToFavorites: 'Добавить в избранное',
      removeFromFavorites: 'Удалить из избранного'
    },
    favorites: {
      title: 'Моё избранное',
      loading: 'Загрузка избранного...',
      empty: 'Пока ничего нет',
      emptyMessage: 'Начните исследовать картины и добавляйте их в избранное!',
      browsePaintings: 'Смотреть картины',
      count: 'картин(а) сохранено',
      remove: '♥ Удалить',
      mergeSuccess: 'Ваше локальное избранное объединено с аккаунтом!'
    },
    footer: {
      ticketMessage: 'Нажмите, чтобы добавить билет',
      ticketButton: 'Добавить',
      visitors: 'Посетителей',
      buyButton: 'Купить билеты',
      paymentMessage: 'Мы отправим данные оплаты на вашу почту'
    },
    offline: {
      title: 'Вы офлайн',
      message: 'Похоже, вы потеряли интернет-соединение.',
      subtitle: 'Не волнуйтесь, вы всё ещё можете просматривать кэшированный контент!',
      cachedArtworks: 'Кэшированные работы',
      cachedArtworksDesc: 'Ранее просмотренные картины всё ещё доступны',
      yourFavorites: 'Ваше избранное',
      yourFavoritesDesc: 'Доступ к сохранённому избранному офлайн',
      autoReconnect: 'Авто-переподключение',
      autoReconnectDesc: 'Мы восстановим полный доступ, когда вы вернётесь онлайн',
      tryAgain: 'Попробовать снова',
      viewFavorites: 'Смотреть избранное',
      waitingConnection: 'Ожидание соединения...'
    },
    common: {
      loading: 'Загрузка...',
      error: 'Произошла ошибка',
      save: 'Сохранить',
      cancel: 'Отмена',
      delete: 'Удалить',
      edit: 'Редактировать',
      close: 'Закрыть'
    }
  },
};

@Injectable({
  providedIn: 'root'
})
export class TranslationService {
  private readonly STORAGE_KEY = 'app_language';
  
  currentLanguage = signal<Language>(this.loadLanguage());
  translations = signal<Translations>(translations[this.currentLanguage()]);

  availableLanguages: { code: Language; name: string; flag: string }[] = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'ru', name: 'Русский', flag: '🇷🇺' },
  ];

  private loadLanguage(): Language {
    if (typeof localStorage !== 'undefined') {
      const stored = localStorage.getItem(this.STORAGE_KEY);
      if (stored && ['en', 'ru'].includes(stored)) {
        return stored as Language;
      }
      // Try to detect browser language
      const browserLang = navigator.language.split('-')[0];
      if (['en', 'ru'].includes(browserLang)) {
        return browserLang as Language;
      }
    }
    return 'en';
  }

  setLanguage(lang: Language): void {
    this.currentLanguage.set(lang);
    this.translations.set(translations[lang]);
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(this.STORAGE_KEY, lang);
    }
  }

  t<K extends keyof Translations>(section: K): Translations[K] {
    return this.translations()[section];
  }

  getTranslation(): Translations {
    return this.translations();
  }
}
