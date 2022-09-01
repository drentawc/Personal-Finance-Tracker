# 
# Personal Finance Tracker project working with both Google Spreadsheet API and Mint API to keep an accurate list of accounts, expenses, and investments. 
# Plan to be run daily on Google Cloud services to familiarize myself with running code on a cloud environment.
#
# @Author: Will Drenta
# @Version 0.2 8/31/2022
# Changelog:
#   - Full uploading of accounts, organization of expenses as well as creating pie charts for data viewing.

# To run on Linux: /miniconda3/envs/mint-tracker/bin/python tracker.py default.conf


#Gameplan:
# Every time you start the program it refreshes the list of transactions (Maybe just append to list when list hits 100, pop off 50 or so), giving each transtion an id, and
# depending on transation label from Mint, sort in google sheets 
# 
# 
# - Split up all monthly charges and depict monthly graphs on other pages of sheets?
#
# - Method to list back money across accounts 
#
#  TODO LIST:
#   - Uploading of plots to imgur to put into google sheet
#   - Map out investment sheet
#   - May want to move all of the dict creation to mint backend so that the functionality is more seperated



import argparse
import configparser

#Local imports
from mintbackend import MintBackend
from gsheet import GSheet

from plot import Plot


def main():

    args = setupArgparser().parse_args()
    config = configparser.ConfigParser()
    
    config.read(args.config)

    # #mint = ""
    # mint = MintBackend(config)

    GSheet(MintBackend(config), config)


    #Test upload
    # testDict = {"Total" : 1234.23333, "Groceries" : 555.05, "Electronics": 1.0000000000000000000000000000000000000006}
    # asd = Plot(testDict, config['Imgur'], "2022")
    # asd.createExpenseChart()
    # print(asd.uploadToImgur())


def setupArgparser():
    parser = argparse.ArgumentParser()

    parser.add_argument("config", help="Config file containing necessary info for Mint and Google Sheets.")

    return parser


if __name__ == "__main__":
    main()

