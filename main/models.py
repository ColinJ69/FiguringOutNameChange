from django.db import models


class points_model(models.Model):
    user = models.CharField(max_length=20, primary_key=True)
    points = models.SmallIntegerField()
    
    def __str__(self):
        return self.user
        