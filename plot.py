
# Python script to create plot and to upload to imgur for use in google sheets.


import numpy as np
import matplotlib.pyplot as plt


class Plot:

    def __init__(self, data, config, name):

        self.data = data
        self.config = config
        self.name = name

        print(config['api_key'])



    def createExpenseChart(self):

        print(self.data)

        #Get labels and data from passed dict, exclude first element which is total amount
        labels = list(self.data.keys())[1:]
        data = [abs(x) for x in list(self.data.values())][1:]

        print(labels)

        print(data)

        fig = plt.figure(figsize=(10,7))

        plt.pie(data, labels=labels)

        plt.show()

        plt.savefig("{0}_expenses.png".format(self.name))




    def uploadToImgur(self):
        ""
