from django.contrib import admin

# Register your models here.
from .models import CarModel, CarMake

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    fields = ['name', 'year', 'car_make', 'dealer_id', 'type']
    
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
