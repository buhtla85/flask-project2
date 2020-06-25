from flask import Flask, render_template
import requests

app = Flask(__name__)


# the idea is to fetch data (global numbers) and display them in cards and some type of chart
# also, the home page should have a dropdown menu for list of countries. The function should fetch the list of countries and save them in dropdown.
@app.route('/')
def fetch_data():
    r = requests.get("https://covid19.mathdro.id/api")
    
    jsonData = r.json()
    confirmed = jsonData["confirmed"]["value"]
    recovered = jsonData["recovered"]["value"]
    deaths = jsonData["deaths"]["value"]

    if len(jsonData) == 0:
        # maybe there should be some error page html...
        return "No data here!" 
    else:
        selectElemList = fetch_countries()
        return render_template("show_data.html", numConf=confirmed, numRec=recovered, numDeat=deaths, selItems=selectElemList)



def fetch_countries():
    r_countries = requests.get("https://covid19.mathdro.id/api/countries")
    jsonCountries = r_countries.json()
    countriesList = [c["name"] for c in jsonCountries["countries"]]
    return countriesList

        
    
