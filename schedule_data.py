import json
import os
import calendar

SCHEDULE_FILE = "schedule.json"

# Initial data block (shortened for brevity — replace this with your full `updated_data`)
updated_data = {
    "2025-04-08": {
        "physics": "Units & Measurement - Lectures + DPP + Book Qs",
        "chemistry": "Mole Concept - Lectures + DPP + Book Qs",
        "maths": "Basic Maths + Log - Lectures + DPP + Book Qs"
    },
    "2025-04-09": {
        "physics": "Motion in Straight Line - Lectures + DPP + Book Qs",
        "chemistry": "Atomic Structure - Lectures + DPP + Book Qs",
        "maths": "Set Theory + Relations - Lectures + DPP + Book Qs"
    },
    "2025-04-10": {
        "physics": "Motion in a Plane - Lectures + DPP + Book Qs",
        "chemistry": "States of Matter - Lectures + DPP + Book Qs",
        "maths": "Trigonometry + Equations - Lectures + DPP + Book Qs"
    },
    "2025-04-11": {
        "physics": "Newton's Laws - Lectures + DPP + Book Qs",
        "chemistry": "Thermodynamics - Lectures + DPP + Book Qs",
        "maths": "Quadratic + Complex - Lectures + DPP + Book Qs"
    },
    "2025-04-12": {
        "physics": "Friction + Circular Motion - Lectures + DPP + Book Qs",
        "chemistry": "Chemical & Ionic Equilibrium - Lectures + DPP + Book Qs",
        "maths": "Permutation & Combination - Lectures + DPP + Book Qs"
    },
    "2025-04-13": {
        "physics": "Work, Power & Energy - Lectures + DPP + Book Qs",
        "chemistry": "Redox + Hydrogen + S-block - Lectures + DPP + Book Qs",
        "maths": "Binomial + Sequence & Series - Lectures + DPP + Book Qs"
    },
    "2025-04-14": {
        "physics": "Centre of Mass + Rotational Motion - Lectures + DPP + Book Qs",
        "chemistry": "Periodic Classification - Lectures + DPP + Book Qs",
        "maths": "Straight Lines + Circles - Lectures + DPP + Book Qs"
    },
    "2025-04-15": {
        "physics": "Gravitation - Lectures + DPP + Book Qs",
        "chemistry": "Chemical Bonding - Lectures + DPP + Book Qs",
        "maths": "Conic Sections - Lectures + DPP + Book Qs"
    },
    "2025-04-16": {
        "physics": "Mechanical Properties of Fluids - Lectures + DPP + Book Qs",
        "chemistry": "GOC + Nomenclature - Lectures + DPP + Book Qs",
        "maths": "Limits + Derivatives - Lectures + DPP + Book Qs"
    },
    "2025-04-17": {
        "physics": "Thermal Properties + Thermodynamics - Lectures + DPP + Book Qs",
        "chemistry": "Isomerism - Lectures + DPP + Book Qs",
        "maths": "Integration + AOD - Lectures + DPP + Book Qs"
    },
    "2025-04-18": {
        "physics": "SHM - Lectures + DPP + Book Qs",
        "chemistry": "Hydrocarbons - Lectures + DPP + Book Qs",
        "maths": "3D + Vectors - Lectures + DPP + Book Qs"
    },
    "2025-04-19": {
        "physics": "Waves - Lectures + DPP + Book Qs",
        "chemistry": "Salt Analysis - Lectures + DPP + Book Qs",
        "maths": "Probability + Stats - Lectures + DPP + Book Qs"
    },
    "2025-04-20": {
        "physics": "Kinetic Theory - Lectures + DPP + Book Qs",
        "chemistry": "Revise Organic + Physical - Lectures + DPP + Book Qs",
        "maths": "Revise Algebra - Lectures + DPP + Book Qs"
    },
    "2025-04-21": {
        "physics": "Error & Measurement - Lectures + DPP + Book Qs",
        "chemistry": "Mock MCQs + DPP - Lectures + DPP + Book Qs",
        "maths": "Mock Paper + DPP - Lectures + DPP + Book Qs"
    },
    "2025-04-22": {
        "physics": "Revise 11th Mechanics - Lectures + DPP + Book Qs",
        "chemistry": "Mole Concept - Lectures + DPP + Book Qs",
        "maths": "Basic Maths + Log - Lectures + DPP + Book Qs"
    },
    "2025-04-23": {
        "physics": "Units & Measurement - Lectures + DPP + Book Qs",
        "chemistry": "Atomic Structure - Lectures + DPP + Book Qs",
        "maths": "Set Theory + Relations - Lectures + DPP + Book Qs"
    },
    "2025-04-24": {
        "physics": "Motion in Straight Line - Lectures + DPP + Book Qs",
        "chemistry": "States of Matter - Lectures + DPP + Book Qs",
        "maths": "Trigonometry + Equations - Lectures + DPP + Book Qs"
    },
    "2025-04-25": {
        "physics": "Motion in a Plane - Lectures + DPP + Book Qs",
        "chemistry": "Thermodynamics - Lectures + DPP + Book Qs",
        "maths": "Quadratic + Complex - Lectures + DPP + Book Qs"
    },
    "2025-04-26": {
        "physics": "Newton's Laws - Lectures + DPP + Book Qs",
        "chemistry": "Chemical & Ionic Equilibrium - Lectures + DPP + Book Qs",
        "maths": "Permutation & Combination - Lectures + DPP + Book Qs"
    },
    "2025-04-27": {
        "physics": "Friction + Circular Motion - Lectures + DPP + Book Qs",
        "chemistry": "Redox + Hydrogen + S-block - Lectures + DPP + Book Qs",
        "maths": "Binomial + Sequence & Series - Lectures + DPP + Book Qs"
    }
}


