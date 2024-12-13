import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Connect to MongoDB
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["POST", "GET"])
    def home():
        if request.method == "POST":
            # Get form content
            ec = request.form.get("content")
            d = datetime.datetime.today().strftime("%Y-%m-%d")

            # Insert the entry into MongoDB
            app.db.entries.insert_one({"content": ec, "date": d})

            # Redirect to the GET route to avoid resubmission
            return redirect(url_for("home"))

        # Fetch entries from the database for the GET request
        ent_date = [
            (
                entry["content"],
                entry["date"],
            )
            for entry in app.db.entries.find({})
        ]

        print(ent_date)

        # Render the page with the entries
        return render_template("home.html", e1=ent_date)

    return app


# uncomment to run the app like python app.py
# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)