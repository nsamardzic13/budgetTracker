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

def read_file(file_name, bucket_name='tf-budget-tracker-bucket'):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
    else:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=bucket_name, Key=file_name)

        # Parse the JSON data
        data = json.loads(response['Body'].read().decode('utf-8'))

    return data

# global data 
config = read_file(file_name='config.json')
gmail_credentials = read_file(file_name='email_credentials.json')


class Email:

    def __init__(self) -> None:
        self.email = EmailSender(
            host=gmail_credentials['host'],
            port=gmail_credentials['port'],
            username=gmail_credentials['smtpUser'],
            password=gmail_credentials['password']
        )

        tdy = datetime.now().strftime('%Y-%m-%d')
        self.subject = f'Budget Report for {tdy}'

    def send_email(self, html: str, plots: dict, tables: dict) -> None:
        try:
            self.email.send(
                subject=self.subject,
                sender=gmail_credentials['from'],
                receivers=gmail_credentials['to'],
                html=html,
                body_images=plots,
                body_tables=tables
            )
            print('Email sent successfully')
        except Exception as e:
            print(f'Email sending failed: {e}')
            raise


class BudgetTracker:

    def __init__(self) -> None:
        self.df = self.get_data()
        self.current_month = int(datetime.now().strftime('%m'))
        self.current_year = int(datetime.now().strftime('%Y'))

    def get_secret(self) -> dict:
        secret_name = config['serviceName']
        region_name = config['regionName']

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
    
    def get_data(self) -> pd.DataFrame:
        gc = gspread.service_account_from_dict(self.get_secret())
        file = gc.open(
            title=config['gSheetName']
        )

        df_list = []
        for sheet in config['sheetNames']:
            curr_sheet = file.worksheet(sheet)
            curr_df = pd.DataFrame(curr_sheet.get_all_records(head=3))
            df_list.append(curr_df)

        df = pd.concat(df_list)

        df = df[df['TYPE'] != 'Transfer']
        df['YEAR'] = df['DATE'].str[:4].astype(int)
        df['MONTH'] = df['DATE'].str[5:7].astype(int)
        df.sort_values(by=['DATE'], inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df

    def get_spendings(self, img_name: str) -> pd.DataFrame:
        ## Spending per Month
        df_spendings = self.df[self.df['AMOUNT'] < 0].groupby(['YEAR', 'MONTH'])['AMOUNT'].sum().reset_index().tail(12)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"{year}/{month}" for year, month in zip(df_spendings['YEAR'], df_spendings['MONTH'])],
            y=df_spendings['AMOUNT'],
            width=0.1,
            text=df_spendings['AMOUNT'],
            textposition='auto'
        ))
        fig.write_image(img_name)

        return df_spendings

    def get_trend(self, img_name: str) -> None:
        self.df['TREND'] = self.df['AMOUNT'].cumsum()
        x = mdates.date2num(self.df['DATE'])
        z = np.polyfit(
            x, 
            self.df['TREND'], 
            1
        )
        p = np.poly1d(z)

        self.df['TREND_VAL'] = p(x)

        df_trend = self.df.groupby(['DATE']).agg({'TREND': 'max', 'TREND_VAL': 'max'}).reset_index()
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
        df_cumsum_month = self.df.groupby(['YEAR', 'MONTH'])['AMOUNT'].sum().groupby(level=0).cumsum().reset_index().tail(12)
        return df_cumsum_month

    def get_spendings_current_month(self, img_name: str) -> None:
        df_category = self.df[(self.df['YEAR'] == self.current_year) & (self.df['MONTH'] == self.current_month) & (self.df['AMOUNT'] < 0)].groupby('TYPE')['AMOUNT'].sum().reset_index()
        df_category['AMOUNT'] = df_category['AMOUNT'] * -1

        df_category.sort_values(by='AMOUNT', ascending=False).reset_index(drop=True)

        fig = go.Figure()
        fig.add_trace(go.Pie(
            values=df_category['AMOUNT'],
            labels=df_category['TYPE']
        ))
        fig.write_image(img_name)

        return df_category