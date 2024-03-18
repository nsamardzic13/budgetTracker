import os
import json
import boto3

from helper import BudgetTracker, Email


def read_file(file_name, bucket_name='tf-budgettracker-bucket'):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
    else:
        # set user - hotflix for 'getpwuid(): uid not found: 10000'
        os.environ['USER'] = 'GlueUser'
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=file_name)

        # Parse the JSON data
        data = json.loads(response['Body'].read().decode('utf-8'))

    return data

# global data 
config = read_file(file_name='config.json')

def main():

    for sheet_name, email_to in zip(config['gSheetNames'], config['targetEmails']):
        print(f'Starting {sheet_name} for {email_to}')
        email = Email(email_to=email_to)
        budget_tracker = BudgetTracker(sheet_name=sheet_name)

        df_spendings = budget_tracker.get_spendings(img_name=config['spendingsImg'])
        budget_tracker.get_trend(img_name=config['trendImg'])
        df_cumsum_month = budget_tracker.get_cumsum_month()
        df_current_month = budget_tracker.get_spendings_current_month(img_name=config['spendingsCurrentMonthImg'])

        # construct email
        html = """
            <h1>Spendings per Month (last 12)</h1>
            {{ img_spendings }}
            <br>
            {{ df_spendings }}
            <br>

            <h1>Total Wallet Value Trend</h1>
            {{ img_trend }}
            <br>

            <h1>Wallet Vaulue per Month</h1>
            {{ df_cumsum_month }}
            <br>

            <h1>Spendings Current Month</h1>
            {{ img_spendings_current_month }}
            <br>
            {{ df_current_month }}
            <br>
        """

        plots = {
            'img_spendings': config['spendingsImg'],
            'img_trend': config['trendImg'],
            'img_spendings_current_month': config['spendingsCurrentMonthImg'],
        }

        tables = {
            'df_spendings': df_spendings,
            'df_cumsum_month': df_cumsum_month,
            'df_current_month': df_current_month
        }

        email.send_email(
            html=html,
            plots=plots,
            tables=tables
        )

if __name__ == '__main__':
    main()
