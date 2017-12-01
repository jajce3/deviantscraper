import requests
from bs4 import BeautifulSoup
from time import sleep
from os import mkdir
from os import listdir
from os import system

username=input('Username:').lower()#solarokchaos,bob
mkdir(username)

s = requests.Session()
s.cookies['agegate_state'] = '1'

#dobi linke strani s slikami
sez_link=[]
sez_link2=[]
page=0
offset=0
sez_link_change=1
print('Subpages:',end='')
while sez_link_change and not len(sez_link)%24:
    print(' ',end='')
    url='http://'+username+'.deviantart.com/gallery/?catpath=%2F&offset='+str(offset)

    page+=1
    offset=page*24

    r=s.get(url)
    soup=BeautifulSoup(r.content,'html.parser')
    links=soup.find_all('a',{'class':'thumb'})

    sez_link_change=len(sez_link)
    for link in links:
        sez_link.append(link.get('href'))
    sez_link_change-=len(sez_link)
        
    print(page,end='')
print('\nImages:',len(sez_link),'\n')

#dobi linke slik
space1=' '
for link2 in range(len(sez_link)):
    url2=sez_link[link2]    
    r2=s.get(url2)
    soup2=BeautifulSoup(r2.content,'html.parser')
    if link2>8:
        space1=''
    if soup2.find_all('a',{'rel':'nofollow'}):
        for image in soup2.find_all('a',{'rel':'nofollow'}):
            sez_link2.append(image.get('href'))
        for image in soup2.find_all('img',{'class':'dev-content-full '}):
            print(space1,link2+1,': ',(image.get('alt')).rsplit((' by '),1)[0],sep='')
    else:
        for image in soup2.find_all('img',{'class':'dev-content-full '}):
            sez_link2.append(image.get('src'))
            print(space1,link2+1,': ',(image.get('alt')).rsplit((' by '),1)[0],sep='')
print()

#zloadaj slike
url=sez_link2[0]
zap_st=0
for url in sez_link2:
    filename =(url.rsplit('?token=')[0]).split('/')[5]
    zap_st+=1
    print('Filename:',filename)
    print('Downloaded image:',zap_st,'\n')
    r = s.get(url,stream=True)
    f = open(username+'/'+filename, 'wb')
    for chunk in r.iter_content(chunk_size=1048576):#chunk_size=1MB
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
            f.flush()
    f.close()
    #print('Downloaded: ',(image.get('href')).split('?token=',1)[0],'\n',sep='')

#safety checks
error=False
print(len(listdir(username)))
if len(sez_link)!=len(sez_link2):
    print('NAPAKA: Strani slik je manj kot linkov slik!')
    error=True
if len(listdir(username))!=len(sez_link2):
    print('NAPAKA: Slik je manj kot linkov slik!')
    error=True
#printanje zakljucka
if not error:
    print('\nStrani je bilo:',page)
    print('Zloadanih slik:',len(sez_link2))

print('\nEND')
system('pause')
