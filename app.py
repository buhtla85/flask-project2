from flask import Flask, render_template
import requests

app = Flask(__name__)


# the idea is to fetch data (global numbers) and display them in cards and some type of chart
# also, the home page should have a dropdown menu for list of countries. The function should fetch the list of countries and save them in dropdown.
@app.route('/')
def fetch_data():
    r = requests.get("https://covid19.mathdro.id/api")
    jsonData = r.json()
    confirmed = jsonData["confirmed"]
    numberOfConfirmed = confirmed["value"]
    recovered = jsonData["recovered"]
    numberOfRecovered = recovered["value"]
    deaths = jsonData["deaths"]
    numberOfDeaths = deaths["value"]
    if len(jsonData) == 0:
        return "No data here!"
    else:
        print(jsonData)
        return render_template("show_data.html", numConf=numberOfConfirmed, numRec=numberOfRecovered, numDeat=numberOfDeaths)
    
