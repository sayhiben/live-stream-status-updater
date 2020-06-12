import argparse
import re

import sheets


def parse_args():
    parser = argparse.ArgumentParser(description='Stream status checker.')
    parser.add_argument(
        "--sheetid", help="ID of the Google Sheet, like '1bx...ms'", required=True,
    )
    args = parser.parse_args()
    return args


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


def fetch_social_account_urls(sheets_service, sheet_id):
    return sheets.get_urls(sheets_service, sheet_id)


def update_live_status(sheets_service, sheet_id, social_account_url, status):
    old_status = sheets.update_status(
        sheets_service, sheet_id, social_account_url, status)
    return old_status

    # TODO: Accept a social account url and a status
    # TODO: Update the status in the CSV/google sheet. consider also updating a "last checked" or "last live" timestamp in the sheet (you may need to add one


# Actually run the program:
args = parse_args()

sheets_service = sheets.get_service()
urls = fetch_social_account_urls(sheets_service, args.sheetid)
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
for (url, status) in updated_statuses.items():
    try:
        update_live_status(sheets_service, args.sheetid, url, status)
        updated_count += 1
    except:
        print(f"Could not update status for {url}. Skipping.")

print(f"Finished updating {updated_count} social media accounts")
