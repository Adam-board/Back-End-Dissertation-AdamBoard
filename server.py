from flask import Flask

app = Flask(__name__)

@app.route("/reports")
def reports():
    return {"reports": ["Report1", "Report2", "Report3"]}

if __name__ == "__main__":
    app.run(debug=True)