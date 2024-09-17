# Username Availability Checker

![Username availability results for a demo username.](https://hosting.photobucket.com/images/i/bernhoftbret/username-availability-checker-2-frontpage-updated.png)

Check the availability of a username across twenty popular platforms.

## Set Up

### Programs Needed

-   [Git](https://git-scm.com/downloads)
-   [Python](https://www.python.org/downloads/) (When installing on Windows, make sure you check the ["Add python 3.xx to PATH"](https://hosting.photobucket.com/images/i/bernhoftbret/python.png) box.)

### Steps

1. Install the above programs.
2. Open a shell window (For Windows open PowerShell, for MacOS open Terminal & for Linux open your distro's terminal emulator).
3. Clone this repository using `git` by running the following command; `git clone https://github.com/devbret/username-availability-checker`.
4. Navigate to the repo's directory by running; `cd username-availability-checker`.
5. Install the needed dependencies for running the script by running; `pip install -r requirements.txt`.
6. Run the script with the command `python3 app.py`. After the Flask server has started, visit [this link](http://127.0.0.1:5000/) in a browser, and you will be brought to the live application.
7. Enter the username you wish to search for, then click the "Check" button. Your results will be returned to you momentarily.
8. If a username is taken on a given platform, then by clicking "taken", the relevant profile is opened in a new tab.
