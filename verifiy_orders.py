from datetime import timedelta, datetime

import MetaTrader5 as mt
import pandas as pd
from MetaTrader5 import TradeDeal

from utils import mt_connect

if __name__ == "__main__":
    with mt_connect():
        deals: tuple[TradeDeal] = mt.history_deals_get(datetime(2022, 3, 1), datetime.now() + timedelta(days=1))
        report, symbols = {}, set()
        for deal in deals:
            if deal.position_id not in report:
                report[deal.position_id] = [
                    deal.time,  # start_time
                    deal.price,  # start_price
                    deal.symbol  # symbol
                ]
                symbols.add(deal.symbol)
            else:
                report[deal.position_id] += [
                    deal.time,  # end_time
                    deal.price,  # end_price
                    deal.volume  # lots
                ]
        verified_symbols = pd.Series([symbol.name
                                      for symbol in mt.symbols_get(group=",".join(symbols))
                                      if "Forex" in symbol.path])
    report = pd.DataFrame([(position_id, *order_args)
                           for position_id, order_args in report.items() if len(order_args) == 6],
                          columns=("position_id", "start_time", "start_price", "symbol", "end_time", "end_price",
                                   "lots"))
    report["is_verified_time_delta"] = (report["end_time"] - report["start_time"]) > (60 * 60 * 2)
    report["is_verified_price_delta"] = (
            (report["start_price"] * 0.0015) < (report["end_price"] - report["start_price"]).abs()
    )
    report["is_verified_symbol"] = report["symbol"].isin(verified_symbols)
    print(report[report["is_verified_time_delta"] & report["is_verified_price_delta"] & report["is_verified_symbol"]
                 ]["lots"].sum())
    print(report.shape)
