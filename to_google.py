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
        row = [
            item.get("my_url", ""),
            item.get("competitor_url", ""),
            item.get("title", ""),
            item.get("description", ""),
            item.get("keywords", ""),
            item.get("html", "")
        ]
        sheet.append_row(row, value_input_option="RAW")

