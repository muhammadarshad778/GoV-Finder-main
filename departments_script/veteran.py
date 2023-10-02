import requests
from bs4 import BeautifulSoup
from departments_script.reusable_code.create_csv import create_csv
from departments_script.reusable_code.csv_columns import csv_col  # Assuming csv_col is defined in csv_columns module
from departments_script.reusable_code.hierarchy import veterans

def veterans_function():
    base_url = 'https://department.va.gov/'


    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarybFriDF1iUKeDfsZ5',
        # 'Cookie': '_ga=GA1.3.1761002096.1695017427; _gid=GA1.3.653759949.1695017427; _ga=GA1.1.1761002096.1695017427; _gat_GSA_ENOR0=1; _ga_CSLL4ZEK4L=GS1.1.1695017427.1.1.1695017597.0.0.0',
        'Origin': 'https://department.va.gov',
        'Referer': 'https://department.va.gov/biographies/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
    }

    page_size = 0  # Number of records per page
    total_records = None  # Total number of records, initialize to None to get it from the first response

    data_to_write = []  # Initialize without the header row

    while True:
        params = {
            'wpgb-ajax': 'refresh',
            '_load_more_bios': str(page_size),
        }

        data_request = '------WebKitFormBoundarybFriDF1iUKeDfsZ5\r\nContent-Disposition: form-data; name="wpgb"\r\n\r\n{"is_main_query":0,"main_query":[],"permalink":"https://department.va.gov/biographies/","facets":[6,7,9,11,12,14],"lang":"","id":2}\r\n------WebKitFormBoundarybFriDF1iUKeDfsZ5--\r\n'

        response = requests.post(base_url, params=params, headers=headers, data=data_request).json()

        # Check if 'total' key exists and is not None in the response before trying to convert it to an integer
        if 'total' in response and response['total'] is not None:
            total_records = int(response['total'])
            # print(f"Total records: {total_records}")

        soup = BeautifulSoup(response.get('posts', ''), 'html.parser')

        Phone = ""
        Email = ""
        articles = soup.find_all('article')
        page_data = []  # Store data for this page

        for article in articles:
            name = article.find('h2').text
            dep_element = article.find('div', {'class': 'wpgb-block-3 wpgb-idle-scheme-1'})
            dep = dep_element.text if dep_element else ""
            title = article.find('div', class_='wpgb-block-2').text
            

            # Append the extracted data to page_data
            page_data.append([name, dep, title, Email, Phone,base_url,veterans()])

        # Add the data for this page to the main data_to_write list
        data_to_write.extend(page_data)

        if page_size >= total_records + 10:
            break

        page_size += 10

    # Call the create_csv function to save the data to a CSV file with the header row
    create_csv(data_to_write, 'veteran.csv', csv_col())

