#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import json

from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


def main(dict):
    databaseName = "reviews"

    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )

        dealerId = dict.get("dealerId", str())

        db = client[databaseName]
        dealers = []

        data = db
        dealerId = dealerId.strip('"')

        if dealerId:
            data = filter(lambda r: r['dealership'] == int(dealerId), data)

        for document in data:

            dealers.append({
                "id": document["id"],
                "name": document.get("name", str()),
                "dealership": document.get("dealership", str()),
                "review": document.get("review", str()),
                "purchase": document.get("purchase", str()),
                "purchase_date": document.get("purchase_date", str()),
                "car_make": document.get("car_make", str()),
                "car_model": document.get("car_model", str()),
                "car_year": document.get("car_year", str())
            })

        return {
            "result": dealers
        }
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}
