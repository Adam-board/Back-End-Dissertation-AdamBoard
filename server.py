from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

app = Flask(__name__)





@app.route("/reports")
def reports():
    return {}

#TODO Implement PyMongo to have as storage and ensure the storage works as intended
#TODO Implement Databank of vulnerabilities that are editable
#TODO Implement four relational Databases: Reports, Report Templates, Audit Logs, Vulnerability Databank
#TODO Connect the Database to the front-end to store all data that is created
if __name__ == "__main__":
    app.run(debug=True)


client = MongoClient('localhost', 27017)

db = client.toolDB
reports = db.report
templates = db.templates
vulnerabilities = db.vulns


ReportPost = {
    "Report": "",
    "Sections" : [{"Heading": "", "Description": "", "Data": ""}],
    "Vulnerabilities" : [],
    "Notes" : [{"Heading": "", "Description": "", "Data": ""}]
}

VulnPost = {
    "VulnName" : "",
    "Severity" : "",
    "Description" : "",
    "Data" : "",
    "VulnID": ""
}

TemplatePost = {
    "TemplateName": "Default",
    "Template": [{"Heading": "Executive Summary", "Description": "", "Data": "Placeholder"}, {"Heading": "Overview of Penetration Test", "Description": "", "Data": "Placeholder"}, {"Heading": "Overview of Methodology", "Description": "", "Data": "Placeholder"}]
}

