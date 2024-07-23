# import requests
# from bs4 import BeautifulSoup
# import json
# import pandas as pd
#
# url = "https://apt.etda.or.th/cgi-bin/listgroups.cgi"
# response = requests.get(url)
# href_link = []
#
# # Status code 200
# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, "html.parser")
#     table = soup.find("table", class_="tborder")
#     if table:
#         links = table.find_all("a")
#         for link in links:
#             href_value = link.get("href")
#             if "https://apt.etda.or.th" not in href_value:
#                 href_value = "https://apt.etda.or.th" + href_value
#             href_link.append(href_value)
#     else:
#         print("Table with class 'tborder' not found")
# else:
#     print("Failed to retrieve the page")
#
# data_list = []
#
# for href in href_link:
#     # print("link connected-->",href)
#     response = requests.get(href)
#     if response.status_code == 200:
#         print('-->', href)
#         operations_performed = []
#         soup = BeautifulSoup(response.content, "html.parser")
#         table = soup.find("table", class_="tborder")
#         # Initialize an empty dictionary to store the extracted data
#         extracted_data = {}
#         rows = table.find_all("tr")
#         for row in rows:
#             # Find the header and data cells
#             header_cell = row.find("td", class_="tshaded")
#             try:
#                 header_cell.text
#             except Exception as e:
#                 if header_cell is None:
#                     data_cells = row.find_all("td", valign="top")
#                     if data_cells:
#                         try:
#                             operation = data_cells[0].text.strip()
#                             if operation is None:
#                                 operation = ""
#                             details = data_cells[1].text.strip()
#                             if details is None:
#                                 details = ""
#                             link = data_cells[1].find("a")["href"]
#                             if link is None:
#                                 link = ""
#                             operation_details = f"{operation}\n{details}\n<{link}>"
#                             operations_performed.append(operation_details.strip())
#                         except Exception as f:
#                             print(f)
#                             # print('-->', href)
#                             # print(link)
#                             # print()
#                             break
#                 break
#             if header_cell.text.strip() == "Operations performed":
#                 data_cells = row.find_all("td", valign="top")
#                 if data_cells:
#                     try:
#                         operation = data_cells[1].text.strip()
#                         details = data_cells[2].text.strip()
#                         link = data_cells[2].find("a")["href"]
#                         if link is None:
#                             link = ""
#                         operation_details = f"{operation}\n{details}\n<{link}>"
#                         operations_performed.append(operation_details.strip())
#                     except Exception as e:
#                         print(data_cells)
#             if header_cell is not None:
#                 data_cell = header_cell.find_next_sibling("td", valign="top")
#                 # Extract the text content of the header and data cells
#             if data_cell:
#                 header = header_cell.text.strip()
#                 data = data_cell.text.strip()
#             if operations_performed:
#                 header = "Operations performed"
#                 data = operations_performed
#
#             # Store the data in the dictionary
#             extracted_data[header] = data
#         if extracted_data:
#             data_list.append(extracted_data)
#
# with open("extracted_data.json", "w") as json_file:
#     json.dump(data_list, json_file, indent=4)
#
# # Read the JSON file into a DataFrame
# df = pd.read_json("extracted_data.json")
# # Write the DataFrame to an Excel file
# excel_file = "extracted_data.xlsx"
# df.to_excel(excel_file, index=False)
# # print(data_list)


