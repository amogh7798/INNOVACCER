# INNOVACCER
The python code (main_code.py) fetches input such as email-ID and TV series.It then searches for details on next streaming episode of entered TV series from IMDb.com and sends a automatic generated mail to the user.
Meanwhile,The user entered details are stored in MYSQL DB.An well built attractive UI is build using tkinter to make user's job easy.

The libraries required to be installed are 
1)IMDbPY   (pip install imdbpy)
2)google-api-python-client   (pip install --upgrade google-api-python-client)
3)mysql-connector    (pip install mysql-connector)
4)OAUTH2client       (pip install oauth2client)

For sending E-mail using python,Google API is used.The steps are as follows
Setup

    Create a project in Google Developers Console with the required Google account and enable the Gmail API [here](https://console.developers.google.com/start/api?id=gmail)

    Add Credentials in the Credentials Tab and select OAuth 2.0 client ID.

    Select the application type Other and create .

    Add homepage URL like http://localhost:8000 for testing.

    Download JSON file as given to the right of the Client ID.

    Rename as client_secret.json and move it to the same directory as main_code.py.

The code asks for Gmail credentials for first time uses.The code then continues running in localhost.
