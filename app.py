from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars.drop()

# Creates a collection in the database and inserts two documents
db.mars.insert_many(
    [
        {
            'title': 'Earth',
            'paragraph': 'Is beautiful'
        },
        {
            'title': 'Mars',
            'paragraph': 'Is great'
        },
        {
            'title': 'Mercury',
            'paragraph': 'Is small'
        }
    ]
)



# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Store the entire team collection in a list
    mars = list(db.mars.find())

    # Run the scrape function
    # mars_headlines = scrape_mars.scrape_info()

    # # Find one record of data from the mongo database
    # headlines = mars_headlines.find_one()

    # # Update the Mongo database using update and upsert=True
    # mars_headlines.update({}, mars_headlines, upsert=True)

    # Return template and data
    return render_template("index.html",mars=mars)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.amrs.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
