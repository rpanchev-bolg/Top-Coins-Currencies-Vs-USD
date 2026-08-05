import requests
# from coingecko_sdk import Coingecko
import pprint


CRYPTO_MAP = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "solana": "Solana (SOL)",
    "binancecoin": "Binance Coin (BNB)",
    "ripple": "Ripple (XRP)"
}
ids_param = ",".join(CRYPTO_MAP.keys())
# url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd&x_cg_demo_api_key=CG-sMmSbNu6gga5rJfeFgFHfCU8"
url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"  #&per_page=250&page=1"
# url = "https://api.coingecko.com/api/v3/coins/list"

def parsing_data(data):
    print(f"{'Место в рейтинге':<16} : {'id':<30} : {'Наименование':<62} : "
          f"{'Буквенный код':<13} : {'Цена $'}")
    for coin in data:
        # if coin['symbol'] == 'xrp':
        name = (f"{coin['name'].strip()} ({coin['id'].strip().title()})"
                if (coin['id'].strip() not in coin['name'].strip().lower().replace(" ","-")
                    and len(coin['id'].strip()) < 26 and coin['id'] != coin['symbol'])
                else coin['name'].strip()
                )
        print(f"{coin['market_cap_rank'] if coin['market_cap_rank'] else '':<16}"
              f" : {coin['id'][:30].strip():<30} : {name[:62].strip():<62} : {coin['symbol'].upper():<13}"
              f" : {coin['current_price']:10,.2f}")
    # pprint(data, indent=4, width=30)
    # for coin_id, display_name in CRYPTO_MAP.items():
    #     if coin_id in data:
    #         price_usd = data[coin_id].get("usd", 0)
    #         # Форматируем цену: отделяем тысячи запятыми и оставляем 2 знака после запятой
    #         print(f"{display_name:<20} : $ {price_usd:,.2f}")
    #     else:
    #         print(f"{display_name:<20} : Данные отсутствуют")


# client = Coingecko(
#     demo_api_key='CG-sMmSbNu6gga5rJfeFgFHfCU8',
#     environment="demo",
# )

# response = client.simple.price.get(vs_currencies="usd",
#     ids="bitcoin",)


try:
    # Установка таймаута на случай проблем со связью
    # response = client.coins.markets.get(
    #     vs_currency="usd",
    # )
    response = requests.get(url, timeout=1000)
    response.raise_for_status()
    if response.status_code == 200:
        data = response.json()
        # data1 = data.copy()
        # data = {d['id']: d for d in data}
        # print(data)
        # pprint.pprint(data, indent=4)
        print(len(data))
        parsing_data(data)
    else:
        print(f"Ошибка API: код {response.status_code}")
except requests.exceptions.RequestException as e: (
        print(f"Ошибка сети: {str(e)}"))