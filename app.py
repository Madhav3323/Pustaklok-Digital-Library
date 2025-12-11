from flask import Flask, jsonify, request, abort
from storage import list_all, list_by_category, find_by_name_exact, get_metadata, create_media, delete_media, borrow_media, return_media, get_borrowed_items

app = Flask(__name__)

@app.route("/media", methods=["GET"])
def api_list_all():
    return jsonify(list_all())

@app.route("/media/category/<category>", methods=["GET"])
def api_list_category(category):
    return jsonify(list_by_category(category))

@app.route("/media/search", methods=["GET"])
def api_search_name():
    name = request.args.get("name")
    if not name:
        abort(400, "Missing 'name' query parameter")
    res = find_by_name_exact(name)
    if not res:
        return jsonify({}), 404
    return jsonify(res)

@app.route("/media/<name>", methods=["GET"])
def api_get_metadata(name):
    res = get_metadata(name)
    if not res:
        return jsonify({}), 404
    return jsonify(res)

@app.route("/media", methods=["POST"])
def api_create_media():
    if not request.is_json:
        abort(400, "Expected JSON body")
    media = request.get_json()
    required = {"name","publication_date","author","category"}
    if not required.issubset(media.keys()):
        abort(400, f"Missing keys. Required: {required}")
    ok = create_media(media)
    if not ok:
        return jsonify({"error":"Item already exists or invalid name"}), 400
    return jsonify({"status":"created"}), 201

@app.route("/media/<name>", methods=["DELETE"])
def api_delete_media(name):
    ok = delete_media(name)
    if not ok:
        return jsonify({"error":"Not found"}), 404
    return jsonify({"status":"deleted"}), 200

@app.route("/media/<name>/borrow", methods=["POST"])
def api_borrow_media(name):
    data = request.get_json()
    borrower = data.get("borrower") if data else None
    if not borrower:
        abort(400, "Missing 'borrower' in JSON body")
    ok = borrow_media(name, borrower)
    if not ok:
        return jsonify({"error":"Item not found or already borrowed"}), 400
    return jsonify({"status":"borrowed", "item":name, "borrower":borrower}), 200

@app.route("/media/<name>/return", methods=["POST"])
def api_return_media(name):
    ok = return_media(name)
    if not ok:
        return jsonify({"error":"Item not found or not borrowed"}), 404
    return jsonify({"status":"returned", "item":name}), 200

@app.route("/media/borrowed/list", methods=["GET"])
def api_get_borrowed():
    return jsonify(get_borrowed_items())

if __name__ == "__main__":
    app.run(debug=True)
