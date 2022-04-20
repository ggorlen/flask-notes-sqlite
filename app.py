from flask import Flask, jsonify, request
from db import DB

app = Flask(__name__)

@app.route("/api/notes", methods=["GET", "POST"])
def notes():
    if request.method == "POST":
        if "content" in request.json:
            DB.create_note(request.json["content"])
            return "", 201

        return "", 422

    return jsonify([dict(x) for x in DB.select_all_notes()])

@app.route("/api/notes/<int:note_id>", methods=["GET", "PUT", "DELETE"])
def note(note_id):
    if request.method == "PUT":
        if "content" not in request.json:
            return "", 422
        elif DB.update_note(note_id, request.json["content"]):
            return "", 200

        return "", 404
    elif request.method == "DELETE":
        if DB.delete_note(note_id):
            return "", 200

        return "", 404
    elif result := DB.select_one_note(note_id):
        return dict(result)

    return "", 404

@app.route("/", methods=["GET"])
def index():
    return "", 200

if __name__ == "__main__":
    DB.create_notes_table_if_not_exists()
    app.run(debug=True)

