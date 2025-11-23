from django.db import models


class Emission(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField()
    emissions = models.DecimalField(max_digits=10, decimal_places=2)
    emission_type = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    activity = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.emission_type} - {self.country} ({self.year})"
