import globalobjects
from schema import createdb, createtables
from db_utils import * #Supporting Functions
import sys 


print("*"*107)
print("\t"*5, "AIR TICKET MANAGEMENT SYSTEM") 
print("*"*107)

createdb()  #Creates database 'ATMS'
createtables() #Creates tables Flights, Bookings, Users, Admins

mycon=globalobjects.mycon
mycursor=globalobjects.mycursor 

#LOG IN/SIGN UP
while True :
    login = input("ENTER 1 FOR USER\nENTER 2 FOR ADMIN\n")
    if login == "1":
            starting_window = input("PRESS 1 FOR CREATING ACCOUNT\nPRESS 2 FOR LOG IN\n")
            if starting_window == "1":
                User_Id = takeinput("USER ID","User_Id")
                globalobjects.user_id=User_Id
                User_Password=input("ENTER PASSWORD: ")
                User_Email=takeinput("USER EMAIL","User_Email")
                User_Phone=takeinput("USER PHONE NUMBER","User_Phone")
                    
                User_Info = '''insert into Users(User_Id,User_Password,User_Email,User_Phone)
       values('{}','{}','{}','{}')'''.format(User_Id,User_Password,User_Email,User_Phone)
                myresult=query_execute(User_Info)
                #mycon.commit()
                print("ACCOUNT CREATED & LOGGED IN AS USER\n")
                break
                
            elif starting_window == "2": 
                User_Id=takeexistinginput("USER ID","User_Id")
                globalobjects.user_id=User_Id
                while True:
                  value = input("ENTER PASSWORD : ")
                  if(ismatchwithuserid("User_Password",value)):
                      print("LOGGED IN AS USER")
                      User_Password=value
                      break
                  else:
                      print("INCORRECT PASSWORD")
                      continue
                break
            
            else:
                print("PLEASE ENTER VALID NUMBER")    

        
    elif login == "2":
                Admin_Id=takeexistinginput("ADMIN ID","Admin_Id","Admins")
                globalobjects.admin_id=Admin_Id
                while True:
                  value = input("ENTER PASSWORD : ")
                  if(ismatchwithadminid("Admin_Password",value,"Admins")):
                      print("LOGGED IN AS ADMIN")
                      Admin_Password=value
                      break
                  else:
                      print("INCORRECT PASSWORD")
                break
            
    else:
        print("KINDLY ENTER A VALID NUMBER")


#USER

