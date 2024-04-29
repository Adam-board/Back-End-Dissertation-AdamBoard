from flask import Blueprint
from jira import JIRA
from Blueprints.database import reports, vulns
from bson import ObjectId

exportJiraBlueprint = Blueprint('exportJiraBlueprint', __name__)


#Grabs all Vulnerabilities for the report to export as Jira Tickets
@exportJiraBlueprint.route("/api/report/<ReportID>/exportjira", methods=["GET"])
def ExportJira(ReportID):
    return {"Heading": "Exporting to Jira as Tickets"}