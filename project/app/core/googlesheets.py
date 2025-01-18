import gspread
from app.core import config
gc = gspread.service_account(filename=config.settings.GOOGLE_CREDENTIALS_FILE)

sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/14Qt5RuRDvJBVqYt7ZQmvqO16-WvNKABX0lntmJmgi5s/edit?gid=0#gid=0")
work_sheet = sheet.get_worksheet_by_id(1955084310)