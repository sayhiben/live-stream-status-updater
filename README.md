# live-stream-status-updater
Reads a list of URLs to social media accounts and determines whether or not they are currently live streaming

## Setup

### Installing dependencies

Make sure you have python3 installed on your system.
If you know about virtualenvironments and stuff, feel free to alter these steps to fit your preferred workflow.

Run `python3 -m pip install -r requirements.txt`. Or, on windows, try `py -m pip install -r requirements.txt`.

### Configuration

To enable authentication to Google Sheets, you need to enable the Sheets API here by obtaining a `credentials.json` file and putting it in the root of this repository. Instructions are available here: [https://developers.google.com/sheets/api/quickstart/python]. Click the `Enable Google Sheets API` button, accept the default of `Desktop App`, and click `Download Client Configuration`.

The first time you run the program, a webpage will open in your browser, asking you to authorize the application you just created to edit your data on Google Sheets. It will be named `Quickstart`. Accept these permissions - authorization will be stored in `token.pickle` for future use.
