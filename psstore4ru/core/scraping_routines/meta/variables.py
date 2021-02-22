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

SELECTORS = {
    "lp full": {'class': 'paginator-control__end'},
    "lp new games": {'class': 'paginator-control__end'},
    "collect ng": {'class': 'ems-sdk-product-tile-link'},
    "collect full": {'href': re.compile(r'\/ru-ru\/product\/.*')},
    "ps plus container": {'class': 'grid-cell--game'},
    "ps plus link": {'class': 'internal-app-link'},

    "products": {'id': "__NEXT_DATA__"},
    "products_script_tag_opening": '[<script id="__NEXT_DATA__" type="application/json">',
    "products_script_tag_closing": '</script>]',

    "products_json_root": 'props',
    "products_json_root_descendant": 'apolloState',
    "category_grid_pattern": r'\'CategoryGrid:[\d\w\-]+\:ru-ru\:[\d]+\:[\d]+\'',
    "cusa_pattern": r'.*:(.*):ru-ru',
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
    "single_player": "Доступна автономная игра",
    "online_gaming": "Возможна игра в сети",
    "ps_plus_required": {"class": "psw-icon--ps-plus-flat"},
    "ps_vr_support": {"class": "psw-icon--psvr-pscamera"},
    "preorder": {"data-track-click": "ctaWithPrice:preOrder"},
    "cover_picture": "div.psw-layer > span.psw-media-frame > img",
}

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-RU,en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Host": "store.playstation.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  }
