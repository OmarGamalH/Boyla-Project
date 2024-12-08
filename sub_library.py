from flask import url_for , session , redirect
from functools import wraps
def login_required(f):
    @wraps(f)
    def log(*args , **kwargs):
        if session.get("exist") == False or not session.get("exist"):
            return redirect("/login")
        return f(*args , **kwargs)
    return log

def logedin(f):
    @wraps(f)
    def loged(*args , **kwargs):
        if session.get("exist") :
            return redirect("/")
        return f(*args , **kwargs)
    return loged

