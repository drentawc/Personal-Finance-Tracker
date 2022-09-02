#
# Class to access Google drive, Google sheets and to format all different sheets.
#
#
#
# Plan : Could maybe have a raw data and formatted sheet, 
# Could set global variables for colors that are going to be used across the sheet
#

#from oauth2client.service_account import ServiceAccountCredentials

import pandas as pd
import gspread as gs

import gspread_formatting as gsformatting
from gspread_formatting import *

from datetime import datetime
from dateutil.relativedelta import relativedelta

#Unused right now
from df2gspread import df2gspread as d2g
from google.oauth2.service_account import Credentials

from plot import Plot

#from time import sleep
#import re

# Things to have:
# 
# Maybe pull from table in gsheet online and append to that table, if it overlaps then reformat cells to keep tables seperated 
#
#

class GSheet:


    #Initialize class
    def __init__(self, mint, config):

        print("Gsheet initialized.")

        #Set parameter variables
        self.mint = mint
        self.accountDB = {}
        self.config = config


        # CURRENTLY UNUSED
        #scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        #creds = Credentials.from_service_account_file(self.config["Google"]["json"], scopes=scope)
        #client = gspread.authorize(creds)


        #Set config Variables
        self.spreadsheetKey = self.config["Google"]["spreadsheet_key"]
        self.sheetName = self.config["Google"]["name"]
        self.json = self.config["Google"]["json"]


        #Currently working as of July 4th at 4 pm to create service account access
        self.client = gs.service_account(filename=self.json)

        #Initalize google sheet class variables
        self.sheet = self.open(self.sheetName)
        self.currentSheets = self.sheet.worksheets()
        self.currentSheetNames = self.getSheetNames()

        #Initialize formatting for class variables
        self.emptyBorder = gsformatting.Border( style='NONE', color=None, width=None, colorStyle=None )
        self.headerFormat = gsformatting.cellFormat(textFormat=textFormat( fontSize=14, fontFamily='Bree Serif', bold=True), horizontalAlignment='CENTER')
        self.bodyFormat = gsformatting.cellFormat(textFormat=textFormat( fontSize=12, fontFamily='Bree Serif', bold=False), horizontalAlignment='CENTER')

        self.generateAccountSheet()
        self.generateExpenseSheet()
        self.generateInvestmentSheet()

        #Generate all main sheets
        # try:
        #     self.generateAccountSheet()
        #     self.generateExpenseSheet()
        #     self.generateInvestmentSheet()

        #     self.sheet.reorder_worksheets( [self.accountSheet, self.expenseSheet, self.investmentSheet] )
        # except Exception as e:
        #     print("Quota limit probably reached")
        #     print(e)


        if mint != "":
            self.mint.mintAuth.close()


    #Generates account sheet 
    def generateAccountSheet(self):

        if self.checkSheet("Accounts"):

            self.accountSheet = self.sheet.get_worksheet_by_id(self.currentSheetNames['Accounts'])

            self.formatSheet(self.accountSheet)

            self.uploadAccounts(self.accountSheet)
        

    #Uploads all accounts to Account spreadsheet
    def uploadAccounts(self, spreadsheet):

        cell = "B14"

        for accounts in self.mint.accounts:


            range = "{0}:{1}".format(cell, chr(ord(cell[0]) + accounts.shape[1]) + cell[1:3])

            gsformatting.format_cell_ranges(spreadsheet, [(range, self.bodyFormat)])

            self.uploadDataframe(spreadsheet, cell, accounts)

            spreadsheet.batch_clear([range])

            spreadsheet.merge_cells(range)


            if "SAVINGS" in accounts['Type'].tolist()[0]:
                accountCell = "Savings Accounts"
            elif "CHECKING" in accounts['Type'].tolist()[0]:
                accountCell = "Checking Accounts"
            elif "Credit" in accounts['Type'].tolist()[0]:
                accountCell = "Credit Accounts"
            else:
                accountCell = "Investment Accounts"
                
            spreadsheet.update_acell(cell, accountCell)
            gsformatting.format_cell_ranges(spreadsheet, [(cell, self.headerFormat)])

            cell = "{0}{1}".format(cell[0], int(cell[1:3]) + accounts.shape[0] + 2)


    #Helper method to generate investment sheet in main spreadsheet
    def generateInvestmentSheet(self):

        if self.checkSheet("Investments"):
            self.investmentSheet = self.sheet.get_worksheet_by_id(self.currentSheetNames['Investments'])


    #Helper method to generate expenses sheet in main spreadsheet
    def generateExpenseSheet(self):

        if self.checkSheet("Expenses"):

            self.expenseCell = "C60"

            self.expenseSheet = self.sheet.get_worksheet_by_id(self.currentSheetNames['Expenses'])

            self.formatSheet(self.expenseSheet)

            self.uploadTransactions(self.expenseSheet, "Expenses", self.expenseCell)

            self.uploadPlots(self.expenseSheet)

    #Creates a Plot object to create pie charts, upload to imgur, and format on expenses sheet
    def uploadPlots(self, spreadsheet):

        for year in self.yearDict:

            if year == "2022":
                yearPlot = Plot(self.yearDict[year], self.config['Imgur'], year)

                yearPlot.createExpenseChart("Yearly Expenses")

                currentUrl = yearPlot.uploadToImgur()

                print(currentUrl)

                plotCell = "{0}{1}".format(self.expenseCell[0], int(self.yearCell[1:3])-27)

                print(plotCell)

                imageString = "=IMAGE(\"{0}\")".format(currentUrl)

                spreadsheet.merge_cells("{0}:{1}{2}".format(plotCell, "G", int(plotCell[1:3]) + 25))

                spreadsheet.update_acell(plotCell, imageString)

                print('Should be updated')

                






    #Format sheets differently depending on sheet name
    def formatSheet(self, spreadsheet):

        if spreadsheet.title == "Expenses":
            self.formatMargin(spreadsheet, ['{0}1:{1}'.format('A', 'B'), '{0}:{1}'.format('H', 'AD') ])
            self.formatHeader(spreadsheet, ['A{0}:G{0}'.format(1), 'A{0}:G{0}'.format(2), 'A{0}:G{0}'.format(3)])
            self.formatExpenseData(spreadsheet)

        elif spreadsheet.title == "Accounts":
            self.formatMargin(spreadsheet, ['{0}1:{0}'.format('A'), '{0}:{1}'.format('H', 'AD') ])
            self.formatHeader(spreadsheet, ['A{0}:G{0}'.format(1), 'A{0}:G{0}'.format(2), 'A{0}:G{0}'.format(3)])

        elif spreadsheet.title == "Investments":
            self.formatMargin(spreadsheet, ['{0}1:{0}'.format('A'), '{0}:{1}'.format('H', 'AD') ])
            self.formatHeader(spreadsheet, ['A{0}:G{0}'.format(1), 'A{0}:G{0}'.format(2), 'A{0}:G{0}'.format(3)])


    #Format data part of Expense Sheet
    def formatExpenseData(self, spreadsheet):
        gsformatting.set_column_width(spreadsheet, 'C:E', 150)
        gsformatting.set_column_width(spreadsheet, 'D', 250)
        gsformatting.set_column_width(spreadsheet, 'F', 200)
        gsformatting.set_column_width(spreadsheet, 'G', 340)

        for row in ['{0}10:{0}'.format('A'), '{0}:{1}'.format('C', 'G') ]:

            gsformatting.format_cell_ranges(spreadsheet, [(row, self.bodyFormat)])



    def uploadTransactions(self, spreadsheet, transactionType, startCell):

        if transactionType == 'Expenses':

            #Upload total
            self.uploadDataframe(spreadsheet, startCell, self.mint.creditTransactions)

            #Format to have last 6 months - last year worth of monthly spending, and then maybe also build a dict with totals of various categories

        
            endDate = datetime.today().strftime("%Y-%m")
            startDate = (datetime.strptime(endDate, "%Y-%m") - relativedelta(months=6)).strftime("%Y-%m")

            endYear = datetime.today().strftime("%Y-")
            startYear = (datetime.strptime(endDate, "%Y-%m") - relativedelta(months=12)).strftime("%Y-%m")


            self.yearDict = {}
            self.monthDict = {}


            firstCell = "{0}{1}".format(startCell[0], int(startCell[1:3]) + 1)


            #@TODO Might be best to add all of this dict creation to mint backend and store it as class variables, then can just upload self.mint.yearDict etc.


            listOfCells = spreadsheet.get_values('{0}:G{1}'.format(firstCell,  int(startCell[1:3]) + self.mint.creditTransactions.shape[0]))


            for row in listOfCells:

                #Only keep track of charges
                if "-" in row[2]:

                    #Append certain categories together 
                    if row[3] == "Air Travel" or row[3] == "Vacation" or row[3] == "Hotel" or row[3] == "Public Transportation" or row[3] == "Parking" \
                        or row[3] == "Ride Share" or row[3] == "Travel":
                        key = "Travel/Vacation"
                    elif row[3] == "Restaurants" or row[3] == "Food & Dining" or row[3] == "Alcohol & Bars" or row[3] == "Coffee Shops" or row[3] == "Fast Food":
                        key = "Food/Drinks"
                    elif row[3] == "Shopping" or row[3] == "Clothing" or row[3] == "Electronics & Software" or row[3] == "Hobbies" or row[3] == "Gift" \
                        or row[3] == "Mobile Phone" or row[3] == "Sporting Goods":
                        key = "Shopping"
                    elif row[3] == "Entertainment" or row[3] == "Music" or row[3] == "Books":
                        key = "Entertainment"
                    elif row[3] == "Business Services" or row[3] == "Doctor" or row[3] == "Child Support" or row[3] == "Uncategorized" or row[3] == "Bank Fee" or row[3] == "Taxes" \
                        or row[3] == "Uncategorized" or row[3] == "Amusement" or row[3] == "Shipping" or row[3] == "Home" or row[3] == "Tuition" or row[3] == "Pharmacy":
                        key = "Random"
                    else:
                        key = row[3]

                    #Initialize year dict keys
                    if row[0][0:4] not in self.yearDict:
                        self.yearDict[row[0][0:4]] = {}
                    if "Total" not in self.yearDict[row[0][0:4]]:
                        self.yearDict[row[0][0:4]]['Total'] = 0
                    if key not in self.yearDict[row[0][0:4]]:

                        self.yearDict[row[0][0:4]][key] = 0


                    if datetime.strptime(startDate, "%Y-%m") <= datetime.strptime(row[0][0:7], "%Y-%m") <= datetime.strptime(endDate, "%Y-%m"):

                        #Initialize month dict keys
                        if row[0][0:7] not in self.monthDict:
                            self.monthDict[row[0][0:7]] = {}
                        if "Total" not in self.monthDict[row[0][0:7]]:
                            self.monthDict[row[0][0:7]]['Total'] = 0
                        if key not in self.monthDict[row[0][0:7]]:
                            self.monthDict[row[0][0:7]][key] = 0

                        self.monthDict[row[0][0:7]]["Total"] += float(row[2])
                        self.monthDict[row[0][0:7]][key] += float(row[2])

                        self.yearDict[row[0][0:4]]["Total"] += float(row[2])
                        self.yearDict[row[0][0:4]][key] += float(row[2])

                    else:

                        self.yearDict[row[0][0:4]]["Total"] += float(row[2])
                        self.yearDict[row[0][0:4]][key] += float(row[2])


            
            #Sort year dict by amount spent
            for year in self.yearDict:
                self.yearDict[year] = dict( sorted(self.yearDict[year].items(), key = lambda item: item[1]) )


            self.yearCell = "{0}{1}".format(startCell[0], int(startCell[1:3]) - 30)

            count = 0

            #print(self.yearDict)

            #Need to figure out actual format of different categories

            for year in self.yearDict:


                if year == '2022':

                    if count == 0:

                        spreadsheet.update_acell(self.yearCell, year)

                        gsformatting.format_cell_ranges(spreadsheet, [(self.yearCell, self.headerFormat)])
                        print("{0}:{1}{2}".format(self.yearCell, "G", self.yearCell[1:3]))
                        spreadsheet.merge_cells("{0}:{1}{2}".format(self.yearCell, "G", self.yearCell[1:3]))

                        self.yearCell = "{0}{1}".format(self.yearCell[0], int(self.yearCell[1:3]) + 1)
                        print("should be updated")

                    labels = list(self.yearDict[year].keys())
                    data = list(self.yearDict[year].values())

                    # if len(labels) > 5:
                    #     range = "{0}:{1}".format()

                    while labels is not None:
                        print(labels)
                        if len(labels) > 5:
                            labelRange = "{0}:{1}{2}".format(self.yearCell, chr(ord(self.yearCell[0]) + 4), self.yearCell[1:3])
                            dataRange = "{0}{1}:{2}{3}".format(self.yearCell[0], int(self.yearCell[1:3]) + 1, chr(ord(self.yearCell[0]) + 4), int(self.yearCell[1:3]) + 1)
                            print(labelRange)
                            print(dataRange)

                            currList = labels[0:5]
                            currData = data[0:5]

                            labels = labels[5:]
                            data = data[5:]
                        else:
                            currList = labels
                            currData = data

                            labels = None
                            data = None

                        #May only be able to do last 3 months, to stay within quota limits

                        spreadsheet.batch_update( [ { 'range' : labelRange, 'values': [currList] }  ] )
                        spreadsheet.batch_update( [ { 'range' : dataRange, 'values': [currData] }  ] )

                        labelRange = "{0}{1}:{2}{3}".format(labelRange[0], int(labelRange[1:3]) + 2, chr(ord(labelRange[0]) + 4), int(labelRange[1:3]) + 2)
                        dataRange = "{0}{1}:{2}{3}".format(dataRange[0], int(dataRange[1:3]) + 2, chr(ord(dataRange[0]) + 4), int(dataRange[1:3]) + 2)

                        #MIGHT NEED TO ADD yearcell value update to reference later?

                        print(labelRange)
                        print(dataRange)
                        #print(labels)
                        print(currList)
                        print(currData)


            #         #Need to change this to batch update for less requests
            #         for key in self.yearDict[year].keys():

            #             spreadsheet.update_acell(self.yearCell, key)

            #             self.yearCell = "{0}{1}".format(self.yearCell[0], int(self.yearCell[1:3]) + 1)

            #             spreadsheet.update_acell(self.yearCell, self.yearDict[year][key])

            #             if self.yearCell[0] == 'G':
            #                 self.yearCell = "{0}{1}".format(chr(ord(self.yearCell[0]) - 4), int(self.yearCell[1:3]) + 1)
            #             else:
            #                 self.yearCell = "{0}{1}".format( chr(ord(self.yearCell[0]) + 1), int(self.yearCell[1:3]) - 1 )

            #             count += 1

            # self.monthCell = "{0}{1}".format(startCell[0], int(startCell[1:3]) - 34)

            # print(self.monthCell)

            # print(self.monthDict)

            # count = 0

            # for month in self.monthDict:

            #     if count == 0:

            #         spreadsheet.update_acell(self.monthCell, month)

            #         gsformatting.format_cell_ranges(spreadsheet, [(self.monthCell, self.headerFormat)])
            #         spreadsheet.merge_cells("{0}:{1}{2}".format(self.monthCell, "G", self.monthCell[1:3]))

            #         self.monthCell = "{0}{1}".format(self.monthCell[0], int(self.monthCell[1:3]) + 1)
            #         print("should be updated")

            #     for key in self.monthDict[month].keys():

            #         if count == 0:

            #             spreadsheet.update_acell(self.monthCell, key)

            #             self.monthCell = "{0}{1}".format(self.monthCell[0], int(self.monthCell[1:3]) + 1)

            #             spreadsheet.update_acell(self.monthCell, self.monthDict[month][key])

            #             if self.monthCell[0] == 'G':
            #                 self.monthCell = "{0}{1}".format(chr(ord(self.monthCell[0]) - 4), int(self.monthCell[1:3]) + 1)
            #             else:
            #                 self.monthCell = "{0}{1}".format( chr(ord(self.monthCell[0]) + 1), int(self.monthCell[1:3]) - 1 )

            #     count += 1

            
            
            

                        
                        # if count == 0:
                        #     spreadsheet.update_acell(self.yearCell, key)
                        # else:
                        #     self.yearCell = "{0}{1}".format( chr(ord(self.yearCell[0]) + 1), int(self.yearCell[1:3]))
                        #     spreadsheet.update_acell(self.yearCell, key)

                        # self.yearCell = "{0}{1}".format(self.yearCell[0], int(self.yearCell[1:3]) + 1)
                        # spreadsheet.update_acell(self.yearCell, self.yearDict[year][key])
                        

                    #     spreadsheet.update_acell(self.yearCell, year[key])

                    #     self.yearCell = "{0}{1}".format(self.yearCell[0], int(self.yearCell[1:3]) + 1)








    #Completed helper methods



    #Format header range
    def formatHeader(self, spreadsheet, range):

        format = gsformatting.cellFormat( backgroundColor=gsformatting.Color(156,156,156), borders=gsformatting.Borders( self.emptyBorder, self.emptyBorder, self.emptyBorder, self.emptyBorder ) )
        for row in range:
            gsformatting.format_cell_ranges(spreadsheet, [(row, format)])
        
    # Format margin range
    # Going to combine formatMargin and header 
    def formatMargin(self, spreadsheet, range):
        
        format = gsformatting.cellFormat( backgroundColor=gsformatting.Color(156,156,156), borders=gsformatting.Borders( self.emptyBorder, self.emptyBorder, self.emptyBorder, self.emptyBorder ) )
        for row in range:
            gsformatting.format_cell_ranges(spreadsheet, [(row, format)])

    # Helper method to get all current sheet names
    def getSheetNames(self):
        nameDict = dict()
        for sheet in self.currentSheets:
            nameDict[sheet.title] = sheet.id

        return nameDict


    #Uploads pandas dataframe to spreadsheet with gspread
    def uploadDataframe(self, spreadsheet, startCell, dataframe):
        spreadsheet.update(startCell, [dataframe.columns.values.tolist()] + dataframe.values.tolist())

        

    #Check if sheet exists and if not create it
    def checkSheet(self, sheetName):

        existFlag = False
        
        # print(sheetName)
        # print(self.currentSheetNames.keys())

        if sheetName in self.currentSheetNames.keys():
            existFlag = True
        else:
            if "Expenses" in sheetName:
                existFlag = self.createSheet(sheetName, 1000, 30)
            else:
                existFlag = self.createSheet(sheetName, 500, 30)

        # for sheet in self.currentSheets:
        #     print(sheetName)
        #     print(sheet.title)

        #     if sheetName == sheet.title:
        #         existFlag = True
        #     else:
        #         existFlag = self.createSheet(sheetName, 500, 30)

        # print(all(sheetName in sheet for sheetName in self.currentSheets))

        # if all(sheetName in sheet.title for sheet in self.currentSheets) or existFlag:
        #     existFlag = True
        # else:
        #     existFlag = self.createSheet(sheetName, 500, 30)

        if existFlag:
            print("Sheet {0} exists".format(sheetName))

        return existFlag


    #Create sheet on sheet with sheetName.
    def createSheet(self, sheetName, rows, cols):
        
        sheet = self.sheet.add_worksheet(title=sheetName, rows=rows, cols=cols)

        if sheet:
            self.currentSheetNames[sheetName] = sheet.id
            return True
        else:
            return False

    #Try to open and return client with given sheetName if not created then print/create it.
    def open(self, sheetName):
        try:
           return self.client.open(sheetName)
        except:
            print("Sheet does not exist")
        





    # CURRENTLY UNUSED HELPER METHODS


    def printAllSheets(self):
        spreadsheets = self.client.openall()
        if spreadsheets:
            print(spreadsheets)

        return spreadsheets

    def getRow(self, dataSheet, index):
        return dataSheet.row_values(index)

    #Return all data from passed spread sheet into pandas dataframe.
    def getAllData(self, dataSheet):
        return pd.DataFrame(dataSheet.get_all_values())



    # Uploads all 3 transaction types into temporary 'Data' worksheets  ------- CURRENTLY UNUSED 
    def uploadAllTransactions(self, spreadsheet, sheetList):

        sheetNameList = ['ExpenseData', 'CheckingData', 'SavingsData']

        currentSheets = spreadsheet.worksheets()

        for sheet in sheetNameList:

            self.checkSheet(sheet)

            tempSheet = self.sheet.worksheet(sheet)

            if 'Expense' in sheet:
                self.uploadDataframe(tempSheet, "A1", self.mint.creditTransactions)
            elif 'Checking' in sheet:
                self.uploadDataframe(tempSheet, "A1", self.mint.checkingTransactions)
            elif 'Saving' in sheet:
                self.uploadDataframe(tempSheet, "A1", self.mint.savingsTransactions)


    # CURRENTLY UNUSED
    def getSheet(self, sheetName):
        return self.sheet.get_worksheet_by_id(sheetName)








