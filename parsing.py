import requests
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings import API_URL


class Pair(CallbackData, prefix="callback_to_..."):
    symbol_from: str
    symbol_to: str = "USDT"

    def __str__(self) -> str:
        return f"{self.symbol_from}{self.symbol_to}"


# BUG: Функція повинна бути простою і тупою, без зайвих кроків і логіки!!!
def get_symbol_keyboard() -> None:
    data_base = [
        Pair(symbol_from="BTC"),
        Pair(symbol_from="ETH"),
        Pair(symbol_from="ALT"),
        Pair(symbol_from="SOL"),
        Pair(symbol_from="DOGE"),
        Pair(symbol_from="SHIB1000"),
        Pair(symbol_from="1000PEPE"),
        Pair(symbol_from="BNB"),
        Pair(symbol_from="ARB"),
        Pair(symbol_from="AVAX"),
        Pair(symbol_from="XPR"),
        Pair(symbol_from="MATIC"),
        Pair(symbol_from="GALA"),
        Pair(symbol_from="TON"),
    ]
    builder = InlineKeyboardBuilder()
    for data in data_base:
        builder.button(
            text=f"{data.symbol_from}{data.symbol_to}", callback_data=data.pack()
        )
    builder.adjust(3,3,3,3,2)
    return builder.as_markup()


# BUG: Функція повинна бути простою і тупою і НЕЗАЛЕЖНОЮ без зайвих кроків і логіки!!!
def get_price(pair: str, api_url: str = API_URL):
    url = f"{api_url}tickers?symbol={pair}"
    print(f"{url=}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"{data=}")
        info = data.get("result")[0]
        print(f"{info=}")
        name = info.get("symbol")
        price = info.get("last_price")
        return(f"The last price of: {name}={price}$")

    else:
        raise NotImplementedError(
            f"HTTP request failed with status code:{response.status_code}"
        )
