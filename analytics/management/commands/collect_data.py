from django.core.management import BaseCommand

from analytics.models import Ticker
from constants import APIClient, ACCESS_TOKEN, ACCOUNT_ID, PRODUCT_CODE


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = ''

    # コマンドライン引数を指定します。(argparseモジュール https://docs.python.org/2.7/library/argparse.html)
    # 今回は無し
    # def add_arguments(self, parser):
    # parser.add_argument('blog_id', nargs='+', type=int)

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        # product_codeを設定する(USD_JPY等)
        api = APIClient(ACCESS_TOKEN, ACCOUNT_ID, PRODUCT_CODE)

        # リアルタイムでtickerデータを取得=>callbackでdbに格納
        api.get_realtime_ticker(callback=self.push_db)

    @ staticmethod
    def push_db(self, ticker: Ticker):
        # truncateする => まずは1min
        print(ticker)