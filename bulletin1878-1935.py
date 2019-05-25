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

anneedebut=1878
anneefin=1936

for annee in range(anneedebut, anneefin):
    print(annee)
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
    print('rendering {0}...'.format(urlannee))
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
            session = HTMLSession()
            page_html=session.get(finalurl)

            # on exécute le javascript
            print('rendering suite {0}...'.format(finalurl))
            page_html.html.render(sleep=2)

            #page_html.html.html contient le html avec javascript exécuté
            soup=bs.BeautifulSoup(page_html.html.html,'lxml')

            # on regarde si la page a affiché une liste de documents ou si elle affiche directement un item
            # exemple : https://gallica.bnf.fr/ark:/12148/cb32730626t/date19330111 =>
            # donne en fait une url https://gallica.bnf.fr/ark:/12148/bpt6k5827116v.item
            urldest=page_html.url
            print("urldest {0}".format(urldest))
            if ".item" in urldest:
                print("lien direct {0}".format(urldest))
                # on enlève item et on met pdf à la place
                lienPDF="{0}{1}".format(urldest.split("item")[0],"pdf")
                lienTXT="{0}{1}".format(urldest.split("item")[0],".texteBrut")
                # title de la forme [<title>Bulletin mensuel des postes et télégraphes | 1933-01-11 | Gallica</title>]
                titre=soup.find('title').text.split(" | ")[1]
                fichierPDF="{0}/PDF/{1}.pdf".format(download_dir,titre)
                fichierTXT="{0}/TXT/{1}.txt".format(download_dir,titre)

                if not os.path.exists(fichierPDF):
                    print("Téléchargement de {0} vers {1}".format(lienPDF,fichierPDF))
                    wget.download(lienPDF,fichierPDF)
                else:
                    print("{0} déjà existant".format(fichierPDF))
                if not os.path.exists(fichierTXT):
                    print("Téléchargement de {0} vers {1}".format(lienTXT,fichierTXT))
                    wget.download(lienTXT,fichierTXT)
                else:
                    print("{0} déjà existant".format(fichierTXT))
            else:
                # on extrait les résultats de la recherche
                for numeros in soup.find_all('div',class_='resultat_img'):
                    # lien vers url en enlevent ce qu'il ya derrière le ? pour le remplacer par .pdf
                    lienPDF="{0}{1}".format(numeros.a.get('href').split('?')[0],'.pdf')
                    lienTXT="{0}{1}".format(numeros.a.get('href').split('?')[0],'.texteBrut')
                    titre=numeros.a.span.get('title').replace('/','-')
                    fichierPDF="{0}/PDF/{1}pdf".format(download_dir,titre)
                    fichierTXT="{0}/TXT/{1}txt".format(download_dir,titre)

                    if not os.path.exists(fichierPDF):
                        print("Téléchargement de {0} vers {1}".format(lienPDF,fichierPDF))
                        wget.download(lienPDF,fichierPDF)
                    else:
                        print("{0} déjà existant".format(fichierPDF))
                    if not os.path.exists(fichierTXT):
                        print("Téléchargement de {0} vers {1}".format(lienTXT,fichierTXT))
                        wget.download(lienTXT,fichierTXT)
                    else:
                        print("{0} déjà existant".format(fichierTXT))
# on execute le javascript
# r.html.render()
# soup=BeautifulSoup(r.text,"lxml")
