from pyllicalabspdf import *


#pdfpress(url="http://gallicalabs.bnf.fr/ark:/12148/cb32817642h/date", title="moderniste", year=1889, month=5, day=25, item=10, rate=7)


# bulletin des postes
titre="bulletindespostes"
periodique="cb32730626t";
#textpress(url="http://gallicalabs.bnf.fr/ark:/12148/cb32817642h/date", title="lemoderniste", year=1889, month=5, day=25, item=52, rate=7, lastpage=11)
url="http://gallica.bnf.fr/ark:/12148/{0}/date".format(periodique)
pdfpress(url="{0}".format(url), title="{0}".format(titre), year=1885, month=1, day=1, item=1, rate=7)
