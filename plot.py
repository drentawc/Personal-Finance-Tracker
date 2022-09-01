
# Python script to create plot and to upload to imgur for use in google sheets.

import numpy as np
import matplotlib.pyplot as plt
import imgurpython

import base64
import json
import requests

from base64 import b64decode

# @TODO Make a method to check if images directory exists and create it if not


class Plot:

    def __init__(self, data, config, name):

        self.data = data
        self.config = config
        self.name = name

        self.workdir = "/home/will/code/Personal-Finance-Tracker/images/"



        self.imageName = "{0}{1}_expenses.png".format(self.workdir, self.name)


        #self.imgurClient = imgurpython.ImgurClient(self.config["client_id"], self.config["client_secret"])



    def createExpenseChart(self):

        print(self.data)

        #Get labels and data from passed dict, exclude first element which is total amount
        labels = list(self.data.keys())[1:]
        data = [abs(x) for x in list(self.data.values())][1:]

        print(labels)

        print(data)

        fig = plt.figure(figsize=(10,7))

        plt.pie(data, labels=labels)

        plt.savefig(self.imageName)




    def uploadToImgur(self):

        client = imgurpython.ImgurClient(self.config['client_id'], self.config["client_secret"], self.config['access_token'], self.config['refresh_token'])

        asd = client.upload_from_path(self.imageName, anon=False)

        print(asd)

        return asd['link']

    def checkImageDirectory(self):
        ""


        #MANUAL Way to upload but was receiving 400 error

        # headers = {"Authorization" : "Client-ID {0}".format(self.config["client_id"]) }

        # headers = eval('{"Authorization": "Client-ID ' + self.config["client_id"] + '"}')

        # print(headers)

        # api_key = self.config['access_token']

        # url = "https://api.imgur.com/3/upload"

        # request = requests.post(url, headers=headers, data = { 'image' : b64decode(open(self.imageName, 'rb').read()), 'type': 'base64'} )

        # print(request.content)

        # data = json.loads(data.text)['data']

        # print(data['link'])

        #uploadedImage = self.imgurClient.upload_image(self.imageName, title="test image")

        #print(uploadedImage.link)
