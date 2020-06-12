
def check_social_account_live_status(social_account_url):
    # TODO: Accept a social_account_url, scrape the page and determine if the social account is currently live streaming
    status = False
    # TODO: return a boolean of whether or not the social account is currently live streaming
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
