# Username Availability Checker

![Username availability results for a demo username.](https://hosting.photobucket.com/bbcfb0d4-be20-44a0-94dc-65bff8947cf2/b7638cad-0d3f-410e-b259-d82c247f521a.png)

Check a username’s availability across twenty major platforms, save the results and visualize them in a bar chart.

## Overview

Checks whether a given username is available or taken across twenty popular online platforms by sending HTTP requests to each site’s profile URL pattern, then stores each search result in a JSON file for persistence. The frontend, built with HTML, JavaScript and D3.js, visualizes the results as a color-coded bar chart indicating availability status, allows users to click through to taken profiles and provides a dropdown menu to revisit and re-display previously searched usernames.

## Set Up Instructions

Below are the required software programs and set up steps for running this application.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository using `git` by running the following command: `git clone git@github.com:devbret/username-availability-checker.git`

4. Navigate to the repo's directory by running: `cd username-availability-checker`

5. Install the needed dependencies for running the script with this command: `pip install -r requirements.txt`

6. Run the script with the command: `python3 app.py`

7. After the Flask server has started, visit `http://127.0.0.1:5000/` in a browser and you will be brought to the live application

8. Enter the username you wish to search for, then click the "Check" button and wait for your results

9. If a username is taken on a given platform, then by clicking "taken", the relevant profile is opened in a new tab

10. You will also notice a dropdown select element toward the bottom of the application where you can access data from all of your prior searches
