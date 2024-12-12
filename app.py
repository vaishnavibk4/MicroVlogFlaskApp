import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient


def create_app():
    app=Flask(__name__)

    client= MongoClient("mongodb+srv://vaishnavi:root@cluster0.t266r.mongodb.net/")

    app.db =client.microblog

    @app.route("/",methods=["POST","GET"])
    def home():
        
        if request.method == "POST":
            ec=request.form.get("content")
            d=datetime.datetime.today().strftime("%Y-%m-%d")
    
            app.db.entries.insert_one({"content":ec,"date":d})
        ent_date= [
            (
            entry["content"],
            entry["date"],
            # datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]


        print(ent_date)

        return render_template("home.html", e1=ent_date)

    
    return app
