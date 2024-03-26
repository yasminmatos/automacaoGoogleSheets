import csv
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_google_sheet():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("sheets", "v4", credentials=creds)
    spreadsheet_id = '1_AeJMJq6EFAzq9N6F4IaQ1GdqVNlamYYTJYC7yIZvFw'
    sheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=[]).execute()
    return sheet.get('sheets')[0]['properties']['title'], service

def sum_sales(service, spreadsheet_id):
    range_to_sum = 'Página1!C2:C1001' 
    formula = f'=SUM({range_to_sum})'
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Página1!D1',
        valueInputOption='USER_ENTERED',
        body={'values': [[formula]]}
    )
    response = request.execute()
    print('Soma de vendas realizada com sucesso!')

def main():
    try:
        sheet_name, service = get_google_sheet()
        spreadsheet_id = '1_AeJMJq6EFAzq9N6F4IaQ1GdqVNlamYYTJYC7yIZvFw' 
        # Ler os dados do arquivo CSV e converter para números
        with open('dados.csv', mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)  # Ignora o cabeçalho
            new_values = [[float(row[2])] for row in csv_reader]  # Converte para float

        # Construa a solicitação de atualização
        request = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Página1!C2:C1001',
            valueInputOption='USER_ENTERED',
            body={'values': new_values}
        )
        response = request.execute()

        sum_sales(service, spreadsheet_id)

    except HttpError as error:
        print(f"Ocorreu um erro: {error}")

if __name__ == "__main__":
    main()
