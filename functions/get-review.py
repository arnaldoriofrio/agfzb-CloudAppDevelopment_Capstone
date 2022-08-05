#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

#import sys

def main(params):

    import json
    from ibmcloudant.cloudant_v1 import CloudantV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_cloud_sdk_core import ApiException

    try:
        authenticator = IAMAuthenticator(params['CLOUDANT_APIKEY'])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(params['CLOUDANT_URL'])
        
        data=service.post_all_docs(db="reviews", include_docs=True).get_result()
        dealerId=params['dealerId']
        
        dealerId = int(dealerId) if type(dealerId) == str else dealerId
        
        if dealerId:
            response = list(filter(lambda r: r['doc']['dealership'] == dealerId, data['rows']))
        
        return {
            "body": {"rows":response}
            #"body": {"rows":data['rows']}
        }
    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])
