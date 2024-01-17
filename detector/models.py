# Create your models here.
from django.db import models

class FraudDetection(models.Model):
    step = models.IntegerField()
    types = models.IntegerField()
    amount = models.FloatField()
    oldbalanceorig = models.FloatField()
    newbalanceorig = models.FloatField()
    oldbalancedest = models.FloatField()
    newbalancedest = models.FloatField()
    isflaggedfraud = models.FloatField()

    def __str__(self):
        return f"{self.id} - {self.types}"

class ImagePrediction(models.Model):
    image = models.ImageField(upload_to='images/')
    prediction = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.image} - {self.prediction}"