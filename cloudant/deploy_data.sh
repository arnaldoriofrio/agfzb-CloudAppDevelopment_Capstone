echo "==== Checking dependencies ===="
npm list -g | grep couchimport || npm install -g couchimport --no-shrinkwrap

echo "Using credentials: $IAM_API_KEY for $COUCH_URL"

echo "==== Installing dealerships.json ===="
cat ./data/dealerships.json | couchimport --type "json" --jsonpath "dealerships.*" --database dealerships

echo "==== Installing reviews.json ===="
cat ./data/reviews.json | couchimport --type "json" --jsonpath "reviews.*" --database reviews


