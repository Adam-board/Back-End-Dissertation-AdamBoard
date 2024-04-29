from flask import Blueprint, jsonify, request
from Blueprints.database import reports, sections, vulns, Notes
from bson import ObjectId

currentReportBlueprint = Blueprint('currentReportBlueprint', __name__)

# ---------------------------------------------------------------------------- #

#GETs the report Sections
@currentReportBlueprint.route("/api/report/<ReportID>/sections", methods=["GET"])
def GetAllSections(ReportID):
    
     # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})
    if report:
        # Extract section IDs from the report document
        sectionIds = report.get("Sections", [])
        # Fetch section documents from the sections collection using the section IDs
        sectionsData = []
        for sectionId in sectionIds:
            section = sections.find_one({"_id": sectionId})
            print(section)
            if section:
                sectionsData.append(section)

        return {"sections": sectionsData}, 200  # Return sections data with a 200 status code
    else:
        return {"error": "Report not found"}, 404  # Return an error with a 404 status code

# ---------------------------------------------------------------------------- #

#GETs the current report 
@currentReportBlueprint.route("/api/report/<ReportID>", methods=["GET"])
def GetCurrentReport(ReportID):
    
      # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})

    if report:
        # Return the report document with a 200 status code
        return {"report": report}, 200
    else:
        # Return an error message if the report is not found
        return {"error": "Report not found"}, 404

    
# ---------------------------------------------------------------------------- #

#GETs the report Vulns
@currentReportBlueprint.route("/api/report/<ReportID>/vulns", methods=["GET"])
def GetAllVulns(ReportID):
    
      # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})

    if report:
        # Extract vulns IDs from the report document
        vulnIds = report.get("Vulnerabilities", [])

        # Fetch vuln documents from the vulnerabilities collection using the vulns IDs
        vulnsData = []
        for vulnId in vulnIds:
            vuln = vulns.find_one({"_id": vulnId})
            if vuln:
                vulnsData.append(vuln)

        return {"vulns": vulnsData}, 200  # Return vulns data with a 200 status code
    else:
        return {"error": "Report not found"}, 404  # Return an error with a 404 status code

# ---------------------------------------------------------------------------- #


# ---------------------------------------------------------------------------- #

#GETs the report Notes
@currentReportBlueprint.route("/api/report/<ReportID>/notes", methods=["GET"])
def GetAllNotes(ReportID):
    
    # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})

    if report:
        # Extract notes IDs from the report document
        NoteIds = report.get("Notes", [])

        # Fetch note documents from the Notes collection using the notes IDs
        NotesData = []
        for NoteId in NoteIds:
            Note = Notes.find_one({"_id": NoteId})
            if Note:
                NotesData.append(Note)

        return {"notes": NotesData}, 200  # Return notes data with a 200 status code
    else:
        return {"error": "Report not found"}, 404  # Return an error with a 404 status code

# ---------------------------------------------------------------------------- #

#Deletes the current Report
@currentReportBlueprint.route("/api/report/<ReportID>/delete", methods=["DELETE"])
def DeleteReport(ReportID):
 # Fetch the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})
    if report is None:
        return {"error": "Report not found"}, 404
    
    # Extract references to associated documents
    SectionIDs = report.get("Sections", [])
    VulnIds = report.get("Vulnerabilities", [])
    NoteIds = report.get("Notes", [])
    
    # Delete the report document
    reports.delete_one({"_id": ObjectId(ReportID)})
    
    # Delete associated sections
    sections.delete_many({"_id": {"$in": SectionIDs}})
    
    # Delete associated vulnerabilities
    vulns.delete_many({"_id": {"$in": VulnIds}})
    
    # Delete associated notes
    Notes.delete_many({"_id": {"$in": NoteIds}})
    
    return {"Deletion": ReportID + " and associated documents have been Deleted!"}