import sys
import globalobjects 
import mysql.connector
import datetime as dt

mycon=globalobjects.mycon
mycursor=globalobjects.mycursor 

#SUPPORTING FUNCTIONS
def query_execute(query):
    try:
        result = back_query_execute(query)
        return result 
    except Exception as e:
        print(e)
        sys.exit()

def back_query_execute(query):
    try:
        mycursor.execute(query)
        # Check if the query is a SELECT or has rows to return
        if mycursor.with_rows:
            return mycursor.fetchall() 
        else:
            mycon.commit()
            return None
            
    except mysql.connector.Error as err:
        mycon.rollback()
        raise Exception(db_error_handle(err))

def db_error_handle(err):
    if err.errno == 1062:
        return "This record already exists."

    elif err.errno == 1452:
        return "Invalid reference: flight or user does not exist."

    elif err.errno == 1451:
        return "Cannot delete: dependent records exist."

    elif err.errno == 1048:
        return "Required field missing."

    else:
        return f"Database error: {err.msg}"
    

def takeinput(PHONE_NUMBER,User_Phone,Table="Users"):
     while True:
                  value= input(f"ENTER {PHONE_NUMBER} : ")
                  if(alreadyexists(User_Phone,value,Table)):
                    print(f"THIS {PHONE_NUMBER} ALREADY EXISTS. ENTER DIFFERENT {PHONE_NUMBER}: ")
                  else:
                      return value

def alreadyexists(User_Phone,value,Table="Users"):
    global mycursor
    mycursor.execute("Select * from {} where {}='{}'".format(Table,User_Phone,value))
    myresult = mycursor.fetchall()
    if(myresult==[]):
        return False
    return True
    
def takeexistinginput(USER_ID,User_Id,Table="Users"):
     while True:
        value= input(f"ENTER {USER_ID} : ")
        if(not(alreadyexists(User_Id,value,Table))):
            print(f"THIS {USER_ID} IS NOT REGISTERED. ENTER REGISTERED {USER_ID}: ")
        else:
            return value

def ismatchwithuserid(User_Password,value,Table="Users"):
     User_Id=globalobjects.user_id
     global mycursor
     mycursor.execute("SELECT * FROM {} WHERE User_Id = '{}' AND {} = '{}' ".format(Table, User_Id, User_Password, value))
     myresult = mycursor.fetchall()
     if(myresult==[]):
        return False
     return True

def ismatchwithadminid(Admin_Password,value,Table="Admins"):
     Admin_Id=globalobjects.admin_id
     global mycursor
     mycursor.execute("SELECT * FROM {} WHERE Admin_Id = '{}' AND {} = '{}' ".format(Table, Admin_Id, Admin_Password, value))
     myresult = mycursor.fetchall()
     if(myresult==[]):
        return False
     return True

def takeinputdate():
    while(True):
     try:
          date=dt.date.fromisoformat(input("ENTER DATE OF FLIGHT (YYYY-MM-DD)"))
          if(date<dt.date.today()):
              print("ENTER VALID DATE")
              continue
          else:
            return date
            break
     except ValueError:
          print("Invalid date format")

def takeinputtime():
    while(True):
     try:
          time=dt.time.fromisoformat(input("Enter time (24 Hour) - HH:MM "))
          return time
          break
     except ValueError:
          print("Invalid time format")

def formattime(record,time_index=None):
    if(time_index):
        temp=list(record)
        time_value=temp[time_index]
        if(isinstance(time_value,dt.timedelta)):
            temp[time_index]=(time_value+dt.datetime.min).strftime("%H:%M")
        elif (isinstance(time_value,dt.time)):
            temp[time_index]=time_value.isoformat()
        return tuple(temp)
    else:
        if(isinstance(record,dt.timedelta)):
            return (record+dt.datetime.min).strftime("%H:%M")
        elif (isinstance(record,dt.time)):
            return record.isoformat()

def formatdate(record,date_index=None):
    if(date_index):
        temp=list(record)
        temp[date_index]=temp[date_index].isoformat()
        return tuple(temp)
    else:
        return record.isoformat()



#USER FUNCTIONS

def showuserdetails():
    User_Id=globalobjects.user_id
    global mycursor
    mycursor.execute("select * from Users where User_Id = '{}' ".format(User_Id))
    myresult = mycursor.fetchall()
    print("##",("USER ID","USER PASSWORD","USER EMAIL", "USER PHONE"),"##")
    for i in myresult:
      print(i)
    print()


