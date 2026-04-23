import time
import subprocess
from bs4 import BeautifulSoup
import csv
import random

def scrape_property_page(page_adress, sleep_time):
    subprocess.run(["bash", "request_site.bash", page_adress])
    time.sleep(sleep_time)

class Anunt:
    titlu = ""
    sup_teren = 0
    sup_util = 0
    stare = ""
    utlitati = ""
    mobilat = ""
    localitate = ""
    parcare = 0
    bai = 0
    fin_constructie = 0
    tip_tranzactie = ""
    pret = 0

def sanitize(text):
    return text.replace(",", "$") if isinstance(text, str) else text


sleep_time = 2
pages_to_scrape = int(input("How many pages to scrape for links? "))

# Open CSV file once, append rows
with open("homeZZ_data.csv", "a+", newline="", encoding="utf-8") as homeZZ_csv:
    writer = csv.writer(homeZZ_csv, delimiter=';')
    first_char = homeZZ_csv.read(1)
    if not first_char:
    # Write header
        writer.writerow([
            "Titlu", "Localitate", "Suprafata teren", "Suprafata utila",
            "Stare", "Numar camere", "Numar bai", "Mobilat", "Tip tranzactie", "Pret"
        ])

    # Loop through listing pages
    for i in range(1, pages_to_scrape + 1):
        print(f"Scraping page{i} of {pages_to_scrape}")
        sleep_time = random.randrange(50, 300)/100
        page_adress = f"https://homezz.ro/vanzare-case-vile?page={i}"
        scrape_property_page(page_adress=page_adress, sleep_time=sleep_time)

        # Read the listing page HTML
        page = open("output.html", mode="r", encoding="utf-8").read()
        pageSoup = BeautifulSoup(page, "html.parser")
        tags = pageSoup.find_all("a", class_="card-box card-l")
        page_list = [tag.get("href") for tag in tags if tag.get("href")]

        # Loop through each property link
        for index, property in enumerate(page_list):
            sleep_time = random.randrange(50, 300)/100
            print(f"Scraping page for {property}, waiting time: {sleep_time}, {index+1}/{len(page_list)}")
            scrape_property_page(page_adress=property, sleep_time=sleep_time)

            # Read the property page HTML
            property_page = open("output.html", mode="r", encoding="utf-8").read()
            property_pageSoup = BeautifulSoup(property_page, "html.parser")  

            # Create a new instance
            property_instance = Anunt()

            # Extract specifications
            specs_section = property_pageSoup.find("div", id="specifications-section")
            if specs_section:
                specs = specs_section.find_all("p", attrs={"data-test-id": "ad-attribute"})
                for spec in specs:
                    spans = spec.find_all("span")
                    if len(spans) == 2:
                        name = spans[0].get_text(strip=True)
                        value = spans[1].get_text(strip=True)

                        # Map to class attributes
                        if "Suprafață teren" in name:
                            property_instance.sup_teren = value
                        elif "Suprafața utilă" in name:
                            property_instance.sup_util = value
                        elif "Stare" in name:
                            property_instance.stare = value
                        elif "Număr camere" in name:
                            property_instance.utlitati = value
                        elif "Număr Băi" in name:
                            property_instance.bai = value
                        elif "Mobilat și Utilat" in name:
                            property_instance.mobilat = value
                        elif "Tip tranzacție" in name:
                            property_instance.tip_tranzactie = value

            # Extract title
            title_tag = property_pageSoup.find("h1", attrs={"data-test-id": "ad-title"})
            if title_tag:
                property_instance.titlu = title_tag.get_text(strip=True)

            # Extract location
            loc_tag = property_pageSoup.find("p", class_="details")

            if loc_tag:
                direct_text = "".join(loc_tag.find_all(string=True, recursive=False)).strip()
                last_part = direct_text.split("|")[-1].strip()
                property_instance.localitate = last_part

            # Extract price
            price_tag = property_pageSoup.find("div", attrs={"data-test-id": "ad-price"})
            if price_tag:
                property_instance.pret = price_tag.get_text(strip=True)

            # Write the property to CSV
            writer.writerow([
                sanitize(property_instance.titlu),
                sanitize(property_instance.localitate),
                sanitize(property_instance.sup_teren),
                sanitize(property_instance.sup_util),
                sanitize(property_instance.stare),
                sanitize(property_instance.utlitati),
                sanitize(property_instance.bai),
                sanitize(property_instance.mobilat),
                sanitize(property_instance.tip_tranzactie),
                sanitize(property_instance.pret)
            ])
