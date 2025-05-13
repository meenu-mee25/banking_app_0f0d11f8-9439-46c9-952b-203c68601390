import logging
from flask import Flask, request, jsonify
from threading import Thread
import time
import math
from functools import wraps
import threading
import hashlib
import random
import os
from flask_cors import CORS
from prefix_middleware import PrefixMiddleware
import msal
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix='/api')

# Configure MSAL client
msal_client = msal.ConfidentialClientApplication(
    client_id='your_client_id',
    client_credential='your_client_secret',
    authority='https://login.microsoftonline.com/your_tenant_id',
)

# Decorator to require authentication
def require_auth(view_func):
    @wraps(view_func)
    def decorated(*args, **kwargs):
        if 'access_token' not in session:
            return 'Unauthorized', 401
        return view_func(*args, **kwargs)
    return decorated

# Configure logging
logging.basicConfig(filename='app_logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Sample data
users = [
    {
        'id': 1,
        'name': 'John Doe',
        'income': 50000,
        'expenses': 20000,
        'credit_score': 750,
        'loans': []
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'income': 75000,
        'expenses': 30000,
        'credit_score': 680,
        'loans': []
    }
]

# Helper functions
def calculate_loan_eligibility(income, expenses, credit_score):
    conn.rollback()
    cur = conn.cursor()

    """
    Calculate loan eligibility based on income, expenses, and credit score.
    """
    # Use a simple formula for demonstration purposes
    eligibility_score = (income - expenses) * 0.3 + credit_score * 0.7
    return eligibility_score > 600

def calculate_emi(loan_amount, interest_rate, tenure):
    conn.rollback()
    cur = conn.cursor()

    """
    Calculate the Equated Monthly Installment (EMI) for a loan.
    """
    interest_rate = interest_rate / (12 * 100)  # Convert interest rate to monthly rate
    tenure = tenure * 12  # Convert tenure from years to months
    emi = (loan_amount * interest_rate * (1 + interest_rate) ** tenure) / ((1 + interest_rate) ** tenure - 1)
    return emi

# Parallelization and concurrency
def run_in_background(func, *args):
    conn.rollback()
    cur = conn.cursor()

    """
    Run a function in a separate thread to improve concurrency.
    """
    thread = Thread(target=func, args=args)
    thread.start()
    return thread

# API endpoints
@app.route('/loan_eligibility', methods=['POST'])
def loan_eligibility():
    conn.rollback()
    cur = conn.cursor()

    """
    Calculate loan eligibility based on user's income, expenses, and credit score.
    """
    data = request.get_json()
    income = data.get('income')
    expenses = data.get('expenses')
    credit_score = data.get('credit_score')

    if not income or not expenses or not credit_score:
        return jsonify({'error': 'Missing required fields'}), 400

    # Optimize by running the calculation in a separate thread
    thread = run_in_background(calculate_loan_eligibility, income, expenses, credit_score)

    # Return a temporary response and log the result when available
    @app.route('/emi_calculator', methods=['POST'])
def emi_calculator():
    conn.rollback()
    cur = conn.cursor()

    """
    Calculate the EMI based on loan amount, interest rate, and tenure.
    """
    data = request.get_json()
    loan_amount = data.get('loan_amount')
    interest_rate = data.get('interest_rate')
    tenure = data.get('tenure')

    if not loan_amount or not interest_rate or not tenure:
        return jsonify({'error': 'Missing required fields'}), 400

    # Optimize by running the calculation in a separate thread
    thread = run_in_background(calculate_emi, loan_amount, interest_rate, tenure)

    # Return a temporary response and log the result when available
    def get_result():
    conn.rollback()
    cur = conn.cursor()

        result = thread.join()
        logging.info(f'EMI calculation result: {result}')
        return jsonify({'emi': result})

    return get_result()

@app.route('/loan_application', methods=['POST'])
def loan_application():
    conn.rollback()
    cur = conn.cursor()

    """
    Submit a loan application.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    loan_amount = data.get('loan_amount')
    tenure = data.get('tenure')

    if not user_id or not loan_amount or not tenure:
        return jsonify({'error': 'Missing required fields'}), 400

    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Calculate loan eligibility
    eligible = calculate_loan_eligibility(user['income'], user['expenses'], user['credit_score'])
    if not eligible:
        return jsonify({'message': 'Loan application rejected due to ineligibility'}), 400

    # Calculate EMI
    interest_rate = 10  # Assume a fixed interest rate for simplicity
    emi = calculate_emi(loan_amount, interest_rate, tenure)

    # Save the loan details
    loan = {
        'amount': loan_amount,
        'interest_rate': interest_rate,
        'tenure': tenure,
        'emi': emi
    }
    user['loans'].append(loan)

    return jsonify({'message': 'Loan application submitted successfully', 'emi': emi})

@app.route('/loan_details/<int:user_id>', methods=['GET'])
def loan_details(user_id):
    conn.rollback()
    cur = conn.cursor()

    """
    Get loan details and repayment schedule for a user.
    """
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    loans = user['loans']
    loan_details = []
    for loan in loans:
        repayment_schedule = []
        remaining_amount = loan['amount']
        for i in range(loan['tenure']):
            emi = loan['emi']
            interest = remaining_amount * (loan['interest_rate'] / (12 * 100))
            principal = emi - interest
            remaining_amount -= principal
            repayment_schedule.append({
                'month': i + 1,
                'emi': emi,
                'interest': interest,
                'principal': principal,
                'remaining_amount': remaining_amount
            })
        loan_details.append({
            'amount': loan['amount'],
            'interest_rate': loan['interest_rate'],
            'tenure': loan['tenure'],
            'emi': loan['emi'],
            'repayment_schedule': repayment_schedule
        })

    return jsonify({'loan_details': loan_details})





# Configure logging
logging.basicConfig(filename='app_logger.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample data
users = [
    {'id': 1, 'name': 'John Doe', 'pin': '1234', 'biometric': 'fingerprint', 'phone': '1234567890'},
    {'id': 2, 'name': 'Jane Smith', 'pin': '5678', 'biometric': 'facial', 'phone': '9876543210'}
]

payees = [
    {'id': 1, 'name': 'Utility Company', 'account': '1234567890', 'bank': 'ABC Bank'},
    {'id': 2, 'name': 'Rent Payment', 'account': '0987654321', 'bank': 'XYZ Bank'}
]

payments = []

# Authentication decorator
def authenticate(func):
    conn.rollback()
    cur = conn.cursor()

    @wraps(func)
    def wrapper(*args, **kwargs):
    conn.rollback()
    cur = conn.cursor()

        auth_data = request.get_json()
        user_id = auth_data.get('user_id')
        auth_method = auth_data.get('auth_method')
        auth_value = auth_data.get('auth_value')

        user = next((user for user in users if user['id'] == user_id), None)
        if user:
            if auth_method == 'pin' and user['pin'] == auth_value:
                logging.info(f"User {user_id} authenticated with PIN")
                return func(*args, **kwargs)
            elif auth_method == 'biometric' and user['biometric'] == auth_value:
                logging.info(f"User {user_id} authenticated with biometric")
                return func(*args, **kwargs)
            elif auth_method == 'otp':
                # Generate and send OTP
                otp = str(random.randint(100000, 999999))
                logging.info(f"OTP {otp} sent to user {user_id}")
                if auth_value == otp:
                    logging.info(f"User {user_id} authenticated with OTP")
                    return func(*args, **kwargs)

        logging.warning(f"Authentication failed for user {user_id}")
        return jsonify({'error': 'Authentication failed'}), 401

    return wrapper

# Parallelization with threads
def run_in_thread(func):
    conn.rollback()
    cur = conn.cursor()

    @wraps(func)
    def wrapper(*args, **kwargs):
    conn.rollback()
    cur = conn.cursor()

        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return jsonify({'message': 'Task started in a separate thread'})

    return wrapper

# Optimize algorithms for better time and space complexity
def search_payments(start_date, end_date, payee_id=None, status=None):
    conn.rollback()
    cur = conn.cursor()

    filtered_payments = [
        payment for payment in payments
        if start_date <= payment['date'] <= end_date
        and (payee_id is None or payment['payee_id'] == payee_id)
        and (status is None or payment['status'] == status)
    ]
    return filtered_payments

# Reduce memory usage and optimize memory footprint
def export_payments(payments, format):
    conn.rollback()
    cur = conn.cursor()

    if format == 'csv':
        csv_data = 'Date,Amount,Payee,Status\n'
        for payment in payments:
            payee_name = next((payee['name'] for payee in payees if payee['id'] == payment['payee_id']), 'Unknown')
            csv_data += f"{payment['date']},{payment['amount']},{payee_name},{payment['status']}\n"
        return csv_data
    elif format == 'pdf':
        # Implement PDF generation logic here
        return 'PDF data'

# Implement hardware-specific optimizations if feasible
# This section can be expanded if specific hardware optimizations are required

# Consider network efficiency if interacting with remote resources
# This section can be expanded if the application interacts with remote resources

# Modernize the codebase by adopting best practices and new language features
# This section can be expanded with specific examples of modern language features and best practices

# API endpoints
@app.route('/authenticate', methods=['POST'])
@authenticate
def authenticate_user():
    conn.rollback()
    cur = conn.cursor()

    return jsonify({'message': 'Authentication successful'})

@app.route('/schedule-payment', methods=['POST'])
@authenticate
@run_in_thread
def schedule_payment():
    conn.rollback()
    cur = conn.cursor()

    payment_data = request.get_json()
    payee_id = payment_data.get('payee_id')
    amount = payment_data.get('amount')
    frequency = payment_data.get('frequency')
    start_date = payment_data.get('start_date')
    end_date = payment_data.get('end_date')

    # Schedule payment logic
    logging.info(f"Scheduling payment for payee {payee_id} with amount {amount} and frequency {frequency}")

    return jsonify({'message': 'Payment scheduled successfully'})

@app.route('/add-payee', methods=['POST'])
@authenticate
def add_payee():
    conn.rollback()
    cur = conn.cursor()

    payee_data = request.get_json()
    name = payee_data.get('name')
    account = payee_data.get('account')
    bank = payee_data.get('bank')

    # Add payee logic
    new_payee = {'id': len(payees) + 1, 'name': name, 'account': account, 'bank': bank}
    payees.append(new_payee)
    logging.info(f"Added new payee: {new_payee}")

    return jsonify({'message': 'Payee added successfully', 'payee': new_payee})

@app.route('/payment-history', methods=['GET'])
@authenticate
def get_payment_history():
    conn.rollback()
    cur = conn.cursor()

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payee_id = request.args.get('payee_id')
    status = request.args.get('status')

    filtered_payments = search_payments(start_date, end_date, payee_id, status)
    logging.info(f"Retrieved payment history with filters: start_date={start_date}, end_date={end_date}, payee_id={payee_id}, status={status}")

    return jsonify({'payments': filtered_payments})

@app.route('/export-payments', methods=['GET'])
@authenticate
def export_payment_history():
    conn.rollback()
    cur = conn.cursor()

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    payee_id = request.args.get('payee_id')
    status = request.args.get('status')
    export_format = request.args.get('format', 'csv')

    filtered_payments = search_payments(start_date, end_date, payee_id, status)
    export_data = export_payments(filtered_payments, export_format)
    logging.info(f"Exported payment history in {export_format} format")

    return export_data



@app.route('/import-schema', methods=['POST'])
def import_schema_endpoint():
    conn = psycopg2.connect(os.environ.get("db_url"))
    cursor = conn.cursor()
    with open('database/db_script.sql', 'r') as file:
        schema_sql = file.read()
    cursor.execute(schema_sql)
    conn.commit()
    return 'Schema imported successfully.'

if __name__ == "__main__":
    app.run(host='0.0.0.0')