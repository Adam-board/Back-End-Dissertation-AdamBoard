from flask import Blueprint, request
from Blueprints.database import reports, sections, sectionTemplates, reportTemplates
from bson import ObjectId

templateBlueprint = Blueprint('templateBlueprint', __name__)

# ---------------------------------------------------------------------------- #

#GETs all templates
@templateBlueprint.route("/api/report/templates", methods=["GET"])
def GetAllTemplates():

    return {
    "Templates": list(reportTemplates.find({}))
    }

# ---------------------------------------------------------------------------- #

#creates a new template
@templateBlueprint.route("/api/report/templates/new", methods=["POST"])
def PostNewTemplate():

    data=request.json

     # Find the report document
    report = reports.find_one({"_id": ObjectId(data.get("_id"))})

    if report:
        
        # Get sections from the report
        sectionsData = report.get("Sections", [])

        # Create a list to store section template IDs for the new report template
        sectionTemplateIds = []

        # Iterate over sections and insert into the section templates collection
        for sectionID in sectionsData:
            print(sectionID)
            section = sections.find_one({"_id": ObjectId(sectionID)})
            print(section)
            if section:
                # Insert section information into the section templates collection
                sectionTemplateId = sectionTemplates.insert_one({
                    "Heading": section.get("Heading", ""),
                    "Description": section.get("Description", ""),
                    "Data": ""
                }).inserted_id

                # Append section template ID to the list
                sectionTemplateIds.append(sectionTemplateId)

        # Get the template name from the data
        templateName = data.get("TemplateName", "")

        # Check if the template name is only whitespace
        if templateName and not templateName.strip():
            # If template name is only whitespace, set it to "NewTemplate"
            templateName = "NewTemplate"


        # Create a new report template document
        reportTemplateId = reportTemplates.insert_one({
            "TemplateName": data.get("TemplateName", ""),  # Include the name of the template
            "Sections": sectionTemplateIds,  # Include all section template IDs in the report template
            "Notes": [],  # Include a blank array for notes
            "Vulnerabilities": []  # Include a blank array for vulnerabilities
        }).inserted_id

        return {"message": reportTemplateId}, 200
    else:
        return {"error": "Report not found"}, 404


# ---------------------------------------------------------------------------- #

#deletes the selected template
@templateBlueprint.route("/api/report/templates/<TemplateID>/delete", methods=["DELETE"])
def DeleteTemplate(TemplateID):

    # Find the report template document
    reportTemplate = reportTemplates.find_one({"_id": ObjectId(TemplateID)})

    if reportTemplate:
        # Retrieve section template IDs from the report template
        sectionTemplateIds = reportTemplate.get("Sections", [])

        # Delete each section template document
        for sectionTemplateId in sectionTemplateIds:
            sectionTemplates.delete_one({"_id": sectionTemplateId})

        # Delete the report template document
        result = reportTemplates.delete_one({"_id": ObjectId(TemplateID)})

        if result.deleted_count > 0:
            return {"message": "Template and associated section templates deleted successfully"}, 200
        else:
            return {"error": "Template not found or no changes were made"}, 404
    else:
        return {"error": "Template not found"}, 404

# ---------------------------------------------------------------------------- #