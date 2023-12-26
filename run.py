import requests as reqs
import pandas as pd
import xlsxwriter

# Instance of result
workbook = xlsxwriter.Workbook('result.xlsx')
worksheet = workbook.add_worksheet()

# Putting the headers
worksheet.write("A1", "DOMAIN")
worksheet.write("B1", "KEYWORDS")

# Reading data from excel
data = pd.read_excel ('sites.xlsx')
rows = pd.DataFrame(data, columns= ["site"])

# padrão de keywords para pesquisar
default_keywords = ["wix","nuvemshop","lojaintegrada","woocommerce","traycommerce","magento","vtex"]

def scrap_site(site,keywords = default_keywords):
  found = False
  try:
    resp = reqs.get(site, timeout=10)
  except Exception as e:
    return ["Error: error loading site"]
  content = resp.text
  if (content == ""):
    return ["Error: could not read source code"]
  keywords_found = []
  for keyword in keywords:
    if keyword in content:
      keywords_found.append(keyword)
      found = True
  if not found:
    return ["not_found"]
  return keywords_found

# Gambi :(
row = 1

for domain in rows['site']:
  print("========== STARTING SITE " + domain + " ==========")
  result = ''
  try:
      result = scrap_site(domain)
  except Exception as exc:
      result = "exception"
  finally:
      row = row + 1
      worksheet.write("{}{}".format("A", row), domain)
      worksheet.write("{}{}".format("B", row), ','.join(result))

workbook.close()