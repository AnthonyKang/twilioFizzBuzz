This application uses mongodb so pymongo needs to be installed.

To start the server:
python3 run.py 

To allow access to server:
./ngrok http 5000

-Go to localhost:4040/status
-Locate the URL

-replace the url for ngroklurl in run.py with the new url
-replace account_sid and auth_token with own token
-replace verified_twilio_num with verified phone number from twilio account
-Get a voice number from twilio account
-Put url for ngrock in voice url field
-save run.py
-Can test by calling your twilio account voice number acquired from twilio
-Or go to url/form and enter in any number

Notes: replay doesn't work with free twilio account, works with regular account

Authentication does not work
Application only sends to verified numbers for twilio account



