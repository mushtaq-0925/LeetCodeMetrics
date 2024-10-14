from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  
import requests  

app = Flask(__name__)
CORS(app)  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch_leetcode_data', methods=['POST'])
def fetch_leetcode_data():
    
    data = request.json
    username = data.get('username')

  
    graphql_query = {
        "query": """
        query userSessionProgress($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                    totalSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
            }
        }
        """,
        "variables": {"username": username}
    }

    response = requests.post(
        'https://leetcode.com/graphql/',
        json=graphql_query,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        return jsonify(response.json()) 
    else:
        return jsonify({"error": "Unable to fetch data from LeetCode"}), 500

if __name__ == '__main__':
    app.run(debug=True)
