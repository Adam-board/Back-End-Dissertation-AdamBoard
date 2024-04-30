from flask import Blueprint, request
from jira import JIRA
from Blueprints.database import reports, vulns
from bson import ObjectId
from draftjs_exporter.html import HTML
import json


exportJiraBlueprint = Blueprint('exportJiraBlueprint', __name__)


#Grabs all Vulnerabilities for the report to export as Jira Tickets
@exportJiraBlueprint.route("/api/report/exportjira", methods=["POST"])
def ExportJira():
    data = request.json
    reportId = data.get("ReportId")

    CriticalVulns = []
    HighVulns = []
    LowVulns = []
    MediumVulns = []


    # Initialize HTML exporter
    html_exporter = HTML()

    # Retrieve report data from MongoDB
    report = reports.find_one({"_id": ObjectId(reportId)})

    if report:
        # Extract vulns IDs from the report document
        vulnIds = report.get("Vulnerabilities", [])

        # Fetch vuln documents from the vulnerabilities collection using the vulns IDs
        vulnsData = []
        for vulnId in vulnIds:
            vuln = vulns.find_one({"_id": vulnId})
            if vuln:
                vulnsData.append(vuln)

        # Convert each vulnerability to HTML
        htmlOutputsVulns = []
        for vulnerability in vulnsData:
            if vulnerability['Data']:
                dataVuln = json.loads(vulnerability['Data'])
                htmlOutputVuln = html_exporter.render(dataVuln)
                htmlOutputsVulns.append(htmlOutputVuln)
                vulnerability['Data'] = htmlOutputVuln

        for vulnerability in vulnsData:
            if vulnerability['Severity'] == 'Critical':
                CriticalVulns.append(vulnerability)
            elif vulnerability['Severity'] == 'High':
                HighVulns.append(vulnerability)
            elif vulnerability['Severity'] == 'Medium':
                MediumVulns.append(vulnerability)
            elif vulnerability['Severity'] == 'Low':
                LowVulns.append(vulnerability)

    


    return {"Heading": "Exporting to Jira as Tickets"}