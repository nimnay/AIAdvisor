from flask import Flask, render_template, request
import os
import json
from API.utils import callAPI

app = Flask(__name__)
data_file = "submitted_data.json"

#Saving submitted data to a JSON File
def collect_data(name, courses):
    if os.path.exists(data_file):
        #Adds data if the file exists
        with open(data_file, "r") as file:
            allData = json.load(file)
    else:
        allData = {"Name":{}, "Classes": {} }

    allData["Name"][name] = name
    allData["Classes"][name] = courses

    with open(data_file, "w") as file:
        json.dump(allData, file, indent = 4)
@app.route("/", methods = ["GET", "POST"])
def home():
    #Taking in the data necessary to get the AI response
    submitted_name = None
    submitted_courses = None
    recommendation = None
    if request.method == "POST":
        submitted_name = request.form.get("user_name")
        submitted_courses = request.form.get("user_classes")
        if submitted_name and submitted_courses:
            collect_data(submitted_name, submitted_courses)
            student = {
                "name": submitted_name,
                "completed_courses": submitted_courses.split(","),
            }
            recommendation = callAPI(student)
        
        return render_template("index.html", submitted_name=submitted_name,
                               submitted_courses=submitted_courses, recommendation=recommendation)
    return render_template("index.html", submitted_name=submitted_name,
                           submitted_courses=submitted_courses, recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
