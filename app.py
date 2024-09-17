from flask import Flask, request, jsonify, render_template
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    try:
        username = request.form['username']
        logging.debug(f'Checking username: {username}')
        results = check_username(username)
        
        os.makedirs('static', exist_ok=True)
        
        with open('static/username_availability.json', 'w') as json_file:
            json.dump(results, json_file, indent=4)
        
        return jsonify(results)
    except Exception as e:
        logging.error('Error checking username:', exc_info=e)
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
