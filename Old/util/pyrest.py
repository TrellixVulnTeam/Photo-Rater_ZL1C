import requests
import json
import base64



###
# credit card class
###
class CreditCard:
    def __init__(self, card_number, security_code, exp_month, exp_year, card_holder_name, billing_address, email):
        self.card_number = card_number
        self.security_code = security_code
        self.expiration_month = exp_month
        self.expiration_year = exp_year
        self.card_holder_name = card_holder_name
        self.billing_address = billing_address
        self.email = email

    # convert the credit card object to json
    def to_json(self):
        json = {
            "cardNumber": self.card_number,
            "securityCode": self.security_code,
            "expirationMonth": int(self.expiration_month),
            "expirationYear": int(self.expiration_year),
            "cardHolderName": self.card_holder_name,
            "billingAddress": self.billing_address,
            "email": self.email,
        }
        ###print (json) returns {'expirationMonth': 3, 'cardHolderName': 'Test', 'expirationYear': 2018, 'cardNumber': '4134185779995000', 'securityCode': '123', 'email': 'example@example.com', 'billingAddress': {'address1': '123 hello', 'address2': '123 hello', 'state': 'QC', 'zipCode': '12345', 'city': 'Montreal'}}
        return str(json)


###
# function for getting an access token
###
def retrieve_access_token(client_id, client_secret):
    # The token request end point
    TOKEN_END_POINT_URL = 'https://hack.softheon.io/oauth2/connect/token'

    # The authorization token - a base 64 encoding of 'client_id:client_secret'
    auth_token = base64.standard_b64encode(client_id + ':' + client_secret)

    # declare request headers
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + auth_token
    }

    # declare request body
    body = {
        'scope': 'paymentapi',
        'grant_type': 'client_credentials'
    }

    # call http POST
    # req returns <Response [200] if success
    req = requests.post(TOKEN_END_POINT_URL, headers=headers, data=body)

    # load the response text as json
    # resp_json returns u'access_token, u'token_type, u'Bearer,u'expires_in
    resp_json = json.loads(req.text)

    # print out the status and access token
    print 'REQUEST STATUS:' + str(req.status_code) + '\n'
    return resp_json['access_token']


###
# retrieve a credit card token from the credit card api using the access token
###
def retieve_credit_card_token(credit_card, access_token):
    CREDIT_CARD_END_POINT_URL = 'https://hack.softheon.io/api/payments/v1/creditcards'

    # set the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }

    # req returns <Response [200] if success
    req = requests.post(CREDIT_CARD_END_POINT_URL, headers=headers, data=credit_card.to_json())

    # resp_json returns u'cardState, u'token, u'code, u'message
    resp_json = json.loads(req.text)

    return resp_json['token']


##
# make a payment using the access token, a credit card token and a payment amount
##

def make_payment(access_token, credit_card_token, payment_amount):
    PAYMENT_END_POINT = 'https://hack.softheon.io/api/payments/v1/payments'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }

    payment_method = {
        'paymentToken': str(credit_card_token),
        'type': 'Credit Card'
    }

    payment = {
        'paymentAmount': payment_amount,
        'paymentMethod': payment_method
    }

    payment_json = str(payment)

    req = requests.post(PAYMENT_END_POINT, headers=headers, data=payment_json)

    resp_json = json.loads(req.text)

    print '\nRESULT: ' + str(resp_json['result']['status'])
    print 'AMOUNT: ' + str(resp_json['paymentAmount'])
    print 'TYPE: ' + str(resp_json['paymentMethod']['type'])

"""
###
# the main program
###
def main():
    # The client id and secret
    client_id = 'f2a2ab8e-9a66-4a05-89e4-c29f196f9e33'
    client_secret = 'b11198e6-9939-4d12-90c9-e024c8ae9367'

    # get an access token
    access_token = retrieve_access_token(client_id, client_secret)
    print '\nACCESS TOKEN: ' + access_token

    # create a fake billing address
    billing_address = {
        'address1': '123 hello',
        'address2': '123 hello',
        'city': 'Montreal',
        'state': 'QC',
        'zipCode': '12345'
    }

    # initialize a credit card object and get a credit card token from api end point
    example_cc = CreditCard('4134185779995000', '123', 3, 2018, 'Test', billing_address, 'example@example.com')
    credit_card_token = retieve_credit_card_token(example_cc, access_token)
    print '\nCREDIT CARD TOKEN: ' + credit_card_token

    # make a payment with the access token, credit card token and an amount
    # get the amount from html form then pay

    # form = cgi.FieldStorage()
    # amount =  form.getvalue('amount')
    # print(amount)

    make_payment(access_token, credit_card_token, 12.3)


main()
"""