from flask import Flask, request, jsonify
from rag_engine import answer_query

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    role = data.get("role", None)  
    if not query:
        return jsonify({"error": "Query not provided"}), 400

    response = answer_query(query, user_role=role)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
