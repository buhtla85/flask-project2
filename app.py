from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# app.debug = True


# the idea is to fetch data (global numbers) and display them in cards and some type of chart
# also, the home page should have a dropdown menu for list of countries. The function should fetch the list of countries and save them in dropdown.
@app.route('/global', methods=["GET","POST"])
def globaldata():
    r = requests.get("https://covid19.mathdro.id/api")
    
    jsonData = r.json()
    confirmed = jsonData["confirmed"]["value"]
    recovered = jsonData["recovered"]["value"]
    deaths = jsonData["deaths"]["value"]
    if request.method == "POST":
        select = request.form.get('country')
        r_country = requests.get("https://covid19.mathdro.id/api/countries/" + select)
        # /api/countries/[country]/og: generate a summary open graph image for a [country]
        country_img = "https://covid19.mathdro.id/api/countries/" + select + "/og"
        jsonCountry = r_country.json()
        countryConfirmed = jsonCountry["confirmed"]["value"]
        countryRecovered = jsonCountry["recovered"]["value"]
        countryDeaths = jsonCountry["deaths"]["value"]
        selectElList = fetch_countries()
        elapsTime = fetch_daily_time()
        return render_template("single_country.html", title=select, numConf=countryConfirmed, numRec=countryRecovered, numDeat=countryDeaths, selItems=selectElList, apiImg=country_img)

    if len(jsonData) == 0:
        # maybe there should be some error page html...
        return "No data here!" 
    else:
        selectElemList = fetch_countries()
        elapsedTime = fetch_daily_time()
        dailyConfirmed = fetch_daily_confirmed()
        dailyDeaths = fetch_daily_deaths()
        return render_template("show_data.html", title="Global", numConf=confirmed, numRec=recovered, numDeat=deaths, selItems=selectElemList, timeData=elapsedTime, dailyConfirmed=dailyConfirmed, dailyDeaths=dailyDeaths)



def fetch_countries():
    r_countries = requests.get("https://covid19.mathdro.id/api/countries")
    jsonCountries = r_countries.json()
    countriesList = [c["name"] for c in jsonCountries["countries"]]
    return countriesList
    

# basicaly, this function does not need to be different for every call because this is constant (when user submits form)
def fetch_daily_time():
    r_daily = requests.get("https://covid19.mathdro.id/api/daily")
    jsonDaily = r_daily.json()
    reportDate = [d["reportDate"] for d in jsonDaily]
    return reportDate

        
def fetch_daily_confirmed():
    r_confirmed = requests.get("https://covid19.mathdro.id/api/daily")
    jsonConfirmed = r_confirmed.json()
    totalConfirmed = [t["totalConfirmed"] for t in jsonConfirmed]
    return totalConfirmed

def fetch_daily_deaths():
    r_deaths = requests.get("https://covid19.mathdro.id/api/daily")
    jsonDeaths = r_deaths.json()
    totalDeaths = [d["deaths"] for d in jsonDeaths]
    justDeaths = [j["total"] for j in totalDeaths]
    return justDeaths
    
