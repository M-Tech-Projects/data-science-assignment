import requests
from requests.auth import HTTPBasicAuth

## Sample API calling function structure
class Api:
    def get_api_data(self):
        url = 'http://mobility427-outpost.trybmc.com:1026/'
        api = '/api/version'
        username = 'swpadmin'
        password = 'J2ee911pw'
        auth = HTTPBasicAuth(username, password)
        response = {'',''}
        try:
            response = requests.get(url + api, auth)
        except:
            print('No Internet')
        self.res = response.json()

        print(self.res)

api = Api()
api.get_api_data()