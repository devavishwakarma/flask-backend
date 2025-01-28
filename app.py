import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Endpoint to get user details from Codeforces
@app.route('/codeforces/user', methods=['GET'])
def get_codeforces_user():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is missing"}), 400

    # Fetch user info from Codeforces API
    api_url = f"https://codeforces.com/api/user.info?handles={username}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error if status code is not 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch data from Codeforces"}), 500

    data = response.json()
    if data['status'] != "OK":
        return jsonify({"error": "User not found"}), 404

    return jsonify(data['result'][0])

# Endpoint to get user rating history from Codeforces
@app.route('/codeforces/rating-history', methods=['GET'])
def get_codeforces_rating_history():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is missing"}), 400

    # Fetch user rating history from Codeforces API
    api_url = f"https://codeforces.com/api/user.rating?handle={username}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error if status code is not 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch rating history from Codeforces: {str(e)}"}), 500

    data = response.json()
    if data['status'] != "OK":
        return jsonify({"error": "User not found"}), 404

    return jsonify(data['result'])

# Endpoint to get user details from CodeChef
@app.route('/codechef/user', methods=['GET'])
def get_codechef_user():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username parameter is missing"}), 400

    # CodeChef user data API URL
    api_url = f"https://www.codechef.com/users/{username}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error if status code is not 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data from CodeChef. Error: {str(e)}"}), 500

    # Parse the HTML response for user details
    if response.status_code == 200:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract user data from the page (this may need updating if CodeChef changes its structure)
        user_info = {
            "username": username,
            "rating": soup.find('div', class_='rating').text.strip() if soup.find('div', class_='rating') else "Not Available",
            "rank": soup.find('div', class_='rank').text.strip() if soup.find('div', class_='rank') else "Not Available"
        }
        return jsonify(user_info)
    else:
        return jsonify({"error": "User not found on CodeChef"}), 404

if __name__ == '__main__':
    app.run(debug=True)
