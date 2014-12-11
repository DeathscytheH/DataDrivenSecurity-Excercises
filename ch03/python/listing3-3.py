# URL for the AlienVault IP Reputation Database (OSSIM format)
# storing the URL in a variable makes it easier to modify later
# if it changes. NOTE: we are using a specific version of the data 
# in these examples, so we are pulling it from an alternate
# book-specific location.
import urllib
import os.path

avURL = "http://datadrivensecurity.info/book/ch03/data/reputation.data"

# relative path for the downloaded data
avRep = "data/reputation.data"

# using an if-wrapped test with urllib.urlretrieve() vs direct read 
# via panads avoids having to re-download a 16MB file every time we 
# run the script
if not os.path.isfile(avRep):
      urllib.urlretrieve(avURL, filename=avRep)
      
# first time using the pandas library so we need to import it
import pandas as pd
import sys

# read in the data into a pandas data frame
av = pd.read_csv(avRep,sep="#")

# make smarter column names
av.columns = ["IP","Reliability","Risk","Type","Country", "Locale","Coords","x"]
print(av) # take a quick look at the data structure

# take a look at the first 10 rows
print av.head().to_csv(sys.stdout)


# require object: av (3-5)
# See corresponding output in Figure 3-1
# import the capability to display Python objects as formatted HTML 
from IPython.display import HTML
# display the first 10 lines of the dataframe as formatted HTML 
print 
HTML(av.head(10).to_html())

"""
Reliability, Risk, x son int
IP, Type, Country, Locale, and Coords son string
IP => Dotted quad notation
Cada linea es una ip unica
Cada ip esta geolocalizada pero vienen en un solo campo separado por comas.

"""
#Listing - 3-8
#Obtener el min, max, promedio y quartiles.

print 'Reliability'
print av['Reliability'].describe()
print '\n'
print 'Risk'
print av['Risk'].describe()

#Listing - 3-10
#factor_col(col)
#Funcion similiar a summary de R, para las columnas de pandas.

def factor_col(col):
    factor = pd.Categorical.from_array(col)
    return pd.value_counts(factor, sort=True).reindex(factor.levels)

#Acomodo por 
rel_ct = pd.value_counts(av['Reliability'])
#Acomodo por riesgo
risk_ct = pd.value_counts(av['Risk'])
#Acomodo por tipo de malware
type_ct = pd.value_counts(av['Type'])
#Acomodo por pais
country_ct = pd.value_counts(av['Country'])

print 'Reliability'
print factor_col(av['Reliability'])
print '\n'
print 'Risk'
print factor_col(av['Risk'])
print '\n'
print 'Type'
print factor_col(av['Type']).head(n=15)
print '\n'
print 'Country'
print factor_col(av['Country']).head(n=15)

#Listing 3-14

#Graficas, porque los numeros no son para personas comunes.

import matplotlib.pyplot as plt

#Quitar comentarios o meterlos en el interprete
"""
plt.axes(frameon=0)
country_ct[:20].plot(kind='bar', rot=0, title="Resumen por Pais", figsize=(8,5)).grid(False)

plt.axes(frameon=0)
factor_col(av['Reliability']).plot(kind='bar', rot=0, title="Resumen por Reliabilidad", figsize=(8,5)).grid(False)

plt.axes(frameon=0)
factor_col(av['Risk']).plot(kind='bar', rot=0, title="Resumen por Riesgo", figsize=(8,5)).grid(False)
"""
#Listing 3-18

#Top 10 de paises
top10 = pd.value_counts(av['Country'])[0:9]

#Calcular el porcentaje de participacion de cada pais
#Meterlo en el interprete si no no sale.
top10.astype(float) / len(av['Country'])

#Listing 3-20

#Haciendo un mapa de calor
#Calcular una tabla de contingencia para las variables de riesgo y reliabilidad

from matplotlib import cm
from numpy import arange

print '\n'
print 'Tabla Riesgo vs Reliabilidad'
print '\n'
print pd.crosstab(av['Risk'], av['Reliability'])
print '\n'

#Grafica de nuestra tabla de contingencia como heatmap
"""
xtab = pd.crosstab(av['Risk'], av['Reliability'])
plt.pcolor(xtab, cmap=cm.Greens)
plt.yticks(arange(0.5, len(xtab.index),1),xtab.index)
plt.xticks(arange(0.5, len(xtab.columns),1),xtab.columns)
plt.colorbar()
"""

#Listing 3-23
#calcular la tabla de contingencia incluyendo los tipos

#Crea una nueva columna como copia del tipo
av['newtype']=av['Type']

#Cambiar las entradas con varios registro a una nueva columna
av[av['newtype'].str.contains(';')]='Multiples'

#Actualizamos las nuevas estructuras
typ = av['newtype']
rel=av['Reliability']
rsk=av['Risk']

#Calcular la crosstab haciendo un split en la columna de newtype
xtab = pd.crosstab(typ, [rel, rsk], rownames=['typ'], colnames=['rel', 'rsk'])

#Representacion en texto de la tabla de contingencia
#print xtab.to_string()

#Graficacion
#xtab.plot(kind='bar', legend=False, title='Riesgo ~ Reliabilidad | Tipo').grid(False)

"""
Se vio que casi todo esta cargado para scaning host de bajo riesgo.
Se va a depreciar para tener un mejor ananlisis de los datos.
"""

#Filtrar todos los scaning hosts

rrt_df = av[av['newtype'] != 'Scanning Host']
typ = rrt_df['newtype']
rel = rrt_df['Reliability']
rsk = rrt_df['Risk']

xtab = pd.crosstab(typ, [rel, rsk], rownames=['typ'], colnames=['rel', 'rsk'])
#xtab.plot(kind='bar', legend=False, title='Riesgo ~ Reliabilidad | Tipo').grid(False)

plt.pcolor(xtab, cmap=cm.Greens)
plt.yticks(arange(0.5, len(xtab.index),1),xtab.index)
plt.xticks(arange(0.5, len(xtab.columns),1),xtab.columns)
plt.colorbar()