from flask import Flask, render_template, request, url_for, redirect
from Blueprints.AllReports import allReportsBlueprint
from Blueprints.currentReport import currentReportBlueprint
from Blueprints.exportJira import exportJiraBlueprint
from Blueprints.exportWord import exportWordBlueprint
from Blueprints.note import noteBlueprint
from Blueprints.section import sectionBlueprint
from Blueprints.template import templateBlueprint
from Blueprints.vuln import vulnBlueprint

from Blueprints.JsonEncoder import CustomJSONProvider

app = Flask(__name__)
app.json = CustomJSONProvider(app)
# ---------------------------------------------------------------------------- #
#               Related to grabbing all of a document/collection               #
# ---------------------------------------------------------------------------- #
app.register_blueprint(allReportsBlueprint)
app.register_blueprint(exportJiraBlueprint)
app.register_blueprint(exportWordBlueprint)
# ---------------------------------------------------------------------------- #
#                         Below is all Report API Calls                        #
# ---------------------------------------------------------------------------- #
app.register_blueprint(currentReportBlueprint)
# ---------------------------------------------------------------------------- #
#                        Below is all Section API calls                        #
# ---------------------------------------------------------------------------- #
app.register_blueprint(sectionBlueprint)
# ---------------------------------------------------------------------------- #
#                          Below is all Vuln API calls                         #
# ---------------------------------------------------------------------------- #
app.register_blueprint(vulnBlueprint)
# ---------------------------------------------------------------------------- #
#                           Below is Notes API Calls                           #
# ---------------------------------------------------------------------------- #
app.register_blueprint(noteBlueprint)
# ---------------------------------------------------------------------------- #
#                   Below this is all the Template API Calls                   #
# ---------------------------------------------------------------------------- #
app.register_blueprint(templateBlueprint)


if __name__ == "__main__":
    app.run(debug=True)
