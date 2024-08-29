from flask_pymongo import PyMongo
from flask import Flask, session, render_template, request, url_for, redirect
from bson import ObjectId
import os


print(str(os.getcwd()))

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://pragadeshr04:<Password>@user-datas.g2ls6.mongodb.net/Users?retryWrites=true&w=majority"
mongo = PyMongo(app)
print(mongo)

db = mongo.db
collection = db.ToDo
no = mongo.db.ToDo


@app.route("/")
@app.route("/home")
def home():
    
    datas = list(no.find())
    if datas is not None:
        return render_template("notes.html ", datas = datas)
    else:
        return render_template("notes.html")

@app.route("/edited/<id>", methods = ['POST', 'GET'])
def edit(id):
    title = request.form.get("editedtitle")
    desc = request.form.get("editeddesc")
    
    query = {"_id" : ObjectId(id)}
    
    if desc == "":
        no.update_one(query, {"$set":{"title":title}})
    elif title == "":
        no.update_one(query, {"$set":{"desc": desc}})
    else:
        no.update_one(query, {"$set":{"title":title, "desc":desc}})
        
    print(query)
    
    datas = list(no.find())
    return render_template("notes.html", datas = datas)
    

@app.route("/form", methods = ['POST', 'GET'])
def form():
    try:
        title = request.form.get("title")
        desc = request.form.get("desc")
        # print(title,desc)
                
        no.insert_one({"title":title, "desc":desc})
        
        datas = list(no.find())
        print(datas[0])
        
        # return "<h2>Okay</h2>"
        return render_template("notes.html", datas = datas)
    except Exception as e:
        print(e)
        return "e"
        
@app.route("/delete/<id>")
def delete(id):
    print()
    print(id)
    print()
     
    id_ = ObjectId(id)
    print(id_)
    
    query={"_id":id_}
    no.delete_one(query)
    
    return redirect(url_for('home'))

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    name = request.form.get("username")
    password = request.form.get("password")
    print(name, password)
    return render_template('signup.html')

# @app.route("/signin")
@app.route("/signin", methods = ['POST', 'GET'])
def signin():
    name = request.form.get("username")
    password = request.form.get("password")
    print(name, password)
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')