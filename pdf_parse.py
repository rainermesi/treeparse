# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 17:22:33 2019

@author: Rainer
"""

import PyPDF2 as ppdf
import os
import pandas as pd
import geocoder

# create list to store parse results

pdflist = []

# create a loop to iterate through all pdf files in a directory, extract text from each file, write result to a list

for filename in os.listdir('file_folder'):
    pdflist.append(ppdf.PdfFileReader(filename).getPage(0).extractText())

# transform list into dataframe

pdfdf = pd.DataFrame(pdflist)

# backup dataframe to csv

pdfdf.to_csv('pdfdf.csv')

# extract columns from dataframe

pdfdf['raieluba'] = pdfdf[0].str.extract('((?<=Raieluba nr: )[0-9]*)',expand = True)

pdfdf['kuupaev'] = pdfdf[0].str.extract('((?<=Avalduse esitamise kuupäev: )[0-9]*.[0-9]*.[0-9]*)',expand = True)

pdfdf['aadress'] = pdfdf[0].str.extract('((?<=Raie toimumise aadress:).*(?=Raie põhjus:))',expand = True)

pdfdf['puid'] = pdfdf[0].str.extract('((?<=KOKKU: ).*?(?= Puu))',expand = True)

# clean extracted columns for messy strings, create a copy of df

pdfdf2 = pdfdf

pdfdf2['aadress'] = pdfdf2['aadress']+', TALLINN, ESTONIA'

pdfdf2['aadress_2'] = pdfdf2['aadress'].str.replace('(\(.*\))', '')

pdfdf2['aadress_2'] = pdfdf2['aadress_2'].str.replace(' ,', ',')

pdfdf2['aadress_2'] = pdfdf2['aadress_2'].str.replace('((\/\/.*,))', ', TALLINN,')

pdfdf2['aadress_2'] = pdfdf2['aadress_2'].str.replace('((\/.*,))', ', TALLINN,')

pdfdf2['aadress_2'] = pdfdf2['aadress_2'].str.replace('(( JA.*?,))', ',')


# store Bing maps api key

mykey = 'my_key'

# create a dicionary to store latitude, longitude data

cdict = {
        'aadress': [],
        'lat': [],
        'lon': []
        }

# call Bing maps api and request lat, lon coordinates from addre
    
for i in pdfdf2['aadress_2']:
    cdict['aadress'].append(i)
    cdict['lat'].append(geocoder.bing(i, key = mykey).latlng[0])
    cdict['lon'].append(geocoder.bing(i, key = mykey).latlng[1])    

# convert results to dataframe

cdf = pd.DataFrame(cdict)

# combine lat and lon coordinates to 1 string

cdf['latlon_4'] = cdf['lat'].map(str) + ', ' + cdf['lon'].map(str)

# create new dictionary to store postal code

postdict = {
        'indeks': [],
        'postikood': []
        }

# create a loop to request post code from maps api

for i in cdf['latlon_4']:
    postdict['indeks'].append(i)
    postdict['postikood'].append(geocoder.bing(i, key = mykey, method = 'reverse').postal)
    
# convert results to dataframe
    
postdf = pd.DataFrame(postdict)

# join separate result dataframes

postmerge = pd.merge(
        cdf,
        postdf,
        left_on = 'latlon_4',
        right_on = 'indeks',
        how = 'left'
        )

resultdf = pd.merge(
        pdfdf2,
        postmerge,
        left_on = 'aadress_2',
        right_on = 'aadress',
        how = 'left'
        )

# select subset from joined dataframe, save to csv

finaldf = resultdf[['raieluba','puid','kuupaev','aadress_2_x','lat','lon','postikood']]

finaldf.to_csv('treeparse.csv')
