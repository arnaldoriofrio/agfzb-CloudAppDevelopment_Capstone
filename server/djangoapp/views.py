import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, analyze_review_sentiments, get_dealer_reviews_from_cf, \
    get_dealers_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

URLS = {
    "DEALERSHIPS": "https://ee46738b.eu-gb.apigw.appdomain.cloud/api/dealership",
    "REVIEW": "https://ee46738b.eu-gb.apigw.appdomain.cloud/api/review"
}


def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/components/about.html', context)


def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/components/contact.html', context)


def login_request(request):
    post_data = request.POST
    user = authenticate(username=post_data['username'], password=post_data['password'])

    if user is not None:
        login(request, user)

    return HttpResponseRedirect('/djangoapp/')


def add_review_request(request, dealer_id):
    context = {}
    if request.method == "POST":
        if request.user.is_authenticated:
            data = request.POST
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = data["review"]
            review["name"] = data["name"]
            review["car_model"] = data["carmodel"]

            json_payload = dict()
            json_payload["review"] = review
            result = post_request(URLS["REVIEW"], json_payload, dealerId=dealer_id)

            context["post_result"] = result
            return HttpResponseRedirect(f"/djangoapp/dealer/{dealer_id}/")


def add_review_page(request, dealer_id):
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            context["dealer_id"] = dealer_id
            return render(request, 'djangoapp/components/add_review.html', context)
        else:
            return HttpResponseRedirect(f"/djangoapp/dealer/{dealer_id}")


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


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            context['username'] = request.user

        url = URLS["DEALERSHIPS"]
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships

        return render(request, 'djangoapp/components/dealers.html', context)


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        with ThreadPoolExecutor(max_workers=4) as executor:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            methods = [(get_dealer_reviews_from_cf, URLS["REVIEW"]), (get_dealers_by_id_from_cf, URLS["DEALERSHIPS"])]
            tasks = [
                loop.run_in_executor(
                    executor,
                    functools.partial(method[0], method[1], dealer_id),
                    *()
                )
                for method in methods
            ]

            result = loop.run_until_complete(asyncio.gather(*tasks))

            reviews = result[0]
            dealer = result[1]

            context["dealer"] = dealer
            context["reviews"] = reviews
            return render(request, 'djangoapp/components/dealer_details.html', context)
