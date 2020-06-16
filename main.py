import argparse
import base64
import json
import re
import os
import logging

import sheets
from status_checkers import checkers

log = logging.getLogger()
args = None


def parse_args():
    parser = argparse.ArgumentParser(description='Stream status checker.')
    parser.add_argument(
        "--sheetid", help="ID of the Google Sheet, like '1bx...ms'", required=True,
    )
    parser.add_argument(
        "--twitch-client-id", help="Twitch Dev. Application Client Id", required=False,
    )
    parser.add_argument(
        "--twitch-client-secret", help="Twitch Dev. Application Client Secret", required=False,
    )
    return parser.parse_args()


def check_facebook_live_status(url):
    # TODO: Scrape FB page/profile and determine if it's currently live streaming
    return False


def check_periscope_live_status(url):
    # TODO: Scrape Periscope profile and determine if it's currently live streaming
    return False


def check_twitch_live_status(url):
    client_id = args.twitch_client_id
    client_secret = args.twitch_client_secret
    if not (client_id and client_secret):
        log.warning(
            f"The URL '{url}' cannot be fetched. Please pass --twitch-client-id and --twitch-client-secret. See Readme."
        )
        return False

    checker = checkers.TwitchStatusChecker(client_id, client_secret)
    return checker.check_status(url)


def check_instagram_live_status(url):
    # TODO: Scrape IG page and return a boolean if it's currently live streaming
    return False


def check_youtube_live_status(url):
    # TODO: Scrape YT page and return a boolean if it's currently live streaming
    return False


PLATFORM_MAPPING = [
    (re.compile('.*facebook\.com.*', re.IGNORECASE), check_facebook_live_status),
    (re.compile('.*periscope\.tv.*', re.IGNORECASE), check_periscope_live_status),
    (re.compile('.*pscp\.tv.*', re.IGNORECASE), check_periscope_live_status),
    (re.compile('.*instagram\.com.*', re.IGNORECASE), check_instagram_live_status),
    (re.compile('.*twitch\.tv.*', re.IGNORECASE), check_twitch_live_status),
    (re.compile('.*youtube\.com.*', re.IGNORECASE), check_youtube_live_status),
]


def get_status_checker(url):
    for regexp, fn in PLATFORM_MAPPING:
        if regexp.match(url):
            return fn


def check_social_account_live_status(social_account_url):
    status_checker = get_status_checker(social_account_url)
    status = status_checker(social_account_url)
    return status


def fetch_social_account_urls(sheet):
    return sheet.urls()


def update_live_status(sheet, social_account_url, status):
    old_status = sheet.update_status(social_account_url, status)
    return old_status

    # TODO: Accept a social account url and a status
    # TODO: Update the status in the CSV/google sheet. consider also updating a "last checked" or "last live" timestamp in the sheet (you may need to add one


def update_sheet(sheetid):
    # main function to update google sheet
    sheet = sheets.Sheet(sheetid)
    sheets_service = sheets.get_service()
    urls = fetch_social_account_urls(sheet)
    print(f"Updating {len(urls)} social media accounts")

    # Loop through urls and collect status info
    updated_statuses = {}
    for url in urls:
        try:
            status = check_social_account_live_status(url)
            updated_statuses[url] = status
        except TypeError:
            print(f"Could not determine status for {url}. Skipping.")

    updated_count = 0
    for (url, status) in updated_statuses.items():
        try:
            update_live_status(sheet, url, status)
            updated_count += 1
        except:
            print(f"Could not update status for {url}. Skipping.")

    print(f"Finished updating {updated_count} social media accounts")


def gcloud_pubsub(event, context):
    """
    Responds to GCloud pubsub messages
    Used for triggering update_sheet from a Google Cloud function
    """
    pubsub_json = base64.b64decode(event['data']).decode('utf-8')
    pubsub_message = json.loads(pubsub_json)
    update_sheet(pubsub_message['sheetid'])


if __name__ == "__main__":
    # Parse args and run main update_sheet function
    args = parse_args()
    update_sheet(args.sheetid)
