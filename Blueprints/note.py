from flask import Blueprint, request, jsonify
from Blueprints.database import reports, Notes
from bson import ObjectId

noteBlueprint = Blueprint('noteBlueprint', __name__)


# ---------------------------------------------------------------------------- #

#Creates a new Note with header and description
@noteBlueprint.route("/api/report/<ReportID>/note/new", methods=["POST"])
def PostNote(ReportID):
    data = request.json

    # Extract header, description, and empty data from the request data
    header = data.get("Heading", "")
    description = data.get("Description", "")
    emptyData = ""

    # Create a new Note document
    newNote = {
        "Heading": header,
        "Description": description,
        "Data": emptyData  # Include the empty data field
    }

    # Insert the new Note document into the Notes collection
    NoteID = Notes.insert_one(newNote).inserted_id

    # Update the corresponding report document in the reports collection
    reports.update_one(
        {"_id": ObjectId(ReportID)},
        {"$push": {"Notes": NoteID}}
    )

    return {"NoteID": str(NoteID), "message": "Note created and linked to report successfully"}

# ---------------------------------------------------------------------------- #

#Gets the Note that is selected for the editor
@noteBlueprint.route("/api/report/note/<NoteID>", methods=["GET"])
def GetNote(NoteID):
    # Find the Note in the Notes collection
    Note = Notes.find_one({"_id": ObjectId(NoteID)})

    if Note:
        # Extract heading, description, and data from the Note
        id = Note.get("_id", "")
        heading = Note.get("Heading", "")
        description = Note.get("Description", "")
        data = Note.get("Data", "")

        # Construct a response containing the heading, description, and data
        response = {
            "_id": id,
            "Heading": heading,
            "Description": description,
            "Data": data
        }

        return jsonify({"Note": response}), 200  # Return the Note with a 200 status code
    else:
        return jsonify({"error": "Note not found"}), 404  # Return an error with a 404 status code

# ---------------------------------------------------------------------------- #

#Saves selected Note
@noteBlueprint.route("/api/report/note/<NoteID>/save", methods=["PUT"])
def PutNote(NoteID):
    data = request.json

    NotesUpdate = Notes.update_one({"_id": ObjectId(NoteID)}, 
                                       {"$set":data})

    if NotesUpdate.modified_count > 0:
        return {"message": "Notes updated successfully"}, 200
    else:
        return {"error": "Notes not found or no changes were made"}, 404
   
# ---------------------------------------------------------------------------- #

#deletes the selected Note
@noteBlueprint.route("/api/report/<ReportID>/note/<NoteID>/delete", methods=["DELETE"])
def DeleteNote(ReportID, NoteID):
   # Find the report document
    report = reports.find_one({"_id": ObjectId(ReportID)})

    if report:
        # Remove the Notes ID from the Notes array
        NotesIds = report.get("Notes", [])
        if ObjectId(NoteID) in NotesIds:
            NotesIds.remove(ObjectId(NoteID))

            # Update the report document to remove the Notes ID
            reports.update_one(
                {"_id": ObjectId(ReportID)},
                {"$set": {"Notes": NotesIds}}
            )

            # Delete the Notes document from the Notess collection
            Notes.delete_one({"_id": ObjectId(NoteID)})

            return {"message": "Note deleted successfully"}, 200
        else:
            return {"error": "Note not found in the report"}, 404
    else:
        return {"error": "Report not found"}, 404