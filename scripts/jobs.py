from selenium import webdriver
import datetime
import csv
import linkedin as li

# todo: store path in shared file
chromedriver_path = "/usr/local/bin/chromedriver_mac64/chromedriver"
b = webdriver.Chrome(chromedriver_path)
b.get(
    "https://www.linkedin.com/jobs/search/?currentJobId=3424954364&distance=25&f_E=4&f_TPR=r604800&f_WT=1%2C3&geoId=103644278&keywords=sdet&sortBy=DD"
)

li.scroll_to_end(b)

filename = f"jobs {datetime.datetime.now()}.csv"
print(filename)
fieldnames = ["list_date", "company", "location", "title", "link", "status"]
header_written = False
# todo: change mode to 'a' for appending
with open(filename, "w", encoding="UTF8", newline="") as f:

    i = 1
    job = b.find_element_by_xpath(f"//ul[@class='jobs-search__results-list']/li[{i}]")
    row = []
    while job:
        job.click()
        title = job.find_element_by_xpath(
            ".//descendant::h3[@class='base-search-card__title']"
        ).text
        company = job.find_element_by_xpath(
            ".//descendant::h4[@class='base-search-card__subtitle']"
        ).text
        location = job.find_element_by_xpath(
            ".//descendant::span[@class='job-search-card__location']"
        ).text
        link = job.find_element_by_xpath(".//descendant::a[1]").get_attribute("href")
        list_date = job.find_element_by_xpath(".//descendant::time").get_attribute(
            "datetime"
        )
        description = b.find_element_by_xpath('//section[@class="show-more-less-html"]').text
        print(title, company, location, list_date, link[:50])
        # print(description)

        row = [
            {
                "list_date": list_date,
                "company": company,
                "location": location,
                "title": title,
                "link": link,
                "status": "",
                "description": description,
            }
        ]

        row = li.filter_job(row[0])
        if row:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not header_written:
                writer.writeheader()
                header_written = True
            writer.writerows(row)

        i += 1
        jobs = b.find_elements_by_xpath(
            f"//ul[@class='jobs-search__results-list']/li[{i}]"
        )
        if len(jobs) > 0:
            job = jobs[0]
        else:
            job = None

        # break

b.quit()
