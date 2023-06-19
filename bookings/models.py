from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class VaccinationCenter(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    from_time = models.TimeField()
    to_time = models.TimeField()

    def __str__(self):
        return self.name

class VaccinationSlot(models.Model):
    center = models.ForeignKey(VaccinationCenter, on_delete=models.CASCADE)
    date = models.DateField()
    available_slots = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.center} - {self.date}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(VaccinationSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.slot}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slot.available_slots = self.slot.available_slots - self.slot.booking_set.count()
        self.slot.save()

