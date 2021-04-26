# -*- coding: utf-8 -*-
print(
"""
#-------------------------------------------------------------------------
# Author: Juan Pablo Trujillo Alviz 
# github: juapatral
# CD: 2021-04-24 
# LUD: 2021-04-24 
# Description: segmentacion de conjunto de datos
#
# v1
# Modification:
# Description:
#-------------------------------------------------------------------------
"""
)

# carga modulos
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# preprocesamiento de datos
# leer datos
data = pd.read_excel("./DATA ENGINEER BASE DE DATOS 2 CASO (1).xlsx")

# descriptivo general
data.info()

# limpiar titulos
new_cols = []
for col in [*data.columns]:
    new_cols.append(
        col
        .lower()
        .replace(" ", "_")
        .replace("á","a")
        .replace("é","e")
        .replace("í","i")
        .replace("ó","o")
        .replace("ú","u")
    )

data.columns = new_cols

# inicio del EDA

# ver distribucion de las compras
compras = sns.violinplot(data=data["compras_acumuladas"])
compras.set(
        ylabel="Valor compras", title="Distribucion de las compras"
    )
compras.figure.savefig("imagenes/compras_acumuladas.png")
plt.close()
del compras

# ver distribucion de las compras
compras_log = sns.violinplot(data=np.log(data["compras_acumuladas"]+1))
compras_log.set(
        ylabel="log(Valor compras)", 
        title="Distribucion del logaritmo de las compras"
    )
compras_log.figure.savefig("imagenes/compras_acumuladas_log.png")
plt.close()
del compras_log


# variables categoricas
cat_vars = [
    'meses_cumpliendo_ventas', 'estado_civil', 'sexo', 'ubicacion_geografica'
]

# mirar unicos
for col in cat_vars:
    data_gr = data[col].value_counts().sort_values(ascending=False) 
    pie, ax = plt.subplots(figsize=[10,6])
    plt.pie(data_gr, autopct="%.1f%%", labels=data_gr.index, startangle=90)
    plt.title(col, fontsize=14)
    pie.savefig("imagenes/{}.png".format(col))
    plt.close()
    del pie, ax

# hacer las mismas graficas por valores compra
for col in cat_vars:
    data_gr = data.groupby(col).sum()["compras_acumuladas"].sort_values(ascending=False)
    pie, ax = plt.subplots(figsize=[10,6])
    plt.pie(data_gr, autopct="%.1f%%", labels=data_gr.index, startangle=90)
    plt.title(col+" por compras", fontsize=14)
    pie.savefig("imagenes/{}_compras.png".format(col))
    plt.close()
    del pie, ax

# hacer las mismas graficas por log valores compra
data2 = data.copy()
data2["log_compras"] = np.log(data2["compras_acumuladas"]+1)

for col in cat_vars:
    compras_col = sns.violinplot(x=col, y="log_compras", data=data2)
    compras_col.set(
        ylabel="log(Valor compras)", 
        title="Distribucion del logaritmo de las compras"
    )
    compras_col.figure.savefig("imagenes/{}_compras_log.png".format(col))
    plt.close()
    del compras_col


## preparar archivo para procesamiento

data_prep = data2.copy()

for col in cat_vars:
    dummies = pd.get_dummies(data[col], prefix = col)
    data_prep = pd.concat([data_prep, dummies], axis = 1)
    data_prep.drop(col, axis = 1, inplace = True)

# estandarizar variables
data_prep.drop("id", axis = 1, inplace = True)
data_prep.drop("compras_acumuladas", axis = 1, inplace = True)
mms = MinMaxScaler()
mms.fit(data_prep)
data_transformed = mms.transform(data_prep)           

## elegir k con el metodo del codo

# metodo codo
Sum_of_squared_distances = []
K = range(1,20)
for k in K:
    km = KMeans(n_clusters=k)
    km = km.fit(data_transformed)
    Sum_of_squared_distances.append(km.inertia_)

# graficar
plt.plot(K, Sum_of_squared_distances, 'bx-')
plt.xlabel('k')
plt.ylabel('Suma de las distancias al cuadrado')
plt.title('Método del codo para el K óptimo')
plt.savefig("imagenes/metodo_codo.png".format(col))
plt.close()

## Crea el clasificador con 6 grupos

# crear clasificador
m = KMeans(n_clusters = 6)

# ajustar clasificador
m.fit(data_transformed)

# pronosticar clasificador
p = m.predict(data_transformed)

# agregar clasificador a la cartera
data2['cluster'] = p

# cabecera de la cartera
data2.head()

# utilizar arbol para identificar variables importantes

# arbol de clasificacion
arbol = DecisionTreeClassifier(random_state = 18)

# ajustar arbol
arbol.fit(data_transformed, p)

# crear variables de importancia
peso = arbol.feature_importances_
dic = {'importancia': peso, 'variable': data_prep.columns}
wr = pd.DataFrame(dic, columns = ['variable', 'importancia'])
wir = wr.sort_values(by = 'importancia', ascending = False) 

# ver precisieon del arbol
arbol.score(data_transformed, p)

# hacer las mismas graficas por valores compra
compras_col = sns.violinplot(x="cluster", y="log_compras", data=data2)
compras_col.set(
    ylabel="log(Valor compras)", 
    title="Distribucion del logaritmo de las compras"
)
compras_col.figure.savefig("imagenes/cluster_compras_log.png")
plt.close()
del compras_col


# importantes
imp_vars = ['estado_civil', 'sexo', 'ubicacion_geografica']

for col in imp_vars:
    data_gr = data2.groupby(["cluster", col])[col].count().unstack().fillna(0).T
    data_gr.plot.pie(subplots = True, figsize = (15,15), autopct='%1.1f%%', legend=False)
    plt.savefig("imagenes/cluster_{}.png".format(col))
    plt.close()
    del data_gr

