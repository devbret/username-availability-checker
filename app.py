from flask import Flask, request, jsonify, render_template
from concurrent.futures import ThreadPoolExecutor
import requests
import json
import logging
import os
import re
import threading

app = Flask(__name__)

DEBUG = os.environ.get("FLASK_DEBUG") == "1"
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

JSON_PATH = os.path.join('static', 'username_availability.json')

data_lock = threading.Lock()

USERNAME_PATTERN = re.compile(r'^[A-Za-z0-9._-]{1,40}$')

REQUEST_TIMEOUT = 5
MAX_WORKERS = 25

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

session = requests.Session()
session.headers.update(HEADERS)

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
    'GitLab': 'https://gitlab.com/{username}',
    'Telegram': 'https://t.me/{username}',
    'Patreon': 'https://www.patreon.com/{username}',
    'Behance': 'https://www.behance.net/{username}',
    'CodePen': 'https://codepen.io/{username}',
    'Replit': 'https://replit.com/@{username}',
    'Steam': 'https://steamcommunity.com/id/{username}',
    'Bandcamp': 'https://{username}.bandcamp.com',
    'Kick': 'https://kick.com/{username}',
    'Threads': 'https://www.threads.net/@{username}',
    'Spotify': 'https://open.spotify.com/user/{username}',
    'Snapchat': 'https://www.snapchat.com/add/{username}',
    'Gravatar': 'https://gravatar.com/{username}',
    'Quora': 'https://www.quora.com/profile/{username}',
    'ProductHunt': 'https://www.producthunt.com/@{username}',
    'Etsy': 'https://www.etsy.com/shop/{username}',
    'Bluesky': 'https://bsky.app/profile/{username}',
    'LastFM': 'https://www.last.fm/user/{username}',
    'Ko-fi': 'https://ko-fi.com/{username}',
    'BuyMeACoffee': 'https://www.buymeacoffee.com/{username}',
    'Gumroad': 'https://{username}.gumroad.com',
    'Itch.io': 'https://{username}.itch.io',
    'DevTo': 'https://dev.to/{username}',
    'Hashnode': 'https://hashnode.com/@{username}',
    'Substack': 'https://{username}.substack.com',
    'Mixcloud': 'https://www.mixcloud.com/{username}',
    'VK': 'https://vk.com/{username}',
    'Letterboxd': 'https://letterboxd.com/{username}',
    'Chess.com': 'https://www.chess.com/member/{username}',
    'Keybase': 'https://keybase.io/{username}',
    'Fiverr': 'https://www.fiverr.com/{username}',
    'Freelancer': 'https://www.freelancer.com/u/{username}',
    'About.me': 'https://about.me/{username}',
    'Disqus': 'https://disqus.com/by/{username}',
    'Trakt': 'https://trakt.tv/users/{username}',
    'Newgrounds': 'https://{username}.newgrounds.com',
    'Wattpad': 'https://www.wattpad.com/user/{username}',
    'Giphy': 'https://giphy.com/{username}',
    'Codeberg': 'https://codeberg.org/{username}',
    'Bitbucket': 'https://bitbucket.org/{username}',
    'SourceForge': 'https://sourceforge.net/u/{username}',
    'npm': 'https://www.npmjs.com/~{username}',
    'PyPI': 'https://pypi.org/user/{username}',
    'Docker Hub': 'https://hub.docker.com/u/{username}',
    'Kaggle': 'https://www.kaggle.com/{username}',
    'HackerRank': 'https://www.hackerrank.com/{username}',
    'LeetCode': 'https://leetcode.com/{username}',
    'Codewars': 'https://www.codewars.com/users/{username}',
    'freeCodeCamp': 'https://www.freecodecamp.org/{username}',
    'CodeChef': 'https://www.codechef.com/users/{username}',
    'Codeforces': 'https://codeforces.com/profile/{username}',
    'Imgur': 'https://imgur.com/user/{username}',
    '500px': 'https://500px.com/p/{username}',
    'Unsplash': 'https://unsplash.com/@{username}',
    'ArtStation': 'https://www.artstation.com/{username}',
    'Foursquare': 'https://foursquare.com/{username}',
    'Untappd': 'https://untappd.com/user/{username}',
    'Myspace': 'https://myspace.com/{username}',
    'Lichess': 'https://lichess.org/@/{username}',
    'Wikipedia': 'https://en.wikipedia.org/wiki/User:{username}',
    'Weibo': 'https://weibo.com/{username}',
    'Douban': 'https://www.douban.com/people/{username}',
    'Odnoklassniki': 'https://ok.ru/{username}',
    'Xing': 'https://www.xing.com/profile/{username}',
    'Linktree': 'https://linktr.ee/{username}',
    'Venmo': 'https://venmo.com/u/{username}',
    'PayPal': 'https://www.paypal.com/paypalme/{username}',
    'Liberapay': 'https://liberapay.com/{username}',
    'Open Collective': 'https://opencollective.com/{username}',
    'Genius': 'https://genius.com/{username}',
    'Discogs': 'https://www.discogs.com/user/{username}',
    'Trello': 'https://trello.com/{username}',
    'Figma': 'https://www.figma.com/@{username}',
    'Hacker News': 'https://news.ycombinator.com/user?id={username}',
    'Glitch': 'https://glitch.com/@{username}',
    'CodeSandbox': 'https://codesandbox.io/u/{username}',
    'Launchpad': 'https://launchpad.net/~{username}',
    'RubyGems': 'https://rubygems.org/profiles/{username}',
    'GameJolt': 'https://gamejolt.com/@{username}',
    'Wellfound': 'https://wellfound.com/u/{username}',
}


def check_site(site, url_pattern, username):
    url = url_pattern.format(username=username)
    try:
        response = session.get(
            url, timeout=REQUEST_TIMEOUT, allow_redirects=False
        )
        if response.status_code == 404:
            return site, {'status': 'available', 'url': None}
        elif response.status_code == 200:
            return site, {'status': 'taken', 'url': url}
        else:
            return site, {'status': 'unsure', 'url': None}
    except requests.exceptions.RequestException as e:
        logging.debug('Request to %s failed: %s', site, e)
        return site, {'status': 'unreachable', 'url': None}


def check_username(username):
    results = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(check_site, site, url_pattern, username)
            for site, url_pattern in websites.items()
        ]
        for future in futures:
            site, result = future.result()
            results[site] = result

    ordered = {site: results[site] for site in websites if site in results}
    return {'username': username, 'results': ordered}


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
    existing_data = load_existing_data(JSON_PATH)
    most_recent = existing_data[-1]['username'] if existing_data else None

    return render_template('index.html', most_recent=most_recent)


@app.route('/saved-data', methods=['GET'])
def saved_data():
    return jsonify(load_existing_data(JSON_PATH))


@app.route('/check', methods=['POST'])
def check():
    try:
        username = request.form.get('username', '').strip()
        if not USERNAME_PATTERN.match(username):
            return jsonify({
                'error': 'Invalid username. Use 1-40 letters, digits, '
                         'dots, hyphens or underscores.'
            }), 400

        logging.debug('Checking username: %s', username)
        new_results = check_username(username)

        with data_lock:
            os.makedirs('static', exist_ok=True)
            existing_data = load_existing_data(JSON_PATH)
            existing_data.append(new_results)
            with open(JSON_PATH, 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

        return jsonify(new_results)
    except Exception as e:
        logging.error('Error checking username:', exc_info=e)
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=DEBUG)
