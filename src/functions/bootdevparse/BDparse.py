import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from src.db.BDDB import BDDB

class BDParser:
    def __init__(self):
        pass
    
    def crawl_data(self):
        url = 'https://boot.dev/leaderboard'
        response = requests.get(url)
        return response.text

    # def save_html(self, file_name):
    #     file_path = os.path.join(os.getcwd(), file_name)
    #     with open(file_path, 'w') as file:
    #         file.write(self.html)

    def parse_html(self, html):
        
        unsorted_entries = []
        
        soup = BeautifulSoup(html, 'html.parser')
        arcanum_section = soup.find('h2', string='Archmage Arcanum').find_parent('div', class_='px-4')

        if arcanum_section is None:
            print("Error: 'Archmage Arcanum' section not found on the webpage.")
            exit(1)

        for item in arcanum_section.find_all('div', class_='glassmorph'):
            rank = item.find('span', class_='text-xl').text.strip()
            name = item.find('p', class_='truncate').text.strip()
            username = item.find('p', class_='text-left').text.strip()
            date = item.find('span', class_='ml-3').text.strip()
            unsorted_entries.append((rank, name, username, date))
            
        return unsorted_entries

    def sort_entries(self, entries):
        entries.sort(key=lambda x: datetime.strptime(x[3], '%m/%d/%Y'))

    def reassign_ranks(self, entries):
        for i, entry in enumerate(entries, start=1):
            entries[i-1] = (i, entry[1], entry[2], entry[3])

    def write_to_db(self, entries):
        bddb = BDDB()
        bddb.insert_leaderboard(entries)


    @staticmethod
    def start():
        parser = BDParser()
        try:
            html = parser.crawl_data()
            entries = parser.parse_html(html)

            parser.sort_entries(entries)
            parser.reassign_ranks(entries)
            parser.write_to_db(entries)

            print("Data crawled successfully.")
        except Exception as e:
            print(f"Failed to crawl data: {e}")
            return

        # try:
        #     parser.save_html('BDraw.html')
        #     print("HTML saved successfully.")
        # except Exception as e:
        #     print(f"Failed to save HTML: {e}")
        #     return

        # try:
        #     parser.parse_html() # 30 entries
        #     print("HTML parsed successfully.")
        # except Exception as e:
        #     print(f"Failed to parse HTML: {e}")
        #     return

        # try:
        #     parser.sort_entries()
        #     print("Entries sorted successfully.")
        # except Exception as e:
        #     print(f"Failed to sort entries: {e}")
        #     return

        # try:
        #     parser.reassign_ranks()
        #     print("Ranks reassigned successfully.")
        # except Exception as e:
        #     print(f"Failed to reassign ranks: {e}")
        #     return

        # try:
        #     parser.write_to_csv('BDparsed.csv')
        #     print("CSV written successfully.")
        # except Exception as e:
        #     print(f"Failed to write CSV: {e}")
        #     return
    
