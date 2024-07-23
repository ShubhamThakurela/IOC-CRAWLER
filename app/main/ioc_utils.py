import re
import ipaddress
from datetime import datetime
from urllib.parse import urlparse
from .ioc_orm import IocOrm


class ProcessAllIoc:
    def __init__(self, raw_data, url, all_domains_list, type_ioc):
        self.raw_data = raw_data
        self.url = url
        self.domain_list = all_domains_list
        self.ioc_type = type_ioc

    def extract_all_ioc(self):
        try:
            # Create empty sets to store unique values encountered for each field
            unique_ref_ips = set()
            unique_ref_domains = set()
            unique_ref_urls = set()
            unique_ref_hashes = set()
            unique_ref_subnet = set()
            ip_dict, domain_dict, url_dict, hash_dict, subnet_dict = {}, {}, {}, {}, {}
            # Initialize an empty list to store the dicts
            (ip_dicts_list, subnet_dicts_list, domain_dicts_list,
             urls_dicts_list, hash_dicts_list, source_url_dt_list) = [], [], [], [], [], []
            # Define regex patterns for ip, domain, url, and hashes
            ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
            domain_pattern = r"(([a-z0-9\-]+\.)+[a-z]{2,63}){1,255}"
            url_pattern = r'https?://[^,]+'
            hash_pattern = r"\b(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\b"
            subnet_pattern = (r"\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]["
                              r"0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]["
                              r"0-9]?)\/\d{1,2}\b")
            source_url = self.url
            source = extract_name_from_url(source_url)  # need to strip the Source name from url
            source_url_dict = {
                "Url": self.url.strip(),
                "last_extraction_time": datetime.now().strftime("%Y-%m-%d"),
                "source": source,
                "source_type": self.ioc_type,
            }
            source_url_dt_list.append(source_url_dict)
            # Split the raw_data by lines
            lines = self.raw_data.strip().split('\n')
            # Loop through each line and extract the required information using regex
            for line in lines:
                current_datetime = datetime.now().strftime("%Y-%m-%d")
                ip_match = re.findall(ip_pattern, line)
                domain_match = re.findall(domain_pattern, line)
                url_match = re.findall(url_pattern, line)
                hash_match = re.findall(hash_pattern, line)
                subnet_match = re.findall(subnet_pattern, line)
                if isinstance(ip_match, type(None)):
                    pass
                else:
                    for ip in ip_match:
                        ip_string_extractor = ip
                        ip_type = check_ip_type(ip_string_extractor)
                        ip_dict = {"ip": ip_string_extractor,
                                   "Ioc_type": "IP",
                                   "ip_type": ip_type,
                                   "source_url": self.url.strip(),
                                   "source_type": self.ioc_type,
                                   "first_timestamp": current_datetime}
                        # Validation for ref_ip
                        if ip_string_extractor not in unique_ref_ips:
                            unique_ref_ips.add(ip_string_extractor)
                        for domain in domain_match:
                            if domain[0] in self.domain_list:
                                pass
                            else:
                                domain_dict.update({"ref_ip": [{"ip": ip_string_extractor, "ip_type": ip_type,
                                                                "ref_source": self.url.strip(),
                                                                "Current_timestamp": datetime.now()}]})
                        if url_match:
                            url_dict.update({"ref_ip": [{"ip": ip_string_extractor, "ip_type": ip_type,
                                                         "ref_source": self.url.strip(),
                                                         "Current_timestamp": datetime.now()}]})
                        if hash_match:
                            hash_dict.update({"ref_ip": [{"ip": ip_string_extractor, "ip_type": ip_type,
                                                          "ref_source": self.url.strip(),
                                                          "Current_timestamp": datetime.now()}]})
                        if subnet_match:
                            subnet_dict.update({"ref_ip": [{"ip": ip_string_extractor, "ip_type": ip_type,
                                                            "ref_source": self.url.strip(),
                                                            "Current_timestamp": datetime.now()}]})

                if isinstance(domain_match, type(None)):
                    pass
                else:
                    for domain in domain_match:
                        domain = domain[0]
                        domain_string_extractor = domain
                        if domain_string_extractor in self.domain_list:
                            pass
                        else:
                            domain_type = check_domain_type(domain_string_extractor)
                            domain_dict = {"domain": domain_string_extractor,
                                           "domain_type": domain_type,
                                           "source_url": self.url.strip(),
                                           "source_type": self.ioc_type,
                                           "first_timestamp": current_datetime}
                            if domain_string_extractor not in unique_ref_domains:
                                unique_ref_domains.add(domain_string_extractor)
                                if ip_match:
                                    ip_dict.update(
                                        {"ref_domains": [{"domain": domain_string_extractor,
                                                          "domain_type": domain_type,
                                                          "ref_source": self.url.strip(),
                                                          "Current_timestamp": datetime.now()}]})
                                if hash_match:
                                    hash_dict.update({"ref_domains": [{"domain": domain_string_extractor,
                                                                       "domain_type": domain_type,
                                                                       "ref_source": self.url.strip(),
                                                                       "Current_timestamp": datetime.now()}]})
                                for url in url_match:
                                    url_string_extractor = extract_name_from_url(url)
                                    if url_string_extractor in self.domain_list:
                                        pass
                                    else:
                                        url_dict.update({"ref_domains": [{"domain": domain_string_extractor,
                                                                          "domain_type": domain_type,
                                                                          "ref_source": self.url.strip(),
                                                                          "Current_timestamp": datetime.now()}]})
                                if subnet_match:
                                    subnet_dict.update({"ref_domains": [{"domain": domain_string_extractor,
                                                                         "domain_type": domain_type,
                                                                         "ref_source": self.url.strip(),
                                                                         "Current_timestamp": datetime.now()}]})
                if isinstance(url_match, type(None)):
                    pass
                else:
                    for url in url_match:
                        url_string_extractor = extract_name_from_url(url)
                        if url_string_extractor in self.domain_list:
                            pass
                        else:
                            url_type = check_url_type(url_string_extractor)
                            url_string_extractor = url_string_extractor.replace("'", '')
                            url_dict = {"url": url_string_extractor,
                                        "url_type": url_type,
                                        "source_url": self.url.strip(),
                                        "source_type": self.ioc_type,
                                        "first_timestamp": current_datetime}
                            if url_string_extractor not in unique_ref_urls:
                                unique_ref_urls.add(url_string_extractor)
                                for domain in domain_match:
                                    if domain[0] in self.domain_list:
                                        pass
                                    else:
                                        domain_dict.update({"ref_urls": [{"url": url_string_extractor,
                                                                          "url_type": url_type,
                                                                          "ref_source": self.url.strip(),
                                                                          "Current_timestamp": datetime.now()}]})
                                if ip_match:
                                    ip_dict.update({"ref_urls": [{"url": url_string_extractor,
                                                                  "url_type": url_type,
                                                                  "ref_source": self.url.strip(),
                                                                  "Current_timestamp": datetime.now()}]})
                                if hash_match:
                                    hash_dict.update({"ref_url": [{"url": url_string_extractor,
                                                                   "url_type": url_type,
                                                                   "ref_source": self.url.strip(),
                                                                   "Current_timestamp": datetime.now()}]})
                                if subnet_match:
                                    subnet_dict.update({"ref_url": [{"url": url_string_extractor,
                                                                     "url_type": url_type,
                                                                     "ref_source": self.url.strip(),
                                                                     "Current_timestamp": datetime.now()}]})
                if isinstance(hash_match, type(None)):
                    pass
                else:
                    for hash_string in hash_match:
                        hash_strg_extractr = hash_string
                        hash_type = check_hash_type(hash_strg_extractr)
                        hash_dict = {"hash": hash_strg_extractr,
                                     "hash_type": hash_type,
                                     "source_url": self.url.strip(),
                                     "source_type": self.ioc_type,
                                     "first_timestamp": current_datetime}
                        if hash_strg_extractr not in unique_ref_hashes:
                            unique_ref_hashes.add(hash_strg_extractr)
                            if ip_match:
                                ip_dict.update({
                                    "ref_hashes": [
                                        {"hash": hash_strg_extractr, "hash_type": hash_type,
                                         "ref_source": self.url.strip(),
                                         "Current_timestamp": datetime.now()}]})
                                for url in url_match:
                                    url_string_extractor = extract_name_from_url(url)
                                    if url_string_extractor in self.domain_list:
                                        pass
                                    else:
                                        url_dict.update({
                                            "ref_hashes": [  # update function
                                                {"ref_hash": hash_strg_extractr, "hash_type": hash_type,
                                                 "ref_source": self.url.strip(),
                                                 "Current_timestamp": datetime.now()}]})
                                for domain in domain_match:
                                    if domain[0] in self.domain_list:
                                        pass
                                    else:
                                        domain_dict.update({
                                            "ref_hashes": [
                                                {"hash": hash_strg_extractr, "hash_type": hash_type,
                                                 "ref_source": self.url.strip(),
                                                 "Current_timestamp": datetime.now()}]})
                                if subnet_match:
                                    subnet_dict.update({
                                        "ref_hashes": [
                                            {"hash": hash_strg_extractr, "hash_type": hash_type,
                                             "ref_source": self.url.strip(),
                                             "Current_timestamp": datetime.now()}]})
                if isinstance(subnet_match, type(None)):
                    pass
                else:
                    for subnet in subnet_match:
                        subnet = subnet
                        ip_address, subnet_cidr_notation = subnet_notation(subnet)
                        ipadress_type = check_ip_type(ip_address)
                        subnet_dict = {"subnet": subnet,
                                       "subnet_cidr_notation": subnet_cidr_notation,
                                       "source_url": self.url.strip(),
                                       "source_type": self.ioc_type,
                                       "subnet_ip_type": ipadress_type,
                                       "first_timestamp": current_datetime}
                        if subnet not in unique_ref_subnet:
                            unique_ref_subnet.add(subnet)
                        if ip_match:
                            ip_dict.update(
                                {"ref_subnet": [{"subnet": subnet,
                                                 "subnet_cidr_notation": subnet_cidr_notation,
                                                 "subnet_ip_type": ipadress_type,
                                                 "ref_source": self.url.strip(),
                                                 "Current_timestamp": datetime.now()}]})
                        if hash_match:
                            hash_dict.update({"ref_subnet": [{"subnet": subnet,
                                                              "subnet_cidr_notation": subnet_cidr_notation,
                                                              "subnet_ip_type": ipadress_type,
                                                              "ref_source": self.url.strip(),
                                                              "Current_timestamp": datetime.now()}]})
                        if url_match:
                            url_dict.update({"ref_subnet": [{"subnet": subnet,
                                                             "subnet_cidr_notation": subnet_cidr_notation,
                                                             "subnet_ip_type": ipadress_type,
                                                             "ref_source": self.url.strip(),
                                                             "Current_timestamp": datetime.now()}]})
                ip_dicts_list.append(ip_dict)
                domain_dicts_list.append(domain_dict)
                hash_dicts_list.append(hash_dict)
                urls_dicts_list.append(url_dict)
                subnet_dicts_list.append(subnet_dict)
            final_ip_dicts_list_ = append_keys_contain_dicts(ip_dicts_list)
            final_domain_dicts_list = append_keys_contain_dicts(domain_dicts_list)
            final_hash_dicts_list = append_keys_contain_dicts(hash_dicts_list)
            final_urls_dicts_list = append_keys_contain_dicts(urls_dicts_list)
            final_subnet_dicts_list = append_keys_contain_dicts(subnet_dicts_list)
            # Initialising the objects and inserting list of dicts
            print("all dicts appended", self.url)
            ip_insert_obj = IocOrm(final_ip_dicts_list_)
            dict_ip_insertion = ip_insert_obj.insert_or_update()
            # Initialising the objects and inserting list of dicts
            domain_insert_obj = IocOrm(final_domain_dicts_list)
            domain_insertion = domain_insert_obj.insert_or_update()
            # Initialising the objects and inserting list of dicts
            urls_insert_obj = IocOrm(final_urls_dicts_list)
            dict_urls_insertion = urls_insert_obj.insert_or_update()
            # Initialising the objects and inserting list of dicts
            source_insrt_obj = IocOrm(source_url_dt_list)
            dict_source_insertion = source_insrt_obj.insert_sources()
            # Initialising the objects and inserting list of dicts
            hash_insert_obj = IocOrm(final_hash_dicts_list)
            hash_insertion = hash_insert_obj.insert_or_update()
            # Initialising the objects and inserting list of dicts
            subnet_insert_obj = IocOrm(subnet_dicts_list)
            subnet_insertion = subnet_insert_obj.insert_or_update()
            if "Data Inserted Successfully!" in hash_insertion and domain_insertion and \
                    dict_urls_insertion and dict_ip_insertion and subnet_insertion:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return repr(e)


