from user_scrapper import user_search, bulk_user_search

user = input("Pass in desired username(s) (if more than one, separate users by comma. No @.): ")
save = input("Would you like to save the results in a CSV file? Type Yes/No: ").lower()

if "," in user:
    user_list = user.split(",")

    try:
        if "yes" in save:
            bulk_user_search(user_list, "custom", True)
        else:
            bulk_user_search(user_list, "custom", False)
    except Exception as e:
        print(f"\nUnexpected Error Occured: {e}")
    finally:
        print("Program finished.")
else:
    try:
        if "yes" in save:
            user_search(user.lower().strip(), True)
        else:
            user_search(user.lower().strip(), False)
    except Exception as e:
        print(f"\nUnexpected Error Occured: {e}")
    finally:
        print("Program finished.")