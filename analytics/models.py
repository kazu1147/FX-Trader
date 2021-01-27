from django.db import models
from django.utils import timezone


# Create your models here.
from django.utils.timezone import localtime


class Ticker(models.Model):
    product_code = models.CharField(verbose_name="通貨ペア", max_length=32, null=False, blank=False)
    datetime = models.DateTimeField(verbose_name="日付時間", null=False, blank=False, default=timezone.now)
    bid = models.FloatField(verbose_name="売値", null=False, blank=False)
    ask = models.FloatField(verbose_name="売値", null=False, blank=False)
    volume = models.IntegerField(verbose_name="ティック数", null=False, blank=False)

    def __str__(self):
        return f"{self.datetime}-{self.bid}-{self.ask}-{self.volume}/{self.product_code}"


class Ticker_Minute_USD_JPY(models.Model):
    time = models.DateTimeField(verbose_name="時間", null=False, blank=False)
    open = models.FloatField(verbose_name="始値", null=False, blank=False)
    close = models.FloatField(verbose_name="終値", null=False, blank=False)
    high = models.FloatField(verbose_name="最高値", null=False, blank=False)
    low = models.FloatField(verbose_name="最低値", null=False, blank=False)
    volume = models.IntegerField(verbose_name="ティック数", null=False, blank=False)
    
    # 区切りの良い時間(1m,5m,15m,30m,60m)でtruncateする
    '''@property
    def truncateTime(self):
        time = self.time
        time_truncate_1m = time.replace(second=0, microsecond=0)
        return time_truncate_1m


    # 2020-01-02 03:04:27
    # 2020-01-02 03:04:25(5s)
    # 2020-01-02 03:04:00(1M)
    # 2020-01-02 03:00:00(1H)

    @property
    def value(self):
        # {"bid","ask","time":{"1m", "5m", "15m", "30m", "60m"}}
        return dict(middle=(self.ask+self.bid)/2, time=self.truncateTime)'''