#Comments 

    # def generateFormatedTransactions(self, spreadsheet):
        
    #     sheetNameList = ['ExpenseData', 'CheckingData', 'SavingsData']

        
        
    #     currentSheets = spreadsheet.worksheets()

    #     self.formatMargin(tempSheet, ['{0}1:{0}'.format('A'), '{0}2:{0}'.format('G') ] )


    #     self.formatHeader(tempSheet, ['A{0}:G{0}'.format(1), 'A{0}:G{0}'.format(2), 'A{0}:G{0}'.format(3)])

    #     for sheet in sheetNameList:

    #         print(currentSheets[sheet])

    #         #Create tempSheet to reference sheet locally
    #         tempSheet = self.sheet.worksheet(sheet)

    #         self.formatData()

    #         if 'Expense' in sheet:
    #             self.uploadDataframe(tempSheet, "B4", self.mint.creditTransactions)
    #         elif 'Checking' in sheet:
    #             self.uploadDataframe(tempSheet, "B4", self.mint.checkingTransactions)
    #         elif 'Saving' in sheet:
    #             self.uploadDataframe(tempSheet, "B4", self.mint.savingsTransactions)






    #Upload dataframe df to spreadsheet with sheetname
    # def upload(self, df, spreadsheet, type, sheetName):
    #     d2g.upload(df, spreadsheet, type, sheetName)

        #Open all sheets to see
        # spreadsheets = client.openall()
        # if spreadsheets:
        #     print(spreadsheets)

    
        #spreadsheets = client.openall()
        #Add check to see if it exists in list of spreadsheets and if not then create it for the user and share it with them? - and transfer ownership from service account to user account?
        #sheet = self.open(client, 'Mint Raw Data Test')

        #Get sheet by Index

        #dataSheet = sheet.get_worksheet(1)


        #print(type(client))

        #utils = gspread.Utils

        #print(self.getRow(dataSheet, 1))

        #print(type(self.getAllData(dataSheet)))




    # Way to upload with df2gspread but honestly gspread might just be easier

        #     def addTransactions(self, sheetList, creds):

        # print(self.mint.creditTransactions)

        # self.uploadDataframe(self.mint.creditTransactions, 'Expenses')

        #print(type(self.mint.creditTransactions))

        ##self.upload(self.mint.creditTransactions, "RAW_DATA", self.spreadsheetKey, 'Expenses')
        #self.upload(self.mint.checkingTransactions, "RAW_DATA", self.spreadsheetKey, 'Checking')
        #self.upload(self.mint.savingsTransactions, "RAW_DATA", self.spreadsheetKey, 'Savings')
        
        # for sheet in sheetList:
        #     if sheet == 'Expenses':
        #         print(type(self.mint.creditTransactions))
        #         print(self.spreadsheetKey)
        #         print(sheet)

        #         self.upload(self.mint.creditTransactions, "RAW_DATA", self.spreadsheetKey, sheet)
        #     elif sheet == 'Checking':
        #         self.upload(self.mint.checkingTransactions, "RAW_DATA", self.spreadsheetKey, sheet)
        #     elif sheet == 'Savings':
        #         self.upload(self.mint.savingsTransactions, "RAW_DATA", self.spreadsheetKey, sheet)





        #FORMAT EXAMPLE




#         worksheet.format("A2:B2", {
#     "backgroundColor": {
#       "red": 0.0,
#       "green": 0.0,
#       "blue": 0.0
#     },
#     "horizontalAlignment": "CENTER",
#     "textFormat": {
#       "foregroundColor": {
#         "red": 1.0,
#         "green": 1.0,
#         "blue": 1.0
#       },
#       "fontSize": 12,
#       "bold": True
#     }
# })