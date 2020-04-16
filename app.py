from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"

mongo = PyMongo(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    mars_headlines = mongo.db.mars_headlines
    # Run the scrape function
    mars_headlines_data = scrape_mars.scrape_info()
    mars_tweet = scrape_mars.mars_tweet()
    mars_html = scrape_mars.mars_html()
    
    #feature() doesn't work
    # mars_feature_image = scrape_mars.image()

    data = {
        "mars_tweet": mars_tweet,
        "mars_headlines_data": mars_headlines_data,
        # "mars_feature_image": mars_feature_image,
        "mars_html": mars_html
    }

    # # Update the Mongo database using update and upsert=True
    # mars_headlines.update({}, data, upsert=True)
    # mars_headlines.update({}, mars_tweet, upsert=True)
    # mars_headlines.update({}, mars_html, upsert=True)

    # print(data)
    # # Find one record of data from the mongo database
    # headlines = mongo.db.mars_headlines.find_one()

    # Featured Image Url
    # featured_image = scrape_mars.featured()
    # print("FROM APP.PY",headlines)
    # Return template and data
    print(data)
    return render_template("index.html",data=data)


# @app.route("/")
# def get_html():
#     mars_html = scrape_mars.mars_html()
#     print(mars_html)
#     return render_template("index.html",mars_html=mars_html)


# # Route that will trigger the scrape function
# @app.route("/scrape")
# def mars_hemi():

#     # Run the scrape function
#     hemispheres = scrape_mars.mars_hemi()

#     # Update the Mongo database using update and upsert=True
#     # mongo.db.mars.update({}, mars_data, upsert=True)

#     return render_template("index.html",hemispheres=hemispheres)
#     # Redirect back to home page
#     # return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
