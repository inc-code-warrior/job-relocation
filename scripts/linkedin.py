import time

def scroll_to_end(browser):
    scroll_pause_time = 1
    screen_height = browser.execute_script("return window.screen.height;")
    i = 1
    while True:
        # scroll one screen height each time
        browser.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(
                screen_height=screen_height, i=i
            )
        )
        i += 1
        time.sleep(scroll_pause_time)

        see_more_button = browser.find_element_by_xpath("//button[@aria-label='See more jobs']")
        if see_more_button.is_displayed():
            see_more_button.click()

        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = browser.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

def filter_job(job):
    # keys: list_date, company, location, title, link, status, description

    title_blacklist = {'manager', 'java', 'c++', 'c#', '.net'}
    required = {'python'}

    # todo: handle splitting on multiple special characters but still work with c#, c++, etc.
    title = set(job['title'].lower().split())
    if len(title.intersection(title_blacklist)) > 0:
        return None
    
    for r in required:
        if r not in job['description']:
            return None

    return job