# Username Availability Checker

![Username availability results for a demo username.](https://hosting.photobucket.com/bbcfb0d4-be20-44a0-94dc-65bff8947cf2/cbbd5e4d-2a95-4d90-a54a-7b6e1496479e.png)

Check a username’s availability across one hundred major platforms, automatically save each search and visualize the results with an interactive UI.

## Application Overview

Checks whether a given username is available or taken across one hundred popular online platforms by sending HTTP requests to each site’s profile URL pattern, then stores each search result in a JSON file for persistence. The frontend (built with HTML, JavaScript and D3.js) visualizes the results as color-coded cards indicating availability status, allowing users to click through to taken profiles and providing a dropdown menu to revisit and re-display previously searched usernames.

## Basic Setup Instructions

Below are the required software programs and set up steps for running this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository: `git clone git@github.com:devbret/username-availability-checker.git`

4. Navigate to the repo's directory: `cd username-availability-checker`

5. Create a virtual environment: `python3 -m venv venv`

6. Activate your virtual environment: `source venv/bin/activate`

7. Install the needed dependencies: `pip install -r requirements.txt`

8. Run the script: `python3 app.py`

9. Visit the frontend in a browser: `http://127.0.0.1:5000/`

10. Exit the virtual environment when finished: `deactivate`

## Other Considerations

Below you will find information not covered in the installation and use sections above. Including the abilities this repo is intended to demonstrate. As well as an overview of the license this code is made available with. And a way to contact the maintainer with questions, suggestions and collaboration opportunities.

### Abilities Demonstrated

This project repo is intended to demonstrate an ability to do the following:

- Check whether a given username is available or already taken across 100 major online platforms

- Classify each result as available, taken or unsure based on the HTTP status code returned

- Persist every search and its results in a JSON file so past lookups can be revisited and compared later

- Serve a Flask web frontend to visualize the results as a color-coded, interactive UI with clickable links to profiles already taken

### License Information

This repository is distributed under the MIT License. You are free to use, copy, modify, merge, publish, distribute, sublicense and sell copies of this software, including as part of proprietary or commercial work. The single condition is the copyright and permission notices contained in the LICENSE file must be included with any copy or substantial portion of the software that you redistribute. The software is provided "as is", without warranty of any kind, and the copyright holder is not liable for any claim or damages arising from its use.

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
