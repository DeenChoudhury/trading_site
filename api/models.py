from django.db import models

# Create your models here.
class AnalystRating(models.Model):
    date = models.DateField()
    ticker = models.CharField(max_length=5)
    company = models.CharField(max_length=30)
    action = models.CharField(max_length=30)
    brokerage = models.CharField(max_length=30)
    current = models.FloatField()
    target_original = models.FloatField()
    target_new = models.FloatField()
    rating = models.CharField(max_length=30)
    impact = models.CharField(max_length=30)
    percent_upside = models.IntegerField()

    def __str__(self):
        return str(self.date) + " " + str(self.ticker)
