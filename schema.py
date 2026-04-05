from globalobjects import mycon, mycursor

def createdb():  
    mycursor.execute("Create database if not exists ATMS_Testing2")
    mycursor.execute("Use ATMS_Testing2")

def createtables():

    #Flights table
    mycursor.execute('''CREATE TABLE IF NOT EXISTS Flights (
    Flight_Code VARCHAR(10) PRIMARY KEY,
    Airline VARCHAR(40) NOT NULL,
    From_ VARCHAR(20) NOT NULL,
    To_ VARCHAR(20) NOT NULL,
    Departure_Time TIME NOT NULL CHECK (Departure_Time>"00:00:00" AND Departure_Time<"24:00:00"),
     Price int NOT NULL CHECK (PRICE>0),
    CONSTRAINT UNIQUE_FLIGHT UNIQUE(AIRLINE,FROM_,TO_,DEPARTURE_TIME,PRICE)
    )'''
  )

    #Users table
    mycursor.execute('''CREATE TABLE IF NOT EXISTS Users (
    User_Id VARCHAR(20) PRIMARY KEY,
    User_Password VARCHAR(255) NOT NULL,
    User_Email VARCHAR(80) UNIQUE NOT NULL,
    User_Phone VARCHAR(12) UNIQUE NOT NULL
)'''
)

    #Bookings table
    mycursor.execute('''Create table if not exists Bookings 
                 (User_Id varchar(20) NOT NULL, Customer_Name varchar(40) NOT NULL,
                 Flight_Code varchar(10) NOT NULL, Date date NOT NULL, 
                 Number_of_Tickets int(20) NOT NULL CHECK (Number_of_Tickets > 0), 
                 Booking_Id int AUTO_INCREMENT primary key,
                 FOREIGN KEY (User_Id) REFERENCES Users(User_Id)
                 ON DELETE CASCADE,
                 FOREIGN KEY (Flight_Code) REFERENCES Flights(Flight_Code)
                 ON DELETE CASCADE
                 )''')


    #Admins table
    mycursor.execute('''Create table if not exists Admins ( Admin_Id varchar(20) primary key,
                    Admin_Password varchar(40) NOT NULL)''')