if (login == "1"):
    while(True):
        print("1. PRESS 1 FOR CHECKING FLIGHTS AVAILABLE WITH US")
        print("2. PRESS 2 FOR BOOKING FLIGHT TICKETS")
        print("3. PRESS 3 FOR CHECKING DETAILS OF BOOKING")
        print("4. PRESS 4 FOR CANCELLING FLIGHT BOOKING")
        print("5. PRESS 5 FOR CHECKING YOUR ACCOUNT DETAILS")
        print("6. PRESS 6 FOR EDITING YOUR ACCOUNT DETAILS")
        print("7. PRESS 7 TO EXIT")
        request = input("ENTER NUMBER: ")

        match request:
        
            case '1':
                 while(True):
                    print("1. PRESS 1 FOR CHECKING ALL OPERATIONAL FLIGHTS")
                    print("2. PRESS 2 FOR CHECKING FLIGHTS AS PER DEPARTURE AND ARRIVAL DESTINATIONS")
                    print("3. PRESS 3 TO RETURN TO MAIN MENU")
                    flightrequest=input("ENTER NUMBER: ")
                    
                    match flightrequest:
                        case '1':
                            myresult=query_execute("select * FROM FLIGHTS")
                            print("##",("FLIGHT CODE","AIRLINE","FROM","TO","DEPARTURE TIME","PRICE"),"##")
                            for j in myresult:
                                j=formattime(j,4)
                                print(j)
                            print()
                        
                        case '2':
                            availability=specificflights()
                            if(availability=="not available"):
                                continue

                        case '3':
                            break
                        
                        case _:
                            print("ENTER VALID NUMBER")

            case '2':
                Customer_Name=input("ENTER CUSTOMER NAME: ")
                
                while(True):
                    
                    Flight_Code= input("ENTER FLIGHT CODE: ")
                    myresult=query_execute('''select Price from FLIGHTS where Flight_Code = '{}' '''.format(Flight_Code))
                    if (myresult==[]):
                        print("FLIGHT DOES NOT EXIST")
                    else:
                        Price=myresult[0][0]
                        print("PRICE OF ONE TICKET IS",Price)
                        break
                
                Date = takeinputdate()
                while(True):
                    try:
                        Tickets = int(input("ENTER NUMBER OF TICKETS : "))
                        break
                    except:
                        print("Please enter valid value")
                
                Total_Cost=Tickets*Price;
                
                print("YOUR BOOKING IS:")
                
                print("##","CUSTOMER NAME", "FLIGHT CODE", "DATE", "NUMBER OF TICKETS","##")
                print([Customer_Name, Flight_Code,  formatdate(Date), Tickets])
                
                print("THE TOTAL COST IS", Total_Cost)
                
    
                
                while(True):
                    print(" PRESS 0 TO STOP BOOKING")
                    print(" PRESS 1 TO CONFIRM THE BOOKING")
                    
                    confirm=input("ENTER NUMBER: ")
                    
                    if(confirm=='1'):
                        Booking_Info = '''insert into Bookings (User_Id,Customer_Name,Flight_Code, Date, Number_of_Tickets) values('{}','{}','{}','{}',{})'''.format(User_Id,Customer_Name,Flight_Code, Date, Tickets)
                        myresult=query_execute(Booking_Info)
                        #mycon.commit()
                        print("BOOKING CONFIRMED")
                        myresult=query_execute('''SELECT LAST_INSERT_ID()''')
                        Booking_Id=myresult[0][0]
                        print("YOUR BOOKING ID IS",Booking_Id)
                        print("HAVE A WONDERFUL JOURNEY\n")
                        break
                    
                
                    elif (confirm=='0'):
                       break 
                   
                    else:
                        print("PLEASE ENTER VALID VALUE")
                                         
                                        
            case '3':
                
                while(True):
                    Booking_Id=input("ENTER BOOKING ID")
                    myresult=query_execute('''select * from Bookings  where User_Id= '{}' and  Booking_Id= '{}' '''.format(User_Id, Booking_Id))
                    if(myresult==[]):
                        print("THIS BOOKING DOES NOT EXIST FOR YOU. PLEASE TRY AGAIN")
                    else:
                        break
                    
                print('##',("USER ID","CUSTOMER NAME" ,"FLIGHT CODE", "DATE", "NUMBER OF TICKETS", "BOOKING ID"),'##')
                for j in myresult:
                                j=formatdate(j,3)
                                print(j)
                print()

            case '4':

                while(True):
                    Booking_Id=input("ENTER BOOKING ID: ")
                    myresult=query_execute('''select * from Bookings  where User_Id= '{}' and Booking_Id= '{}' '''.format(User_Id,Booking_Id))
                    if(myresult==[]):
                        print("THIS BOOKING DOES NOT EXIST FOR YOU. PLEASE TRY AGAIN")
                    else:
                        break
                
                while(True):
                        print(" PRESS 1 TO CONFIRM CANCELLATION")
                        print(" PRESS 2 TO STOP CANCELLATION")
                        
                        confirm=input("ENTER NUMBER: ")
                        
                        if(confirm=='1'):
                             myresult=query_execute("delete from Bookings where User_Id='{}' and Booking_Id='{}' ".format(User_Id,Booking_Id))
                             print(f"BOOKING WITH ID {Booking_Id} HAS BEEN CANCELLED\n")
                             break
                    
                    
                        elif (confirm=='2'):
                           break 
                       
                        else:
                            print("PLEASE ENTER VALID VALUE")


            case "5":
                showuserdetails()

            case "6":
                print("CURRENT DETAILS:\n")
                showuserdetails()

                while(True):
                    print("1. PRESS 1 FOR UPDATING YOUR PASSWORD")
                    print("2. PRESS 2 FOR UPDATING YOUR EMAIL")
                    print("3. PRESS 3 FOR UPDATING YOUR PHONE NUMBER")
                    print("4. PRESS 4 TO RETURN TO MAIN MENU")
                    updaterequest=input("ENTER NUMBER: ")

                    match updaterequest:
                        case "1":
                            User_Password=update_password()
                            print("UPDATED DETAILS:\n")
                            showuserdetails()
                        case "2":
                            User_Email=update_email()
                            print("UPDATED DETAILS:\n")
                            showuserdetails()
                        case "3":
                            User_Phone=update_phone_no()
                            print("UPDATED DETAILS:\n")
                            showuserdetails()
                        case "4":
                            break
                        case _:
                            print("ENTER VALID NUMBER")

            case '7':
                break 
      
            case _:
                print("PLEASE ENTER VALID VALUE")


#ADMIN

