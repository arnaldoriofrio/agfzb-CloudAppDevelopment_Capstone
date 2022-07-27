/**
 * Get all dealerships
 */
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests


async function main(params):
    const cloudant = Cloudant({
          url: params.COUCH_URL,
          plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

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


/*
const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
      const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY })
      const cloudant = CloudantV1.newInstance({
          authenticator: authenticator
      });
      cloudant.setServiceUrl(params.COUCH_URL);
      
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
*/
