import requests
from bs4 import BeautifulSoup
import sys


#r = requests.get('https://www.dr.com.tr/Kitap/Hayatim-Bir-Tasralinin-Hikayesi/Anton-Pavlovic-Cehov/Edebiyat/Roman/Dunya-Klasik/urunno=0001822343001')
link = "https://www.kitapsepeti.com/urun/detay/kitap/bir-psikanalistin-notlari/1362328"

f = open("linkler.txt","a")
f.write(link+"\r")
f.close()
r = requests.get(link)
source = BeautifulSoup(r.content,"lxml")
#print(source.text)
productinfo = source.find("div",attrs={"class":"productdetailout"}).find("table",attrs={"class":"productdetailtable"})
book_details = []
book_details.append(source.find("div",attrs={"class":"productright"}).find("h1").text)

headinfos = source.find("table",attrs={"class":"bookinfo"}).find_all("td")
j = 0

for info in headinfos:
    if(j%2==1):
        book_details.append(info.text.replace('\n',''))        
    j+=1

infolar = productinfo.find_all("td")
i = 0
for info in infolar:
    if i==5 or i==7:
        i+=1
        continue
    if i%2==1:
        book_details.append(info.text)
    i+=1

price = source.find("div",attrs={"class":"price clearfix"}).find("p",attrs={"class":"old"})
pricetext = price.text

pricetext = (pricetext[0:len(pricetext)-3])
book_details.append(pricetext)
detail_len = len(book_details)

for x in range (0,detail_len):
    print(book_details[x])



#fiyat = source.find("div",attrs={"class":"salePrice"})
#info_arr = []
#for info in infolar:
#    info_arr.append(info.text)
#info_arr.append(fiyat.find("span").text)
#print(info_arr)

# array siralamasi:
# Kitap adi
# Yazar
# Çevirmen (eğer varsa)
# Yayinevi
# Barkod
# Dil
# Hamur tipi
# Sayfa sayısı (eğer varsa)
# Baski yili
# Baski sayisi
# Ebat
# Fiyat

