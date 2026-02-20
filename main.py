from hash_scrapper import hashtag_search

hashtag = input("Enter search hashtag(s) (no #; if multiple, separate with ','):")
entries = int(input("Enter number of desired results (no commas or decimals):"))

if "," in hashtag:
    hash_list = hashtag.split(",")

    for h in hash_list:
        try:
            hashtag_search(h.lower().replace(" ",""), entries)
        except Exception as e:
            print(f"\nUnexpected Error Occured: {e}")
        finally:
            print("Program finished.")
else:
    try:
        hashtag_search(hashtag.lower().replace(" ",""), entries)
    except Exception as e:
        print(f"\nUnexpected Error Occured: {e}")
    finally:
        print("Program finished.")