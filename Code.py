import logging
import os

from flask import Flask
from flask_ask import Ask, request,context,version, session, question, statement
import pdb
import RPi.GPIO as GPIO
import urllib2
from geopy import geocoders
import json
gn = geocoders.GeoNames(username="mithul")

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

STATUSON = ['on','high']
STATUSOFF = ['off','low']
prev_session = None

@ask.launch
def launch():
    global prev_session
    speech_text = 'Welcome HackDFW ! Get ready for some awesomeness. What is up ?'
    if prev_session and 'money' in prev_session:
        prev_session = None
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('TestAlexa', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17,GPIO.OUT)
    if status in STATUSON:
        print "Setting LED to high"
	GPIO.output(17,GPIO.HIGH)
	return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        print "Setting LED to high"
        GPIO.output(17,GPIO.LOW)
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry not possible.')
@ask.intent('AMAZON.SearchAction<object@WeatherForecast>', mapping = {'city':'object.location.addressLocality.name'})
def weather(city):
    lat,lng = gn.geocode(city)[-1]
    contents = json.loads(urllib2.urlopen("https://api.darksky.net/forecast/1288f79562e960d5ba0e9111b907fa68/"+str(lat)+","+str(lng)).read())
    print "DEBUG", contents, city
    with open("t.json","w") as f:
        f.write(json.dumps(contents))
    print city, contents.keys(), contents["currently"].keys()
    return statement("The temperature in "+city+" is currently "+str(contents["currently"]["temperature"]))

@ask.intent('hackWeather')
def hackWeather():
    return statement('Hot among the hackers while it is too cold outside')

@ask.intent('StateFarmLoanIntent', mapping = {'loan':'loan_type'})
def stateFarmLoans(loan):
    # pdb.set_trace()

    if loan!=None:
        if request["intent"]["slots"]["loan_type"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid loan
            return statement("You are looking for "+loan+" loan")
        else:
            # asked loan but invalid
            return question("Which loan are you looking for: vehicle or house?").reprompt("Which loan are you looking for: vehicle or house?")

    return statement(str(loan))

@ask.intent('StateFarmInsuranceIntent', mapping = {'insurance' : 'insurance_type'})
def stateFarmInsurance(insurance):
    # pdb.set_trace()
    if  insurance!=None:
        if request["intent"]["slots"]["insurance_type"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid insurance
            print "SESSION", session
            return statement("You are looking for "+insurance+" insurance")
        else:
            # asked insurance but invalid
            session.attributes["TEST"] = "testing this"
            return question("Which insurance are you looking for: vehicle, house & property, life, health & disability?").reprompt("Which insurance are you looking for: vehicle, house & property, life, health & disability?")
                  # .reprompt("I didn't get that. When would you like to be seen?")

    return statement(str(insurance))


@ask.intent('BuyIntent', mapping = {'obj' : 'object'})
def buyIntent(obj):
    # pdb.set_trace()
    global prev_session
    if  object!=None:
        if request["intent"]["slots"]["object"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid insurance
            print "SESSION", session
            session.attributes['buyObj'] = obj
            prev_session = json.loads(json.dumps(session.attributes))
            return question("Thats great news. Do you want to look for an " + obj + " insurance or loan").reprompt("Thats great news. Do you want to look for an " + obj + " insurance or loan")

@ask.intent('YesIntent', mapping = {'service_type' : 'type'})
def yesIntent(service_type):
    # pdb.set_trace()
    global prev_session
    if  service_type!=None:
        if request["intent"]["slots"]["type"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid insurance
            print "SESSION", session
            session.attributes['serviceType'] = service_type
            prev_session = json.loads(json.dumps(session.attributes))
            return question("Awesome! Let me get you a quote. What is your age ?").reprompt("Awesome! Let me get you a quote. What is your age ?")

@ask.intent('AgeIntent', mapping = {'age' : 'age'})
def ageIntent(age):
    # pdb.set_trace()
    global prev_session
    if  age!=None:
    #    if request["intent"]["slots"]["age"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid insurance
            print "SESSION", session
            session.attributes['age'] = age
            prev_session = json.loads(json.dumps(session.attributes))
            if session.attributes['buyObj'] == 'car':
                return question("Cool ! How long have you been driving ?").reprompt("Cool ! How long have you been driving ?")
            elif session.attributes['buyObj'] == 'home':
                return question("Cool ! How many years have you owned the house for ?").reprompt("Cool ! How many years have you owned the house for ?")


@ask.intent('ExpIntent', mapping = {'exp' : 'exp'})
def expIntent(exp):
    # pdb.set_trace()
    global prev_session
    if  exp!=None:
    #    if request["intent"]["slots"]["exp"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid insurance
            print "SESSION", session
            session.attributes['exp'] = exp
            prev_session = json.loads(json.dumps(session.attributes))
            if session.attributes['serviceType'] == 'loan':
                return question("Wow ! So how long do you want the loan for ?").reprompt("Wow ! So how long do you want the loan for ?")
            else:
                prev_session['money'] = "$1000000"
                return statement("Awesome ! Hmmmm. So StateFarm can give you an insurance for $100000")
                # .reprompt("Awesome ! Hmmmm. So StateFarm can give you an insurance for $100000")

@ask.intent('LoanTermIntent', mapping = {'loan_term' : 'loan_term'})
def loanTermIntent(loan_term):
    # pdb.set_trace()
    global prev_session
    if  loan_term!=None:
    #    if request["intent"]["slots"]["loan_term"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid insurance
            print "SESSION", session
            session.attributes['loan_term'] = loan_term
            prev_session = json.loads(json.dumps(session.attributes))
            prev_session['money'] = "$1000000"
            return statement("Awesome ! Hmmmm. So StateFarm can give you a loan for $100000 with 10% interest")
            # .reprompt("Awesome ! Hmmmm. So StateFarm can give you a loan for $100000 with 10% interest")

@ask.intent('HangingIntent')
def hangingIntent(loan_term):
    # pdb.set_trace()
    global prev_session
    if prev_session:
        session.attributes = prev_session
    if True:
    #    if request["intent"]["slots"]["loan_term"]["resolutions"]["resolutionsPerAuthority"][0]["status"]["code"]=="ER_SUCCESS_MATCH":
            # valid insurance
            print "SESSION", session
            return question("Oops! My bad, lets continue").reprompt("Oops! My bad, lets continue")





@ask.intent('AMAZON.FallbackIntent')
def fallback():
    return statement("In fallback intent")

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return question("Retry that").reprompt("Retry that")
    print prev_session
    return "{}", 200


@app.route("/")
def hello():
    if prev_session:
        if 'buyObj' in prev_session:
            current_state = prev_session['buyObj']
        if 'serviceType' in prev_session:
            current_state = prev_session["serviceType"]
        if 'age' in prev_session:
            current_state = "age"
        if 'exp' in prev_session:
            current_state = "exp"
        if 'loan_term' in prev_session:
            current_state = "loan_term"
        if 'money' in prev_session:
            current_state = "done"
    else:
        current_state = "init"
    return json.dumps({'current_state': current_state})


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
