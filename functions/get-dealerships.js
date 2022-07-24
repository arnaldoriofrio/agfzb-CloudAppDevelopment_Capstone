/**
 * Get all dealerships
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      /*
      *try {
      *  let db = await cloudant.use("dealerships");
      *  let ldealerships = await db.list({include_docs: true})
      *
      * return { ldealerships };
      *} catch (error) {
      *    return { error: error.description };
      *}
      */
     const state = params.state;
     const dealerId = params.dealerId

     try {
         const db = await cloudant.use('dealerships');
         const dealerships = await db.list({include_docs: true})

         if(state) {
             let filter = state.replace(/"/g, '');
             dealerships.rows = dealerships.rows.filter(({doc}) => doc.state === filter )
         }

         if(dealerId) {
             let filter = Number(dealerId)
             dealerships.rows = dealerships.rows.filter(({doc}) => doc.id === filter )
         }

         return {
             result: dealerships.rows.map(({doc}) => ({
                 id: doc.id,
                 city: doc.city,
                 state: doc.state,
                 st: doc.st,
                 address: doc.address,
                 zip: doc.zip,
                 lat: doc.lat,
                 long: doc.long,
                 short_name: doc.short_name,
                 full_name: doc.full_name
             }))
         };
     } catch (error) {
         console.log(error)
         return { error: error.description };
     }
      
}