# Load or initialize schedule
if os.path.exists(SCHEDULE_FILE):
    with open(SCHEDULE_FILE, "r") as f:
        schedule = json.load(f)
else:
    schedule = updated_data
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(updated_data, f, indent=4)

def save_schedule():
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedule, f, indent=4)

def get_monthly_schedule(year=2025, month=4):
    month_days = calendar.monthrange(year, month)[1]
    result = {}
    for day in range(1, month_days + 1):
        date_key = f"{year}-{month:02d}-{day:02d}"
        result[date_key] = schedule.get(date_key, {
            "physics": "",
            "chemistry": "",
            "maths": ""
        })
    return result

def generate_day_plan(date_str, topics):
    return [
        "6:00 AM - 7:00 AM: Wake Up + Freshen Up + Light Exercise",
        f"7:00 AM - 9:00 AM: Physics Lecture + Notes ({topics['physics']})",
        "9:00 AM - 9:30 AM: Breakfast + Short Break",
        f"9:30 AM - 11:30 AM: Chemistry Lecture + Concept Revision ({topics['chemistry']})",
        "11:30 AM - 12:00 PM: Quick Break (Walk / Relax)",
        f"12:00 PM - 2:00 PM: Maths Lecture + Examples ({topics['maths']})",
        "2:00 PM - 3:00 PM: Lunch + Power Nap",
        "3:00 PM - 5:00 PM: Physics DPP + DC Pandey Qs",
        "5:00 PM - 5:30 PM: Snack + Refresh",
        "5:30 PM - 7:30 PM: Chemistry DPP + Modern ABC Qs",
        "7:30 PM - 9:00 PM: Maths DPP + RD Sharma Practice",
        "9:00 PM - 9:30 PM: Dinner",
        "9:30 PM - 10:30 PM: Full Day Quick Revision + Notes Review",
        "10:30 PM: Sleep"
    ]

def update_topic(date_str, subject, new_topic):
    if date_str not in schedule:
        schedule[date_str] = {"physics": "", "chemistry": "", "maths": ""}
    schedule[date_str][subject] = new_topic
    save_schedule()
