## Description

Budget Tracker is a simple project created out of fun to send email reports on your personal finances. It collects data from GSheet hosted on your Google Drive. GSheet's template is [following](https://docs.google.com/spreadsheets/d/19QmyL81UbqdCaX4Xi77h8M2GM_s9AWMgcfalyqxrAhA/edit?usp=drive_link).

## Environment setup

Make sure to add service_account.json file - standard json key file generated from IAM & Admin -> Service Accounts -> Keys. Also, to send emails, setup your smtp server and create email_credentials.json file with following structure:

```json
{
    "from": "",
    "to": [
        ""
    ],
    "host": "",
    "port": ,
    "smtpUser": "",
    "password": ""
}
```

In this case, poetry is used to install all Python libraries needed to execute the code. It is also required to have virtual environment creatd in the project dir:

`poetry config virtualenvs.in-project true `

To install all the dependencies, use standard:

`pip install poetry `

Finally, make sure to adjust values in config.json
