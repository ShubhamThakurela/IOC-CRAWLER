# import re
# import markdown
#
#


"""""The use_reloader=False argument disables the Flask reloader. The reloader is used during development to 
automatically restart the server when changes are made to the code. It's common to set this to False in production 
environments to prevent automatic server restarts."""""
# class RegexPatternDB:
#     @staticmethod
#     def all_regex_patterns():
#         # Defined rgx\
#         regex_patterns = [
#             r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
#             r'(?:[a-z]+\.)+[a-z]+\.[a-z]+',
#             r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+)',
#             https?://[^,]+',
#             r"\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\b"
#         ]
#         print("Adding More frequently_____")
#         # Create a list containing the regex patterns
#         # regex_patterns = [ip_pattern, domain_pattern, domain_pattern2, url_pattern, hash_pattern]
#         print(regex_patterns)
#         # searched_string = re.search(ip_pattern, domain_pattern, domain_pattern2, url_pattern, hash_pattern, line)
#         return regex_patterns
#
#
# import re
#
# # Define the list of regex patterns
# # regex_patterns = [
# #     r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
# #     r'(?:[a-z]+\.)+[a-z]+\.[a-z]+',
# #     r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+)',
# #     https?://[^,]+',
# #     r'\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\b',
# # ]
#
# # Call the function
# # lines = raw_data.strip().split('\n')
# # # patterns_stng = RegexPatternDB.all_regex_patterns()
# # regex_patterns = [
# #     r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
# #     r'(?:[a-z]+\.)+[a-z]+\.[a-z]+',
# #     r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+)',
# #     https?://[^,]+',
# #     r"\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\b"
# # ]
# # for line in lines:
# #     for pattern in regex_patterns:
# #         matches = re.findall(pattern, line)
# #         if matches:
# #             print(f"Pattern: {pattern}, Found: {matches}")
# #         #print(pattern)
#
# print(markdown.markdown('###Example for above '))
# # def extract_info_from_lines(lines):
# #     ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
# #     domain_pattern = r'(?:[a-z]+\.)+[a-z]+\.[a-z]+'
# #     domain_pattern2 = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+)'
# #     url_pattern = https?://[^,]+'
# #     hash_pattern = r"\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\b"
# #
# #     regex_patterns = [ip_pattern, domain_pattern, domain_pattern2, url_pattern, hash_pattern]
# # result = []
# # for line in lines.splitlines():
# #     data = line.split(',')
# #     info_dict = {}
# #     for i, pattern in enumerate(regex_patterns):
# #         matches = re.findall(pattern, data[i + 3])
# #         if matches:
# #             info_dict[["ip", "domain", "domain", "url", "hash"][i]] = matches[0]
# #     result.append(info_dict)
# # return result
#
# # Call the function to extract information from the lines
# # extracted_info = extract_info_from_lines(lines)
# # # Print the extracted information
# # for info in extracted_info:
# #     print(info)
#
#
# ## Extract Names from the url
# # from urllib.parse import urlparse
# #
# #
# # def extract_name_from_url(url):
# #     parsed_url = urlparse(url)
# #     domain = parsed_url.netloc
# #     if domain.startswith('www.'):
# #         domain = domain[4:]
# #     return domain
# #
# #
# # # Test the function with the provided URLs
# # urls = [
# #     "https://malshare.com/daily/2023-07-04/malshare_fileList.2023-07-04.sha1.txt",
# #     "http://malshare.com/daily/2023-07-04/malshare_fileList.2023-07-04.sha256.txt",
# #     "https://bazaar.abuse.ch/export/txt/sha256/recent/"]
# # for url in urls:
# #     result = extract_name_from_url(url)
# #     print(f"URL: {url} | Name: {result}")
