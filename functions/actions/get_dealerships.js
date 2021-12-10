/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');

 async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });

     const state = params.state;

     try {
         const db = await cloudant.use('dealerships');
         const dealerships = await db.list({include_docs: true})

         if(state){
             let filter = state.replace(/"/g, '');
             dealerships.rows = dealerships.rows.filter(({doc}) => doc.state === filter )
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
                 long: doc.long
             }))
         };
     } catch (error) {
         return { error: error.description };
     }

 }