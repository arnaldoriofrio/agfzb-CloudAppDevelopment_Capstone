import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    api_key = kwargs.get("api_key", None)
    print("GET from {} with params {}".format(url, str(kwargs)))
    response = None
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]

            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except Exception as ex:
        print("Network exception occurred:\n" + str(ex))

    #json_data = json.loads(response.text)
    return response.text

    #print(kwargs)
    #print("GET from {} ".format(url))
    #try:
        # Call get method of requests library with URL and parameters
    #    response = requests.get(url, headers={'Content-Type': 'application/json'},
    #                                params=kwargs)
    #except:
        # If any error occurs
    #    print("Network exception occurred")
    #status_code = response.status_code
    #print("With status {} ".format(status_code))
    #return response.text
     
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
#def post_request(url, json_payload=None, **kwargs):
def post_request(url, json_payload, **kwargs):
    try:
        result = requests.post(url, params=kwargs, json=json_payload)

        if result:
            json_data = json.loads(result.text)
            return json_data
    except Exception as ex:
        print("Network exception occurred:\n" + str(ex))

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    dict_result = json.loads(get_request(url))
    if dict_result:
        # Get the row list in JSON as dealers
        dealers = dict_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    dict_result = json.loads(get_request(url,dealerId=dealerId))
    if dict_result:
        # Get the row list in JSON as dealers
        reviews = dict_result["rows"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review["doc"]
            sentiment = analyze_review_sentiments(review_doc['review'])
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   review=review_doc["review"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"], car_year=review_doc["car_year"], id=review_doc["id"],sentiment=sentiment)
            results.append(review_obj)

    return results
   
# def get_dealer_by_id_from_cf(url, dealerId):
def get_dealers_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    dict_result = json.loads(get_request(url, dealerId))
    if dict_result:
        # Get the row list in JSON as dealers
        dealers = dict_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# def get_dealer_by_state_from_cf(url, dealerId):
def get_dealers_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    dict_result = json.loads(get_request(url, state))
    if dict_result:
        # Get the row list in JSON as dealers
        dealers = dict_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(review_text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/2e43f859-6933-4546-b73f-c5c31a390746/v1/analyze"
    api_key = "uhyOWqpZooV0Q-9f1xPSbg2dz9jjyfSdDhm1A-vU6jWI"
    
    result = json.loads(get_request(url, text=review_text, features={"sentiment": {}}, version='2021-08-01',
                         return_analyzed_text=False, api_key=api_key))
    if result.get('sentiment', False):
        return result["sentiment"]["document"]["label"]
