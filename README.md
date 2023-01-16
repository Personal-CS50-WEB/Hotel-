# MY HOTEL
#### Video Demo:  
https://youtu.be/vNSFxNEIf5o
#### Description:

 
A flask web application hotel reservation system that enables users to reserve rooms. It offers an administration interface to manage hotel rooms, prices, and reservations.



The website has two different types of users:

  - client: *who can view, book, and cancel reservations.*

  - admin: *In addition to what the client can do, an admin can edit rooms info, and reservations, besides adding/removing another admin.*


**The project consists of the following:**

* Database: *SQLite database file.*
* Business *Layer: It contains all the required logic to perform and maintain hotel operations.*
* UI Layer: *HTML files with CSS and some static files.*

### **Database:**

* hotel.db

  contains three tables

1. users table

*contains user id, name, hashed password, and user type which can be client or admin.*

2. rooms table

*contains information about rooms, room id, number of beds, and price for one day.*

3. reservation table

*contains information about every reservation id (PK), reserved room id (FK), user id (FK), start date, end date, total price for the reservation, and check if it is canceled or valid.*

### **Business Layer:**

A set of python files:

* app.py: *application logic that forwards database requests to sqlifile.py.*

* sqlifile.py: c*ontains database queries and statements.*

* helpers.py : *contains helper functions.*

### **UI:**

### **static files**

  - style.css.
  - static photos.

### **html files**

  * Userlayout.html: *contains the website title and main format for the pages.*

  * register.html:* registration form contains 3 inputs:*
```
username.
password.
password confirmation.
```
*and send post request.*

  * login.html: *login form contians:*
```
username.
password.
```
*and allows users to log in by sending a post request.*

  * index.html: *homepage that shows the hotel photo and information.*

* rooms.html: *table shows information about rooms.*

* book.html: *form allows users to book a number of rooms by sending a post request.*

  * reservation.html: *a form do the following*
```
     * shows information about the reservation.
     * allows users to cancel or edit the reservation.
```

  * edit.html: *form allows admin to change room prices and add more rooms by sending a post request.*

  * admin.html: *form to add/remove admins to/from users by sending a post request.*

   * apology.html: *apology when an error happens.*

   * contact.html: *shows some contact info.*



