from contextlib import contextmanager

import MetaTrader5 as mt


@contextmanager
def mt_connect(*args, **kwargs) -> mt:
    try:
        if not mt.initialize(*args, **kwargs):
            raise Exception(mt.last_error())
        yield mt
    finally:
        mt.shutdown()
