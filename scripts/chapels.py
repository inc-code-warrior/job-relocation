from selenium import webdriver
import csv
import os

district_links, rows = [], []
chromedriver_path = "/usr/local/bin/chromedriver_mac64/chromedriver"
b = webdriver.Chrome(chromedriver_path)
b.get("https://directory.iglesianicristo.net/districts")


# get districts in America
districts = b.find_elements_by_xpath(
    "//h2[contains(text(),'Americas')]/following::ul[1]/child::li/a"
)
for district in districts:
    district_links.append(district.get_attribute("href"))


# loop thru districts
for district_link in district_links:
    b.get(district_link)

    # loop thru locales and get their link, name, district
    locales = b.find_elements_by_xpath(
        "//h2[contains(text(),'Local Congregations')]/following::ul/li/span/a"
    )
    for locale in locales:
        locale_link = locale.get_attribute("href")
        locale_name = locale_link.rsplit("/", 1)[-1]
        district = district_link.rsplit("/", 1)[-1]
        rows.append(
            {
                "district": district,
                "district_link": district_link,
                "locale": locale_name,
                "locale_link": locale_link,
            }
        )


# loop thru locale_links and get address
for i in range(len(rows)):
    b.get(rows[i]["locale_link"])
    address = b.find_element_by_xpath("//address")
    rows[i]["address"] = address.text


# store results in csv
# todo: store in output folder or s3
filename = "locales.csv"
fieldnames = ["district", "district_link", "locale", "locale_link", "address"]
with open(filename, "w", encoding="UTF8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


b.quit()
