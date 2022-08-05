from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, analyze_review_sentiments, get_dealer_reviews_from_cf, get_dealers_by_id_from_cf, get_dealers_by_state_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
#

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html',context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html',context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login_bootstrap.html', context)
    else:
        return render(request, 'djangoapp/user_login_bootstrap.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration_bootstrap.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5a9cd3d9-02cb-4f48-bd18-cf9f0e61270e/string/get-dealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context={}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/5a9cd3d9-02cb-4f48-bd18-cf9f0e61270e/string/get-review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url,dealer_id)
        # Concat all dealer's short name
        # review_names = ' '.join([review.review for review in reviews])
        # Return a list of dealer short name
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        # query the cars with the dealer id to be reviewed. The queried cars will be used in the <select> dropdown.
        # Then append the queried cars into context and call render method to render add_review.html.
        cars={'carros'}
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        # When request.method ==POST , you need to update the json_payload["review"] to use the actual values 
        ## obtained from the review form.
        # For review time, you may use some Python datetime formatting method such as datetime.utcnow().isoformat() 
        ## to convert it into ISO format to be consistent with the format in
        # Cloudant. - For purchase, you may use car.year.strftime("%Y") to only get the year from the date field.
        # Update return statement to redirect user to the dealer details page once the review post is done for example.
        ## "redirect("djangoapp:dealer_details", dealer_id=dealer_id)"
        
        if request.user.is_authenticated:
            data = request.POST
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = data["review"]
            review["name"] = data["name"]
            review["purchase_date"] = data["purchasedate"]

            car = CarModel.objects.get(id=data["carmodel"])
            review["car_model"] = car.name
            review["car_year"] = car.year.year

            json_payload = dict()
            json_payload["review"] = review
            result = post_request(URLS["REVIEW"], json_payload, dealerId=dealer_id)

            context["post_result"] = result
            return HttpResponseRedirect(f"/djangoapp/dealer/{dealer_id}/")

