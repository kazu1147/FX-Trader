from django.core.management import BaseCommand

from analytics.models import Ticker, Ticker_Minute_USD_JPY
from constants import APIClient, ACCESS_TOKEN, ACCOUNT_ID, PRODUCT_CODE


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = ''

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout=None, stderr=None, no_color=False, force_color=False)
        self.api = APIClient(ACCESS_TOKEN, ACCOUNT_ID, PRODUCT_CODE)
        self.ticker_1min = Ticker_Minute_USD_JPY()
        self.ticker_1min.time = None

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        # リアルタイムでtickerデータを取得=>callbackでdbに格納
        self.api.get_realtime_ticker(callback=self.push_db)

    def push_db(self, ticker: Ticker):
        middle_val = ticker.middle
        # truncateした時間を取得 => 現状1minのみ
        time_val = ticker.truncateTime

        # 初期状態
        if self.ticker_1min.time is None:
            self.ticker_1min.time = time_val
            self.ticker_1min.open = middle_val
            self.ticker_1min.high = middle_val
            self.ticker_1min.low = middle_val
            self.ticker_1min.volume = 0
        # 同じtermの場合
        elif self.ticker_1min.time == time_val:
            if self.ticker_1min.high < middle_val:
                self.ticker_1min.high = middle_val
            if self.ticker_1min.low > middle_val:
                self.ticker_1min.low = middle_val
            self.ticker_1min.volume += 1
        # termが変化するタイミング
        else:
            self.ticker_1min.close = middle_val
            self.ticker_1min.volume += 1
            self.ticker_1min.save()
            print(self.ticker_1min)
            self.ticker_1min = Ticker_Minute_USD_JPY()
            self.ticker_1min.time = time_val
            self.ticker_1min.open = middle_val
            self.ticker_1min.high = middle_val
            self.ticker_1min.low = middle_val
            self.ticker_1min.volume = 0