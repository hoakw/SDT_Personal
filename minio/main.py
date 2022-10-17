from minio import Minio

minioClient = Minio("192.168.1.207:30333",
                    access_key='sdt',
                    secret_key='sdt251327',
                    secure=False)

## put
#minioClient.fput_object('sujune', 'main.py', './main.py')

## get
#minioClient.fget_object('sujune', 'zzio.png', 'zzio.png')

## get list
ob_data = minioClient.list_objects('sujune', prefix="/")

for obj in ob_data:
    print(obj.bucket_name) # string type
    print(obj.object_name) # string type
    print(obj.last_modified)  # datetime type
    print(obj.size) # int type