from time import monotonic
from logging import getLogger

from faker import Faker

fake = Faker(locale='en_US')


def time_decorator(text, loger=getLogger(__name__)):
    def inner(func):
        def wrapper(*args, **kwargs):
            start_time = monotonic()
            result = func(*args, **kwargs)
            end_time = monotonic()
            loger.info(f"{text}: {end_time - start_time} секунд.")
            return result

        return wrapper

    return inner
