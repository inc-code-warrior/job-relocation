from selenium import webdriver
import datetime
import csv
import linkedin as li
import time

start_url = "https://www.linkedin.com/jobs/search/?currentJobId=4215852391&f_E=4&f_TPR=r86400&f_WT=2&geoId=103644278&keywords=Python&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&spellCorrectionEnabled=true"
# todo: store path in shared file
chromedriver_path = "/usr/local/bin/chromedriver-mac-x64/chromedriver"
b = webdriver.Chrome(chromedriver_path)
b.get(start_url)

li.scroll_to_end(b)

filename = f"jobs {datetime.datetime.now()}.csv"
print(filename)
fieldnames = [
    "list_date",
    "company",
    "location",
    "title",
    "link",
    "status",
    "description",
]
header_written = False

i = 1
job = b.find_element_by_xpath(f"//ul[@class='jobs-search__results-list']/li[{i}]")
row = []


def display_job_description(driver, i):
    timeout_secs = 20
    t = 0
    while t < timeout_secs:
        if i > 1:
            other_index = i - 1
        elif i == 1:
            other_index = i + 1
        driver.find_element_by_xpath(
            f"//ul[@class='jobs-search__results-list']/li[{other_index}]"
        ).click()
        time.sleep(1)
        driver.find_element_by_xpath(
            f"//ul[@class='jobs-search__results-list']/li[{i}]"
        ).click()
        if driver.find_element_by_xpath(
            '//section[@class="show-more-less-html"]'
        ).is_displayed():
            return True
        time.sleep(3)
        t += 1
    return False


# todo: change mode to 'a' for appending
with open(filename, "w", encoding="UTF8", newline="") as f:

    i = 1
    job = b.find_element_by_xpath(f"//ul[@class='jobs-search__results-list']/li[{i}]")
    while job:
        job.click()
        display_job_description(b, i)

        description_element = b.find_element_by_xpath(
            '//section[@class="show-more-less-html"]'
        )

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
        description = description_element.text

        if not description:
            description = "description did not load"


        row = {
                "list_date": list_date,
                "company": company,
                "location": location,
                "title": title,
                "link": link,
                "status": "",
                "description": description,
            }

        row = li.filter_job(row)
        if row:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not header_written:
                writer.writeheader()
                header_written = True
            writer.writerow(row)

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
