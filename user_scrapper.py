from playwright.sync_api import sync_playwright, TimeoutError
import csv

def user_search(user: str, save: bool):
    with sync_playwright() as p:
    #-- Set up new browser and page --
        browser = p.chromium.launch(headless=False, args=[
            "--disable-blink-features=AutomationControlled"
        ])

        try:
            page = browser.new_page()

            page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """)

            page.goto(
                f"https://urlebird.com/user/{user}/",
                wait_until="domcontentloaded"
            )

            try:
                page.wait_for_selector("div.thumb.wc", timeout=5000)
            except TimeoutError:
                print("User has no videos. Exiting.")
                browser.close()
                return

            print(f"Found user: {user}...")

        #-- Load data --
            
            res = {}
            res["Username"] = user
            
            header_items = page.locator("div.row div.col-md-12 div.stats-header div.row.text-center div.col-3.p-0 b")

            try:
                followers = header_items.nth(1).inner_text()
                videos = header_items.nth(3).inner_text()
            except:
                followers = videos = None

            res["Followers"] = followers
            res["Total User Videos"] = videos

            try:
                bio = page.locator("div.row div.col-md-12 div.text-center div.text-center.pl-2.pr-2.pb-3").inner_text()
            except:
                bio = None

            res["Profile biography"] = bio
            
            if not save:
                print(f"bio: {bio}")
                print(f"followers: {followers}")
                print(f"# of videos: {videos}")

            faq_items = page.locator("#faqAccordion .card #collapse2 .card-body ul li")

            for i in range(faq_items.count()):
                try:
                    text = faq_items.nth(i).inner_text()
                except:
                    text = None
                    
                try:
                    value = faq_items.nth(i).locator("span").inner_text()
                except:
                    value = None

                res[f"User {text.split(":")[0]}"] = value

                if not save:
                    print(f"{text.split(":")[0]}: {value}")

            if save:
                keys = res.keys()

                with open("user_" + user + ".csv", "w", newline="", encoding="utf-8") as f:
                    dic_writer = csv.DictWriter(f, keys)
                    dic_writer.writeheader()
                    dic_writer.writerow(res)
            return res
            
        finally:
            browser.close()

def bulk_user_search(users, title, save):
    bulk_data = []
    
    for user in users:
        user_data = user_search(user.lower().strip(), False)

        if not user_data:
            print("No data extracted. user not saved. Continuing")
        else:
            bulk_data.append(user_data)
        
    if save:
        print(f"Saving results to {title}_users.csv...")
        keys = bulk_data[0].keys()

        with open(title + "_users.csv", "w", newline="", encoding="utf-8") as f:
            dic_writer = csv.DictWriter(f, keys)
            dic_writer.writeheader()
            dic_writer.writerows(bulk_data)

        print(f"Saved {len(bulk_data)} videos to {title}_users.csv.")
        pass