import requests
import json
from .models import CarDealer, DealerReview

from requests.auth import HTTPBasicAuth


def post_request(url, json_payload=None, **kwargs):
    try:
        result = requests.post(url, params=kwargs, json=json_payload)

        if result:
            json_data = json.loads(result.text)
            return json_data
    except Exception as ex:
        print("Network exception occurred:\n" + str(ex))


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

            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=params, auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except Exception as ex:
        print("Network exception occurred:\n" + str(ex))

    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    result = get_request(url, **kwargs)

    if result:
        dealers = []
        json_data = result['result']
        for dealer in json_data:
            dealers.append(CarDealer().build_from(dealer))

        return dealers


def get_dealers_by_state_from_cf(url, state):
    result = get_request(url, state=state)
    return get_response_dealers(result)


def get_dealers_by_id_from_cf(url, id):
    result = get_request(url, dealerId=id)
    return get_response_dealers(result)[0]


def get_response_dealers(result):
    if result:
        dealers = []
        json_data = result['result']
        for dealer in json_data:
            dealers.append(CarDealer().build_from(dealer))

        return dealers


def get_dealer_reviews_from_cf(url, dealer_id):
    result = get_request(url, dealerId=dealer_id)

    if result:
        json_data = result['result']
        reviews = []

        for json_review in json_data:
            sentiment = analyze_review_sentiments(json_review['review'])
            review = DealerReview() \
                .build_from(json_review) \
                .with_sentiment(sentiment)

            reviews.append(review)

        return reviews


def analyze_review_sentiments(review_text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2191c73b-8d1d-4606-ba8e-a01418dbfa02/v1/analyze"
    api_key = "GAGc_iMCAd9FDzaXG3khyeJePs46ZuvG8k841ZVxqprt"

    result = get_request(url, text=review_text, features={"sentiment": {}}, version='2021-08-01',
                         return_analyzed_text=False, api_key=api_key)
    if result.get('sentiment', False):
        return result["sentiment"]["document"]["label"]
