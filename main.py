import logging
from datetime import datetime

import MetaTrader5 as mt
import pandas as pd

from utils import mt_connect

logger = logging.getLogger(__name__)


def get_symbol_data(symbol: str):
    df = pd.DataFrame(mt.copy_rates_from_pos(symbol, mt.TIMEFRAME_D1, 0, 120))
    df.time = pd.to_datetime(df.time, unit="s")
    return df


if __name__ == "__main__":
    with mt_connect():
        symbols = pd.Series([symbol.name for symbol in mt.symbols_get() if "Forex" in symbol.path])
        for symbol in symbols:
            data = get_symbol_data(symbol)
            metric = (data.low.iat[-1] - data.low.min()) / data.low.min() * 100
            # TODO: получить текущее значение рассчитать отклонение в 0,0016 (с запасом) и распечатывать сразу с ним;
            #  реализовать автоматическое открытие сделок
            if metric < 0.5:
                print(datetime.now(), symbol, metric)
