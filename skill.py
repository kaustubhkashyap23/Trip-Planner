import os
import sqlite3

from flask import Flask
from flask_ask import Ask, question, statement, request, delegate, session


app = Flask(__name__)
ask = Ask(app, "/")


def get_dialog_state():
    return session['dialogState']


@ask.launch
def launch():
    speech_text = 'I can help you booking flights, bus and trains, would you like to book flight, bus or train? I can also show you hotels and tourist attractions in a particular city.'
    return question(speech_text).reprompt(speech_text)            


@ask.intent('bookingType')
def bookingType():
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()
    global t_type
    t_type=request.intent.slots.t_type.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    from_city=request.intent.slots.from_city.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    to_city=request.intent.slots.to_city.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    #global user_id_alexa
    #user_id_alexa=username.lower()
    #pwd=password.lower();
    print(t_type)
    print(from_city)
    print(to_city)
    #print(username)
    #print(password)
    from_city_alexa=from_city.lower();
    to_city_alexa=to_city.lower();
    con = sqlite3.connect("tripdb.db")
    cur = con.cursor()
    f='Flights are\n'
    b='Buses are\n'
    t='Trains are\n'
    i=1
    j=1
    k=1
    if t_type=='flight':
        cur.execute("select * from flight where from_city=? and to_city=?",(from_city_alexa, to_city_alexa))
        rows=cur.fetchall()
        if rows:
            for row in rows:
                #print(row)
                f=f+str(i)+': '+row[1]+' ('+row[0]+') '+'Fare='+str(row[4])+','+'\n'
                i=i+1
                #print(f)
            i=1
            f=f+'.'
            return question(f+'To book, go to www.makemytrip.com')
        else:
            return question("No Flights. Try other travel options")
    elif t_type=='bus':
        cur.execute("select * from bus where from_city=? and to_city=?",(from_city_alexa, to_city_alexa))
        rows=cur.fetchall()
        if rows:
            for row in rows:
                #print(row)
                b=b+str(i)+': '+row[1]+' ('+row[0]+') '+'Fare='+str(row[4])+','+'\n'
                j=j+1
                #print(b)
            j=1
            b=b+'.'
            return question(b+'To book, go to www.redbus.in')
        else:
            return question("No Buses. Try other travel options")
    elif t_type=='train':
        cur.execute("select * from train where from_city=? and to_city=?",(from_city_alexa, to_city_alexa))
        rows=cur.fetchall()
        if rows:
            for row in rows:
                #print(row)
                t=t+str(i)+': '+row[1]+' ('+row[0]+') '+'Fare='+str(row[4])+','+'\n'
                k=k+1
                #print(t)
            k=1
            t=t+'.'
            return question(t+'To book, go to www.irctc.co.in')
        else:
            return question("No Trains. Try other travel options")
    else:
        return question("Please give a valid mode of travel")


@ask.intent('hotels')
def hotels():
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()
    city=request.intent.slots.city.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    print(city)
    #print(user_id_alexa)
    city_alexa=city.lower();
    h='Hotels are: \n'
    i=1
    con = sqlite3.connect("tripdb.db")
    cur = con.cursor()
    cur.execute("select * from hotel where city=?",(city_alexa,))
    rows=cur.fetchall()
    if rows:
        for row in rows:
            #print(row)
            h=h+str(i)+': '+row[1]+' '+'Rent='+str(row[3])+','+'\n'
            i=i+1
        i=1
        h=h+'.'
        return question(h+'To book, go to www.makemytrip.com')
    else:
        return question('No hotels in this city')
            

@ask.intent('touristPlaces')
def touristPlaces():
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()
    city=request.intent.slots.city.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    print(city)
    city_alexa=city.lower();
    tp='Tourist attractions are: \n'
    i=1
    con = sqlite3.connect("tripdb.db")
    cur = con.cursor()
    cur.execute("select * from tourist_places where city=?",(city_alexa,))
    rows=cur.fetchall()
    if rows:
        for row in rows:
            #print(row)
            tp=tp+str(i)+': '+row[0]+','+'\n'
            i=i+1
        i=1
        tp=tp+'.'
        return question(tp+'To know more, go to www.google.com')
    else:
        return question('No Tourist Attractions in this city')

