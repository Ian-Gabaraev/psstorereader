import re

EXTERNAL = {
    "host": 'https://store.playstation.com',
    "product": 'https://store.playstation.com/ru-ru/product/',
    "ftp home": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-FREETOPLAYSEEALL/1',
    "ftp": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-FREETOPLAYSEEALL/%d',
    "soon home": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-COMINGSOON/1',
    "soon": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-COMINGSOON/%d',
    "top sellers home": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-GAMETOPSELLERS/1',
    "top sellers": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-GAMETOPSELLERS/%d',
    "store_homepage":
        'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PS4CAT/1?platform=ps4',
    "new_games_homepage":
        'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-GAMELATEST/1?platform=ps4',
    "latest": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-GAMELATEST/%d',
    "all": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PS4CAT/%d?platform=ps4',
    "ps plus": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PLUSINSTANTGAME/1',
    "discounts": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PRICEDROPSCHI/1?platform=ps4',
    "discounts homepage": 'https://store.playstation.com/ru-ru/grid/STORE-MSF75508-PRICEDROPSCHI/%d?platform=ps4',
}

SPECS = {
    "languages": ['немецкий', 'норвежский', 'финский', 'шведский',
                          'русский', 'португальский', 'английский', 'итальянский',
                          'французский', 'испанский', 'арабский', 'польский',
                          'датский', 'Турецкий', 'нидерландский', 'китайский (упрощ. письмо)'],

    "genres": ['Боевик', 'Приключения', 'Гонки', 'Аркада', 'Ужасы', 'Пазлы',
                       'Симуляторы', 'Спорт', 'Семейные', 'Казуальные',
                       'Ролевые игры', 'Тусовка', 'Стратегия',
                       'Единоборства', 'Шутер', 'MUSIC/RHYTHM', 'Уникальные']
}

SELECTORS = {
    "lp full": {'class': 'paginator-control__end'},
    "lp new games": {'class': 'paginator-control__end'},
    "collect ng": {'href': re.compile(r'\/ru-ru\/product\/.*')},
    "collect full": {'href': re.compile(r'\/ru-ru\/product\/.*')},
    "ps plus container": {'class': 'grid-cell--game'},
    "ps plus link": {'class': 'internal-app-link'},
}

GAME_SELECTORS = {
    "title": {"data-qa": "mfe-game-title#name"},
    "publisher": {"data-qa": "mfe-game-title#publisher"},
    "category": {"class": "provider-info__list-item"},
    "price": {"data-qa": "mfeCtaMain#offer0#finalPrice"},
    "original_price": {"data-qa": "mfeCtaMain#offer0#originalPrice"},
    "previous price":  {"class": "price-display__strikethrough"},
    "psplus discount": {"class": "price-display__price__label"},
    "specs": {"class": "tech-specs__pivot-menus"},

    "voice": {"data-qa": "gameInfo#releaseInformation#voice-value"},
    "subtitles": {"data-qa": "gameInfo#releaseInformation#subtitles-value"},
    "genres": {"data-qa": "gameInfo#releaseInformation#genre-value"},
    "platforms": {"data-qa": "gameInfo#releaseInformation#platform-value"},
    "release": {"data-qa": "gameInfo#releaseInformation#releaseDate-value"},
    "description": {"data-qa": "mfe-game-overview#description"},
    "rating": {"data-qa": "mfe-content-rating#ratingImage#image"},
    "in_game_purchases": {"class": "psw-icon--in-game-purchases"},
    "ps_pro_support": {"class": "psw-icon--ps4"},
    "online_gaming": {"class": "psw-icon--online-play"},
    "ps_plus_required": {"class": "psw-icon--ps-plus-flat"},
    "preorder": {"data-track-click": "ctaWithPrice:preOrder"},
    "cover_picture": "div.psw-layer > span.psw-media-frame > img",

}


PATTERNS = {
    "lp full": re.compile('\/(\d{3})\?'),
    "lp new games": re.compile('\/(\d{1})\?'),
    "lp discounts": re.compile('\/(\d{2})\?'),
    "lp top sellers": re.compile('\/(\d{1})'),
}
