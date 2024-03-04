import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

r = requests.get("https://www.tiobe.com/tiobe-index/")
soup = BeautifulSoup(r.text, features="html.parser")
htmltable = soup.find("table")

def tableDataText(table):
    """Parses a html segment started with tag <table> followed
    by multiple <tr> (table rows) and inner <td> (table data) tags.
    It returns a list of rows with inner columns.
    Accepts only one <th> (table header/data) in the first row.
    """

    def rowgetDataText(tr, coltag='td'):  # td (data) or th (header)
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]

    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow:  # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs:  # for every table row
        rows.append(rowgetDataText(tr, 'td'))  # data row
    return rows

rows = []
for row in tableDataText(htmltable):
    rows.append([row[0], row[4], row[5]])
rows.pop(0)
f = open("site.md", "w")
md = "# Most popular programming languages\n"
with DDGS() as duckduckgo:
    for r in rows:
        md += ("## " + r[0] + ". " + r[1] + " - " + r[2] + "\n")
        img = duckduckgo.images(r[1] + " language logo")[1]["image"]
        md += ("<img src=\"" + img + "\" alt=\"logo\" width=\"40\" height=\"40\" /> \n\n")
        results = duckduckgo.text("What is " + r[1], timelimit="y")
        md += (results[0]["body"] + "\n")
f.write(md)
f.close()
