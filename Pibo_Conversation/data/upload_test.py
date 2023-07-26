# upload_file2.py
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build, MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# 권한 인증 및 토큰 확인
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/drive.metadata']
creds = None

# 이미 발급받은 Token이 있을 때
if os.path.exists('token.pickle'):
   with open('token.pickle', 'rb') as token:
       creds = pickle.load(token)

# 최초 1회 실행
# 발급받은 토큰이 없거나 AccessToken이 만료되었을 때
if not creds or not creds.valid:
   if creds and creds.expired and creds.refresh_token:
       creds.refresh(Request())
   else:
       flow = InstalledAppFlow.from_client_secrets_file('/home/pi/client_secret_451979961046-m9ams7bffqtgko7m2jmb8e1aa3d5f1u8.apps.googleusercontent.com.json', SCOPES)
       creds = flow.run_local_server(port=0)
   # 현재 토큰 정보를 저장
   with open('token.pickle', 'wb') as token:
       pickle.dump(creds, token)

def drive_upload(filepath, filename):
   
   # 연결 인스턴스 생성
   service = build('drive', 'v3', credentials=creds)

   # 특정 폴더에 업로드 예제
   request_body = {
      'name': filename, # 파일 명 정보
      'parents': ['1Il6CBNjmH9u-ldCyVG1WEteFbW--aItR'] # 부모가 될 폴더의 ID. 즉 업로드할 폴더 위치
   }
   media = MediaFileUpload(f'{filepath}/{filename}',resumable=True)
   file = service.files().create(body=request_body,media_body=media,fields='id').execute()

   print("Upload Success, File ID:",file.get('id'))