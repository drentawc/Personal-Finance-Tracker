
# Python script to create plot and to upload to imgur for use in google sheets.

from glob import glob
import os
import numpy as np
import matplotlib.pyplot as plt
#import imgurpython


#Unused currently
import base64
import json
import requests

from base64 import b64decode

# @TODO Make a method to check if images directory exists and create it if not


class Plot:

    def __init__(self, data, name):

        self.data = data
        #self.config = config
        self.name = name

        self.imageDir = os.getcwd() + "/finance_tracker/static/"


        self.imageName = "{0}{1}".format(self.imageDir, self.name)

        self.checkImageDirectory()
        #self.removeImages()


        #self.imgurClient = imgurpython.ImgurClient(self.config["client_id"], self.config["client_secret"])



    def createExpenseChart(self, figureTitle):

        #print(self.data.head())

        #Get labels and data from passed dict, exclude first element which is total amount
        labels = list(self.data.keys())
        data = [abs(x) for x in list(self.data.values())]
        #data.sort(reverse=True)


        myexplode = []
        for ind,val in enumerate(data):
            if ind == 0:
                myexplode.append(0.05)
            else:
                myexplode.append(0.1)
        #data = list(self.data.values())

        print(labels)
        print(data)
        
        # color = []
        # for label in labels:

        # print(labels)

        #Figsize of 7.5 seems to be the best middle ground of resolution to readability, 10 add more info but with increased resolution appears blurry on google sheets, can maybe
        # look into compressing these images before uploading to imgur / gsheets to see if it would have any benefit to image quality

        fig = plt.figure(figsize=(10,10))

        plt.title(figureTitle)

        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['savefig.dpi'] = 300

        print("made it here ")

        plt.pie(data, autopct='%.0f%%', pctdistance=0.9, explode=myexplode, startangle=90)


        plt.legend(labels, title="Transaction Type", loc='lower right', bbox_to_anchor=(1.1, -0.1))#bbox_to_anchor=(1, 1), loc=1, borderaxespad=0)

        #plt.subplots_adjust(left=0.1, bottom=0.1, right=0.75)

        #plt.setp(autotexts, size=8, weight="bold")

        #plt.axis('equal')

        print(self.imageName)

        plt.savefig(self.imageName)



    #Need to add to update same link of image 
    # def uploadToImgur(self):

    #     client = imgurpython.ImgurClient(self.config['client_id'], self.config["client_secret"])#, self.config['access_token'], self.config['refresh_token'])

    #     asd = client.upload_from_path(self.imageName, anon=False)

    #     return asd['link']


    def removeImages(self):

        for file in glob(self.imageDir + "*"):
            os.remove(file)

        print("Files deleted.")

    def checkImageDirectory(self):
        
        if not os.path.exists(self.imageDir):
            os.mkdir(self.imageDir)


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
