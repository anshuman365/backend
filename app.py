from flask import Flask, render_template
from api.detect_reviews import detect_fake_review
from api.detect_transactions import detect_fraud_transaction
from api.detect_scams import detect_scam
import config
from flask import session, redirect, url_for
from auth import auth

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

app.register_blueprint(auth)

@app.before_request
def require_login():
    if 'admin' not in session and request.endpoint in ['dashboard']:
        return redirect(url_for('login'))
        
@app.route('/fraud_report')
def fraud_report():
    cursor.execute("SELECT COUNT(*) FROM reviews WHERE is_fake = TRUE")
    fake_reviews = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE is_fraud = TRUE")
    fraud_transactions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scams WHERE detected = TRUE")
    scams = cursor.fetchone()[0]

    return jsonify({'fake_reviews': fake_reviews, 'fraud_transactions': fraud_transactions, 'scams': scams})
    
if __name__ == '__main__':
    app.run(debug=True)