from flask import Flask, render_template, jsonify, request
from schedule_data import get_monthly_schedule, generate_day_plan, update_topic
import calendar
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def index():
    month_schedule = get_monthly_schedule()
    days_in_month = calendar.monthrange(2025, 4)[1]
    dates = [f"2025-04-{str(day).zfill(2)}" for day in range(1, days_in_month + 1)]
    return render_template("index.html", month_schedule=month_schedule, dates=dates)

@app.route("/day_schedule/<date_str>")
def day_schedule(date_str):
    month_schedule = get_monthly_schedule()
    topics = month_schedule.get(date_str, {
        "physics": "Physics",
        "chemistry": "Chemistry",
        "maths": "Maths"
    })
    day_plan = generate_day_plan(date_str, topics)
    return jsonify(day_plan)

@app.route("/update_topic", methods=["POST"])
def update_topic_route():
    data = request.form  # Use request.form for form data
    date = data.get("date")
    physics = data.get("physics")
    chemistry = data.get("chemistry")
    maths = data.get("maths")

    update_topic(date, "physics", physics)
    update_topic(date, "chemistry", chemistry)
    update_topic(date, "maths", maths)

    return jsonify({"success": True})

@app.route("/day_topics/<date_str>")
def get_topics(date_str):
    monthly = get_monthly_schedule()
    return jsonify(monthly.get(date_str, {
        "physics": "",
        "chemistry": "",
        "maths": ""
    }))

@app.route("/current_datetime")
def get_current_datetime():
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    return jsonify({"date": date_str, "time": time_str})

if __name__ == "__main__":
    app.run(debug=True,port=8080,host='0.0.0.0')