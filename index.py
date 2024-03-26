import csv
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # ID da planilha que você deseja editar
        spreadsheet_id = '1_AeJMJq6EFAzq9N6F4IaQ1GdqVNlamYYTJYC7yIZvFw'

        #INTERVALO
        range_name = '1:1000'  

        # Ler os dados do arquivo CSV
        with open('dados.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            new_values = list(csv_reader)

        value_input_option = 'RAW'
        body = {
            'values': new_values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()

        print('{0} cells updated.'.format(result.get('updatedCells')))

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
