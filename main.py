import os.path
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

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
    spreadsheet_id = '1_AeJMJq6EFAzq9N6F4IaQ1GdqVNlamYYTJYC7yIZvFw'  # ID da sua planilha
    sheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=[]).execute()
    return sheet.get('sheets')[0]['properties']['title'], service

def get_api_data():
    response = requests.get('http://localhost:5000/api/posts')  # Requisição para a API fictícia
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter dados da API: {response.status_code}")
        return []

def update_sheet(sheets_service, sheet_title, data):
    values = [["ID", "Campanha", "Tipo", "Custo", "Cliques", "Conversoes"]]
    for post in data:
        values.append([post['id'], post['campanha'], post['tipo'],  post['custo'], post['cliques'], post['conversoes']])
    
    body = {
        'values': values
    }
    result = sheets_service.spreadsheets().values().update(
        spreadsheetId='1_AeJMJq6EFAzq9N6F4IaQ1GdqVNlamYYTJYC7yIZvFw',
        range=f'{sheet_title}!A1',  # Começa a escrever da célula A1
        valueInputOption='RAW',
        body=body
    ).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def main():
    try:
        sheet_title, service = get_google_sheet()
        api_data = get_api_data()
        if api_data:
            update_sheet(service, sheet_title, api_data)
            print("Dados da API atualizados na planilha com sucesso!")
        else:
            print("Não foram encontrados dados na API.")

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()
