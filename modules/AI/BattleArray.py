import pandas as pd
# import xlrd

data = pd.read_excel('modules/AI/阵型筛选器.xlsx', engine='openpyxl')

battleArraies = []
for battleArray in data['Unnamed: 1']:
  if battleArray != '阵型': battleArraies.append(battleArray.lower())