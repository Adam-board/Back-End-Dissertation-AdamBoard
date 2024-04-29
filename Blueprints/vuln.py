from flask import Blueprint, request, jsonify
from Blueprints.database import reports, vulns, vulnTemplates
from bson import ObjectId

vulnBlueprint = Blueprint('vulnBlueprint', __name__)


# ---------------------------------------------------------------------------- #
#Creates a new vuln with header and description
@vulnBlueprint.route("/api/report/<ReportID>/vuln/new", methods=["POST"])
def PostVuln(ReportID):
    
    data = request.json

    #Extract the following info to put into the new document
    VulnName = data.get("VulnName")
    Severity = data.get("Severity")
    Description = data.get("Description")
    Data = data.get("Data")
    
    #Create a new vuln document
    NewVuln ={
                "VulnName" : VulnName,
                "Severity" : Severity,
                "Description" : Description,
                "Data" : Data,
    }

    # Insert the new vuln document into the vulns collection
    VulnID = vulns.insert_one(NewVuln).inserted_id

    # Update the corresponding report document in the reports collection
    reports.update_one(
        {"_id": ObjectId(ReportID)},
        {"$push": {"Vulnerabilities": VulnID}}
    )

    return {"vulnID": str(VulnID), "message": "vuln created and linked to report successfully"}

# ---------------------------------------------------------------------------- #


#Gets the vuln that is selected for the editor
@vulnBlueprint.route("/api/report/vuln/<VulnID>", methods=["GET"])
def GetVuln(VulnID):

    # Find the vuln in the vulns collection
    vuln = vulns.find_one({"_id": ObjectId(VulnID)})

    if vuln:
        # Extract heading, description, and data from the vuln
        id = vuln.get("_id", "")
        VulnName = vuln.get("VulnName")
        Severity = vuln.get("Severity")
        Description = vuln.get("Description")
        Data = vuln.get("Data")

        # Construct a response containing the heading, description, and data
        response ={
                "_id": id,
                "VulnName" : VulnName,
                "Severity" : Severity,
                "Description" : Description,
                "Data" : Data,
    }

        return jsonify({"vuln": response}), 200  # Return the vuln with a 200 status code
    else:
        return jsonify({"error": "vuln not found"}), 404  # Return an error with a 404 status code

# ---------------------------------------------------------------------------- #

#Saves selected vuln
@vulnBlueprint.route("/api/report/vuln/<VulnID>/save", methods=["PUT"])
def PutVuln(VulnID):

    data = request.json

    SectionUpdate = vulns.update_one({"_id": ObjectId(VulnID)}, 
                                       {"$set":data})

    if SectionUpdate.modified_count > 0:
        return {"message": "Section updated successfully"}, 200
    else:
        return {"error": "Section not found or no changes were made"}, 404

# ---------------------------------------------------------------------------- #

#deletes the selected vuln from report
@vulnBlueprint.route("/api/report/<ReportID>/vuln/<VulnID>/delete", methods=["DELETE"])
def DeleteVuln(ReportID, VulnID):

    # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})

    if report:
        # Remove the section ID from the Sections array
        vulnsIds = report.get("Vulnerabilities", [])
        if ObjectId(VulnID) in vulnsIds:
            vulnsIds.remove(ObjectId(VulnID))

            # Update the report document to remove the section ID
            reports.update_one(
                {"_id": ObjectId(ReportID)},
                {"$set": {"Vulnerabilities": vulnsIds}}
            )

            # Delete the section document from the vulns collection
            vulns.delete_one({"_id": ObjectId(VulnID)})

            return {"message": "Section deleted successfully"}, 200
        else:
            return {"error": "Section not found in the report"}, 404
    else:
        return {"error": "Report not found"}, 404

# ---------------------------------------------------------------------------- #

#inserts the selected vuln into the vulnerability databank
@vulnBlueprint.route("/api/report/<ReportID>/vuln/insertDatabank", methods=["POST"])
def InsertVulnEntry(ReportID):

    data = request.json
    # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})

    if report:
        # Find the vulnerability document using the ID stored in the report
        vulnerability = vulns.find_one({"_id": ObjectId(data["VulnId"])})
        if vulnerability:
            # Insert the vulnerability details into the vulnerability template
            insertedVulnID = vulnTemplates.insert_one({
                "VulnName": vulnerability.get("VulnName", ""),
                "Severity": vulnerability.get("Severity", ""),
                "Description": vulnerability.get("Description", ""),
                "Data": vulnerability.get("Data", "")
            }).inserted_id

            return {"message": f"Vulnerability inserted into the vulnerability template with ID: {insertedVulnID}"}, 200
        else:
            return {"error": "Vulnerability not found"}, 404
    else:
        return {"error": "Report not found"}, 404

# ---------------------------------------------------------------------------- #

#deletes the selected vuln from the databank
@vulnBlueprint.route("/api/report/vuln/<VulnID>/delete", methods=["DELETE"])
def DeleteVulnEntry(VulnID):
  # Find the vulnerability document by its ID
    vulnerability = vulnTemplates.find_one({"_id": ObjectId(VulnID)})

    if vulnerability:
        # Delete the vulnerability document
        vulnTemplates.delete_one({"_id": ObjectId(VulnID)})
        return {"message": "Vulnerability deleted successfully"}, 200
    else:
        return {"error": "Vulnerability not found"}, 404
    
# ---------------------------------------------------------------------------- #

@vulnBlueprint.route("/api/report/vulnTemplates", methods=["GET"])
def getAllVulnTemplates():
    # Find all vulnerability templates
    allVulns = vulnTemplates.find({})

    # Create a list to store the vulnerability data
    vulns_data = []

    # Iterate over each vulnerability template and extract its data
    for vuln in allVulns:
        vuln_data = {
            "_id": vuln.get("_id", ""),
            "VulnName": vuln.get("VulnName", ""),
            "Severity": vuln.get("Severity", ""),
            "Description": vuln.get("Description", ""),
            "Data": vuln.get("Data", "")
        }
        vulns_data.append(vuln_data)

    return {"vulnerabilities": vulns_data}, 200

 # ---------------------------------------------------------------------------- #

@vulnBlueprint.route("/api/report/<ReportID>/vuln/new/Template", methods=["POST"])
def PostVulnFromTemplate(ReportID):
    
    data = request.json

    #Fetch the template using the provided TemplateID
    template = vulnTemplates.find_one({"_id": ObjectId(data["VulnId"])})
    if not template:
        return {"error": "Vulnerability template not found"}, 404

    #Create a new vulnerability document based on the template
    NewVuln = {
        "VulnName": template.get("VulnName"),
        "Severity": template.get("Severity"),
        "Description": template.get("Description"),
        "Data": template.get("Data"),
    }

    # Insert the new vulnerability document into the vulns collection
    VulnID = vulns.insert_one(NewVuln).inserted_id

    # Update the corresponding report document in the reports collection
    reports.update_one(
        {"_id": ObjectId(ReportID)},
        {"$push": {"Vulnerabilities": VulnID}}
    )

    return {"vulnID": str(VulnID), "message": "Vulnerability created and linked to report successfully"}