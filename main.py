from keyword_scrapper import keyword_search

mode = input("Enter search mode ('K' for keyword search, 'H' for hashtag search:)")
keyword = input("Enter search words (if multiple, separate with ','):")
entries = int(input("Enter number of desired results (no commas or decimals):"))
join = input("Would you like to join the keyword and user data results? (Yes/no):")

while mode.strip() != 'K' and mode.strip() != 'H':
    print("Invalid input. Please enter a valid search mode.")
    mode = input("Enter search mode ('K' for keyword search, 'H' for hashtag search:)")

toJoin = "yes" in join.lower()

if "," in keyword:
    kword_list = keyword.split(",")

    for h in kword_list:
        try:
            if mode.strip() == 'K':
                keyword_search(mode.strip(), h.lower().strip().replace(" ","+"), entries, toJoin)
            else:
                keyword_search(mode.strip(), h.lower().replace(" ",""), entries, toJoin)
        except Exception as e:
            print(f"\nUnexpected Error Occured: {e}")
        finally:
            print("Program finished.")
else:
    try:
        if mode.strip() == 'K':
            keyword_search(mode.strip(), keyword.lower().strip().replace(" ","+"), entries, toJoin)
        else:
            keyword_search(mode.strip(), keyword.lower().replace(" ",""), entries, toJoin)
    except Exception as e:
        print(f"\nUnexpected Error Occured: {e}")
    finally:
        print("Program finished.")