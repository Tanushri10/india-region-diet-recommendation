from flask import Flask, request, jsonify
from logic.load_data import load_food_data
from logic.rule_engine import rule_based_filter, generate_meal_plan

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():
    user = request.get_json()

    if not user:
        return jsonify({"error": "No input data provided"}), 400

    df = load_food_data()
    filtered = rule_based_filter(df, user)
    meal_plan = generate_meal_plan(filtered)

    return jsonify(meal_plan)

if __name__ == "__main__":
    app.run(debug=True)


