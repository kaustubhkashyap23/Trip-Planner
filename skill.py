import os

from flask import Flask
from flask_ask import Ask, question, statement


app = Flask(__name__)
ask = Ask(app, "/")


@ask.launch
def launch():
    speech_text = 'I can help you booking flights, bus and trains, would you like to book flight, bus or train?'
    return question(speech_text).reprompt(speech_text)


@ask.intent('bookingType')
def booking(t_type, from_city, to_city):
    print(t_type)
    print(from_city)
    print(to_city)
    if t_type=='flight' and from_city=='Delhi' and to_city=="Mumbai":
        return statement('Flight booking')
    elif t_type=='bus' and from_city=="Delhi":
        return statement('Bus booking')
    else:
        return statement('Train booking')
    return question("Confirm once again?")


@ask.intent('AMAZON.HelpIntent')
def help_intent():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


#@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, port=5001)
