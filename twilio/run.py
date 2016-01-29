from flask import Flask, request, redirect, abort, render_template, session
import twilio.twiml
from twilio.util import RequestValidator
from twilio.rest import TwilioRestClient
import time
from time import gmtime, strftime
import threading
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

ngrokurl = 'https://d3a1f348.ngrok.io'
account_sid = 'AC5a78230d71e40410aa6e85fb15f39c96'
auth_token = '019623b67a91f8442955c451cee5a2ce'
verified_twilio_num = "+15106730466"
app = Flask(__name__)


def call_thread(url, number, from_, delay):
    print('waiting..........................')
    time.sleep(delay)
    print('calling..........................')
    
    client = TwilioRestClient(account_sid, auth_token)
    call = client.calls.create(url=ngrokurl, to=number, from_=verified_twilio_num)


@app.route("/replay", methods=['GET', 'POST'])
def replay():
    number = request.values.get('number' ,)
    digits = request.values.get('digits',)
    client = TwilioRestClient(account_sid, auth_token)
    call = client.calls.create(url=ngrokurl+'fizzbuzzreplay', to=number, from_=verified_twilio_num, send_digits=digits)
    
    return redirect("/form")

@app.route("/fizzbuzzreplay", methods=['GET', 'POST'])
def fizzbuzzreplay():
    resp = twilio.twiml.Response()

    resp.say("Repeating Fizz Buzz")
    digits = request.values.get('Digits', None)

    for i in range(1,int(digits)+1):
            resp.say('Fizz'*(i%3==0) + 'Buzz'*(i%5==0) or str(i))
    

    return str(resp)
 



@app.route("/form")
def my_form():
    mongoClient = MongoClient()
    callDb = mongoClient.calls

    cursor = callDb.calls.find()
    numbers = []
    digits = []
    times = []
    ids = []
    for document in cursor:
        numbers.append(document['number'])
        digits.append(document['digits'])
        times.append(document['time'])
        ids.append(document['_id'])
        
    return render_template('/index.html', numbers=numbers, digits=digits, times=times, ids=ids)

@app.route("/form-submit", methods=['POST'])
def my_form_post():
    

    if request.form['my-form'] == "Send":
        client = TwilioRestClient(account_sid, auth_token)
        number = request.values.get('number', '')
        hours = request.values.get('hours', '')
        minutes = request.values.get('minutes', '')
        seconds = request.values.get('seconds','')
        delay = int(hours)*3600 + int(minutes)*60 + int(seconds)
        

        #time.sleep(int(hours)*3600 + int(minutes)*60 + int(seconds))
        t = threading.Thread(target=call_thread, args=([ngrokurl, number, verified_twilio_num, delay]))
        
        t.start()

    elif request.form['my-form'] == 'Replay':
        print('hi')
    
    #call = client.calls.create(url='https://e1fb5a60.ngrok.io/', to=number, from_="+15106730466")
    return redirect("/form")


@app.route("/", methods=['GET', 'POST'])
def answer():

    validator = RequestValidator('898351780a26f6e5f0efbbdfb57251c2')
    signature = request.headers.get('X-Twilio-Signature', '')
    
    #print(request.form)

    if not validator.validate(url, request.form, signature):
        print('not valid')

    resp = twilio.twiml.Response()
    
    resp.say("Hello")

    
    # Say a command, and listen for the caller to press a key. When they press
    # a key, redirect them to /handle-key.
    with resp.gather(action="/handle-key", method="POST") as g:
        g.say("Please enter a number, and then press the pound key")

    return str(resp)
 
@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""
 
    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if len(str(digit_pressed)) > 0:
        resp = twilio.twiml.Response()
       
        # If the dial fails:
        for i in range(1,int(digit_pressed)+1):
            resp.say('Fizz'*(i%3==0) + 'Buzz'*(i%5==0) or str(i))

        
        number = request.values.get('From', None)
        curr_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        print(session)

        call_info = {
            'number' : number,
            'time' : curr_time,
            'digits' : digit_pressed,
            '_id' : ObjectId()
        }

        mongoClient = MongoClient()
        callDb = mongoClient.calls
        callDb.calls.insert_one(call_info)
        #from_num = request.values.get('_')

        resp.say("Thanks for buzzing. Bye!")
 
        return str(resp)
 
    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")
 
if __name__ == "__main__":
    app.secret_key = 'secret'

    app.run(debug=True)