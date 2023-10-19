# OgameBot

## Dependencies
- Python 3.8 or higher
- [Discord.py v2.3.2](https://discordpy.readthedocs.io/en/stable/)
- [Google API](https://developers.google.com/sheets/api/quickstart/python)
    - `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`


## Installation
- `git clone https://github.com/Army-py/OgameBot`
- `cd OgameBot`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `python3 -m pip install -r requirements.txt`


## Execution
- Create a Discord bot [here](https://discord.com/developers/applications)
- Fill in the `bot_config/secret.json` file with the token of your bot
- Fill in the `bot_config/sheet.json` file with the ID of your Google Sheet file
- Execute the `bot.py` file with Python 3.8 or higher (`python bot.py`)

## Google API

### Service Account
- To use Google APIs, you need to create a service account.
- To do this, go to [this page](https://console.cloud.google.com/iam-admin/serviceaccounts) and select the project you want to use, or create a new one.
- Then click on `Create credentials` and then `Service account`.
- You can then choose the name of the service account.
- Then click on `Create and continue`.
- On the next page, you can choose the roles of the service account.
- For this project, you need to choose `Project` then `Owner`, `Editor`, and `Viewer`.
- Then click on `Continue`.


### credentials.json
- To obtain a key, which will be in a .json file, go to the interface of the service account you want to use.
- Then go to `Keys` in the top bar, then `Add key` and finally `Create key`.
- You will then choose `JSON` as the key type, and you will get a .json file.
- Then place this file in the `bot_config` folder located in the root of the project, and rename it to `credentials.json`.


### Google Sheet
- To use Google Sheet APIs, you will need to create a Google Sheet file beforehand.
- To do this, go to [this page](https://docs.google.com/spreadsheets/u/0/) and click on `New` then `Google Sheets`.
- You can then choose the name of the file.
- Retrieve the email address of the service account you created earlier, in the service account interface.
- Then go to the Google Sheet file you created, and click on `Share` in the top right corner.
- Paste the email address of the service account into the search bar, and select the appropriate rights.
- You can then retrieve the ID of the Google Sheet file in the file's URL. It is the string of characters after `/d/` and before `/edit`.
- You can then place the file ID in the `bot_config/sheet.json` file.

