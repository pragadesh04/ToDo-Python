import bcrypt as bc
from flask_pymongo import PyMongo
from flask import Flask, session, render_template, request, url_for, redirect, flash
from bson import ObjectId
import os
import re
import secrets

app = Flask(__name__)

def is_valid_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, ""

# Configurations
app.config["MONGO_URI"] = "mongodb+srv://pragadeshr04:<password>@user-datas.g2ls6.mongodb.net/Users?retryWrites=true&w=majority"
app.config["SECRET_KEY"] = secrets.token_hex(32)

mongo = PyMongo(app)
db = mongo.db
notes = db.ToDo
users = db.usersToDo

@app.route("/")
@app.route("/home/<name>/<id>")
def home(name = None, id=None):
    if not session.get("username"):
        return render_template("login.html")
    
    session["user_id"] = id
    datas = list(notes.find({"user_id":ObjectId(id)}))
    print(datas)
    print(f"{session.get('username')}".center(150, "="))
    if datas is not None:
        return render_template("notes.html", datas = datas, id = id)


@app.route("/edited/<id>", methods=['POST', 'GET'])
def edit(id=None):
    title = request.form.get("editedtitle")
    desc = request.form.get("editeddesc")
    query = {"_id": ObjectId(id)}
    
    update_data = {}
    if title:
        update_data["title"] = title
    if desc:
        update_data["desc"] = desc
    
    if update_data:
        notes.update_one(query, {"$set": update_data})
    
    datas = list(notes.find({"user_id":ObjectId(id)}))
    return redirect(url_for("home", name = session["username"], id =ObjectId(session["user_id"])))


@app.route("/form/<id>", methods=['POST', 'GET'])
def form(id):
    try:
        print(f"""{id}""".center(150,"-"))
        
        title = request.form.get("title")
        desc = request.form.get("desc")
        
        
        
        notes.insert_one({"user_id":ObjectId(id),"title": title, "desc": desc})
        datas = list(notes.find({"user_id":ObjectId(id)}))
        return redirect(url_for("home", name = session["username"], id = id))
    except Exception as e:
        print(e)
        return "Error"

@app.route("/delete/<id>")
def deleted(id):
    query = {"_id": ObjectId(id)}
    notes.delete_one(query)
    return redirect(url_for('home', name = session["username"], id= session["user_id"]))

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/signup-form", methods=['POST', 'GET'])
def signup_form():
    name = request.form.get("username")
    password = request.form.get("password")
    newpassword = request.form.get("newpassword")
    mail = request.form.get("mail")
    
    msg = is_valid_password(password)
    
    if msg[0] is False:
        return render_template("message.html", message  = msg[1], message_head = "Not valid Info")
    if password != newpassword:
        return render_template("message.html", message  = "Password Does Not Match", message_head = "Not valid Info")
    
    userN = users.find_one({"username": name})
    userM = users.find_one({"mail": mail})
    
    if userN or userM:
        return redirect(url_for("signin"))
    
    salt = bc.gensalt()
    hashPass = bc.hashpw(password.encode('utf-8'), salt)
    users.insert_one({"uname": name, "password": hashPass, "mail": mail})
    return render_template('login.html')

@app.route("/signin")
def signin():
    return render_template('login.html')

@app.route("/signin-form", methods=['POST', 'GET'])
def signin_form():
    name = request.form.get("username")
    password = request.form.get("password")
    
    userN = users.find_one({"uname": name})
    
    if not userN:
        return redirect(url_for("signup"))
    
    if bc.checkpw(password.encode('utf-8'), userN["password"]):
        session['username'] = name
        return redirect(url_for("home", name  = name, id = userN["_id"]))
    else:
        return render_template("message.html", message_head  = "something", message = "sorry, Something Went Wromg")

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for("home"))

@app.route("/message")
def message():
    return render_template("message.html", message_head = "empty Message", message = "Know Better Get Better")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
