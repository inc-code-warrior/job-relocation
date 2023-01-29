import time


def scroll_to_end(browser):
    time.sleep(2)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 2
    screen_height = browser.execute_script("return window.screen.height;")
    i = 1
    while True:
        # scroll one screen height each time
        browser.execute_script("window.scrollBy(0, window.innerHeight);")

        see_more_button = browser.find_element_by_xpath(
            "//button[@aria-label='See more jobs']"
        )
        if see_more_button.is_displayed():
            see_more_button.click()

        i += 1
        time.sleep(scroll_pause_time)

        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = browser.execute_script("return document.body.scrollHeight;")
        print('screen_height:', screen_height, 'i:', i, 'scroll_height:', scroll_height)
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break


def filter_job(job):
    # keys: list_date, company, location, title, link, status, description

    title_blacklist = {"manager", "java", "c++", "c#", ".net"}
    required = {"python"}

    # todo: handle splitting on multiple special characters but still work with c#, c++, etc.
    title = set(job["title"].lower().split())
    blacklisted_words_in_title = title.intersection(title_blacklist)
    if len(blacklisted_words_in_title) > 0:
        print(f"FILTERING - Word(s) found in title: {blacklisted_words_in_title}")
        return None

    for r in required:
        if r in job["description"].lower():
            job["description"] = "PYTHON IN DESCRIPTION --- " + job["description"]
            continue
        elif r in job["title"].lower():
            job["description"] = "PYTHON IN DESCRIPTION --- " + job["description"]
            continue
        else:
            print(f'FILTERING - "{r}" not found in description nor title')
            return job

    return job
