from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, flash
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, get_dates, get_total_price
from sqlfile import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hotel.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = select_by_name(request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_type"] = rows[0]["type"]

        #usertype
        if session["user_type"] == 'admin':
            # query room types
            roomstype = get_room_info()
            return render_template("edit.html", roomstype=roomstype)


        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/")
@login_required
def index():
    """Show hotel photos"""

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Ensure confirm was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        # Ensure password confirm matchs
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password doesn't match")

        # Query database for username
        check = select_by_name(request.form.get("username"))

        # Ensure username is not taken
        if len(check) != 0:
            return apology("username already exists")

        # hash password
        hashed_pass = generate_password_hash((request.form.get("password")), salt_length=len(request.form.get("password")))

        # insert into users table
        insert_into_users(request.form.get("username"), hashed_pass)

        user = select_by_name(request.form.get("username"))
        # Remember which user has logged in
        session["user_id"] = user[0]["id"]
        session["user_type"] = user[0]["type"]

        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/contact")
def contact():
    """Show portfolio of stocks"""

    return render_template("contact.html")


@app.route("/rooms")
def rooms():
    """Show hotelrooms photos"""

    # room information
    roominfo = get_room_info()
    return render_template("rooms.html", roominfo=roominfo)


@app.route("/book", methods=["GET", "POST"])
@login_required
def book():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # check errors
        if not request.form.get("number of rooms"):
            return apology("Missing rooms ")

        # check if room type is blank
        if not request.form.get("room"):
            return apology("Missing room type ")

        # check if invalid number of rooms
        try:
            numberOfrooms = int(request.form.get("number of rooms"))
        except ValueError:
            return apology("Unavailable")

        # get start and end date
        dates = get_dates(request.form.get("daterange"))
        if dates[0] == dates[1]:
            return apology("Must choose date")
        # query to find unreseved rooms
        available_rooms = get_available_rooms_by_roomtype_dates(request.form.get("room") , dates[0], dates[1])

        # if unavaliable room(s)
        if len(available_rooms) < numberOfrooms:
             return apology("Unavailable number of rooms in that date", 400)

        # calculate total price for one room
        total = get_total_price(dates[0], dates[1], available_rooms[0]['price'])

        # if avaliable room (s)
        for i in range(numberOfrooms):
            # insert reservation into sql table
            insert_into_reservasion(available_rooms[i]['room_id'], session["user_id"], dates[0], dates[1], total[1], available_rooms[0]['price'], total[0])
        flash('Reservation confirmed!')

        # Redirect user
        return redirect("/reservation")

    # if method = get
    else:
        # query room types
        rooms = get_room_info()
        return render_template("book.html", rooms=rooms)


@app.route("/reservation", methods=["GET", "POST"])
@login_required
def reservation_cancel():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # if user wants to cancel
        if request.form['submit'] == 'Cancel':
            # cancel reservation
            cancel_reservation_by_order_id(request.form['id'])
            flash('Room canceled!')

        # if user wants to change room
        elif request.form['submit'] == 'Change room':

            # check if room type is blank
            if not request.form.get("room"):
                return apology("Missing room type ")

            #query to get order info
            orderinfo = get_order_info(request.form.get("order_id"))
            # query to find unreseved rooms
            available_rooms = get_available_rooms_by_roomtype_dates(request.form.get("room") ,
                                                                    orderinfo[0]['start_date'],
                                                                    orderinfo[0]['end_date'])

            # if unavaliable room(s)
            if len(available_rooms) == 0:
                return apology("unavailable number of rooms in that date")

            # if user selected the same room type
            if int(orderinfo[0]['number_of_beds']) == int(request.form.get("room")):
                flash('Must choose number of beds!')
                return redirect("/reservation")

            # calculate total price for all days
            total = get_total_price(orderinfo[0]['start_date'], orderinfo[0]['end_date'], available_rooms[0]['price'])

            # update sql table changing room id
            change_room_in_reservation(available_rooms[0]['room_id'], total[1], available_rooms[0]['price'], request.form.get("order_id"))
            flash('Room changed!')

        # if user wants to change date
        elif request.form['submit'] == 'Change date':
            # get start and end date
            dates = get_dates(request.form.get("daterange"))
            if dates[0] == dates[1]:
                return apology("Must choose date")

            #query to get order info
            orderinfo = get_order_info(request.form.get("order_id"))

            # query to find unreseved rooms
            available_rooms = get_available_rooms_by_roomtype_dates_exept_order_id(orderinfo[0]['number_of_beds'], dates[0],
                                                                                   dates[1], request.form.get("order_id"))

            if not available_rooms:
                return apology("Not available in that date")

            # total price for all days
            total = get_total_price(dates[0], dates[1], available_rooms[0]['price'])

            # update sql table changing dates and room id
            change_date_in_reservation(available_rooms[0]['room_id'], dates[0], dates[1], total[1], available_rooms[0]['price'],
                                       request.form.get("order_id"), total[0])
            flash('Date changed!')

        return redirect("/reservation")

    # if method = get
    else:
        # if admin
        if session["user_type"] == 'admin':
            table = get_all_reservations_info()
        else:
            # query to get information about user's reservation when client
            table = get_reservation_info(session["user_id"])

        # query room types
        roomstype = get_room_info()
        return render_template("reservation.html", table=table, roomstype=roomstype)


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # when adding more rooms
        if request.form['submit'] == 'Add rooms':
            # check errors
            if not request.form.get("number of rooms"):
                return apology("Missing number of rooms ")

            # check if room type is blank
            if not request.form.get("number_of_beds"):
                return apology("Missing room type ")

            try:
                numberOfrooms = int(request.form.get("number of rooms"))
            except ValueError:
                return apology("Unavailable")

            # insert into rooms table
            for _ in range(numberOfrooms):
                add_room_by_type(request.form.get("number_of_beds"))
            flash('Room added!')

        # when changing rooms price
        elif request.form['submit'] == 'Change':
            # check errors if any field is blank
            if not request.form.get("room"):
                return apology("Missing room type ")

            # check if price is blank
            if not request.form.get("price"):
                return apology("Missing price")

            # update every room' price in one type in sql table
            change_room_price(request.form.get("price"), request.form.get("room"))
            flash('Price changed!')
        return redirect("/")

    # if method = get
    else:
        # query room types
        roomstype = get_room_info()
        return render_template("edit.html", roomstype=roomstype)


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # if using add admin form
        if request.form['submit'] == 'Add':
            # check errors
            if not request.form.get("name"):
                return apology("Must provide name")

            # update sql table adding new admin
            change_to_admin(request.form.get("name"))
            flash('Admin added!')

        # if using remove admin form
        elif request.form['submit'] == 'Remove':
            # check errors
            if not request.form.get("name"):
                return apology("Must provide name")

            # update sql table removing admin
            change_to_client(request.form.get("name"))
            flash('Admin removed')
        return redirect("/")

    # if method = get
    else:
        users = get_users()
        admins = get_other_admins(session["user_id"])
        return render_template("admin.html", users=users, admins=admins)
