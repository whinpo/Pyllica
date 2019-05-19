# from bs4 import BeautifulSoup
import bs4 as bs
import urllib.request, urllib.error, urllib.parse
import re
import os
import requests
import wget
from pathlib import Path

from requests_html import HTMLSession
import certifi

for annee in range(1878, 1936):
    download_dir="/home/whinpo/Philatélie/Daguins/Infos/Bulletins mensuels des postes/{0}".format(annee)

    # si le répertoire n'existe pas on le crée
    dirAcreer = Path(download_dir)
    if not dirAcreer.exists():
    	dirAcreer.mkdir(parents=True, exist_ok=True)
    dirAcreer = Path("{0}/TXT".format(download_dir))
    if not dirAcreer.exists():
    	dirAcreer.mkdir(parents=True, exist_ok=True)
    dirAcreer = Path("{0}/PDF".format(download_dir))
    if not dirAcreer.exists():
    	dirAcreer.mkdir(parents=True, exist_ok=True)


    session = HTMLSession()

    urlannee="https://gallica.bnf.fr/ark:/12148/cb32730626t/date{0}".format(annee)
    page_html=session.get(urlannee)
    # on exécute le javascript
    print('rendering...')
    page_html.html.render(sleep=2)
    #page_html.html.html contient le html avec javascript exécuté
    soup=bs.BeautifulSoup(page_html.html.html,'lxml')

    # on récupère tous les liens de l'année
    resultat=soup.find_all('span',{"class": "day-number"})
    for spans in resultat:
        if spans.a.get('href'):
            finalurl=spans.a.get('href')
            # finalurl="https://gallica.bnf.fr/ark:/12148/cb32730626t/date{0}0101".format(annee)
            print(finalurl)
            #urllib.request.urlopen(finalurl)
            #urllib.request.urlopen(finalurl)
            page_html=session.get(finalurl)

            # on exécute le javascript
            print('rendering...')
            page_html.html.render(sleep=2)

            #page_html.html.html contient le html avec javascript exécuté
            soup=bs.BeautifulSoup(page_html.html.html,'lxml')

            # on extrait les résultats de la recherche
            for numeros in soup.find_all('div',class_='resultat_img'):
                # lien vers url en enlevent ce qu'il ya derrière le ? pour le remplacer par .pdf
                lienPDF="{0}{1}".format(numeros.a.get('href').split('?')[0],'.pdf')
                lienTXT="{0}{1}".format(numeros.a.get('href').split('?')[0],'.texteBrut')
                titre=numeros.a.span.get('title').replace('/','-')
                fichierPDF="{0}/PDF/{1}pdf".format(download_dir,titre)
                fichierTXT="{0}/TXT/{1}txt".format(download_dir,titre)

                print("Téléchargement de {0} vers {1}".format(lienPDF,fichierPDF))
                wget.download(lienPDF,fichierPDF)
                print("Téléchargement de {0} vers {1}".format(lienTXT,fichierTXT))
                wget.download(lienTXT,fichierTXT)
# on execute le javascript
# r.html.render()
# soup=BeautifulSoup(r.text,"lxml")
