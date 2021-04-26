# -*- coding: utf-8 -*-
print(
"""
#-------------------------------------------------------------------------
# Author: Juan Pablo Trujillo Alviz 
# github: juapatral
# CD: 2021-04-24 
# LUD: 2021-04-24 
# Description: carga de datos a google storage
#
# v1
# Modification:
# Description:
#-------------------------------------------------------------------------
"""
)



# carga de librerias
from google.cloud import storage
import glob
#import gzip
#import shutil

# leer archivos
files = glob.glob("./Informacion Base/*.gz")

# # descomprimir archivos
# with gzip.open('file.txt.gz', 'rb') as f_in:
#     with open('file.txt', 'wb') as f_out:
#         shutil.copyfileobj(f_in, f_out)

# establecer credenciales
client = storage.Client.from_service_account_json(
    json_credentials_path='jp-credentials.json'
)

# elegir el bucket
bucket = client.get_bucket('glucky_parte2')

new_files = []
# subir datos
for file in files:

    # nombre en bucket
    new_file = file[2:].replace("\\","/").replace(" ", "_")
    new_files.append(new_file)

    # cargar archivo
    object_name_in_gcs_bucket = bucket.blob(new_file)

    # cargar archivo
    object_name_in_gcs_bucket.upload_from_filename(file)

# descomprimir en nube

command_unzip = """
gcloud dataflow jobs run unzip \
--gcs-location gs://dataflow-templates-us-east1/latest/Bulk_Decompress_GCS_Files \
--region us-east1 \
--num-workers 1 \
--staging-location gs://glucky_parte2/temp \
--parameters inputFilePattern=gs://glucky_parte2/Informacion_Base/*.gz,outputDirectory=gs://glucky_parte2/descomprimido/,outputFailureFile=gs://glucky_parte2/decomperror.txt
"""


# concatenar

def compose_file(client, bucket_name, list_of_blobs, destination_blob_name):
    """Concatenate source blobs into destination blob."""
    # bucket_name = "your-bucket-name"
    # first_blob_name = "first-object-name"
    # second_blob_name = "second-blob-name"
    # destination_blob_name = "destination-object-name"

    storage_client = client
    bucket = storage_client.bucket(bucket_name)
    destination = bucket.blob(destination_blob_name)
    destination.content_type = "text/plain"

    # sources is a list of Blob instances, up to the max of 32 instances per request
    sources = [bucket.get_blob(blob) for blob in list_of_blobs]
    destination.compose(sources)

    print(
        "New composite object {} in the bucket {} was created by combining".format(
            destination_blob_name, bucket_name,
        )
    )
    return destination

part1 = [file.replace("Informacion_Base","descomprimido").replace(".gz","") for file in new_files if file.rfind("20201211")!=-1]
part2 = [file.replace("Informacion_Base","descomprimido").replace(".gz","") for file in new_files if file.rfind("20201212")!=-1]

names = ["notificacion_clicked_part1.csv", "notificacion_clicked_part2.csv"]

compose_file(client, "glucky_parte2", part1, names[0])
compose_file(client, "glucky_parte2", part2, names[1])
compose_file(client, "glucky_parte2", names, "notificacion_clicked.csv")

