from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client["ToolDB"]
reports = db["report"]
reportTemplates = db["reportTemplates"]
vulns = db["vulns"]
sections = db["sections"]
Notes = db["notes"]
vulnTemplates = db["vulnTemplates"]
sectionTemplates = db["sectionTemplates"]


# ---------------------------------------------------------------------------- #
#                        Collection and Document layout                        #
# ---------------------------------------------------------------------------- #

# Reports = {
#     "Report": "",
#     "Sections" : [],
#     "Vulnerabilities" : [],
#     "Notes" : []
# }
# Notes = {
#     "Heading": "",
#     "Description": "",
#     "Data": ""
# }
# Sections = {
#     "Heading": "",
#     "Description": "",
#     "Data": ""
# }
# Vulns = {
#     "VulnName" : "",
#     "Severity" : "",
#     "Description" : "",
#     "Data" : "",
# }
# ReportTemplates = {
#     "TemplateName": "",
#     "Sections" : [],
#     "Vulnerabilities": [],
#     "Notes": []
# }
# VulnTemplates = {
#     "VulnName" : "",
#     "Severity" : "",
#     "Description" : "",
#     "Data" : "",
# }  
# SectionTemplates = {
#     "Heading": "",
#     "Description": "",
#     "Data": ""
# }
 