from globalobjects import mycon, mycursor

def createdb():  
    mycursor.execute("Create database if not exists ATMS")
    mycursor.execute("Use ATMS")

def createtables():
    #Flights table
    mycursor.execute('''Create table if not exists Flights ( Flight_Code varchar(10) primary key,
                    Airline varchar(40), From_ varchar(20), To_ varchar(20),
                    Departure_Time varchar(20))''')

    #Ticket_Price table
    mycursor.execute('''Create table if not exists Ticket_Price ( Flight_Code varchar(10) primary key,
                    Price int(10))''')

    #Users table
    mycursor.execute('''Create table if not exists Users ( User_Id varchar(20) primary key, User_Password varchar(40),
                    User_Email varchar(80) unique key, User_Phone varchar(14) unique key)''')

    #Bookings table
    mycursor.execute('''Create table if not exists Bookings (User_Id varchar(20), Customer_Name varchar(40),
                    Flight_Code varchar(10), Date varchar(20), Number_of_Tickets int(20), Booking_Id varchar(5) primary key)''')

    #Admins table
    mycursor.execute('''Create table if not exists Admins ( Admin_Id varchar(20) primary key,
                    Admin_Password varchar(40))''')