from playwright.sync_api import sync_playwright, TimeoutError
import random
import time
import csv

def hashtag_search(hash: str, num_entries: int):
    with sync_playwright() as p:
    #-- Set up new browser and page --
        browser = p.chromium.launch(headless=False, args=[
            "--disable-blink-features=AutomationControlled"
        ])

        try:
            print("Launching browser...")
            page = browser.new_page()

            page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            """)

            page.goto(
                f"https://urlebird.com/hash/{hash}/",
                wait_until="domcontentloaded"
            )

            try:
                page.wait_for_selector("div.thumb.wc", timeout=5000)
            except TimeoutError:
                print("No videos found for this hashtag. Exiting.")
                browser.close()
                return
        
            #limit of videos to count, as noted by user
            MAX_VIDEOS = num_entries

            previous_count = page.locator("div.thumb.wc").count()

            print(f"Processing hashtag: #{hash}...")
            print(f"Processing up to {MAX_VIDEOS} videos...")

        #-- Load and count videos --
            while previous_count < MAX_VIDEOS:

                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(random.uniform(2,4))

                load_more = page.locator("text=Load more")

                #if button is not found, code stops
                if load_more.count() == 0:
                    print("Load more button not found.")
                    break
                
                load_more.first.scroll_into_view_if_needed()
                time.sleep(random.uniform(1,2))

                with page.expect_response(lambda r: '/ajax/' in r.url):
                    load_more.first.click(delay=random.randint(100, 300))

                time.sleep(random.uniform(2,4))
                
                new_count = page.locator("div.thumb.wc").count()

                #if the new count is the same as previous, there are no new vids
                if new_count == previous_count:
                    print("no new videos detected. stopping.")
                    break
                
                previous_count = new_count
                    
            #final count of vids
            print(f"Final total videos for #{hash}: ", min(previous_count, MAX_VIDEOS))

        #-- Extra Video data --
            total_videos = min(previous_count, MAX_VIDEOS)
            videos = page.locator("div.thumb.wc")
            extracted_data = []

            for i in range(total_videos):
                video = videos.nth(i)

                try:
                    overlay_link = video.locator("a:has(div.overlay-s)").get_attribute("href")
                except:
                    overlay_link = None
                    
                try:
                    stats = video.locator("div.stats div.flex.items-center.mb-1 span")
                    time_posted = stats.nth(0).inner_text()
                    views = stats.nth(1).inner_text()
                    likes = stats.nth(2).inner_text()
                    comments = stats.nth(3).inner_text()
                except:
                    time_posted = views = likes = comments = None

                try:
                    info = video.locator("div.info3")
                    username = info.locator("div.author-name a").inner_text()
                    caption = info.locator("a span").inner_text()
                except:
                    username = caption = None

                extracted_data.append({"video_url": overlay_link,
                    "username": username,
                    "caption": caption,
                    "time_posted": time_posted,
                    "views": views,
                    "likes": likes,
                    "comments": comments})
                
        #-- Save to CSV --
            if not extracted_data:
                print("No data extracted. CSV not created.")
                return
            
            print(f"Saving results to {hash}_videos.csv...")
            keys = extracted_data[0].keys()

            with open(hash + "_videos.csv", "w", newline="", encoding="utf-8") as f:
                dic_writer = csv.DictWriter(f, keys)
                dic_writer.writeheader()
                dic_writer.writerows(extracted_data)

            print(f"Saved {len(extracted_data)} videos to {hash}_videos.csv.")
            pass
        
        finally:
            browser.close()
