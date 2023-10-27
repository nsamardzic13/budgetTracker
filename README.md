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


Poetry has too many packages, some are needed for GCP version, others for AWS. Cleanup will be done in the future.


## AWS 

AWS version of the solution is the main one. It is using Infrastructure as a Code in Terraform in adition to custom python scripts. Keep in mind service_account.json content is stored as a part of SM.

To refresh code of AWS Glue in case any of the code files is updated, use following tf command:

```
terraform apply -replace aws_s3_object.tf_budget_tracker_bucket_object_main \
                -replace aws_s3_object.tf_budget_tracker_bucket_object_helper \
                -replace aws_s3_object.tf_budget_tracker_bucket_object_config\
                -replace aws_s3_object.tf_budget_tracker_bucket_object_email

```
