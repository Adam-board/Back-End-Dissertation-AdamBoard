from flask import Blueprint, request
from bson import ObjectId
from Blueprints.database import reports, vulnTemplates, reportTemplates, sections, sectionTemplates

allReportsBlueprint = Blueprint('allReportsBlueprint', __name__)

# ---------------------------------------------------------------------------- #

#GETs all reports 
@allReportsBlueprint.route("/api/report", methods=["GET"])
def GetAllReports():
    return {
    "reports": list(reports.find({}))
    }

# ---------------------------------------------------------------------------- #

#Creates new report - either blank or based on a template WIP
@allReportsBlueprint.route("/api/report/new", methods=["POST"])
def PostNewReport():
    data = request.json

    if data and "templateId" in data:
        # If a template ID is provided, fetch the template
        templateId = ObjectId(data["templateId"])
        template = reportTemplates.find_one({"_id": templateId})
        
        if template:
            newReport = template.copy()  # Create a copy of the template
            del newReport["TemplateName"]  # Remove the template name from the new report
            del newReport["_id"]  # Remove the _id from the template copy
        
            sectionTemplateIds = newReport.get("Sections", [])
            sectionIds = []
            for sectionTemplateId in sectionTemplateIds:
                sectionTemplate = sectionTemplates.find_one({"_id": sectionTemplateId})
                if sectionTemplate:
                    section = {
                        "Heading": sectionTemplate.get("Heading", ""),
                        "Description": sectionTemplate.get("Description", ""),
                        "Data": ""
                    }
                    sectionId = sections.insert_one(section).inserted_id
                    sectionIds.append(sectionId)
                else:
                    return {"error": "Section template not found"}, 404
            
            # Update the new report with section IDs
            newReport["Sections"] = sectionIds
        else:
            return {"error": "Template not found"}, 404
    else:
        # If no template ID is provided, create a new blank report
        newReport = {"Sections": [], "Vulnerabilities": [], "Notes": []}

    # Set the title of the new report if provided
    title = data.get("title", "NewReport")
    newReport["Report"] = title
    # Insert the new report into the database
    report_id = reports.insert_one(newReport).inserted_id

    return {"ReportID": report_id}