from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io
# If modifying these scopes, delete the file token.pickle.

SCOPES = ['https://www.googleapis.com/auth/drive']
#mimetype dict
PickleFile=r'D:\Python\All_Practice\GoogleAPI\apitesla_token.pickle'
mimetype_dict={'xls': 'application/vnd.ms-excel', 'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'xml': 'text/xml', 'ods': 'application/vnd.oasis.opendocument.spreadsheet', 'csv': 'text/csv', 'tmpl': 'text/plain', 'pdf': 'application/pdf', 'php': 'application/x-httpd-php', 'jpg': 'image/jpeg', 'png': 'image/png', 'gif': 'image/gif', 'bmp': 'image/bmp', 'txt': 'text/plain', 'doc': 'application/msword', 'js': 'text/js', 'swf': 'application/x-shockwave-flash', 'mp3': 'audio/mpeg', 'zip': 'application/zip', 'rar': 'application/rar', 'tar': 'application/tar', 'arj': 'application/arj', 'cab': 'application/cab', 'html': 'text/html', 'htm': 'text/html', 'default': 'application/octet-stream', 'folder': 'application/vnd.google-apps.folder', '': 'application/vnd.google-apps.video', 'Google Docs': 'application/vnd.google-apps.document', '3rd party shortcut': 'application/vnd.google-apps.drive-sdk', 'Google Drawing': 'application/vnd.google-apps.drawing', 'Google Drive file': 'application/vnd.google-apps.file', 'Google Drive folder': 'application/vnd.google-apps.folder', 'Google Forms': 'application/vnd.google-apps.form', 'Google Fusion Tables': 'application/vnd.google-apps.fusiontable', 'Google Slides': 'application/vnd.google-apps.presentation', 'Google Apps Scripts': 'application/vnd.google-apps.script', 'Shortcut': 'application/vnd.google-apps.shortcut', 'Google Sites': 'application/vnd.google-apps.site', 'Google Sheets': 'application/vnd.google-apps.spreadsheet'}

def main():
    
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(PickleFile):
        with open(PickleFile, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8012)
        # Save the credentials for the next run
        with open(PickleFile, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    

    # Call the Drive v3 API#
   
    
    return service
service=main()
def get_minitype_txt_todict(f=r'mimetype.txt'):# get mimetype dict from  txt
    dict_mime={}
    with open(f,'r') as ff:
        for i in ff:
                if'=>' in str(i):
                        aa,bb=i.split('=>')
                        aa=aa.replace('"','').strip()
                        bb=bb.replace("'",'').replace(",",'').strip()
                        dict_mime[aa]=bb

                else:
                        aa,bb=i.split(',')
                        aa=aa.replace('"','').strip()
                        bb=bb.replace("'",'').replace(",",'').strip()
                        dict_mime[bb]=aa
    return dict_mime
def get_dict(dict_form):
    
    newdict={}
    # dict_form={'a':'b'} , this fun will return a dict
    split1=dict_form.split(',')
    for i in split1:
            a,b=i.split(':')
            a=a.replace('{','').replace("'",'')
            b=b.replace('{','').replace("'",'')
            newdict[a]=b
    return newdict
    

def find_folder():
            results = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=None).execute()

def find_file(filename):
      
      results = service.files().list(     pageSize=1000,
                                          fields='files(id, name)',
                                          pageToken=None).execute()
      
      
      items = results.get('files', [])
      
      
      if not items:return 0
      
      for item in items:
             id_=item['id']
             name_=item['name']
             
             if filename==name_:
            
                 return id_
    #if find nothing
      for item in items:
             id_=item['id']
             name_=item['name']
             catchname=re.findall(filename,name_,re.IGNORECASE)
             if catchname:
                
                 return id_
      return 0
def download(file,dst):
    fileid=find_file(file)
    
    if fileid:
        
        filedict=service.files().get(fileId=fileid).execute()
        name_=filedict['name']
        mimeType_=filedict['mimeType']
        print("Download " +name_ )
        if 'application/vnd.google-apps' in str(mimeType_):
            if 'spreadsheet' in str(mimeType_):
                mimeType_='text/csv'
                name_=name_+'.csv'
            elif 'document'in str(mimeType_):
                mimeType_='application/msword'
                name_=name_+'.csv'
       
            request = service.files().export_media(fileId=fileid,mimeType=mimeType_)
        else:
            request = service.files().get_media(fileId=fileid)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        
        done = 0
        while not done :
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        
        filepath=dst+'\\'+name_
        with io.open(filepath,'wb') as f:
            fh.seek(0)
            f.write(fh.read())
def change_permissions():# 將某ID的檔案權限更改
    service.permissions().create(fileId='1wgobAC45IMM-TUE58fO1P8D8_FURMXyLjRXzPaKI_pQ',
                                         body= {
                                        'role': 'writer',
                                        'type': 'anyone',
                                          }
                                        ).execute()
def create_newsheet(filename):
    
    file_metadata = {
    'name': filename,
    'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
   
    file = service.files().create(body=file_metadata).execute()
def upload(filename,file_type):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filename, mimetype=file_type)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
def find_folder_id(foldername):
      results = service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=None).execute()
      items = results.get('files', [])
      if not items:return 0
      
      for item in items:
             id_=item['id']
             name_=item['name']
             
             if foldername==name_:
                 #folderID=id_
                 return id_
      return 0
