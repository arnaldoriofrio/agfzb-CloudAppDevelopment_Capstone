from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/components/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/components/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    post_data = request.POST
    user = authenticate(username=post_data['username'], password=post_data['password'])

    if user is not None:
        login(request, user)

    return HttpResponseRedirect('/djangoapp/')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return HttpResponseRedirect('/djangoapp/')


def registration_page(request):
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect('/djangoapp/')

        return render(request, 'djangoapp/components/signup.html', context)


def registration_request(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            data = request.POST
            first_name = data['firstname']
            last_name = data['lastname']
            password = data['password']
            username = data['username']

            user = User.objects.create_user(username, '', password)
            user.first_name = first_name
            user.last_name = last_name

            user.save()
            login(request, user)

        return HttpResponseRedirect('/djangoapp/')


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            context['username'] = request.user
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
