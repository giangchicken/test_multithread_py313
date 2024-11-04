def remove_specific_links(url_list):
  """Removes links containing specific keywords from a list of URLs."""
  if not isinstance(url_list, list):
    return []
  keywords = ["topcv", "masothue", "thuvienphapluat", "masocongty", "massothue", "ma-so-thue",
              "tratencongty", "hosocongty", "trangvangdoanhnghiep", "vieclam24h", "vnmore", "dauthau.net",
              "doanhnghiep.biz", "infocom", "baogiaothong.vn", "facebook", "yellowpages", "nhathuygroup",
              "phaply.net", "fiingate.vn", "ibaohiem"]
  filtered_urls = [url for url in url_list if not any(keyword in url for keyword in keywords)]
  return filtered_urls

def remove_duplicate_links(url_list):
  if not isinstance(url_list, list):
    return []
  unique_urls = []
  seen_domains = set()
  for url in url_list:
    if url:
      # Extract the domain part of the URL (e.g., example.com)
      domain = url.split('/')[2] if '//' in url else url.split('/')[0]
      if domain not in seen_domains:
        unique_urls.append(url)
        seen_domains.add(domain)
  return unique_urls

def preprocessing(df):
    extracted_urls_list = []
    for index, row in df.iterrows():
        name_company = row['name_company']
        list_website = row['list_website']
        code = row['code']

        # Extract URLs from list_website
        urls = []
        if isinstance(list_website, str):
            try:
                website_list = eval(list_website)  # Safely evaluate the string as a list
                urls = [item['url'] for item in website_list if 'url' in item]
            except (SyntaxError, NameError, TypeError):
                print(f"Error parsing list_website for {name_company}: {list_website}")
        else:
            print(f"list_website is not a string for {name_company}: {list_website}")

        extracted_urls_list.append(urls)

    # Add the extracted_urls_list as a new column to the DataFrame
    df['extracted_urls'] = extracted_urls_list                                         
    # Apply the function to the 'extracted_urls' column
    df['extracted_urls'] = df['extracted_urls'].apply(remove_specific_links)

    # Apply the function to the 'extracted_urls' column
    df['extracted_urls'] = df['extracted_urls'].apply(remove_duplicate_links)

    return df