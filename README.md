# Username Availability Checker

![Username availability results for a demo username.](https://hosting.photobucket.com/bbcfb0d4-be20-44a0-94dc-65bff8947cf2/cbbd5e4d-2a95-4d90-a54a-7b6e1496479e.png)

Check a username’s availability across one hundred major platforms, automatically save each search and visualize the results with an interactive bar chart.

## Overview

Checks whether a given username is available or taken across twenty popular online platforms by sending HTTP requests to each site’s profile URL pattern, then stores each search result in a JSON file for persistence. The frontend, built with HTML, JavaScript and D3.js, visualizes the results as a color-coded bar chart indicating availability status, allows users to click through to taken profiles and provides a dropdown menu to revisit and re-display previously searched usernames.

## Set Up Instructions

Below are the required software programs and set up steps for running this application on a Linux machine.

### Programs Needed

- [Git](https://git-scm.com/downloads)

- [Python](https://www.python.org/downloads/)

### Steps

1. Install the above programs

2. Open a terminal

3. Clone this repository using `git` by running the following command: `git clone git@github.com:devbret/username-availability-checker.git`

4. Navigate to the repo's directory: `cd username-availability-checker`

5. Create a virtual environment: `python3 -m venv venv`

6. Activate your virtual environment: `source venv/bin/activate`

7. Install the needed dependencies for running the Python script: `pip install -r requirements.txt`

8. Run the script: `python3 app.py`

9. Visit the following URL after the Flask server has started to view the frontend: `http://127.0.0.1:5000/`

10. Enter a username you wish to search for, then click the `Check` button and wait for your results

11. If a username is taken on a given platform and after clicking "taken", the relevant profile is opened in a new browser tab

12. Notice a dropdown select element toward the bottom of the application where you can access data from all of your prior searches

13. Exit the virtual environment when finished: `deactivate`

## Other Considerations

This project repo is intended to demonstrate an ability to do the following:

- Check a given username across multiple popular platforms to determine whether it is available, taken or uncertain

- Store each username search and its results in a JSON file, allowing users to revisit and compare previous checks

- Visualize the availability results in an interactive D3.js bar chart, with clickable links to profiles when usernames are already taken

If you have any questions or would like to collaborate, please reach out either on GitHub or via [my website](https://bretbernhoft.com/).
