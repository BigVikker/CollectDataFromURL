import xml.etree.ElementTree as ET
import xml.dom.minidom



mydoc = xml.dom.minidom.parse("data.xml");

days = mydoc.getElementsByTagName('item')
urls = mydoc.getElementsByTagName('url')
titles = mydoc.getElementsByTagName('name')
items = mydoc.getElementsByTagName('item')

tiem_kiem = "bé trai"
tim_kiem_splitted = tiem_kiem.split()

dataResult = []
print(len(titles))
for item in range(0, len(titles)):
    count = 0
    for conditions in tim_kiem_splitted:
        if titles[item].firstChild.data.lower().find(conditions.lower()) != -1:
            count += 1
        if count >= len(tim_kiem_splitted)/2:
            dataResult.append(titles[item].firstChild.data)
            break


for item in dataResult:
    print(item)
