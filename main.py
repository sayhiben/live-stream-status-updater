import re

def check_facebook_live_status(url):
    # TODO: Scrape FB page/profile and determine if it's currently live streaming
    return False

def check_periscope_live_status(url):
    # TODO: Scrape Periscope profile and determine if it's currently live streaming
    return False

def check_twitch_live_status(url):
    # TODO: Scrape Twitch page and return a boolean if it's currently live streaming
    return False

def check_instagram_live_status(url):
    # TODO: Scrape IG page and return a boolean if it's currently live streaming
    return False

PLATFORM_MAPPING = [
    (re.compile('.*facebook\.com.*', re.IGNORECASE), check_facebook_live_status),
    (re.compile('.*periscope\.tv.*', re.IGNORECASE), check_periscope_live_status),
    (re.compile('.*pscp\.tv.*', re.IGNORECASE), check_periscope_live_status),
    (re.compile('.*instagram\.com.*', re.IGNORECASE), check_instagram_live_status),
    (re.compile('.*twitch\.tv.*', re.IGNORECASE), check_twitch_live_status),
]
def get_status_checker(url):
    for regexp, fn in PLATFORM_MAPPING:
        if regexp.match(url):
            return fn

def check_social_account_live_status(social_account_url):
    status_checker = get_status_checker(social_account_url)
    status = status_checker(url)
    return status

def fetch_social_account_urls():
    # TODO: Accept credentials/URL etc. to a Google sheet or CSV or something to get a list of social media account URLs to scrape
    urls = []
    # TODO: Return a list of urls to scrape
    return urls

def update_live_status(social_account_url, status):
    # TODO: Accept a social account url and a status
    # TODO: Update the status in the CSV/google sheet. consider also updating a "last checked" or "last live" timestamp in the sheet (you may need to add one
    pass


# Actually run the program:
# TODO: Set credentials for Google Sheets so we can get the info we need to pass into the above functions
urls = fetch_social_account_urls()
print(f"Updating {len(urls)} social media accounts")

# Loop through urls and collect status info
updated_statuses = {}
for url in urls:
    try:
        status = check_social_account_live_status(url)
        updated_statuses[url] = status
    except:
        print(f"Could not determine status for {url}. Skipping.")

updated_count = 0
for url, status in updated_statuses:
    try:
        update_live_status(url, status)
        updated_count += 1
    except:
        print(f"Could not update status for {url}. Skipping.")

print(f"Finished updating {updated_count} social media accounts")
