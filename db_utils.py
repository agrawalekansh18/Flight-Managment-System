import random
import globalobjects 

mycon=globalobjects.mycon
mycursor=globalobjects.mycursor 

#SUPPORTING FUNCTIONS

def takeinput(PHONE_NUMBER,User_Phone,Table="Users"):
     while True:
                  value= input(f"ENTER {PHONE_NUMBER} : ")
                  if(alreadyexists(User_Phone,value,Table)):
                    print(f"THIS {PHONE_NUMBER} ALREADY EXISTS. ENTER DIFFERENT {PHONE_NUMBER}: ")
                  else:
                      return value

def alreadyexists(User_Phone,value,Table="Users"):
    global mycursor
    mycursor.execute(f"Select * from {Table} where {User_Phone}='{value}'")
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
            mycursor.execute('''UPDATE Users SET User_Password = '{}' where User_Id='{}' '''.format(New_Password,User_Id))
            mycon.commit()
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
            mycursor.execute('''UPDATE Users SET User_Email = '{}' where User_Id='{}' '''.format(New_Email,User_Id))
            mycon.commit()
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
            mycursor.execute('''UPDATE Users SET User_Phone = '{}' where User_Id='{}' '''.format(New_Phone,User_Id))
            mycon.commit()
            print("PHONE NUMBER UPDATED\n")
            return New_Phone

def specificflights():
    global mycursor
    Departure = input("DEPARTURE LOCATION : ")
    Arrival = input("ARRIVAL LOCATION : ")
    mycursor.execute(f"select Flights.Flight_Code, Airline, Departure_Time, Price from Flights, Ticket_Price where Flights.Flight_Code=Ticket_Price.Flight_Code and From_ = '{Departure}' and To_ ='{Arrival}'")
    myresult = mycursor.fetchall()
    if myresult == []:
        print("THIS FLIGHT IS NOT AVAILABLE WITH US.\n")
        return "not available"
    else:
        print("AVAILABLE FLIGHTS:")
        print("##",("FLIGHT CODE","AIRLINE","FROM","TO", "DEPARTURE TIME", "TICKET PRICE"),"##")
        for j in myresult:
            print(j)
        print()
        return "available"

def createbookingid():
    value=random.randint(0,99999)
    while(alreadyexists("Booking_Id", value, "Bookings")):
        value=random.randint(0,99999)
    return str(value)

#ADMIN FUNCTIONS

def showflightdetails(Flightcode):
    mycursor.execute("select Flights.*, Price from Flights, Ticket_Price where Flights.Flight_Code='{}' and Ticket_Price.Flight_Code='{}' ". format(Flightcode,Flightcode))
    myresult = mycursor.fetchall()
    print("##",("FLIGHT CODE","AIRLINE","FROM","TO","DEPARTURE TIME","PRICE"),"##")
    for j in myresult:
        print(j)
    print()


def flightalreadyexists(Flightcode, Airline, Departure, Arrival, Time, Price):
     global mycursor
     mycursor.execute('''select *  from Flights, Ticket_Price where
         Flights.Flight_Code=Ticket_Price.Flight_Code and Airline='{}' 
        and From_ = '{}' and To_ = '{}' and Departure_Time='{}'
        and Price={} '''.format(Airline,Departure,Arrival,Time,Price))
     myresult = mycursor.fetchall()
     if(myresult==[]):
          return False
     return True

def updateflightfield(Flightcode, Fieldname, value):
     global mycursor
     global mycon
     mycursor.execute("UPDATE FLIGHTS SET {} = '{}' where Flight_Code = '{}' ".format(Fieldname, value, Flightcode))
     mycon.commit()
     return value

def updateprice(Flightcode, value):
     global mycursor
     global mycon
     mycursor.execute("UPDATE TICKET_PRICE SET PRICE = {} where Flight_Code = '{}' ".format(value, Flightcode))
     mycon.commit()
     return value