from googletrans import Translator

trans = Translator()

sku_file = open("inv_uk.txt", "r+")
inv_details = sku_file.read().splitlines()
sku_file.close()
skus = []
titles = []
keywords = []

for i in range(0, len(inv_details), 3):
    skus.append(inv_details[i])
    titles.append(inv_details[i + 1])
    keywords.append(inv_details[i + 2])

titles_t = trans.translate(titles, dest='de')
keywords_t = trans.translate(keywords, dest='de')

file = open("inv_de.txt", "w+", encoding="utf-8")

for i in range(len(skus)):
    file.write(skus[i]+"\n"+titles_t[i].text+"\n"+keywords_t[i].text+"\n")

file.close()
