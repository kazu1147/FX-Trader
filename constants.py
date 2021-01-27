import configparser
from datetime import datetime

import dateutil
from django.utils.timezone import localtime, make_aware
from oandapyV20 import API
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20.exceptions import V20Error

from analytics.models import Ticker

conf = configparser.ConfigParser()
conf.read('settings.ini')

ENVIRONMENT = conf["os"]["environment"]
ACCESS_TOKEN = conf["oanda"]["access_token"]
ACCOUNT_ID = conf["oanda"]["account_id"]
PRODUCT_CODE = conf["oanda"]["product_code"]


class APIClient(object):
    def __init__(self, access_token, account_id, product_code, environment=ENVIRONMENT):
        self.access_token = access_token
        self.account_id = account_id
        self.product_code = product_code
        self.client = API(access_token=access_token, environment=environment)

    # realtimeでtickerを取得
    def get_realtime_ticker(self, callback):
        req = PricingStream(accountID=self.account_id, params={'instruments': self.product_code})
        try:
            for resp in self.client.request(req):
                if resp["type"] == "PRICE":
                    # tickerオブジェクトの作成
                    # product_code, timestamp, bid, ask, volume

                    # instruments
                    instrument = resp["instrument"]

                    # str -> datetime
                    timestamp = resp["time"]
                    timestamp = make_aware(datetime.strptime(timestamp.split('.')[0], '%Y-%m-%dT%H:%M:%S').now())

                    bid = float(resp["bids"][0]["price"])
                    ask = float(resp["asks"][0]["price"])

                    volume = 1
                    ticker = Ticker(product_code=instrument, datetime=timestamp, bid=bid, ask=ask, volume=volume)
                    # callbackにtickerを渡す->mainに用意したcallback関数が都度呼ばれる
                    callback(self, ticker)

        except V20Error as e:
            raise