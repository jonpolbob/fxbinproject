from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

filecsv = drive.CreateFile()
print("create")





#pour ranger le fichier dans un dossier du drive, il faut
#recuperer un ID du parent et modifier le createfile
fid = ""

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print 'title: %s, id: %s' % (file1['title'], file1['id'])
    if file1['title'] == 'data':
        fid = file1['id']
#    sys.exit()

f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": fid}]})

# ci dessous : le fichier part dans la racine du drive
filecsv.SetContentFile("c:\\tmp\\DAT_NT_USDCHF_T_BID_201603.csv")
print("setcontent")



filecsv.Upload();

print("upload")

#files = drive.ListFile()

#for x in files:
#    print(x)
