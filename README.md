## Description

Budget Tracker is a simple project created out of fun to send email reports on your personal finances. It collects data from GSheet hosted on your Google Drive. GSheet's template is [following](https://docs.google.com/spreadsheets/d/19QmyL81UbqdCaX4Xi77h8M2GM_s9AWMgcfalyqxrAhA/edit?usp=drive_link).

## Environment setup

In this case, poetry is used to install all Python libraries needed to execute the code. It is also required to have virtual environment creatd in the project dir:

`poetry config virtualenvs.in-project true `

To install all the dependencies, use standard:

`pip install poetry `

Followed by:

`poetry install`

Finally, make sure to adjust values in config.json according to your needs.

## AWS

Project is using Infrastructure as a Code in Terraform in adition to custom Python scripts. Keep in mind service_account.json content is stored as a part of SM.

Vairables file is not added to Git, so you have to add it locally.
