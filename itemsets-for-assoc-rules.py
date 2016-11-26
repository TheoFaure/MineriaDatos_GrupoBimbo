#java -Xmx6144m -jar weka.jar


import pandas as pd

#Loading csv with Pandas
filepath = "C:/Users/eleonguz/Documents/"
in_file = filepath + "sample.csv"
bimbo = pd.read_csv(in_file)

#Setting appropiate column data types
bimbo[['Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID']] = bimbo[['Semana','Agencia_ID','Canal_ID','Ruta_SAK','Cliente_ID','Producto_ID']].astype('str')

#Dropping uninteresting columns
bimbo = bimbo[['Semana','Agencia_ID','Cliente_ID','Producto_ID']]



#Group products by Cliente_ID and Semana        853894 >> 124649 >> 124649x1144
indexsets = bimbo.groupby(['Cliente_ID','Semana']).indices.values()

#Group products by Cliente_ID		458428 >> 248435 >> 248435x1287
indexsets = bimbo.groupby(['Cliente_ID']).indices.values()

#Group products by Agencia_ID 		551 >> 550 >> 550x1337
indexsets = bimbo.groupby(['Agencia_ID']).indices.values()



#Convert groups of row index to groups of Producto_ID's
def indexset_to_itemset(indexset):
	itemset = ' '.join(bimbo['Producto_ID'][indexset].tolist())
	return itemset

itemsets = [indexset_to_itemset(indexset) for indexset in indexsets if len(indexset) > 1]

#Procucto_ID frequency matrix
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
texts = itemsets
vectorizer = CountVectorizer(binary=True)
sparse_matrix = pd.DataFrame(vectorizer.fit_transform(texts).toarray(), columns=vectorizer.get_feature_names())

#Write binary matrix to csv
out_file = filepaht + "producto_by_agencia_matrix.csv"
sparse_matrix.to_csv(out_file)
