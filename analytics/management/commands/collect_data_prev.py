from datetime import datetime, timedelta

import pytz
from django.core.management import BaseCommand
from django.utils.timezone import make_aware
from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory

from analytics.models import Ticker, Ticker_Minute_USD_JPY
from constants import PRODUCT_CODE, ENVIRONMENT, ACCESS_TOKEN


utc = pytz.timezone('Utc')
tokyo = pytz.timezone('Asia/Tokyo')
class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = ''

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout=None, stderr=None, no_color=False, force_color=False)
        self.api = API(environment=ENVIRONMENT, access_token=ACCESS_TOKEN)
        self.ticker_1min = Ticker_Minute_USD_JPY()
        # self.ticker_1min.time = None

    def add_arguments(self, parser):
        parser.add_argument('-o', '--option', type=str, nargs='+')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        utc = pytz.timezone('Utc')

        start = options['option'][0]
        end = options['option'][1]
        granularity = 'M1'

        start = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S') - timedelta(hours=9)
        end = datetime.strptime(end, '%Y-%m-%dT%H:%M:%S') - timedelta(hours=9)

        start = datetime.strftime(start, '%Y-%m-%dT%H:%M:%SZ')
        end = datetime.strftime(end, '%Y-%m-%dT%H:%M:%SZ')

        params = {
            "from": start,
            "to": end,
            "granularity": granularity
        }

        self.res = []
        for r in InstrumentsCandlesFactory(instrument=PRODUCT_CODE, params=params):
            self.api.request(r)
            candle_lst = r.response.get('candles')
            candle_lst = list(map(self.candle_dic_to_ticker_obj, candle_lst))
            print(candle_lst)

    @staticmethod
    def candle_dic_to_ticker_obj(x: dict) -> Ticker_Minute_USD_JPY:
        return Ticker_Minute_USD_JPY(**{
            'time': str_localize(x['time']),
            'open': x['mid']['o'],
            'close': x['mid']['c'],
            'high': x['mid']['h'],
            'low': x['mid']['l'],
            'volume': x['volume']
        })


def str_localize(t: str):
    return utc.localize(datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.000000000Z')).astimezone(tokyo)
