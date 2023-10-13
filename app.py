from flask import Flask, render_template, request
import requests
import random
import json  # Don't forget to import json

app = Flask(__name__)

# Replace 'YOUR_API_MEMBER_ID' and 'YOUR_PIN' with your actual values
API_MEMBER_ID = 'AP608572'
PIN = '3F96C7A742'

def get_api_response(api_url):
    payload = {}
    headers = {}
    response = requests.get(api_url, headers=headers, data=payload)
    try:
        return response.json()  # Try to parse JSON response
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return response.text  # Return raw response text if JSON decoding fails

def format_response(response):
    if isinstance(response, list):
        # If the response is a list, assume it's a list of dictionaries and format each item
        formatted_response = "<br>".join("<br>".join(f"{key}: {value}" for key, value in item.items()) for item in response)
    elif isinstance(response, dict):
        # If the response is a dictionary, format it
        formatted_response = "<br>".join(f"{key}: {value}" for key, value in response.items())
    else:
        formatted_response = str(response)  # Fallback for other types
    return formatted_response.replace(',', '<br>')  # Replace commas with line breaks

def recharge(number, operator, circle, amount):
    # Generate a random 10-digit number for usertx
    usertx = str(random.randint(1000000000, 9999999999))

    api_url = f"https://cyrusrecharge.in/api/recharge.aspx?memberid={API_MEMBER_ID}&pin={PIN}&number={number}&operator={operator}&circle={circle}&amount={amount}&usertx={usertx}&format=json"
    return get_api_response(api_url)

@app.route('/')
def api_response():
    transaction_id = request.args.get('transaction_id')
    number = request.args.get('number')
    operator = request.args.get('operator')
    circle = request.args.get('circle')
    amount = request.args.get('amount')

    # Get balance information
    balance_url = f"http://Cyrusrecharge.in/api/GetOperator.aspx?memberid={API_MEMBER_ID}&pin={PIN}&Method=getbalance"
    balance_response = get_api_response(balance_url)
    formatted_balance_response = format_response(balance_response)

    # Get status information if a transaction ID is provided
    status_response = ""
    if transaction_id:
        status_url = f"https://cyrusrecharge.in/api/rechargestatus.aspx?memberid={API_MEMBER_ID}&pin={PIN}&transid={transaction_id}"
        status_response = get_api_response(status_url)
        formatted_status_response = format_response(status_response)
        # If it's a dictionary, replace commas with line breaks
        if isinstance(status_response, dict):
            formatted_status_response = formatted_status_response.replace(',', '<br>')
    else:
        formatted_status_response = ""

    # Recharge if all required parameters are provided
    recharge_response = ""
    if number and operator and circle and amount:
        recharge_response = recharge(number, operator, circle, amount)
        formatted_recharge_response = format_response(recharge_response)
        # If it's a dictionary, replace commas with line breaks
        if isinstance(recharge_response, dict):
            formatted_recharge_response = formatted_recharge_response.replace(',', '<br>')
    else:
        formatted_recharge_response = ""

    return render_template('index.html', balance_response_text=formatted_balance_response,
                           status_response_text=formatted_status_response, recharge_response_text=formatted_recharge_response)

if __name__ == '__main__':
    app.run(debug=True)
