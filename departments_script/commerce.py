import requests
from bs4 import BeautifulSoup
import csv
from departments_script.reusable_code.create_csv import create_csv
from departments_script.reusable_code.csv_columns import csv_col  # Assuming csv_col is defined in csv_columns module
from departments_script.reusable_code.hierarchy import commerce

# Function to scrape data from the current page
def scrape_page(url):
    base_url = "https://www.commerce.gov/about/leadership?q=/about/leadership&page="
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        divs = soup.find_all('div', {"class": 'leadership-row'})

        # Initialize a list to store the extracted data
        data = []
        Email=''
        Phone=''
        dep='commerce'
        for div in divs:
            name = div.find('h3', {"class": 'leader-name'}).text
            title = div.find('div', {'class': 'leader-title'}).text
            data.append([name, dep, title, Email, Phone,base_url,commerce()])

        return data, soup  # Return both the data and the soup object

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return [], None
def commerce_function():
    # Define the URL and CSV file name
    base_url = "https://www.commerce.gov/about/leadership?q=/about/leadership&page="
    csv_file = "commerce.csv"

    # # Initialize a CSV file and write the header
    # with open(csv_file, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['Name', 'Title'])

    # Loop through the pages and scrape data
    page_number = 0
    while True:
        page_url = base_url + str(page_number)
        data, soup = scrape_page(page_url)  # Get data and the updated soup

        if not data:
            break  # Stop if no more data is found on the page

        # Append the data to the CSV file
        # with open(csv_file, 'a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerows(data)
        create_csv(data, csv_file, csv_col())

        page_number += 1

        # Find the next page URL
        next_page = soup.find('a', {'class': 'usa-pagination__button', 'rel': 'next'})
        if next_page:
            next_page_url = next_page['href']
        else:
            break  # Stop if there is no next page


    print("Data has been scraped and saved to", csv_file)
