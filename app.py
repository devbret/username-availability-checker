from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
import json
import logging
import os

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

websites = {
    'YouTube': 'https://www.youtube.com/@{username}',
    'WordPress': 'https://{username}.wordpress.com',
    'X': 'https://x.com/{username}',
    'Facebook': 'https://www.facebook.com/{username}',
    'Instagram': 'https://www.instagram.com/{username}',
    'GitHub': 'https://github.com/{username}',
    'Reddit': 'https://www.reddit.com/user/{username}',
    'LinkedIn': 'https://www.linkedin.com/in/{username}',
    'Pinterest': 'https://www.pinterest.com/{username}',
    'Tumblr': 'https://{username}.tumblr.com',
    'TikTok': 'https://www.tiktok.com/@{username}',
    'Twitch': 'https://www.twitch.tv/{username}',
    'Medium': 'https://{username}.medium.com',
    'Vimeo': 'https://vimeo.com/{username}',
    'DeviantArt': 'https://www.deviantart.com/{username}',
    'SoundCloud': 'https://soundcloud.com/{username}',
    'Flickr': 'https://www.flickr.com/people/{username}',
    'Dribbble': 'https://dribbble.com/{username}',
    'Slack': 'https://{username}.slack.com',
    'Blogger': 'https://{username}.blogspot.com',
}

def check_username(username):
    results = {}

    for site, url_pattern in websites.items():
        url = url_pattern.format(username=username)
        try:
            response = requests.get(url)
            if response.status_code == 404:
                results[site] = {'status': 'available', 'url': None}
            elif response.status_code == 200:
                results[site] = {'status': 'taken', 'url': url}
            else:
                results[site] = {'status': 'unsure', 'url': None}
        except requests.exceptions.RequestException as e:
            results[site] = {'status': f'error: {e}', 'url': None}

    return {'username': username, 'results': results}

def load_existing_data(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

@app.route('/')
def index():
    json_path = os.path.join('static', 'username_availability.json')
    existing_data = load_existing_data(json_path)
    most_recent = existing_data[-1]['username'] if existing_data else None

    return render_template('index.html', most_recent=most_recent)

@app.route('/saved-data', methods=['GET'])
def saved_data():
    json_path = os.path.join('static', 'username_availability.json')
    if os.path.exists(json_path):
        data = load_existing_data(json_path)
        return jsonify(data)
    else:
        return jsonify([])

@app.route('/check', methods=['POST'])
def check():
    try:
        username = request.form['username']
        logging.debug(f'Checking username: {username}')
        new_results = check_username(username)

        os.makedirs('static', exist_ok=True)
        json_path = os.path.join('static', 'username_availability.json')
        existing_data = load_existing_data(json_path)

        existing_data.append(new_results)

        with open(json_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        return jsonify(new_results)
    except Exception as e:
        logging.error('Error checking username:', exc_info=e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
