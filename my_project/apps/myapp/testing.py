import requests
import json

business_id='edcdC4ixlSjPn50WdwSpBQ'

#Define the API Key, Define the Endpoint, and deefine the Header
API_KEY='JA-SJIs2e-2ib3JVAqmIMzlWPigODEw0Djc_oKehvjmuvI92e-t-lEmYlZCGW9W3T-En7RQLuTZ9ABm_wLADJ7tw65LamAIjqFiKRA76S7x1kpT6ubtcU1QxVrMSXXYx'
ENDPOINT='https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}


# Define the parameters
PARAMETERS = {'term' : 'breweries',
             'limit':50,
             'radius':10000,
             'location': 'Long Beach'}

response=requests.get(url= ENDPOINT,params=PARAMETERS,headers=HEADERS)

business_data=response.json()

for biz in business_data['business']:
    print(biz)