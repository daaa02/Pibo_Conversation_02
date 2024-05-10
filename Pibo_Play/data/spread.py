from datetime import datetime
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = {
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
}

json_file='/home/pi/stt-test-000-0226dec785df.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
gc = gspread.authorize(credentials)
url = "https://docs.google.com/spreadsheets/d/1mtetNRxVyOGZB9y1FL1OM1x3Ob7APSPXWiPkjqx_eTs/edit#gid=353058849"

today = datetime.now().strftime('%Y-%m-%d %H:%M')
with open('/home/pi/name_config.json', 'r') as f:
    config = json.load(f)        
    user_name = config['user_name'] 


class google_spread_sheet():
    
    def make_sheet(self):
        ms = gc.create(f'{user_name}')    # file name
        worksheet = ms.get_worksheet(0)     # 첫 번째 시트
        worksheet.append_row(['이름', '날짜', '활동'])
        worksheet.resize(500, 10)
        ms.share('dyk98498@gmail.com', perm_type='user', role='writer')     
    
    def write_sheet(self, name, today, activities):
        # # 새로 만든 시트에 쓰기
        # ws = gc.open(f'{user_name}')
        # worksheet = ws.get_worksheet(0)
        
        # 만들어졌던 시트에 쓰기
        os = gc.open_by_url(url)
        # worksheet = os.get_worksheet(5)
        worksheet = os.worksheet('활동상황')
        
        str_list = list(filter(None, worksheet.col_values(1)))
        next = len(str_list)+1
        worksheet.update(f'A{next}', name)
        worksheet.update(f'B{next}', today)
        worksheet.update(f'C{next}', activities)
        # worksheet.append_row(activities, table_range=f'C{next}')

    def save_sheet(self):
        ss = gc.open(f'{user_name}')
        worksheet = ss.get_worksheet(0)
        ss.share('dyk98498@gmail.com', perm_type='user', role='writer')