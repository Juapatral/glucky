# Prueba técnica Data Engineer

El repositorio consiste en la solución entregada para los puntos de Información Base y Segmentación

## Información Base

1. Se envían los archivos comprimidos a un bucket en Google Storage, realizado en Python. Nota: no se carga el archivo de credenciales al GitHub por temas de seguridad.
2. Utilizando la API de Dataflow se descomprimen los archivos, realizado en la consola de Google Cloud.
3. Utilizando las funciones de los buckets, se agrega la información descomprimida en un solo archivo, realizado en Python.
4. Utilizando la API de SQL Admin, se cargan los datos a una tabla de MySQL, realizado en la consola de Google Cloud.
5. Utilizando SQL, se crean las tablas neccesarias y se inserta la información, realizado en la consola de Google Cloud.

## Segmentación
1. Se carga la información *DATA ENGINEER BASE DE DATOS 2 CASO (1).xlsx*, utilizando Python.
2. Se realiza análisis descriptivo inicial y se guarda en imágenes.
3. Se realiza análisis de segmentación utilizando *k-medias*.
4. Se crea informe *punto3_segmentacion_pdf.pdf*

Cualquier duda o comentario pueden contactarme al correo:
juanptrujilloalviz@gmail.com
