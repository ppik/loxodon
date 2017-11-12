from django.db import models


# Create your models here.
class LogoAnalyze (models.Model):
    logo_name_1 = models.CharField(max_length=200, default="Unknown")
    logo_name_2 = models.CharField(max_length=200, default="Unknown")
    logo_name_3 = models.CharField(max_length=200, default="Unknown")

    video = models.FileField(upload_to='videos', default="")

    precision_1 = models.CharField(max_length=20, default="0.0")
    precision_2 = models.CharField(max_length=20, default="0.0")
    precision_3 = models.CharField(max_length=20, default="0.0")
