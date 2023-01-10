from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hotel.db")

def select_by_name(username):

    # Query database for username
     rows = db.execute("SELECT * FROM users WHERE name = ?", username)
     return (rows)


def insert_into_users(username, hash):
    # insert into users table
    db.execute("INSERT INTO users(name, hash) VALUES(?, ?)", username, hash)


def get_room_info():

    # query to get rooms prices
    roominfo = db.execute("SELECT price, number_of_beds FROM rooms group by number_of_beds")
    return(roominfo)


def get_available_rooms_by_roomtype_dates(room_type, check_in , check_out):

    # query to find unreseved rooms
    available_rooms = db.execute("SELECT room_id, price FROM rooms where number_of_beds= ? AND"
                                 +" room_id NOT IN (SELECT room_id FROM reservation WHERE cancel = 0 AND (start_date >= ? AND start_date < ? OR"
                                 +" end_date > ? AND end_date <= ? OR start_date < ? and"
                                 +" end_date > ?))", room_type , check_in, check_out, check_in, check_out, check_in, check_out)
    return (available_rooms)


def insert_into_reservasion(room_id, user_id, check_in , check_out, totalprice, price, number_of_nights):

    # insert reservation into sql table
    db.execute("INSERT INTO reservation (room_id, user_id, start_date, end_date, total, price, number_of_nights) VALUES (?, ?, ?, ?, ?, ?, ?)",
               room_id, user_id, check_in, check_out, totalprice, price, number_of_nights)

def cancel_reservation_by_order_id(id):

    # cancel reservation
    db.execute("UPDATE reservation SET canceL = 1 WHERE order_id = ? ", id)


def change_room_in_reservation(room_id, totalprice, price, order_id):

    # update sql table changing room id
    db.execute("UPDATE reservation SET room_id = ?, total = ?, price = ? WHERE order_id = ? ", room_id, totalprice, price, order_id)


def get_available_rooms_by_roomtype_dates_exept_order_id(room_type, check_in , check_out, order_id):

    # query to find unreseved rooms
    available_rooms =  db.execute("SELECT room_id, price FROM rooms where number_of_beds= ? AND room_id NOT IN"
                                         +" (SELECT room_id FROM reservation WHERE cancel = 0 AND order_id != ? AND"
                                         +" (start_date >= ? AND start_date < ? OR end_date > ? AND end_date <= ? OR start_date < ? and"
                                         +" end_date > ?))", room_type , order_id, check_in, check_out, check_in, check_out, check_in, check_out)
    return (available_rooms)


def change_date_in_reservation(room_id, check_in , check_out, totalprice, price, order_id, number_of_nights):

    # update sql table changing dates and room id
    db.execute("UPDATE reservation SET room_id = ?, start_date = ?, end_date = ?, total = ?, price = ?, number_of_nights = ? WHERE order_id = ? ", room_id,
               check_in , check_out, totalprice, price, number_of_nights, order_id)


def change_to_admin(name):

    # update sql table adding new admin
    db.execute("UPDATE users SET type = 'admin' WHERE name = ?", name)

def change_to_client(name):

    # update sql table removing admin
    db.execute("UPDATE users SET type = 'client' WHERE name = ?", name)


def change_room_price(price, roomtype):

    # update every room' price in one type in sql table
    db.execute("UPDATE rooms SET price = ? WHERE number_of_beds = ?", price, roomtype)


def add_room_by_type(type):

    # insert into rooms table
    db.execute("INSERT INTO rooms (number_of_beds, price) VALUES (?, (SELECT price FROM rooms WHERE number_of_beds = ?))",type , type)


def get_reservation_info(user_id):

    # query to get information about user's reservation WHEN client
    table = db.execute("SELECT rooms.room_id, number_of_beds, number_of_nights, reservation.price, start_date, end_date, total, order_id FROM rooms"
                       +" JOIN reservation ON rooms.room_id = reservation.room_id WHERE user_id = ? AND cancel = 0 ORDER BY start_date ASC", user_id)
    return(table)


def get_all_reservations_info():

    # query to get information about users reservations if admin
    table = db.execute("SELECT rooms.room_id, number_of_beds, number_of_nights, reservation.price, start_date, end_date, total, order_id,"
                       +" user_id FROM rooms JOIN reservation ON rooms.room_id = reservation.room_id WHERE cancel = 0 ORDER BY start_date ASC")
    return(table)


def get_order_info(id):

    # query to get order info
    orderinfo = db.execute("SELECT reservation.room_id, start_date, end_date, number_of_beds FROM rooms JOIN reservation ON"
                           +" rooms.room_id = reservation.room_id WHERE order_id= ?", id)
    return(orderinfo)


def get_users():

    # Query database for username
     rows = db.execute("SELECT name FROM users WHERE type != 'admin'")
     return (rows)


def get_other_admins(id):

    # Query database for username
     rows = db.execute("SELECT name FROM users WHERE type = 'admin' AND id != ?", id)
     return (rows)
