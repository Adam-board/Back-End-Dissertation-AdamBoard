from flask import Blueprint, request, jsonify
from Blueprints.database import reports, sections
from bson import ObjectId

sectionBlueprint = Blueprint('sectionBlueprint', __name__)

# ---------------------------------------------------------------------------- #

#Creates a new section with header and description
@sectionBlueprint.route("/api/report/<ReportID>/section/new", methods=["POST"])
def PostSection(ReportID):
    data = request.json

    # Extract header, description, and empty data from the request data
    header = data.get("Heading", "")
    description = data.get("Description", "")
    emptyData = ""

    # Create a new section document
    newSection = {
        "Heading": header,
        "Description": description,
        "Data": emptyData  # Include the empty data field
    }

    # Insert the new section document into the sections collection
    sectionID = sections.insert_one(newSection).inserted_id

    # Update the corresponding report document in the reports collection
    reports.update_one(
        {"_id": ObjectId(ReportID)},
        {"$push": {"Sections": sectionID}}
    )

    return {"sectionID": sectionID, "message": "Section created and linked to report successfully"}

# ---------------------------------------------------------------------------- #

#Gets the section that is selected for the editor
@sectionBlueprint.route("/api/report/section/<SectionID>", methods=["GET"])
def GetSection(SectionID):
    # Find the section in the sections collection
    section = sections.find_one({"_id": ObjectId(SectionID)})

    if section:
        # Extract heading, description, and data from the section
        id = section.get("_id", "")
        heading = section.get("Heading", "")
        description = section.get("Description", "")
        data = section.get("Data", "")

        # Construct a response containing the heading, description, and data
        response = {
            "_id": id,
            "Heading": heading,
            "Description": description,
            "Data": data
        }

        return jsonify({"Section": response}), 200  # Return the section with a 200 status code
    else:
        return jsonify({"error": "Section not found"}), 404  # Return an error with a 404 status code


# ---------------------------------------------------------------------------- #

#Saves selected section
@sectionBlueprint.route("/api/report/section/<SectionID>/save", methods=["PUT"])
def PutSection(SectionID):

    data = request.json

    SectionUpdate = sections.update_one({"_id": ObjectId(SectionID)}, 
                                       {"$set":data})

    if SectionUpdate.modified_count > 0:
        return {"message": "Section updated successfully"}, 200
    else:
        return {"error": "Section not found or no changes were made"}, 404

# ---------------------------------------------------------------------------- #

#deletes the selected section
@sectionBlueprint.route("/api/report/<ReportID>/section/<SectionID>/delete", methods=["DELETE"])
def DeleteSection(ReportID, SectionID):
    # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})

    if report:
        # Remove the section ID from the Sections array
        sectionsIds = report.get("Sections", [])
        if ObjectId(SectionID) in sectionsIds:
            sectionsIds.remove(ObjectId(SectionID))

            # Update the report document to remove the section ID
            reports.update_one(
                {"_id": ObjectId(ReportID)},
                {"$set": {"Sections": sectionsIds}}
            )

            # Delete the section document from the sections collection
            sections.delete_one({"_id": ObjectId(SectionID)})

            return {"message": "Section deleted successfully"}, 200
        else:
            return {"error": "Section not found in the report"}, 404
    else:
        return {"error": "Report not found"}, 404
 
 