from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/user/<username>/stats', methods=['GET'])
def get_user_stats(username):
    response = requests.get(f"https://auth.geeksforgeeks.org/user/{username}/practice/", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
    })

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch user data from GeeksforGeeks"})

    soup = BeautifulSoup(response.content, "html.parser")

    problem_elements = soup.find_all("li", {"class": "tab"})
    get_data = soup.find_all("span", {"class": "score_card_value"})

    x = (str(get_data).split())
    y = str(problem_elements)

    sentences = y.split()
    formatted_str = y.replace(" ", "")
    formatted_str1 = formatted_str.replace("(", "")

    medium_match = re.findall(r'MEDIUM\d+', formatted_str1)
    hard_match = re.findall(r'HARD\d+', formatted_str1)
    easy_match = re.findall(r'EASY\d+', formatted_str1)

    medium = re.findall(r'\d+', str(medium_match))
    hard = re.findall(r'\d+', str(hard_match))
    easy = re.findall(r'\d+', str(easy_match))
    get_score_value = re.findall(r'\d+', x[1])
    get_problem_solved = re.findall(r'\d+', x[3])

    stats = {
        "medium_problems_solved": medium,
        "hard_problems_solved": hard,
        "easy_problems_solved": easy,
        "total_problems_solved": get_problem_solved,
        "overall_coding_score": get_score_value
    }

    return jsonify(stats)

if __name__ == '__main__':
    app.run()
