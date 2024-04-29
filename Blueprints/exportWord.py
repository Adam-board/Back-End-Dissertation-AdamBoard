from flask import Blueprint

from Blueprints.database import reports, vulns, sections
from bson import ObjectId


exportWordBlueprint = Blueprint('exportWordBlueprint', __name__)

#GETs the selected report for exporting to Word
@exportWordBlueprint.route("/api/report/<ReportID>/exportword", methods=["GET"])
def ExportWord(ReportID):
    return {"Heading": "Exporting to Word"}