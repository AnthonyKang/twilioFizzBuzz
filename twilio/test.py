from twilio.rest import TwilioRestClient

account_sid = 'AC5a78230d71e40410aa6e85fb15f39c96'
auth_token = '019623b67a91f8442955c451cee5a2ce'
client = TwilioRestClient(account_sid, auth_token)

call = client.calls.create(url='https://e1fb5a60.ngrok.io/', to="+15106730466", from_="+15106730466")

print(call.sid)