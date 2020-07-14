import xml.etree.ElementTree as ET
from xml.dom import minidom
import xml

from unidecode import unidecode
import io

mydoc = xml.dom.minidom.parse("data.xml");
titiles = mydoc.getElementsByTagName('name')



fillet_name = 'Singapore'
habitant = 'Phim Khoa Học Viễn Tưởng'

print(habitant.lower().find(fillet_name))

list = []
for item in titiles:
    if(item.firstChild.data.find(fillet_name) != -1):
        list.append(item)


for i in titiles:
    print(i.firstChild.data)
for item in list:
    print(item.firstChild.data)