else:
    while(True):
        print("1. PRESS 1 FOR VIEWING REGISTERED FLIGHTS")
        print("2. PRESS 2 FOR ADDING FLIGHTS TO DATABASE")
        print("3. PRESS 3 FOR MODIFYING FLIGHT DETAILS")
        print("4. PRESS 4 FOR REMOVING FLIGHT FROM DATABASE")
        print("5. PRESS 5 FOR VIEWING FLIGHT BOOKINGS")
        print("6. PRESS 6 FOR CANCELLING CUSTOMER BOOKING")
        print("7. PRESS 7 FOR VIEWING REGISTERED USERS")
        print("8. PRESS 8 FOR REMOVING REGISTERED USER ")
        print("9. PRESS 9 FOR VIEWING YOUR ACCOUNT DETAILS")
        print("10. PRESS 10 FOR CHANGING YOUR PASSWORD")
        print("11. PRESS 11 TO EXIT")

        request = input("ENTER NUMBER: ")
        print()

        match request:

            case '1': #See available flights 

                while(True):
                        print("1. PRESS 1 FOR CHECKING ALL OPERATIONAL FLIGHTS")
                        print("2. PRESS 2 FOR CHECKING FLIGHTS AS PER DEPARTURE AND ARRIVAL DESTINATIONS")
                        print("3. PRESS 3 TO RETURN TO MAIN MENU")
                        flightrequest=input("ENTER NUMBER: ")
                        
                        match flightrequest:
                            case '1':
                                myresult=query_execute("select * FROM FLIGHTS")
                                print("##",("FLIGHT CODE","AIRLINE","FROM","TO","DEPARTURE TIME","PRICE"),"##")
                                for j in myresult:
                                    j=formattime(j,4)
                                    print(j)
                                print()

                            case '2':
                                availability=specificflights()
                                if(availability=="not available"):
                                    continue

                            case '3':
                                break
                            
                            case _:
                                print("ENTER VALID NUMBER")
                                
            case '2': #Add flight 
                    
                Flightcode= takeinput("FLIGHT CODE","FLIGHT_CODE","Flights")
                Airline=input("ENTER AIRLINE")
                Departure=input("ENTER DEPARTURE LOCATION")
                Arrival=input("ENTER ARRIVAL LOCATION")
                Time=takeinputtime()
                while(True):
                    try:
                        Price = int(input("ENTER PRICE OF ONE TICKET : "))
                        break
                    except:
                        print("Please enter valid value")
                
                if(not flightalreadyexists(Airline,Departure,Arrival,Time,Price)):

                    myresult=query_execute('''insert into Flights (Flight_Code, Airline, From_ , To_, Departure_Time, Price) 
                    values ('{}','{}','{}','{}','{}',{}) '''.format(Flightcode,Airline,Departure,Arrival,Time,Price))
                    
                    print("NEW FLIGHT HAS BEEN ADDED:")
                    print("##",("FLIGHT CODE","AIRLINE","FROM","TO", "DEPARTURE TIME, TICKET PRICE"),"##")
                    print(Flightcode," ", Airline, " ",  Departure," ",Arrival, " " ,formattime(Time), " ", Price)
                    print()

                else:
                    print("THIS FLIGHT ALREADY EXISTS\n")
                    
            case '3': #Modify Flight
                print("ENTER FLIGHT CODE OF FLIGHT YOU WISH TO MODIFY")
                Flightcode= takeexistinginput("FLIGHT CODE","FLIGHT_CODE","Flights")
                myresult=query_execute('''select * FROM FLIGHTS
                     WHERE Flights.Flight_Code='{}' '''. format(Flightcode))
                #myresult = mycursor.fetchone()
                Airline=myresult[0][1]
                Departure=myresult[0][2]
                Arrival=myresult[0][3]
                Time=myresult[0][4]
                Price=myresult[0][5]
                

                while(True):
                        
                        print("1. PRESS 1 TO CHANGE THE AIRLINE")
                        print("2. PRESS 2 TO CHANGE THE DEPARTURE LOCATION")
                        print("3. PRESS 3 TO CHANGE THE ARRIVAL LOCATION")
                        print("4. PRESS 4 TO CHANGE THE TIME OF DEPARTURE")
                        print("5. PRESS 5 TO CHANGE THE TICKET PRICE")
                        print("6. PRESS 6 TO RETURN TO MAIN MENU")
                        updaterequest=input("ENTER NUMBER: ")
                        
                        match updaterequest:
                                
                                case '1':
                                    while(True):
                                        newairline= input("ENTER NEW AIRLINE")
                                        if(not flightalreadyexists(newairline,Departure,Arrival,Time,Price)):
                                            Airline=updateflightfield(Flightcode, "Airline", newairline)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS. PLEASE ENTER DIFFERENT AIRLINE")
                                        
                                case '2':
                                    while(True):
                                        newdeparture= input("ENTER NEW DEPARTURE LOCATION")
                                        if(not flightalreadyexists(Airline,newdeparture,Arrival,Time,Price)):
                                            Departure=updateflightfield(Flightcode, "From_", newdeparture)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS. PLEASE ENTER DIFFERENT DEPARTURE LOCATION")
                                    
                                
                                case '3':
                                    while(True):
                                        newarrival= input("ENTER NEW ARRIVAL LOCATION")
                                        if(not flightalreadyexists(Airline,Departure,newarrival,Time,Price)):
                                            Arrival=updateflightfield(Flightcode, "To_", newarrival)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS. PLEASE ENTER DIFFERENT ARRIVAL LOCATION")
                                case '4':
                                    while(True):
                                        newtime= takeinputtime()
                                        if(not flightalreadyexists(Airline,Departure,Arrival,newtime,Price)):
                                            Time=updateflightfield(Flightcode, "Departure_Time", newtime)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS. PLEASE ENTER DIFFERENT TIME OF DEPARTURE")
                                    
                                case '5':
                                    while(True):
                                        newprice= input("ENTER NEW TICKET PRICE")
                                        if(not flightalreadyexists(Airline,Departure,Arrival,Time,newprice)):
                                            Price=updateflightfield(Flightcode, "Price", newprice)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS. PLEASE ENTER DIFFERENT TICKET PRICE")
                                    
                                case '6' :
                                    break
                            
                                case _ :
                                    print ("PLEASE ENTER VALID NUMBER\n")
                                
            case '4': #Remove flight

                Flightcode= takeexistinginput("FLIGHT CODE","FLIGHT_CODE",Table="Flights")
            
                while(True):
                    print(" PRESS 1 TO CONFIRM REMOVAL")
                    print(" PRESS 2 TO STOP REMOVAL")
                    
                    confirm=input("ENTER NUMBER: ")
                    
                    if(confirm=='1'):
                            myresult=query_execute("delete from Flights where Flight_Code='{}' ".format(Flightcode))
                            print(f"FLIGHT WITH FLIGHT CODE {Flightcode} HAS BEEN REMOVED\n")
                            break
                
                
                    elif (confirm=='2'):
                        break 
                    
                    else:
                        print("PLEASE ENTER VALID VALUE")

            case '5': #See customers booking details
                myresult=query_execute("select * from bookings")
                print('##',("USER ID","CUSTOMER NAME" ,"FLIGHT CODE", "DATE", "NUMBER OF TICKETS", "BOOKING ID"),'##')
                for j in myresult:
                    j=formatdate(j,3)
                    print(j)
                print()

            case '6': #cancel customer booking
                Booking_Id=takeexistinginput("BOOKING ID", "Booking_Id", "Bookings")
                while(True):
                    print(" PRESS 1 TO CONFIRM CANCELLATION")
                    print(" PRESS 2 TO STOP CANCELLATION")
                    
                    confirm=input("ENTER NUMBER: ")
                    
                    if(confirm=='1'):
                            myresult=query_execute("delete from Bookings where Booking_Id='{}' ".format(Booking_Id))
                            print(f"BOOKING WITH ID {Booking_Id} HAS BEEN CANCELLED\n")
                            break
                
                
                    elif (confirm=='2'):
                        break 
                    
                    else:
                        print("PLEASE ENTER VALID VALUE")

            case '7': #see user details
                myresult=query_execute("select User_Id, User_Email, User_Phone from Users")
                print("##",("USER ID","USER EMAIL", "USER PHONE"),"##")
                for i in myresult:
                    print(i)
                print()

            case '8': #remove user 
                User_Id=takeexistinginput("USER ID","User_Id")
            
                while(True):
                    print(" PRESS 1 TO CONFIRM REMOVAL")
                    print(" PRESS 2 TO STOP REMOVAL")
                    
                    confirm=input("ENTER NUMBER: ")
                    
                    if(confirm=='1'):
                            myresult=query_execute("delete from Users where User_Id='{}' ".format(User_Id))
                            print(f"USER WITH USER ID {User_Id} HAS BEEN REMOVED\n")
                            break
                
                
                    elif (confirm=='2'):
                        break 
                    
                    else:
                        print("PLEASE ENTER VALID VALUE")

            case '9': #checking your admin account details 
                myresult=query_execute("select * from Admins where Admin_Id = '{}' ".format(Admin_Id))
                print("##",("ADMIN ID","ADMIN PASSWORD"),"##")
                for i in myresult:
                    print(i)
                print()
        
            case '10': #changing password

                while(True):
                    New_Password=input("ENTER NEW PASSWORD")
                    Confirm_New_Password=input("CONFIRM NEW PASSWORD")
                    if(New_Password==Confirm_New_Password):
                        myresult=query_execute('''UPDATE Admins SET Admin_Password = '{}' where Admin_Id='{}' '''.format(New_Password,Admin_Id))
                        print("PASSWORD UPDATED\n")
                        break
                    else: 
                        print("PASSWORDS DO NOT MATCH. TRY AGAIN")

            case '11':
                break

            case _:
                print("PLEASE ENTER VALID NUMBER\n")

    
           
                    
                

  
            

    
    




