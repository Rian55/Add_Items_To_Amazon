from googletrans import Translator

trans = Translator()
C_CODE = "sv"

sku_file = open("inv_uk.txt", "r+")
inv_details = sku_file.read().splitlines()
sku_file.close()
skus = []
titles = []
keywords = []

for i in range(0, len(inv_details), 3):
    skus.append(inv_details[i])
    titles.append(inv_details[i + 1].lower())
    keywords.append(inv_details[i + 2])

titles_t = []
for title in titles:
    if " - " in title:
        title_split = title.split(" - ")
        titles_t.append(trans.translate(title_split[0], dest=C_CODE, src='en').text+" - "+title_split[1])
    else:
        titles_t.append(trans.translate(title, dest=C_CODE, src='en').text)
    print(titles_t[len(titles_t)-1])

print("titles translated")
keywords_t = trans.translate(keywords, dest=C_CODE, src='en')
print("keywords translated")

file = open(f"inv_{C_CODE}.txt", "w+", encoding="utf-8")

print("writing to file...")
for i in range(len(skus)):
    file.write(skus[i]+"\n"+titles_t[i].lower().replace(",", "")+"\n"+keywords_t[i].text+"\n")
print("writing to file completed")

file.close()
