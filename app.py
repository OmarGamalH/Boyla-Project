from flask import Flask , render_template , redirect , session , request
from flask_session import Session
from cs50 import SQL
from sub_library import login_required , logedin
from werkzeug.security import generate_password_hash , check_password_hash
from datetime import datetime



app = Flask(__name__)

app.config["SESSION_PERMENANT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")



@app.route("/" , methods = ["GET", "POST"])
@login_required
def index():
        session["products"] = ["car" , "phone"]
        if request.method == "GET" or (request.method == "POST" and (request.form.get("category") == "all")):
            products = db.execute("SELECT * FROM products , connect WHERE products.id = connect.product_id ORDER BY date DESC")
        elif request.method == "POST" and request.form.get("category") == "recommend":
            cash = db.execute("SELECT cash FROM users WHERE id = ?" , session.get("id"))[0]["cash"]
            products = db.execute("SELECT * FROM products , connect WHERE products.id = connect.product_id AND price <= ? ORDER BY date DESC" , cash)
        elif request.method == "POST" and request.form.get("category"):
            products = db.execute("SELECT * FROM products , connect WHERE products.id = connect.product_id AND type = ? ORDER BY date DESC" , request.form.get("category"))
        else:
            products = products = db.execute("SELECT * FROM products , connect WHERE products.id = connect.product_id ORDER BY date DESC")
        return render_template("index.html" , products = products , user_id = session.get("id") , category = session.get("products"))

@app.route("/logingin" , methods = ["POST"])
def logingin():
    email = request.form.get("email")
    password= request.form.get("password")
    person = db.execute("SELECT * FROM users WHERE email = ?" , email)
    if not email or not password:
         return render_template("error.html" , error = "All info required")
    if len(person) != 1 or not check_password_hash( person[0]["hash"] , password):
        return render_template("error.html" , error = "Invalid email or password")
    else:
        session["exist"] = True
        session["id"] = db.execute("SELECT id FROM users WHERE email = ?" , email)[0]["id"]
        return redirect("/")


@app.route("/login" , methods = ["GET" ,"POST"])
@logedin
def login():

    if request.method == "POST":
        first_name = request.form.get("first_name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        if not first_name or not surname or not email or not password or gender == "not_selected" or not phone:
             return render_template("error.html" , error = "All info required")
        person = db.execute("SELECT * FROM users WHERE email = ?" , email)
        if not person:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (name , email , hash , gender , phone) VALUES(? , ? , ? , ? , ?)" , (first_name + "" + surname) , email , hash , gender , phone)
            session["id"] = db.execute("SELECT id FROM users WHERE email = ?" , email)[0]["id"]
            session["exist"] = True
            return redirect("/login")
        else:
            return render_template("error.html" , error = "EMAIL USED ALREADY")


    else:
        return render_template("login.html")


@app.route("/register")
@logedin
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/profile/<number>" , methods = ["GET" , "POST"])
@login_required
def profile(number):
        person = db.execute("SELECT * FROM users WHERE id = ?" , number)
        return render_template("profile.html" , humen = person , number = number)

@app.route("/profile" , methods = ["GET" , "POST"])
def profile2():
        if request.method == "POST":
             person_cash = request.form.get("cash")
             if not person_cash:
                  return render_template("error.html" , error = "YOU DIDN'T ENTER CASH")
             else:
                  person_cash = float(person_cash)
                  db.execute("UPDATE users SET cash = ? WHERE id = ?" , person_cash , session.get("id"))
                  return redirect("/profile")
        else:
            person2 = db.execute("SELECT * FROM users WHERE id = ?" , session.get("id"))
            return render_template("profile.html" , humen = person2)

@app.route("/add" , methods = ["GET" , "POST"])
def add():
    if request.method == "POST":
            product = request.form.get("product")
            price = request.form.get("price")
            number = request.form.get("number")
            short_description = request.form.get("short_description")
            long_description = request.form.get("long_description")
            if not product or not price or not number or not short_description or not long_description or not number.isdigit():
                return render_template("error.html" , error = "NOT VALID INFO")
            if product or price or number or short_description or long_description or number.isdigit():
                time = datetime.now()
                db.execute("INSERT INTO products (type , price , number , description , product_header , date) VALUES(? , ? , ? , ? , ? , ?)" , product , price , number , long_description , short_description , time)
                product_id = db.execute("SELECT id FROM products WHERE type = ? AND price = ? AND number = ? And date = ?" , product , price , number , time)[0]["id"]
                db.execute("INSERT INTO connect (user_id , product_id) VALUES(? , ?)" , session.get("id") , product_id)
                return redirect("/")
            else:
                return render_template("error.html" , error = "You must provide all details needed")

    else:
        products = session.get("products")
        return render_template("add.html" , products = products)

@app.route("/details/<number>")
@login_required
def details(number):
   product = db.execute("SELECT * FROM products WHERE id = ? LIMIT 1" , number)
   person_selling = db.execute("SELECT user_id FROM connect WHERE product_id = ?" , number)[0]["user_id"]
   return render_template("details.html" , product_id = number , person_selling = person_selling , products = product)



@app.route("/password" , methods = ["GET" , "POST"])
@logedin
def password():
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        email = request.form.get("email")
        person = db.execute("SELECT * FROM users WHERE email = ?" , email)
        if len(person)!= 1  or not check_password_hash(person[0]["hash"] , old_password):
             return render_template("error.html" , error = "Invalid password or email")
        else:
            id = person[0]["id"]
            db.execute("UPDATE users SET hash = ? WHERE id = ?" , generate_password_hash(new_password) , id)
            return redirect("/password")
    else:
         return render_template("password.html")
# products = db.execute("SELECT * FROM products , connect WHERE products.id = connect.product_id")
            # return render_template("index.html" , products = products)
