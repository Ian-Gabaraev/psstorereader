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
    "cover": "div.large-3 > div.pdp__"
             "thumbnail-img > div.product-image > "
             "div.product-image__img > "
             "div.product-image__img--main > img",
    "title": {"class": "pdp__title"},
    "publisher": {"class": "provider-info__text"},
    "category": {"class": "provider-info__list-item"},
    "price": {"class": "price-display__price"},
    "previous price":  {"class": "price-display__strikethrough"},
    "psplus discount": {"class": "price-display__price__label"},
    "specs": {"class": "tech-specs__pivot-menus"},
    "description": {"class": "pdp__description"},
}


PATTERNS = {
    "lp full": re.compile('\/(\d{3})\?'),
    "lp new games": re.compile('\/(\d{1})\?'),
    "lp discounts": re.compile('\/(\d{2})\?'),
    "lp top sellers": re.compile('\/(\d{1})'),
}
