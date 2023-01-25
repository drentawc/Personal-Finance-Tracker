#
# Mint Backend class to interface with Mint API and perform pandas dataframe calculations and filtering to prepare for google sheet class.
#
# @author Will Drenta
# @version 0.1 7/4/2022
# 
#

import mintapi as mintapi
import pandas as pd
import secrets
import pymysql


#Possible methods:
# self.mintAuth.get_net_worth_data(), 

class MintBackend:

    #Initialize class
    def __init__(self, config):

        self.config = config
        self.mintAuth = self.connectToMint()

        self.accounts = pd.DataFrame()

        self.setUser()

        self.setTransactions()

        self.setAccounts()

        self.importToSql()


    #Helper method to organize all transactions into months
    def organizeTransactions(self):
        ""

    #Helper to get month of transaction data
    def getTransactionMonth(self, date):
        ""

    #Set current user to be sent to MySQL database
    def setUser(self):
        self.firstName = self.config['Database']['firstName']
        self.lastName = self.config['Database']['lastName']


    #Set various transaction class variables
    def setTransactions(self):
        transactions = self.getTransactions()

        #print(transactions.keys()) #To see various categories with each transaction

        #Drop all unneeded columns
        transactions.drop(columns=['isReviewed', 'etag', 'matchState', 'transactionReviewState', 'merchantId', 'isLinkedToRule'], inplace=True)

        #Index(['type', 'id', 'accountId', 'accountRef', 'date', 'description',
    #    'category', 'amount', 'status', 'matchState', 'fiData', 'isReviewed',
    #    'merchantId', 'etag', 'isExpense', 'isPending', 'discretionaryType',
    #    'isLinkedToRule', 'transactionReviewState', 'lastUpdatedDate'],
    #   dtype='object')


        #Set base class variable transactions

        self.transactions = transactions[transactions['type'] == "CashAndCreditTransaction"]
        self.investTrans = transactions[transactions['type'] == "InvestmentTransaction"]


        #Set up empty dataframes
        self.savingsTransactions = pd.DataFrame(columns=['Date', 'Account', 'Amount', 'Category', 'Description']) #, 'Status'])#, 'Type'])
        self.checkingTransactions = pd.DataFrame(columns=['Date', 'Account', 'Amount', 'Category', 'Description']) #, 'Status'])#, 'Type'])
        self.creditTransactions = pd.DataFrame(columns=['Date', 'Account', 'Amount', 'Category', 'Description']) #, 'Status'])#, 'Type'])

        #self.transactions = self.transactions.reset_index()

        #Loop through all transactions in DataFrame
        for index, row in self.transactions.iterrows():

            #Seperate all transactions by account ID

            if row["accountId"] == '9578312_8650884':
                currentAccount = "Main Checking account"
            elif row["accountId"] == '9578312_8802348':
                currentAccount = "Wells Fargo Credit Card"
            elif row['accountId'] == '9578312_8650897':
                currentAccount = "Discover It Credit Card"
            elif row['accountId'] == '9578312_8650883':
                currentAccount = "Second Checking account"
            else:
                currentAccount = row["accountRef"]["name"]


            data = { 'Date': [row['date']], 'Account': [currentAccount], 'Amount': [row['amount']], 'Category' : [row['category']['name']], 'Description': [row['description']] } #, 'Status': [row['status']]  } #, 'AccountRef': row['accountRef'] }
            #data = { 'Date': [row['date']], 'Account': [currentAccount], 'Amount': [row['amount']], 'Category' : [row['category']], 'Description': [row['description']], 'Status': [row['status']]  } #, 'AccountRef': row['accountRef'] }
            entry = pd.DataFrame( data )

            #entry = entry.fillna('')

            if "Checking" in currentAccount:
                self.checkingTransactions = pd.concat([self.checkingTransactions, entry], axis = 0)
            elif "Credit" in currentAccount:
                self.creditTransactions = pd.concat([self.creditTransactions, entry], axis = 0)
            else:
                self.savingsTransactions = pd.concat([self.savingsTransactions, entry], axis = 0)

        self.checkingTransactions = self.checkingTransactions.sort_values(by='Date', ascending=False)
        self.creditTransactions = self.creditTransactions.sort_values(by='Date', ascending=False)
        self.savingsTransactions = self.savingsTransactions.sort_values(by='Date', ascending=False)



    #Set accounts dictionary with all accounts and balances
    def setAccounts(self):

        self.checkingAccounts = pd.DataFrame(columns=['Company', 'Name', 'Balance', 'Type'])#, 'Type'])
        self.savingsAccounts = pd.DataFrame(columns=['Company', 'Name', 'Balance', 'Type'])
        self.creditAccounts = pd.DataFrame(columns=['Company', 'Name', 'Balance', 'Type'])
        self.investmentAccounts = pd.DataFrame(columns=['Company', 'Name', 'Balance', 'Type'])

        for account in self.getAccounts():
            # if i == 2:
            #print(account.keys())
            #     print(account)

            # All account columns:

            #['type', 'bankAccountType', 'availableBalance', 'userFreeBillPay', 'userAtmFeeReimbursement', 'numOfTransactions', 'id', 'name', 'value', 'isVisible', 
            # 'isDeleted', 'planningTrendsVisible', 'accountStatus', 'systemStatus', 'currency', 'fiLoginId', 'fiLoginStatus', 'currentBalance', 'cpId', 'cpAccountName', 'cpAccountNumberLast4', 'hostAccount', 
            # 'fiName', 'accountTypeInt', 'isAccountClosedByMint', 'isAccountNotFound', 'isActive', 'isClosed', 'isError', 'isHiddenFromPlanningTrends', 'isTerminal', 'credentialSetId', 'ccAggrStatus', 'createdDate', 'lastUpdatedDate'])

            #print(account)

            if account['cpAccountNumberLast4'] == '6031':
                name = "Old Capital One Savings Account"
            elif account['cpAccountNumberLast4'] == '1849':
                name = "Secondary Checking Account"
            elif account['cpAccountNumberLast4'] == '5159':
                name = "Main Checking Account"
            elif account['cpAccountNumberLast4'] == '0894':
                name = "Rent Savings Account"

            elif account['cpAccountNumberLast4'] == '7004':
                name = "Discover Credit Card"
            elif account['cpAccountNumberLast4'] == '9758':
                name = "Wells Fargo Credit Card"
            elif account['cpAccountNumberLast4'] == '2306':
                name = "Capital One Credit Card"

            elif account['cpAccountNumberLast4'] == 'enta':
                name = "401k"
            elif account['cpAccountNumberLast4'] == '8027':
                name = "SoFi Roth IRA"
            else:
                print(account)

            #print("{0} - {1}".format(account['cpAccountNumberLast4'], account['bankAccountType']))

            if 'availableBalance' in account:
                data = { 'Company' : [account['fiName']], 'Name' : [name], 'Balance' : [account['availableBalance']], 'Type': [account['bankAccountType']] }
            elif 'value' in account:
                data = { 'Company' : [account['fiName']], 'Name' : [name], 'Balance' : [account['value']], 'Type': [account['type']] }

            entry = pd.DataFrame(data)

            if "Bank" in account['type']:
                if "SAVINGS" in account['bankAccountType']:
                    self.savingsAccounts = pd.concat([self.savingsAccounts, entry])
                elif "CHECKING" in account['bankAccountType']:
                    self.checkingAccounts = pd.concat([self.checkingAccounts, entry])
            elif "Credit" in account['type']:
                self.creditAccounts = pd.concat([self.creditAccounts, entry])
            elif "Investment" in account['type']:
                self.investmentAccounts = pd.concat([self.investmentAccounts, entry])

        self.checkingAccounts = self.checkingAccounts.sort_values(by='Balance', ascending=False)
        self.savingsAccounts = self.savingsAccounts.sort_values(by='Balance', ascending=False)
        self.creditAccounts = self.creditAccounts.sort_values(by='Balance', ascending=True)
        self.investmentAccounts = self.investmentAccounts.sort_values(by='Balance', ascending=False)

        self.accounts = [ self.checkingAccounts, self.savingsAccounts, self.creditAccounts, self.investmentAccounts ]


    #Helper method to return all connected accounts
    def getAccounts(self):
        return self.mintAuth.get_account_data()

    #Helper method to return all transactions
    def getTransactions(self):
        return pd.DataFrame(self.mintAuth.get_transaction_data())

    #Connects to Mint API
    def connectToMint(self):

        # mint = mintapi.Mint()
        # mint.driver = Firefox()
        # mint.status_message, mint.token = mintapi.sign_in(
        #     self.config["Mint"]["email"], self.config["Mint"]["pass"], mint.driver, mfa_method=None, mfa_token=None,
        #     mfa_input_callback=None, intuit_account=None, wait_for_sync=True,
        #     wait_for_sync_timeout=5 * 60,
        #     imap_account=None, imap_password=None,
        #     imap_server=None, imap_folder="INBOX",
        # )

        # return mint


        return mintapi.Mint(
            self.config["Mint"]["email"],
            self.config["Mint"]["pass"],
            mfa_method = 'sms',
            mfa_input_callback=None,
            mfa_token=None,
            intuit_account=None,
            headless=False,
            session_path=None,
            imap_account=None,
            imap_password=None,
            imap_server=None,
            imap_folder='INBOX',
            wait_for_sync=False, 
            wait_for_sync_timeout=300,
            use_chromedriver_on_path=False
        )


    def importToSql(self):

        connection = pymysql.connect(host=self.config['Database']['host'], user=self.config['Database']['user'], password=self.config['Database']['password'], db=self.config['Database']['db'])

        #connection = pymysql.connect(host="localhost", user="root", password="Elheat1337@$", db="finances")

        with connection:

            with connection.cursor() as cursor:

                #I think I want REPLACE INTO for all of these commands, so that it replaces if entry is there if not it inserts
                
                #NEED insert into with usersCommand, since auto increment is on now don't need to pass userId in, may want to add email into database
                usersCommand = 'INSERT INTO `users` (`firstName`, `lastName`, `password`) VALUES (%s, %s, %s)'
                
                cursor.execute(usersCommand, (self.config['Database']['firstName'], self.config['Database']['lastName'], self.config['Mint']['pass'] ))

                connection.commit()



            with connection.cursor() as cursor:

                userIdCommand = 'SELECT `userId` FROM `users` WHERE `firstName`=%s AND `lastName`=%s'

                cursor.execute(userIdCommand, (self.config['Database']['firstName'], self.config['Database']['lastName']) )

                userId = cursor.fetchone()

                print(userId)

                #@TODO Accounts are currently list, maybe more beneficial to just have them all in the same dataframe
                # for account in self.accounts:
                #     currentAccount = list(account.itertuples(index=False, name=None))
                #     print(currentAccount)
                # transactionList = list(self.transactions.itertuples(index=False, name=None))
                # investmentList = list()



                #accountsCommand = 'INSERT INTO `accounts` (`userId`, `bankName`, `description`, `balance`, `accountType`, `accountId`) VALUES (%s, %s, %s, %s, %s, %s)'

                #transactionCommand = 'INSERT INTO `transactions` (`transactionId`, `userId`, `accountId`, `date`, `amount`, `category`, `description`) VALUES (%s, %s, %s, %s, %s, %s)'


                # cursor.executemany(accountsCommand, accountsCommand)
                # cursor.executemany()



    #Change email and password to be command line arguments you pass or maybe even environment variables
#     mint = mintapi.Mint(
#     username,  # Email used to log in to Mint
#     password,  # Your password used to log in to mint
 
#     #Optional parameters
#     mfa_method='sms',  # Can be 'sms' (default), 'email', or 'soft-token'.
#                        # if mintapi detects an MFA request, it will trigger the requested method
#                        # and prompt on the command line.
#     headless=False,  # Whether the chromedriver should work without opening a
#                      # visible window (useful for server-side deployments)
#     mfa_input_callback=None,  # A callback accepting a single argument (the prompt)
#                               # which returns the user-inputted 2FA code. By default
#                               # the default Python `input` function is used.
#     session_path=None, # Directory that the Chrome persistent session will be written/read from.
#                        # To avoid the 2FA code being asked for multiple times, you can either set
#                        # this parameter or log in by hand in Chrome under the same user this runs
#                        # as.
#     imap_account=None, # account name used to log in to your IMAP server
#     imap_password=None, # account password used to log in to your IMAP server
#     imap_server=None,  # IMAP server host name
#     imap_folder='INBOX',  # IMAP folder that receives MFA email
#     wait_for_sync=False,  # do not wait for accounts to sync
#     wait_for_sync_timeout=300,  # number of seconds to wait for sync
# )

