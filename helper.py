"""
Helper file
"""
import os
import json
from datetime import datetime

import boto3
import gspread
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from botocore.exceptions import ClientError
from redmail import EmailSender


def read_file(file_name, bucket_name='tf-budgettracker-bucket'):
    """
    Reads file from s3 bucket
    """
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=file_name)

        # Parse the JSON data
        data = json.loads(response['Body'].read().decode('utf-8'))

    return data

# global data
config = read_file(file_name='config.json')


class AWS:
    """
    AWS helper class
    """
    def _get_secret(self, secret_name: str, region_name: str) -> dict:
        """
        Getting values from secret managerr
        """
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e

        # Decrypts secret using the associated KMS key.
        secret = get_secret_value_response['SecretString']
        secret_dict = json.loads(secret)

        return secret_dict


class Email(AWS):
    """
    Email helper class
    """
    def __init__(self, email_to: str) -> None:
        self.email_to = email_to
        gmail_credentials = self._get_secret(
            secret_name=config['smtpServerSecret'],
            region_name=config['regionName']
        )
        self._email = EmailSender(
            host=gmail_credentials['host'],
            port=gmail_credentials['port'],
            username=gmail_credentials['smtpUser'],
            password=gmail_credentials['password']
        )

        tdy = datetime.now().strftime('%Y-%m-%d')
        self._subject = f'Budget Report for {tdy}'

    def send_email(self, html: str, plots: dict, tables: dict) -> None:
        """
        Send email after all components are built
        """
        try:
            self._email.send(
                subject=self._subject,
                sender='budgetTracket@gmail.com',
                receivers=self.email_to,
                html=html,
                body_images=plots,
                body_tables=tables
            )
            print(f'Email sent successfully to {self.email_to}')
        except Exception as e:
            print(f'Email sending to {self.email_to} failed: {e}')
            raise


class BudgetTracker(AWS):
    """
    Main helper function
    """
    def __init__(self, sheet_name: str) -> None:
        self.sheet_name = sheet_name

        self._df = self._get_data()
        self._current_month = int(datetime.now().strftime('%m'))
        self._current_year = int(datetime.now().strftime('%Y'))

    def _get_data(self) -> pd.DataFrame:
        gc = gspread.service_account_from_dict(self._get_secret(
            secret_name=config['googleServiceSecret'],
            region_name=config['regionName']
        ))
        file = gc.open(
            title=self.sheet_name
        )

        df_list = []
        workshet_list = file.worksheets()
        workshet_list = [
            x.title for x in workshet_list if x.title not in config['excludeSheetNames']
        ]
        for sheet in workshet_list:
            curr_sheet = file.worksheet(sheet)
            curr_df = pd.DataFrame(curr_sheet.get_all_records(head=3))
            df_list.append(curr_df)

        df = pd.concat(df_list)

        df = df[df['TYPE'] != 'Transfer']
        df['YEAR'] = df['DATE'].str.split('-').str[0].astype(int)
        df['MONTH'] = df['DATE'].str.split('-').str[1].astype(int)
        df.sort_values(by=['DATE'], inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    def get_spendings(self, img_name: str) -> pd.DataFrame:
        """
        Spending per Month
        """
        df_spendings = (
            self._df[self._df['AMOUNT'] < 0]
            .groupby(['YEAR', 'MONTH'])['AMOUNT']
            .sum()
            .round(2)
            .reset_index()
            .tail(12)
        )

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[
                f"{year}/{month}" 
                for year, month in zip(df_spendings['YEAR'], df_spendings['MONTH'])
            ],
            y=df_spendings['AMOUNT'],
            width=0.1,
            text=df_spendings['AMOUNT'],
            textposition='auto'
        ))
        fig.write_image(img_name)
        return df_spendings

    def get_trend(self, img_name: str) -> None:
        """
        Wallet value trend
        """
        self._df['TREND'] = self._df['AMOUNT'].cumsum()
        x = mdates.date2num(self._df['DATE'])
        z = np.polyfit(
            x,
            self._df['TREND'],
            1
        )
        p = np.poly1d(z)

        self._df['TREND_VAL'] = p(x)

        df_trend = (
            self._df.groupby(['DATE'])
            .agg({'TREND': 'max', 'TREND_VAL': 'max'})
            .reset_index()
        )
        slope = np.round(
            z[0] / df_trend['TREND'].iloc[0] * 100,
            2
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_trend['DATE'],
            y=df_trend['TREND'],
            name='cumsum'
        ))

        fig.add_trace(go.Scatter(
            x=df_trend['DATE'],
            y=df_trend['TREND_VAL'],
            name=f'trendline {slope}'
        ))
        fig.write_image(img_name)

    def get_cumsum_month(self) -> pd.DataFrame:
        """
        Cumsum walet value per month
        """
        df_cumsum_month = (
            self._df.groupby(['YEAR', 'MONTH'])['AMOUNT']
            .sum()
            .cumsum()
            .round(2)
            .reset_index()
            .tail(12)
        )
        return df_cumsum_month

    def get_spendings_current_month(self, img_name: str) -> None:
        """
        Current month spending per category
        """
        df_category = (
            self._df[
                (self._df['YEAR'] == self._current_year) &
                (self._df['MONTH'] == self._current_month) &
                (self._df['AMOUNT'] < 0)
            ]
            .groupby('TYPE')['AMOUNT']
            .sum()
            .round(2)
            .reset_index()
        )
        df_category['AMOUNT'] = df_category['AMOUNT'] * -1

        df_category = df_category.sort_values(by='AMOUNT', ascending=False).reset_index(drop=True)

        fig = go.Figure()
        fig.add_trace(go.Pie(
            values=df_category['AMOUNT'],
            labels=df_category['TYPE']
        ))
        fig.write_image(img_name)

        return df_category