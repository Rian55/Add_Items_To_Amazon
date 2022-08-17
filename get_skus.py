import re

file = open("html.txt", "r")
html_lines = file.read().splitlines()
file.close()
skus = []

for line in html_lines:
    if '<a class="a-link-normal mt-link-content mt-table-main" target="_blank" rel="noopener" href=' in line:
        m = re.search("=([A-Z0-9a-z].+)&", line)
        if m:
            skus.append(m.group()[1:len(m.group())-1])

file = open("skus.txt", "w+")
for sku in skus:
    file.write(sku+"\n")
file.close()
