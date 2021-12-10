from django.db import models
from django.utils.timezone import now

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"CarMake(name={self.name}, description={self.description})"


class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'

    TYPE_CHOICES = (
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon')
    )

    name = models.CharField(max_length=20)
    dealer_id = models.IntegerField()
    year = models.DateField()
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE_CHOICES, max_length=20)

    def __str__(self):
        return f"CarModel(name={self.name}, dealer_id={self.dealer_id})"


class Car(models.Model):
    pass

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
