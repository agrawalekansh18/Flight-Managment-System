import globalobjects
from schema import createdb, createtables
from db_utils import * #Supporting Functions 


print("*"*107)
print("\t"*5, "AIR TICKET MANAGEMENT SYSTEM") 
print("*"*107)

createdb()  #Creates database 'ATMS'
createtables() #Creates tables Flights, Ticket_Price, Bookings, Users, Admins

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
                mycursor.execute(User_Info)
                mycon.commit()
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
                            mycursor.execute("select Flights.*, Price from Flights, Ticket_Price where Flights.Flight_Code=Ticket_Price.Flight_Code")
                            myresult = mycursor.fetchall()
                            print("##",("FLIGHT CODE","AIRLINE","FROM","TO","DEPARTURE TIME","PRICE"),"##")
                            for j in myresult:
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
                    mycursor.execute('''select Price from Ticket_Price where Flight_Code = '{}' '''.format(Flight_Code))
                    myresult=mycursor.fetchall()
                    if (myresult==[]):
                        print("FLIGHT DOES NOT EXIST")
                    else:
                        Price=myresult[0][0]
                        print("PRICE OF ONE TICKET IS",Price)
                        break
                
                Date = input("ENTER DATE OF FLIGHT (YYYY-MM-DD): ")
                Tickets = int(input("ENTER NUMBER OF TICKETS : "))
                
                Total_Cost=Tickets*Price;
                
                print("YOUR BOOKING IS:")
                
                print("CUSTOMER NAME,   FLIGHT CODE,   DATE,   NUMBER OF TICKETS")
                print(Customer_Name," ", Flight_Code, " ",  Date," ",  Tickets)
                
                print("THE TOTAL COST IS", Total_Cost)
                
    
                
                while(True):
                    print(" PRESS 0 TO STOP BOOKING")
                    print(" PRESS 1 TO CONFIRM THE BOOKING")
                    
                    confirm=int(input("ENTER NUMBER: "))
                    
                    if(confirm==1):
                        Booking_Id=createbookingid()
                        Booking_Info = '''insert into Bookings (User_Id,Customer_Name,Flight_Code, Date, Number_of_Tickets, Booking_Id) values('{}','{}','{}','{}',{},'{}')'''.format(User_Id,Customer_Name,Flight_Code, Date, Tickets, Booking_Id)
                        mycursor.execute(Booking_Info)
                        mycon.commit()
                        print("BOOKING CONFIRMED")
                        print("YOUR BOOKING ID IS",Booking_Id)
                        print("HAVE A WONDERFUL JOURNEY\n")
                        break
                    
                
                    elif (confirm==0):
                       break 
                   
                    else:
                        print("PLEASE ENTER VALID VALUE")
                                         
                                        
            case '3':
                
                while(True):
                    Booking_Id=input("ENTER BOOKING ID")
                    mycursor.execute('''select * from Bookings  where User_Id= '{}' and  Booking_Id= '{}' '''.format(User_Id, Booking_Id))
                    myresult=mycursor.fetchall()
                    if(myresult==[]):
                        print("THIS BOOKING DOES NOT EXIST FOR YOU. PLEASE TRY AGAIN")
                    else:
                        break
                    
                print('##',("USER ID","CUSTOMER NAME" ,"FLIGHT CODE", "DATE", "NUMBER OF TICKETS", "BOOKING ID"),'##')
                for j in myresult:
                                print(j)
                print()

            case '4':

                while(True):
                    Booking_Id=input("ENTER BOOKING ID: ")
                    mycursor.execute('''select * from Bookings  where User_Id= '{}' and Booking_Id= '{}' '''.format(User_Id,Booking_Id))
                    myresult=mycursor.fetchall()
                    if(myresult==[]):
                        print("THIS BOOKING DOES NOT EXIST FOR YOU. PLEASE TRY AGAIN")
                    else:
                        break
                
                while(True):
                        print(" PRESS 1 TO CONFIRM CANCELLATION")
                        print(" PRESS 2 TO STOP CANCELLATION")
                        
                        confirm=int(input("ENTER NUMBER: "))
                        
                        if(confirm==1):
                             mycursor.execute("delete from Bookings where User_Id='{}' and Booking_Id='{}' ".format(User_Id,Booking_Id))
                             mycon.commit()
                             print(f"BOOKING WITH ID {Booking_Id} HAS BEEN CANCELLED\n")
                             break
                    
                    
                        elif (confirm==2):
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
                                mycursor.execute("select Flights.*, Price from Flights, Ticket_Price where Flights.Flight_Code=Ticket_Price.Flight_Code")
                                myresult = mycursor.fetchall()
                                print("##",("FLIGHT CODE","AIRLINE","FROM","TO","DEPARTURE TIME","PRICE"),"##")
                                for j in myresult:
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
                Time=input("ENTER TIME OF DEPARTURE (IN 24 HOUR FORMAT AS HR:MIN)")
                Price=int(input("ENTER PRICE OF ONE TICKET"))
                
                if(not flightalreadyexists(Flightcode,Airline,Departure,Arrival,Time,Price)):

                    mycursor.execute('''insert into Flights (Flight_Code, Airline, From_ , To_, Departure_Time) 
                    values ('{}','{}','{}','{}','{}') '''.format(Flightcode,Airline,Departure,Arrival,Time))
                    mycursor.execute('''insert into Ticket_Price (Flight_Code, Price)
                        values ('{}',{})'''.format(Flightcode,Price) )
                    mycon.commit()
                    
                    print("NEW FLIGHT HAS BEEN ADDED:")
                    print("##",("FLIGHT CODE","AIRLINE","FROM","TO", "DEPARTURE TIME, TICKET PRICE"),"##")
                    print(Flightcode," ", Airline, " ",  Departure," ",Arrival, " " ,Time, " ", Price)
                    print()

                else:
                    print("THIS FLIGHT ALREADY EXISTS UNDER DIFFERENT FLIGHT CODE\n")
                    
            case '3': #Modify Flight
                print("ENTER FLIGHT CODE OF FLIGHT YOU WISH TO MODIFY")
                Flightcode= takeexistinginput("FLIGHT CODE","FLIGHT_CODE","Flights")
                mycursor.execute('''select Flights.*, Price from Flights, Ticket_Price where 
                    Flights.Flight_Code='{}' and Ticket_Price.Flight_Code='{}' '''.format(Flightcode,Flightcode))
                myresult = mycursor.fetchone()

                Airline=myresult[1]
                Departure=myresult[2]
                Arrival=myresult[3]
                Time=myresult[4]
                Price=myresult[5]
                

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
                                        if(not flightalreadyexists(Flightcode,newairline,Departure,Arrival,Time,Price)):
                                            Airline=updateflightfield(Flightcode, "Airline", newairline)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS UNDER DIFFERENT FLIGHT CODE. PLEASE ENTER DIFFERENT AIRLINE")
                                        
                                case '2':
                                    while(True):
                                        newdeparture= input("ENTER NEW DEPARTURE LOCATION")
                                        if(not flightalreadyexists(Flightcode,Airline,newdeparture,Arrival,Time,Price)):
                                            Departure=updateflightfield(Flightcode, "From_", newdeparture)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS UNDER DIFFERENT FLIGHT CODE. PLEASE ENTER DIFFERENT DEPARTURE LOCATION")
                                    
                                
                                case '3':
                                    while(True):
                                        newarrival= input("ENTER NEW ARRIVAL LOCATION")
                                        if(not flightalreadyexists(Flightcode,Airline,Departure,newarrival,Time,Price)):
                                            Arrival=updateflightfield(Flightcode, "To_", newarrival)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS UNDER DIFFERENT FLIGHT CODE. PLEASE ENTER DIFFERENT ARRIVAL LOCATION")
                                case '4':
                                    while(True):
                                        newtime= input("ENTER NEW TIME OF DEPARTURE")
                                        if(not flightalreadyexists(Flightcode,Airline,Departure,Arrival,newtime,Price)):
                                            Time=updateflightfield(Flightcode, "Departure_Time", newtime)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS UNDER DIFFERENT FLIGHT CODE. PLEASE ENTER DIFFERENT TIME OF DEPARTURE")
                                    
                                case '5':
                                    while(True):
                                        newprice= input("ENTER NEW TICKET PRICE")
                                        if(not flightalreadyexists(Flightcode,Airline,Departure,Arrival,Time,newprice)):
                                            Time=updateprice(Flightcode, newprice)
                                            print("UPDATED FLIGHT DETAILS:\n")
                                            showflightdetails(Flightcode)
                                            break
                                        else:
                                            print("THIS FLIGHT ALREADY EXISTS UNDER DIFFERENT FLIGHT CODE. PLEASE ENTER DIFFERENT TICKET PRICE")
                                    
                                case '6' :
                                    break
                            
                                case _ :
                                    print ("PLEASE ENTER VALID NUMBER\n")
                                
            case '4': #Remove flight

                Flightcode= takeexistinginput("FLIGHT CODE","FLIGHT_CODE",Table="Flights")
            
                while(True):
                    print(" PRESS 1 TO CONFIRM REMOVAL")
                    print(" PRESS 2 TO STOP REMOVAL")
                    
                    confirm=int(input("ENTER NUMBER: "))
                    
                    if(confirm==1):
                            mycursor.execute("delete from Flights where Flight_Code='{}' ".format(Flightcode))
                            mycursor.execute("delete from Ticket_Price where Flight_Code='{}' ".format(Flightcode))
                            mycon.commit()
                            print(f"FLIGHT WITH FLIGHT CODE {Flightcode} HAS BEEN REMOVED\n")
                            break
                
                
                    elif (confirm==2):
                        break 
                    
                    else:
                        print("PLEASE ENTER VALID VALUE")

            case '5': #See customers booking details
                mycursor.execute("select * from bookings")
                myresult = mycursor.fetchall()
                print('##',("USER ID","CUSTOMER NAME" ,"FLIGHT CODE", "DATE", "NUMBER OF TICKETS", "BOOKING ID"),'##')
                for j in myresult:
                    print(j)
                print()

            case '6': #cancel customer booking
                Booking_Id=takeexistinginput("BOOKING ID", "Booking_Id", "Bookings")
                while(True):
                    print(" PRESS 1 TO CONFIRM CANCELLATION")
                    print(" PRESS 2 TO STOP CANCELLATION")
                    
                    confirm=int(input("ENTER NUMBER: "))
                    
                    if(confirm==1):
                            mycursor.execute("delete from Bookings where Booking_Id='{}' ".format(Booking_Id))
                            mycon.commit()
                            print(f"BOOKING WITH ID {Booking_Id} HAS BEEN CANCELLED\n")
                            break
                
                
                    elif (confirm==2):
                        break 
                    
                    else:
                        print("PLEASE ENTER VALID VALUE")

            case '7': #see user details
                mycursor.execute("select User_Id, User_Email, User_Phone from Users")
                myresult = mycursor.fetchall()
                print("##",("USER ID","USER EMAIL", "USER PHONE"),"##")
                for i in myresult:
                    print(i)
                print()

            case '8': #remove user 
                User_Id=takeexistinginput("USER ID","User_Id")
            
                while(True):
                    print(" PRESS 1 TO CONFIRM REMOVAL")
                    print(" PRESS 2 TO STOP REMOVAL")
                    
                    confirm=int(input("ENTER NUMBER: "))
                    
                    if(confirm==1):
                            mycursor.execute("delete from Users where User_Id='{}' ".format(User_Id))
                            mycon.commit()
                            print(f"USER WITH USER ID {User_Id} HAS BEEN REMOVED\n")
                            break
                
                
                    elif (confirm==2):
                        break 
                    
                    else:
                        print("PLEASE ENTER VALID VALUE")

            case '9': #checking your admin account details 
                mycursor.execute("select * from Admins where Admin_Id = '{}' ".format(Admin_Id))
                myresult = mycursor.fetchall()
                print("##",("ADMIN ID","ADMIN PASSWORD"),"##")
                for i in myresult:
                    print(i)
                print()
        
            case '10': #changing password

                while(True):
                    New_Password=input("ENTER NEW PASSWORD")
                    Confirm_New_Password=input("CONFIRM NEW PASSWORD")
                    if(New_Password==Confirm_New_Password):
                        mycursor.execute('''UPDATE Admins SET Admin_Password = '{}' where Admin_Id='{}' '''.format(New_Password,Admin_Id))
                        mycon.commit()
                        print("PASSWORD UPDATED\n")
                        break
                    else: 
                        print("PASSWORDS DO NOT MATCH. TRY AGAIN")

            case '11':
                break

            case _:
                print("PLEASE ENTER VALID NUMBER\n")

    
           
                    
                

  
            

    
    




