/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */

/**
 * Get all dealerships
 */
async function main(params) {
    
    const { CloudantV1 } = require('@ibm-cloud/cloudant');
    const { IamAuthenticator } = require('ibm-cloud-sdk-core');

	/*return { body: {'message':'Hello World '}};*/

     
    const state = params.state;
    const dealerId = params.dealerId


    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
    const cloudant = CloudantV1.newInstance({ authenticator: authenticator});
    cloudant.setServiceUrl(params.COUCH_URL);

    try {
         const dealerships = await cloudant.postAllDocs({db: 'dealerships',  includeDocs: true})
         if(state) {
             let matriz=dealerships.result.rows
             let dict=matriz.filter(x=>x.doc.state==state)
             cuerpo={ body: { rows: dict} }
         }
         else if(dealerId) {
             let matriz=dealerships.result.rows
             let dict=matriz.filter(x=>x.doc.id==Number(dealerId))
             cuerpo={ body: { rows: dict} }
         }
         else {     
            let dict=dealerships.result
            cuerpo={ body: dict }
         }        
         return cuerpo
         
     } catch (error) {
         console.log(error)
         return { error: error.description };
         
    }
     
}
