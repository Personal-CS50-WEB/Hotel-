from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def get_dates(daterange):

    dates = daterange.split(" - ")
    return(dates)


def get_total_price(date1, date2, price):

    list =[]
    d1 = datetime.strptime(date1, "%m/%d/%Y")
    d2 = datetime.strptime(date2, "%m/%d/%Y")
    difference_in_days = abs((d2 - d1).days)
    total = difference_in_days * price
    list.append(difference_in_days)
    list.append(total)
    
    return(list)