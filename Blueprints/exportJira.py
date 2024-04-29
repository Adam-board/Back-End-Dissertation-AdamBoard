from flask import Blueprint, request
from jira import JIRA
from Blueprints.database import reports, vulns
from bson import ObjectId


exportJiraBlueprint = Blueprint('exportJiraBlueprint', __name__)


#Grabs all Vulnerabilities for the report to export as Jira Tickets
@exportJiraBlueprint.route("/api/report/exportjira", methods=["POST"])
def ExportJira():
    data = request.json

    ReportID = data["id"]


    report = reports.find_one({"_id": ObjectId(ReportID)})
    return {"Heading": "Exporting to Jira as Tickets"}