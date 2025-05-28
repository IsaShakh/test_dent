import gspread
from oauth2client.service_account import ServiceAccountCredentials

def upload_to_google_sheets(data_list, creds_path, spreadsheet_name):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).sheet1

    for item in data_list:
        sheet.append_row([
            item['url'],
            item['title'],
            item['description'],
            item['keywords'],
            item['html']
        ], value_input_option="RAW")

    print(f"succes: {spreadsheet_name}")
