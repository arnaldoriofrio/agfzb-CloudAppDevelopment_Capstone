#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
def main(params):

    import json
    from ibmcloudant.cloudant_v1 import Document, CloudantV1
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_cloud_sdk_core import ApiException

    try:
        #print(params)
        authenticator = IAMAuthenticator(params['CLOUDANT_APIKEY'])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(params['CLOUDANT_URL'])
        
        reviews_doc = Document(
        #id=params['id'],
        name=params['name'],
        dealership=params['dealership'],
        review=params['review'],
        purchase=params['purchase'],
        purchase_date=params['purchase_date'],
        car_make=params['car_make'],
        car_model=params['car_model'],
        car_year=params['car_year'])
        
        response = service.post_document(db='reviews', document=reviews_doc).get_result()
        #print(response)
        #return reviews_doc
        
        return response

#    try:
#        authenticator = IAMAuthenticator('l5LNBMImpBgQmrLUmuqlCmG4w0ZbnbP7-8Prd48hVzZl')
#        service = CloudantV1(authenticator=authenticator)
#        service.set_service_url('https://c4a1e7aa-3d04-493c-897d-f71e393bbeb1-bluemix.cloudantnosqldb.appdomain.cloud')
#        
#        data=service.post_all_docs(db="reviews", include_docs=True).get_result()
#        dealerId=15
#        dealerId = dealerId.strip('"') if type(dealerId) == str else dealerId
        
#        if dealerId:
#            response = list(filter(lambda r: r['doc']['dealership'] == dealerId, data['rows']))
        
#        return {
#            "body": {"rows":response}
#        }

    except ApiException as ae:
        print("Method failed")
        print(" - status code: " + str(ae.code))
        print(" - error message: " + ae.message)
        if ("reason" in ae.http_response.json()):
            print(" - reason: " + ae.http_response.json()["reason"])

