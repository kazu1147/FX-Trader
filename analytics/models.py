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
    
    @property
    def middle(self):
        return (self.bid + self.ask) / 2

    @property
    def truncateTime(self):
        time = self.datetime
        # 1minでtruncate
        time_truncate_1m = time.replace(second=0, microsecond=0)
        return time_truncate_1m


class Ticker_Minute_USD_JPY(models.Model):
    time = models.DateTimeField(verbose_name="時間", null=False, blank=False)
    open = models.FloatField(verbose_name="始値", null=False, blank=False)
    close = models.FloatField(verbose_name="終値", null=False, blank=False)
    high = models.FloatField(verbose_name="最高値", null=False, blank=False)
    low = models.FloatField(verbose_name="最低値", null=False, blank=False)
    volume = models.IntegerField(verbose_name="ティック数", null=False, blank=False)
    
    def __str__(self):
        return f"{self.time}-{self.open}-{self.close}-{self.high}-{self.low}-{self.volume}"