def subnet_notation(subnet):
    subnet_string = str(subnet)
    # Split the string by "/"
    ip_address, prefix_length_str = subnet_string.split("/")
    # Convert the prefix length to an integer
    prefix_length = int(prefix_length_str)
    return ip_address, prefix_length


def check_hash_type(hash_string):
    hash_length = len(hash_string)
    if hash_length == 32:
        return 'MD5'
    elif hash_length == 40:
        return 'SHA1'
    elif hash_length == 64:
        return 'SHA256'
    else:
        return 'Unknown'


def check_url_type(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme == "http":
        return "HTTP"
    elif parsed_url.scheme == "https":
        return "HTTPS"
    else:
        return "Unknown"


def check_domain_type(domain_string):
    tld_pattern = r"(\.[a-z]+)$"
    match = re.search(tld_pattern, domain_string)
    if match:
        domain = match.group(0)  # Remove the leading dot from the domain
        return domain
    else:
        return "Invalid URL or domain not found"


def check_ip_type(ip_address):
    try:
        # Try to create an IP address object
        ip = ipaddress.ip_address(ip_address)

        # Check if it's an IPv4 address
        if isinstance(ip, ipaddress.IPv4Address):
            return "IPv4"
        # Check if it's an IPv6 address
        elif isinstance(ip, ipaddress.IPv6Address):
            return "IPv6"
        else:
            return "Unknown"
    except ValueError:
        # If the IP address is invalid, ValueError will be raised
        return "IP not Given"


# Define a function to handle None values and extract the matched text or return an empty string
# def get_match_text(match_object):
#     if match_object is not None:
#         return match_object.group(0)
#     else:
#         return "Null"


def extract_name_from_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain


def append_keys_contain_dicts(original_list):
    new_list = []
    for dictionary in original_list:
        if dictionary:  # Check if the dictionary is not empty
            first_key = next(iter(dictionary))  # Get the first key of the dictionary
            if first_key == 'ip':
                new_list.append(dictionary)
            elif first_key == 'url':
                new_list.append(dictionary)
            elif first_key == 'domain':
                new_list.append(dictionary)
            elif first_key == 'hash':
                new_list.append(dictionary)
            elif first_key == 'subnet':
                new_list.append(dictionary)

    return new_list
