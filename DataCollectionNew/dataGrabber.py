import requests
import json


class dataGrabber():
    def getAPICall(self, param):
        """
		This method will request an API call from the recipe API
        :param param: the URL ending which defines which api call is made
		:param payload: Payload text that will be sent to the API
		:return: Will return ether response or None if there is no result
		"""
        url = "http://www.themealdb.com/api/json/v2/9973533/"


        response = requests.request("GET", url+param)
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
