from flask import Flask, request, jsonify

from logic.load_data import load_food_data
from logic.rule_engine import (
    rule_based_filter,
    rank_meals,
    generate_meal_plan,
    calculate_daily_totals
)

from db import init_db, save_feedback

app = Flask(__name__)

@app.route("/recommend", methods=["POST"])
def recommend():
    user = request.get_json()
    if not user:
        return jsonify({"error": "No input data provided"}), 400

    df = load_food_data()
    filtered = rule_based_filter(df, user)

    if filtered.empty:
        return jsonify({
            "message": "No suitable meals found.",
            "suggestion": "Try changing goal or diet type."
        })

    ranked = rank_meals(filtered, user)
    meal_plan = generate_meal_plan(ranked)
    daily_summary = calculate_daily_totals(meal_plan)

    return jsonify({
        "meal_plan": meal_plan,   # ✅ ORDER GUARANTEED
        "daily_summary": daily_summary
    })


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No feedback data provided"}), 400

    save_feedback(data)
    return jsonify({"message": "Feedback saved successfully"})


init_db()

if __name__ == "__main__":
    app.run(debug=True)

