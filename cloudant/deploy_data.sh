export IAM_API_KEY=""
export COUCH_URL=""

echo "==== Checking dependencies ===="
npm list -g | grep couchimport || npm install -g couchimport --no-shrinkwrap

echo "Using credentials: $IAM_API_KEY for $COUCH_URL"

echo "==== Installing dealerships.json ===="
cat ./data/dealerships.json | couchimport --url --type "json" --jsonpath "dealerships.*" --database dealerships

echo "==== Installing reviews.json ===="
cat ./data/reviews.json | couchimport --type "json" --jsonpath "reviews.*" --database reviews

echo "==== Installing reviews_full.json ===="
cat ./data/reviews-full.json | couchimport --type "json" --jsonpath "reviews.*" --database reviews


