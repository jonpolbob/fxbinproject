from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


#penser a couper skype !
#sinon port 8080 est bloqué

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)



#pour ranger le fichier dans un dossier du drive, il faut
#recuperer un ID du parent et modifier le createfile
fid = ""

file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print ('title: %s, id: %s' % (file1['title'], file1['id']))
    if file1['title']== 'data':
        fid = file1['id']
        print ("found : ",fid)
#    sys.exit()


#les bon arguments pour indiquer le id d'un sous repertoire ou ecrire
# et changer le titre dans le drive
filecsv = drive.CreateFile({"title":"moncsdetest" , "parents": [{"kind": "drive#fileLink","id": fid}]})

print("create ok")

# ci dessous : le fichier part dans la racine du drive
filecsv.SetContentFile("c:\\tmp\\form1.cs")
print("setcontent")



filecsv.Upload();

print("upload")

print ('Created file %s with mimeType %s' % (filecsv['title'], filecsv['mimeType']))

#files = drive.ListFile()

#for x in files:
#    print(x)
