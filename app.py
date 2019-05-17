from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import datetime
import mars_scrape

app = Flask(__name__)

#Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

@app.route("/")
def index():
    scraped = mongo.db.mars_data.find_one()
    return render_template("index.html", scraped=scraped)

@app.route("/scrape")
def scraper():
    scraped = mars_scrape.scrape()
    mongo.db.mars_data.update({}, scraped, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)