import requests
import json


class dataGrabber():
    def getAPICall(self, payload):
        """
		This method will request an API call from the recipe API
		:param payload: Payload text that will be sent to the API
		:return: Will return ether response or None if there is no result
		"""
        url = "https://recipe-by-api-ninjas.p.rapidapi.com/v1/recipe"

        querystring = {"query": payload}

        # TODO: Test if API Key also works for different setups
        headers = {
            "X-RapidAPI-Key": "7fcf65267cmsh61f9c42d02002edp17ea59jsn6560c0c2ec6e",
            "X-RapidAPI-Host": "recipe-by-api-ninjas.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.text == "[]":
            response = None
        return response

    def convert(self, response):
        """
		This method will convert the API response from string to dict
		:param response: Response from the API
		:return: Will return the converted response
		"""
        if response == None:
            result = ["Could not find Recipe"]
        else:
            result = json.loads(response.text)
        return result
    # Get every Key in dict:
    # print(result[0].keys())
