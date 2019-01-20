# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 16:39:51 2018

@author: Overlord
"""

from bs4 import BeautifulSoup
import pandas as pd
import pickle
import urllib
import re
import collections

###
###
'''define functions for grabbing info from sites'''
###
###
def get_speech_links():
    '''
scrape content of pages with all presidential transcript links
'''
    home_url = 'http://www.presidency.ucsb.edu/sou.php'
    try:
        response = urllib.request.urlopen(home_url)
        page_source = response.read()
        soup = BeautifulSoup(page_source, "html5lib")
        transcript_links = soup.findAll("td", {'class': 'ver12'})
        return transcript_links
    except urllib.error.HTTPError:
        print('Homepage not available!')
        return None
        
def get_transcript(url):
    try:
        response= urllib.request.urlopen(url)
        page_source= response.read()
        soup= BeautifulSoup(page_source, 'html5lib')
        speech_text= soup.findAll("span", {'class': 'displaytext'})
        return speech_text
    except urllib.error.HTTPError:
        print('Homepage not available!')
        return None

def get_transcript_date(url):
    try:
        response= urllib.request.urlopen(url)
        page_source= response.read()
        soup= BeautifulSoup(page_source, 'html5lib')
        speech_text= soup.findAll("span", {'class': 'docdate'})
        return speech_text
    except urllib.error.HTTPError:
        print('Homepage not available!')
        return None


transcript_links= get_speech_links()
str_transcript_links= [str(i) for i in transcript_links]

#Fixes problems #problems= str_transcript_links[210, 235, 240]
str_transcript_links[210]= 'http://www.presidency.ucsb.edu/ws/index.php?pid=10593'
str_transcript_links[235]= 'http://www.presidency.ucsb.edu/ws/index.php?pid=16603'
str_transcript_links[240]= 'http://www.presidency.ucsb.edu/ws/index.php?pid=16595'

s= re.compile('http.*pid=[0-9]+')
url_list= []

for i in str_transcript_links:
    if len(re.findall(s,i)) > 0:
        url_list.append(re.findall(s,i))
'''Looking for name: <span class="ver10">Donald J. Trump:'''

transcripts= []

for i in url_list:
    transcript= str(get_transcript(i[0]))
    transcripts.append(transcript)

print(transcripts[0][0:100])

'''Makes a .txt file'''
path= r"C:\\Users\\Overlord\\Desktop\\Py\\SpeechAnalysis\\Speeches\\"
'''T17inaug already exists'''
#T17inaug= open(path+'T17inaug.txt', 'w')
#T17inaug.write(transcripts[0])

###
###
'''BUILD LIST FOR TXT LABELS'''
###
###
'''Finds names and creates names[] list'''
pattern= re.compile(r'span class="ver10">\w*\s?\w*?\.?\s?\w*:', re.UNICODE)
seg_names= [re.findall(pattern,i) for i in transcripts]

'''pulls just the names except for empties'''
#empties are differently formatted html than names
names_nums= [i for i,j in enumerate(seg_names) if len(j) > 0]
names_pattern= re.compile('[A-Z]\w+\s?\w+\.?\s?\w+')
seg_names_names= [seg_names[i] for i in names_nums]
seg_names_names= [i[0] for i in seg_names_names]
names= [re.findall(names_pattern, i) for i in seg_names_names]
names= [i[0] for i in names]
print(names[0])


'''identifies empty list items'''
empties_nums= [i for i,j in enumerate(seg_names) if len(j) == 0]
empties_pat= re.compile(r'([A-Z]+\.?\s+[A-Z]+\.?\s?[A-Z]+)', re.UNICODE)
seg_names_empties= [transcripts[i][(len(transcripts[i])-100):len(transcripts[i])] for i in empties_nums]
names_empties= [re.findall(empties_pat, i) for i in seg_names_empties]
names_empties= [i[0] for i in names_empties]
print(names_empties[0])

'''builds list of initials'''
dic_names= dict(zip(names_nums, names))
dic_names_empties= dict(zip(empties_nums, names_empties))
Dic_names= {**dic_names, **dic_names_empties}
Dic_names= collections.OrderedDict(sorted(Dic_names.items()))
initials= [[j[0] for j in i.split()] for i in Dic_names.values()]
initials= [''.join(i) for i in initials]
print(len(initials), '\t', initials[0],'  ', initials[len(initials)-1])

'''builds list of dates'''
transcripts_dates= [get_transcript_date(i[0]) for i in url_list]
transcripts_dates= [str(i[0]) for i in transcripts_dates]
date_pat= re.compile('(?:January?|February?|March?|April?|May?|June?|July?|August?|September?|October?|November?|December?)\s\d\d?,\s\d+')
dates_list= [re.findall(date_pat, i) for i in transcripts_dates]
dates_list= [str(i)[2:len(i)-3].replace(" ","_").replace(",","") for i in dates_list]
print(dates_list[6:11])

'''builds list of names for the files'''
filenames= [i+"_"+j for i,j in zip(initials,dates_list)]
print(filenames[100:105])


'''Working on something to clean up transcripts'''
pattern= re.compile("<.*?>")
fixed= [re.sub(pattern,"",i) for i in transcripts]


'''create text files in bulk'''
for i in range(0,len(fixed)):
    writefile= open(path+filenames[i]+'.txt','w',encoding="utf-8")
    writefile.write(fixed[i])
    writefile.close()
#Missing 11 speeches
#These appear to be the series of written and radio speeches by RN 1973


#pat_list= ['<p>', '</p>', '<i>', '</i>', '<span class=ver10>', '<strong>', '</strong>', '<hr noshade="noshade"size="1"/>','<span class="displaynotes">', '<span class="displaytext">', '</span>', '<span>']
#pat_list= [re.compile(i) for i in pat_list]

#def fixins(pat_list, replacement, string):
#    fixed= [re.sub(i, replacement, string) for i in pat_list]
#    return(fixed[(len(fixed)-1)])
        

#fixed_str_transcripts= []
#for j in str_transcripts:
#    for i in pat_list:
#        fixed= str_transcripts[0]
        

''' Example code '''
#def get_transcript(speech_link):
#    '''
#scrape title of speech, date of speech and full transcipt
#contained in the input speech_link URL
#'''
#    speaking = speech_link.split('/')[2]
#    new_link = base_url + str(speech_link)
#    try:
#        response = urllib.request.urlopen(new_link)
#        page_source = response.read()
#        soup = BeautifulSoup(page_source, "html5lib")
#        title = soup.find('title').text
#        speech_date = title.split('(', 1)[1].split(')')[0]
#        transcript = soup.find('div', {'id': 'transcript'}).text
#        transcript = transcript.replace('\n', ' ').replace('\r', '').replace('\t', '')
#        return {'speaker': speaking,
#                'date': speech_date,
#                'title': title,
#                'transcript': transcript}
#    except urllib2.HTTPError:
#        print 'skipped ' + str(speech_link)
#        return None

#transcript_links = get_speech_links()
#base_url = 'http://millercenter.org/'
#transcript_dict = {}
#for i, link in enumerate(transcript_links):
#    if i % 100 == 0:
#        print 'Scraped ' + str(i) + '/' + str(len(transcript_links)) + ' of links...'
#    if link.has_attr('href'):
#        transcript_data = get_transcript(link['href'])
#        if transcript_data is not None:
#            key = transcript_data['speaker'] + '|' + transcript_data['date']
#            transcript_dict[key] = transcript_data
