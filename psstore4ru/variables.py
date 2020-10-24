import re

EXTERNAL = {
    "host": 'https://store.playstation.com',
    "product": 'https://store.playstation.com/ru-ru/product/',
    "vr": 'https://store.playstation.com/ru-ru/category/95239ca7-2dcf-43d9-8d4b-b7672ee9304a/%d',
    "f2p": 'https://store.playstation.com/ru-ru/category/5c30b111-b867-4037-8f42-5b3db18d8e20/%d',
    "soon": 'https://store.playstation.com/ru-ru/category/be9cf690-90de-4772-b09e-b327fc82c5c5/%d',
    "latest": 'https://store.playstation.com/ru-ru/category/12a53448-199e-459b-956d-074feeed2d7d/%d',
    "all": 'https://store.playstation.com/ru-ru/category/44d8bb20-653e-431e-8ad0-c0a365f68d2f/%d',
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
    "collect ng": {'class': 'ems-sdk-product-tile-link'},
    "collect full": {'href': re.compile(r'\/ru-ru\/product\/.*')},
    "ps plus container": {'class': 'grid-cell--game'},
    "ps plus link": {'class': 'internal-app-link'},
}

GAME_SELECTORS = {
    "title": {"data-qa": "mfe-game-title#name"},
    "publisher": {"data-qa": "mfe-game-title#publisher"},
    "price": {"data-qa": "mfeCtaMain#offer0#finalPrice"},
    "original_price": {"data-qa": "mfeCtaMain#offer0#originalPrice"},
    "voice": {"data-qa": "gameInfo#releaseInformation#voice-value"},
    "subtitles": {"data-qa": "gameInfo#releaseInformation#subtitles-value"},
    "genres": {"data-qa": "gameInfo#releaseInformation#genre-value"},
    "platforms": {"data-qa": "gameInfo#releaseInformation#platform-value"},
    "release": {"data-qa": "gameInfo#releaseInformation#releaseDate-value"},
    "description": {"data-qa": "mfe-game-overview#description"},
    "rating": {"data-qa": "mfe-content-rating#ratingImage#image"},
    "in_game_purchases": {"class": "psw-icon--in-game-purchases"},
    "ps_pro_tuned": {"class": "psw-icon--ps4"},
    "online_gaming": {"class": "psw-icon--online-play"},
    "ps_plus_required": {"class": "psw-icon--ps-plus-flat"},
    "ps_vr_support": {"class": "psw-icon--psvr-pscamera"},
    "preorder": {"data-track-click": "ctaWithPrice:preOrder"},
    "cover_picture": "div.psw-layer > span.psw-media-frame > img",

}


PATTERNS = {
    "lp full": re.compile('\/(\d{3})\?'),
    "lp new games": re.compile('\/(\d{1})\?'),
    "lp discounts": re.compile('\/(\d{2})\?'),
    "lp top sellers": re.compile('\/(\d{1})'),
}
