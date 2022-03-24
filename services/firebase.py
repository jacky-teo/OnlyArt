from firebase_admin import storage
PROJECT_ID = 'onlyfence-9eb40'
IS_EXTERNAL_PLATFORM = True
firebase_app = None

def init_firebase():
    global firebase_app
    if firebase_app:
        return firebase_app

    import firebase_admin
    from firebase_admin import credentials
    if IS_EXTERNAL_PLATFORM:
        cred = credentials.Certificate('keys/firebase-adminsdk.json')
    else:
        cred = credentials.ApplicationDefault()

    firebase_app = firebase_admin.initialize_app(cred, {
        # 'projectId': PROJECT_ID,
        'storageBucket': f"{PROJECT_ID}.appspot.com"
    })
    return firebase_app

init_firebase()

def upload_firebase(file,creatorID,description):
    bucket = storage.bucket() ## Get the storage in firebase
    blobs = list(bucket.list_blobs(prefix=f'{creatorID}/')) #Point to creator's directory
    urls = [] #Create a place to store all the URLS
    url_links =[]# Append all the links in blobs to URL except parent file

    # Append all the files in blobs to URL except parent file
    for item in blobs[1:]: 
        item.make_public() #Get a session url that is public
        urls.append(item.public_url) #Get a session url that is public
        url_links.append(item.path) #Get the url pathing

    lastImgID = None  #Declared to use image naming
    for url in url_links: 
        url = url.lower() 
        id = url.split("f")[2] #Declared split the path by f
        lastImgID =id  #Assign image ID
    
    if lastImgID != None: #If its not none,

    # ['img1.png', 'img3.png']
        lastImgID = lastImgID.replace('img','')
        lastImgID = lastImgID.replace('.png','')
        imageID = 'img'+ str(int(lastImgID)+1)## Create the Image ID based on the number of files inside the storage under creatorID
    else:
        imageID = 'img1'

    postID = f'{creatorID}_{imageID}' #Create a post id
    fileEXT = file.mimetype.split('/')[1]

    path_on_cloud = f'{creatorID}/{imageID}.{fileEXT}' ##Declare the path to upload
    blob = bucket.blob(path_on_cloud) #Point to the path and the file name

    blob.upload_from_file(file,content_type = file.mimetype)  #Upload the file into the storate
    data = {
        'POSTID':postID,
        'CREATORID':creatorID,
        'DESCRIPTION':description,
        'IMAGE_ID':imageID,
        'IMG_EXT':fileEXT,
        'POST_DATE':None,
        'modified':None,
    } #Create a data to transfer as json
    #Convert to JSON
    return data