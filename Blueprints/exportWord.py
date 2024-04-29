from flask import Blueprint, jsonify, request
from docx import Document
from Blueprints.database import reports, vulns, sections
from bson import ObjectId

exportWordBlueprint = Blueprint('exportWordBlueprint', __name__)

#GETs the selected report for exporting to Word
@exportWordBlueprint.route("/api/report/exportword", methods=["POST"])
def ExportWord():
    data = request.json

    ReportID = data["id"]

    ExecutiveSummary = {{}}
    Sections = {{}}
    CriticalVulns = {{}}
    HighVulns = {{}}
    MediumVulns = {{}}
    LowVulns = {{}}
 

    report = reports.find_one({"_id": ObjectId(ReportID)})
    return {"Heading": "Exporting to Word"}