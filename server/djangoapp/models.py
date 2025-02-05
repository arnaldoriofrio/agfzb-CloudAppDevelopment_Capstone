from django.db import models
from django.utils.timezone import now
from django.conf import settings

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"CarMake(name={self.name}, description={self.description})"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'

    TYPE_CHOICES = (
        (SEDAN, 'Sedan'),
        (SUV, 'Suv'),
        (WAGON, 'Wagon')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    dealer_id = models.IntegerField()
    year = models.DateField()
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPE_CHOICES, max_length=20)

    def __str__(self):
        return f"CarModel(name={self.name}, dealer_id={self.dealer_id})"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self):
        self.state = None
        self.zip = None
        self.st = None
        self.long = None
        self.lat = None
        self.id = None
        self.city = None
        self.address = None

    def build_from(self, json_data):
        self.address = json_data["address"]
        self.city = json_data["city"]
        self.id = json_data["id"]
        self.lat = json_data["lat"]
        self.long = json_data["long"]
        self.st = json_data["st"]
        self.zip = json_data["zip"]
        self.state = json_data["state"]

        return self

    def __str__(self):
        return "Dealer address: " + self.address


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self):
        self.dealership = None
        self.name = None
        self.purchase = None
        self.review = None
        self.purchase_date = None
        self.car_make = None
        self.car_model = None
        self.car_year = None
        self.sentiment = None
        self.id = None

    def build_from(self, json_data):
        self.dealership = json_data["dealership"]
        self.name = json_data["name"]
        self.purchase = json_data["purchase"]
        self.review = json_data["review"]
        self.purchase_date = json_data["purchase_date"]
        self.car_make = json_data["car_make"]
        self.car_model = json_data["car_model"]
        self.car_year = json_data["car_year"]
        self.id = json_data["id"]
        return self

    def with_sentiment(self, sentiment):
        self.sentiment = sentiment
        return self
    
# An instance of CarDealer is used as a plain data object returned from dealer-get service.
    
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model 
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
