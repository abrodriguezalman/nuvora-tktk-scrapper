from keyword_scrapper import keyword_search

keyword = input("Enter search words (if multiple, separate with ','):")
entries = int(input("Enter number of desired results (no commas or decimals):"))

if "," in keyword:
    kword_list = keyword.split(",")

    for h in kword_list:
        try:
            keyword_search(h.lower().strip().replace(" ","+"), entries)
        except Exception as e:
            print(f"\nUnexpected Error Occured: {e}")
        finally:
            print("Program finished.")
else:
    try:
        keyword_search(keyword.lower().strip().replace(" ","+"), entries)
    except Exception as e:
        print(f"\nUnexpected Error Occured: {e}")
    finally:
        print("Program finished.")