from flask import Blueprint

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/quiz')
def quiz_home():
    return "Quiz system is working!"