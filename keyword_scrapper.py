from playwright.sync_api import sync_playwright, TimeoutError
from user_scrapper import bulk_user_search
import random
import time
import pandas as pd
import csv
import os

def keyword_search(mode: str, kword: str, num_entries: int, join: bool = True):
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

            if mode == 'K':
                page.goto(
                    f"https://urlebird.com/search/?q={kword}",
                    wait_until="domcontentloaded"
                )
            else:
                page.goto(
                f"https://urlebird.com/hash/{kword}/",
                wait_until="domcontentloaded"
                )

            try:
                page.wait_for_selector("div.thumb.wc", timeout=5000)
            except TimeoutError:
                print("No videos found for this keyword. Exiting.")
                browser.close()
                return
        
            #limit of videos to count, as noted by user
            MAX_VIDEOS = num_entries

            previous_count = page.locator("div.thumb.wc").count()

            print(f"Processing keyword: {kword}...")
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
            print(f"Final total videos for {kword}: ", min(previous_count, MAX_VIDEOS))

        #-- Extra Video data --
            total_videos = min(previous_count, MAX_VIDEOS)
            videos = page.locator("div.thumb.wc")
            extracted_data = []
            users = []

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
                    username = None
                    caption = None

                #-- Visit video to extract full caption TO DO--
                if overlay_link is not None:
                    video_page = None
                    try:
                        video_page = browser.new_page()

                        try:
                            video_page.goto(overlay_link, wait_until="domcontentloaded", timeout=10000)
                        except Exception as e:
                            print(f"video URL navigation failed: {e}")
                            continue

                        try:
                            video_page.wait_for_selector("div.info2", timeout=8000)
                            caption = video_page.locator("div.info2 h1").inner_text()
                        except Exception as e:
                            print(f"Could not scrape full caption, keeping partial. Reason: {e}")

                    except Exception as e:
                        print(f"Unexpected error opening video page: {e}")
                    
                    finally:
                        if video_page:
                            video_page.close()

                        page.wait_for_timeout(random.randint(1000, 2500))
                else:
                    print("video URL failed, URL does not exist.")
                
                extracted_data.append({"video_url": overlay_link,
                    "Username": username,
                    "Video Caption": caption,
                    "time_posted": time_posted,
                    "Video Views": views,
                    "Video Likes": likes,
                    "Video Comments": comments})
                
                if username not in users:
                    users.append(username)

        #-- Save to CSV --
            if not extracted_data:
                print("No data extracted. CSV not created.")
                return
            
            print(f"Saving results to {kword}_videos.csv...")
            keys = extracted_data[0].keys()

            with open(kword + "_videos_" + mode + "_mode.csv", "w", newline="", encoding="utf-8") as f:
                dic_writer = csv.DictWriter(f, keys)
                dic_writer.writeheader()
                dic_writer.writerows(extracted_data)

            print(f"Saved {len(extracted_data)} videos to {kword}_videos_{mode}_mode.csv.")
            pass
        
        finally:
            browser.close()
    #-- Pass users to user_scrapper --      
    bulk_user_search(users, kword, True)

    if (join):
        try:
            df1 = pd.read_csv(f"{kword}_videos_{mode}_mode.csv")
            df2 = pd.read_csv(f"{kword}_users.csv")

            combined_df = pd.merge(df1, df2, on='Username', how='left')
            combined_df.to_csv(f"{kword}_videos_and_users.csv", index=False)

            #delete individual CSVs after merge
            df1_path = f"{kword}_videos_{mode}_mode.csv"
            df2_path = f"{kword}_users.csv"

            # Check if file exists before deleting to avoid errors
            if os.path.exists(df1_path) and os.path.exists(df2_path):
                os.remove(df1_path)
                os.remove(df2_path)
                print(f"{df1_path} and {df2_path} have been deleted.")
            else:
                print("The file does not exist.")
        except:
            print("Could not merge CSVs. Closing program.")
