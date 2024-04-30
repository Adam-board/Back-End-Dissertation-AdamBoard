from flask import Blueprint, request
from docx import Document
from Blueprints.database import reports, vulns, sections
from bson import ObjectId
from docxtpl import DocxTemplate
from draftjs_exporter.html import HTML
import json
import re
import os
from bs4 import BeautifulSoup 

exportWordBlueprint = Blueprint('exportWordBlueprint', __name__)

#GETs the selected report for exporting to Word
@exportWordBlueprint.route("/api/report/exportword", methods=["POST"])
def ExportWord():
    data = request.json
    reportId = data.get("ReportId")
    print(os.getcwd())
    doc = DocxTemplate("PenetrationTestTemplateForTool.docx")
    execSummarySection = []
    CriticalVulns = []
    HighVulns = []
    LowVulns = []
    MediumVulns = []

    # Initialize HTML exporter
    html_exporter = HTML()
    # Retrieve report data from MongoDB
    report = reports.find_one({"_id": ObjectId(reportId)})

    if report:
        # Extract sections and vulnerabilities from the report document
        sectionIds = report.get("Sections", [])
        vulnIds = report.get("Vulnerabilities", [])

        # Fetch vuln documents from the vulnerabilities collection using the vulns IDs
        vulnsData = []
        for vulnId in vulnIds:
            vuln = vulns.find_one({"_id": vulnId})
            if vuln:
                vulnsData.append(vuln)

        # Convert each vulnerability to HTML and then to formatted text
        for vulnerability in vulnsData:
            if vulnerability['Data']:
                dataVuln = json.loads(vulnerability['Data'])
                htmlOutputVuln = html_exporter.render(dataVuln)
                vulnerability['Data'] = convert_html_to_rich_text(htmlOutputVuln)

        # Fetch section documents from the sections collection using the section IDs
        sectionsData = []
        for sectionId in sectionIds:
            section = sections.find_one({"_id": sectionId})
            if section:
                sectionsData.append(section)

        # Convert each section's HTML content to formatted text
        for section in sectionsData:
            if section['Data']:
                sectionData = json.loads(section['Data'])
                htmlOutputSection = html_exporter.render(sectionData)
                section['Data'] = convert_html_to_rich_text(htmlOutputSection)

        # Separate sections based on headings
        for section in sectionsData:
            if re.search(r'executive summary', section['Heading'], re.IGNORECASE):
                execSummarySection = section
                sectionsData.remove(execSummarySection)
                break

        for section in sectionsData:
            if re.search(r'appendix', section['Heading'], re.IGNORECASE):
                appendixSection = section
                sectionsData.remove(appendixSection)
                break
        
        for section in sectionsData:
            if re.search(r'glossary', section['Heading'], re.IGNORECASE):
                glossarySection = section
                sectionsData.remove(glossarySection)
                break

        # Separate vulnerabilities based on severity
        for vulnerability in vulnsData:
            if vulnerability['Severity'] == 'Critical':
                CriticalVulns.append(vulnerability)
            elif vulnerability['Severity'] == 'High':
                HighVulns.append(vulnerability)
            elif vulnerability['Severity'] == 'Medium':
                MediumVulns.append(vulnerability)
            elif vulnerability['Severity'] == 'Low':
                LowVulns.append(vulnerability)

        print(MediumVulns)

        # Prepare context for rendering the template
        context = {'ExecutiveSumHead': execSummarySection.get("Heading", ""),
                   'ExecutiveSumBody': execSummarySection.get("Data", ""),
                   'Sections': sectionsData,
                   'CriticalVulns': CriticalVulns,
                   'HighVulns': HighVulns,
                   'MediumVulns': MediumVulns,
                   'LowVulns': LowVulns,
                   'AppendixHead': appendixSection.get("Heading", ""),
                   'AppendixBody': appendixSection.get("Data", ""),
                   'GlossaryHead': glossarySection.get("Heading", ""),
                   'GlossaryBody': glossarySection.get("Data", "")}

        # Render the template
        doc.render(context)

        # Save the generated Word document
        doc.save(report["Report"] + '.docx')

        return {"message": "Word document generated successfully."}, 200
    else:
        return {"error": "Report not found."}, 404

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