def update_password():
    User_Id=globalobjects.user_id
    global mycon
    global mycursor
    while(True):
        New_Password=input("ENTER NEW PASSWORD")
        Confirm_New_Password=input("CONFIRM NEW PASSWORD")
        if(New_Password==Confirm_New_Password):
            myresult=query_execute('''UPDATE Users SET User_Password = '{}' where User_Id='{}' '''.format(New_Password,User_Id))
            print("PASSWORD UPDATED\n")
            return New_Password
        else: 
            print("PASSWORDS DO NOT MATCH. TRY AGAIN")

def update_email():
    User_Id=globalobjects.user_id
    global mycon
    global mycursor
    while(True):
        New_Email=input("ENTER NEW EMAIL")
        if(alreadyexists("User_Email",New_Email)):
            print("THIS EMAIL ALREADY EXISTS. ENTER DIFFERENT EMAIL: ")
        else:
            myresult=query_execute('''UPDATE Users SET User_Email = '{}' where User_Id='{}' '''.format(New_Email,User_Id))
            print("EMAIL UPDATED\n")
            return New_Email

def update_phone_no():
   User_Id=globalobjects.user_id
   global mycon
   global mycursor
   while(True):
        New_Phone=input("ENTER NEW PHONE NUMBER")
        if(alreadyexists("User_Phone",New_Phone)):
            print("THIS PHONE NUMBER ALREADY EXISTS. ENTER DIFFERENT PHONE NUMBER: ")
        else:
            myresult=query_execute('''UPDATE Users SET User_Phone = '{}' where User_Id='{}' '''.format(New_Phone,User_Id))
            print("PHONE NUMBER UPDATED\n")
            return New_Phone

def specificflights():
    global mycursor
    Departure = input("DEPARTURE LOCATION : ")
    Arrival = input("ARRIVAL LOCATION : ")
    mycursor.execute('''select *
            from Flights 
            WHERE Flights.From_ = '{}' and Flights.To_ ='{}' '''.format(Departure,Arrival))
    myresult = mycursor.fetchall()
    if myresult == []:
        print("THIS FLIGHT IS NOT AVAILABLE WITH US.\n")
        return "not available"
    else:
        print("AVAILABLE FLIGHTS:")
        print("##",("FLIGHT CODE","AIRLINE","FROM","TO", "DEPARTURE TIME", "TICKET PRICE"),"##")
        for j in myresult:
            j=formattime(j,4)
            print(j)
        print()
        return "available"
'''
def createbookingid():
    value=random.randint(0,99999)
    while(alreadyexists("Booking_Id", value, "Bookings")):
        value=random.randint(0,99999)
    return str(value)
'''

#ADMIN FUNCTIONS

def showflightdetails(Flightcode):
    mycursor.execute('''select *
                     FROM Flights
                     WHERE Flights.Flight_Code='{}' '''. format(Flightcode))
    myresult = mycursor.fetchall()
    print("##",("FLIGHT CODE","AIRLINE","FROM","TO","DEPARTURE TIME","PRICE"),"##")
    for j in myresult:
        j=formattime(j,4)
        print(j)
    print()


def flightalreadyexists(Airline, Departure, Arrival, Time, Price):
     global mycursor
     mycursor.execute('''
        select 1 from Flights
        WHERE Airline='{}' 
        and From_ = '{}' and To_ = '{}' and Departure_Time='{}'
        and Price={} '''.format(Airline,Departure,Arrival,Time,Price))
     myresult = mycursor.fetchall()
     if(myresult==[]):
          return False
     return True

def updateflightfield(Flightcode, Fieldname, value):
     global mycursor
     global mycon
     if Fieldname!='Departure_Time':
         myresult=query_execute("UPDATE FLIGHTS SET {} = '{}' where Flight_Code = '{}' ".format(Fieldname, value, Flightcode))
     else:
         myresult=query_execute("UPDATE FLIGHTS SET {} = {} where Flight_Code = '{}' ".format(Fieldname, value, Flightcode))
     return value

'''
def updateprice(Flightcode, value):
     global mycursor
     global mycon
     mycursor.execute("UPDATE TICKET_PRICE SET PRICE = {} where Flight_Code = '{}' ".format(value, Flightcode))
     mycon.commit()
     return value
'''