@ask.intent('travelDetails')
def TravelDetails(username, password, t_nn):
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()
    #t_type=request.intent.slots.t_type.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    #t_no=request.intent.slots.t_no.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    user_id_alexa=username.lower()
    pwd=password.lower();
    print(t_type)
    print(t_nn)
    str(t_nn)
    con=sqlite3.connect("tripdb.db")
    cur=con.cursor()
    cur.execute("select * from user where user_id=?",(user_id_alexa,))
    rows=cur.fetchall()
    if rows:
        for row in rows:
            s=row[1]
        if s==pwd:
            if t_type=='flight':
                cur.execute("select * from flight where f_no=?",(t_nn,))
                rows=cur.fetchall()
                if rows:
                    cur.execute("insert into booking_details (u_id, t_type, t_no) values (?,?,?)", (user_id_alexa,t_type,t_nn))
                    con.commit()
                    return question("Your booking is successful.")
                else:
                    return question("You chose an invalid option. Please choose a valid option")
            elif t_type=='train':
                cur.execute("select * from train where t_no=?",(t_nn,))
                rows=cur.fetchall()
                if rows:
                    cur.execute("insert into booking_details (u_id, t_type, t_no) values (?,?,?)", (user_id_alexa,t_type,t_nn))
                    con.commit()
                    return question("Your booking is successful.")
                else:
                    return question("You chose an invalid option. Please choose a valid option")
            elif t_type=='bus':
                cur.execute("select * from bus where b_no=?",(t_nn,))
                rows=cur.fetchall()
                if rows:
                    cur.execute("insert into booking_details (u_id, t_type, t_no) values (?,?,?)", (user_id_alexa,t_type,t_nn))
                    con.commit()
                    return question("Your booking is successful.")
                else:
                    return question("You chose an invalid option. Please choose a valid option")
        else:
            return question("Password is wrong. Please Try again.")
    else:
        return question("Username does not exist. Create new id and try again.")


@ask.intent('showBooking')
def showBooking(username, password):
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()
    u_id_alexa=username.lower();
    pwd=password.lower();
    bd = "Your booking details are: "
    i=1
    con = sqlite3.connect("tripdb.db")
    cur = con.cursor()
    cur.execute("select * from user where user_id=?",(u_id_alexa,))
    rows=cur.fetchall()
    if rows:
        for row in rows:
            s=row[1]
        if s==pwd:
            cur.execute("select * from booking_details where u_id=?",(u_id_alexa,))
            rows=cur.fetchall()
            if rows:
                for row in rows:
                    print(row)
                    bd=bd+str(i)+": "
                    i=i+1
                    if row[1]=='flight':
                        bd=bd+"Flight : "
                        cur.execute("select * from flight where f_no=?",(row[2],))
                        rows=cur.fetchall()
                        for row in rows:
                            print(row)
                            bd=bd+row[1]+" ("+row[0]+") "+"From: "+row[2]+" To: "+row[3]+" Fare: "+str(row[4])+","
                    elif row[1]=='train':
                        bd=bd+"train : "
                        cur.execute("select * from train where t_no=?",(row[2],))
                        rows=cur.fetchall()
                        for row in rows:
                            print(row)
                            bd=bd+row[1]+" ("+row[0]+") "+"From: "+row[2]+" To: "+row[3]+" Fare: "+str(row[4])+","
                    elif row[1]=='bus':
                        bd=bd+"Bus : "
                        cur.execute("select * from bus where b_no=?",(row[2],))
                        rows=cur.fetchall()
                        for row in rows:
                            print(row)
                            bd=bd+row[1]+" ("+row[0]+") "+"From: "+row[2]+" To: "+row[3]+" Fare: "+str(row[4])+","
                bd=bd+"."
                return question(bd)
            else:
                return question("Wrong username")
        else:
            return question("Password is wrong. Please Try again.")
    else:
        return question("Username does not exist.")



@ask.intent('cancelBooking')
def cancelBooking(username, password, t_nn):
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()
    t_type=request.intent.slots.t_type.resolutions.resolutionsPerAuthority[0]['values'][0]['value']['name']
    u_id_alexa=username.lower();
    pwd=password.lower();
    con = sqlite3.connect("tripdb.db")
    cur = con.cursor()
    cur.execute("select * from user where user_id=?",(u_id_alexa,))
    rows=cur.fetchall()
    if rows:
        for row in rows:
            s=row[1]
        if s==pwd:
            cur.execute("select * from booking_details where u_id=? and t_type=? and t_no=?",(u_id_alexa,t_type,t_nn))
            rows=cur.fetchall()
            if rows:
                for row in rows:
                    cur.execute("delete from booking_details where u_id=? and t_type=? and t_no=?",(u_id_alexa,t_type,t_nn))
                    con.commit()
                return question("Your booking is cancelled successfully")
            else:
                return question("No such booking exists")
        else:
            return question("Password is wrong. Please Try again.")
    else:
        return question("Username does not exist.")


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