def upload_file(filepath,dstpath):# 上傳檔案到特地資料夾
    
    if os.path.isdir(filepath):
        foldername=os.path.basename(filepath)
        
        eachfoldername=os.path.dirname(dstpath)
        folderID=find_folder_id(eachfoldername)
        file_metadata = {
        'name': foldername,
        'parents' : [folderID],
        'mimeType': 'application/vnd.google-apps.folder'
        }
       
        file = service.files().create(body=file_metadata).execute()
        
        for i in os.listdir(filepath):
            eachnewpath=filepath+'/'+i
            
            if foldername:# 代表有指定資料夾
                dstpath=foldername+'/'+i
                print(dstpath)
               
            upload_file(eachnewpath,dstpath)
        return
    foldername=os.path.dirname(dstpath)
    filename=os.path.basename(dstpath)
    if '.' in str(os.path.splitext(filename)[-1]):
        Extension=os.path.splitext(filename)[-1].replace('.','')
        if Extension in mimetype_dict:
            file_type=mimetype_dict[Extension]
    else:
        print("Mimetype not found , try to upload to this folder")
        foldername=os.path.basename(dstpath)
        filename=os.path.basename(filepath)
        Extension=os.path.splitext(filename)[-1].replace('.','')
        
        if Extension in mimetype_dict:
            
            file_type=mimetype_dict[Extension]
        else:return
        

    
    
    
   
    if foldername:
      folderID=0
      folderID=find_folder_id(foldername)
      
      
      if  not folderID:return
      file_metadata = {
        'name': filename,
        'parents': [folderID]
        }       
    else:
      file_metadata = { 'name': filename}          
    
    
    media = MediaFileUpload(filepath,
                            mimetype=file_type,
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    print("Finish !")
def delete_file(filename):
  file_id=find_file(filename)
  """Permanently delete a file, skipping the trash

  Args:
    service: Drive API service instance.
    file_id: ID of the file to delete.
  """
  try:
        service.files().delete(fileId=file_id).execute()
  except :
      print("Delete Error")
    


if __name__ == '__main__':
     service = main()

   # = Upload =
   
    # src=r'D:\Python\All_Practice\GoogleAPI\test/test.txt'
    # dst='test.txt'
    
    # upload_file(src,dst)# src /to dst (若沒給會自動偵測)//資料夾ID
    
   # = download =
   
     #file_='....txt'
     #dst=r'D:\Python\All_Practice\GoogleAPI\test'
     # download(file_,dst)
     
   # = delete =
     #delete_file(filename)
   
   # = create sheet =
   
    # create_newsheet("HI信登")
     
  
     
  
