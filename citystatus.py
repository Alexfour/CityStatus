from flask import Flask, render_template, request
import urllib.parse
import requests

app = Flask(__name__)             # create an app instance

main_api = "https://api.teleport.org/api/"  #API root

@app.route("/", methods=['GET', 'POST'])    #Website root that handsles both GET and POST
def citystatus():

    imageurl = "https://api.teleport.org/api/urban_areas/slug:new-york/images/"
    informationurl = "https://api.teleport.org/api/urban_areas/slug:new-york/scores/"
    corruptionurl = "https://api.teleport.org/api/urban_areas/slug:new-york/details/"
    city = "new-york"

    if request.method == 'POST':    #If POST has been triggered get the "city" value from HTML input field
        city = request.form['city']
        if city:    #If city is not empty replace spaces with hyphens and get the URL
            city = city.replace(' ', '-')
            imageurl = "https://api.teleport.org/api/urban_areas/slug:" + city + "/images/"
            informationurl = "https://api.teleport.org/api/urban_areas/slug:" + city + "/scores/"
            corruptionurl = "https://api.teleport.org/api/urban_areas/slug:" + city + "/details/"

    json_data_image = requests.get(imageurl).json()     #Get city images
    if 'status' not in json_data_image:
        print("Successfull call") #donothing
    elif json_data_image["status"] == 404:    #If city not found default to new-york
        imageurl = "https://api.teleport.org/api/urban_areas/slug:new-york/images/"
        informationurl = "https://api.teleport.org/api/urban_areas/slug:new-york/scores/"
        corruptionurl = "https://api.teleport.org/api/urban_areas/slug:new-york/details/"
        city = "new-york"
        json_data_image = requests.get(imageurl).json()
        
    city_image = json_data_image["photos"][0]["image"]["web"]

    json_data_corruption = requests.get(corruptionurl).json()   #Get corruption statistic
    city_corruption = json_data_corruption["categories"][0]["data"][2]["float_value"]

    json_data = requests.get(informationurl).json()     #Get rest of statistics
    city_summary = json_data["summary"]
    city_housing = json_data["categories"][0]["score_out_of_10"]
    city_total_score = float("{:.2f}".format(json_data["teleport_city_score"]))
    categories = []
    colors = []
    scores = []

    for each in json_data["categories"]:    #Place statistics into arrays
            categories.append(each["name"]) 
            colors.append(each["color"]) 
            scores.append(float("{:.2f}".format(each["score_out_of_10"])) )

    return render_template("index.html",
    city = city.capitalize(),
    city_image = city_image,
    city_summary = city_summary,
    city_housing = city_housing,
    city_corruption = city_corruption,
    categories = categories,
    colors = colors,
    scores = scores,
    len = len(categories),
    city_total_score = city_total_score)

if __name__ == "__main__":        # on running python app.py
    app.run(debug=True)                     # run the flask app