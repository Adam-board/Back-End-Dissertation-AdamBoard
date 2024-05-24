from flask import Blueprint, request
from jira import JIRA
from Blueprints.database import reports, vulns
from bson import ObjectId
from draftjs_exporter.html import HTML
import json
from draftjs_exporter.html import HTML
from bs4 import BeautifulSoup

exportJiraBlueprint = Blueprint('exportJiraBlueprint', __name__)



# Jira API credentials
JIRA_URL = '<INSERT ADDRESS>'
JIRA_USERNAME = '<INSERT ATTACHED EMAIL>'
JIRA_API_TOKEN = '<INSERT API TOKEN>'
JIRA_PROJECT_KEY = '<INSERT PROJECT KEY>'


jira_client = JIRA(JIRA_URL, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

# Function to create a Jira issue
def create_jira_issue(summary, description):
    issue_dict = {
        'project': {'key': JIRA_PROJECT_KEY},
        'summary': summary,
        'description': description,
        'issuetype':  {"id": "10001"}, 
    }

    return jira_client.create_issue(fields=issue_dict)

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

        for vulnerability in vulnsData:
            if vulnerability['Data']:
                dataVuln = json.loads(vulnerability['Data'])
                htmlOutputVuln = html_exporter.render(dataVuln)
                vulnerability['Data'] = convert_html_to_rich_text(htmlOutputVuln)
                create_jira_issue(vulnerability['VulnName'], vulnerability['Data'])


    return {"Heading": "Exporting to Jira as Tickets"}


def convert_html_to_rich_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    formatted_text = ''
    for tag in soup.find_all():
        if tag.name == 'h1':
            formatted_text += f'\n\n{tag.text.upper()}\n'  # Convert to uppercase for heading 1
        elif tag.name in ['h2', 'h3', 'h4', 'h5', 'h6']:
            formatted_text += f'\n\n{tag.text}\n'
        elif tag.name == 'p':
            formatted_text += f'\n{tag.text}\n'
        elif tag.name == 'code':
            formatted_text += f'\n{tag.text}\n'  # Assuming code tag represents code block
        elif tag.name == 'ul':
            for li in tag.find_all('li'):
                formatted_text += f'\n- {li.text}\n'  # Convert list items to bullet points
        elif tag.name == 'ol':
            for index, li in enumerate(tag.find_all('li'), start=1):
                formatted_text += f'\n{index}. {li.text}\n'  # Convert list items to numbered list
    return formatted_text.strip()
