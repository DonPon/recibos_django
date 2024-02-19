import datetime

def parse_date_string(date_str):
    try:
        # Try to parse with "/"
        date_object = datetime.datetime.strptime(date_str, '%d/%m/%y')
    except ValueError:
        try:
            # Try to parse with "."
            date_object = datetime.datetime.strptime(date_str, '%d.%m.%y')
        except ValueError:
            try:
                # Try to parse with "/" and full year
                date_object = datetime.datetime.strptime(date_str, '%d/%m/%Y')
            except ValueError:
                try:
                    # Try to parse with "." and full year
                    date_object = datetime.datetime.strptime(date_str, '%d.%m.%Y')
                except ValueError:
                    raise ValueError("Invalid date format")
    return date_object

def flag_one_month_to_date(date_str):
    target_date = date_str

    print(date_str)
    print(datetime.datetime.now())
    # Calculate the difference between the target date and the current date
    difference = target_date - datetime.datetime.now()
    print(f"difference: {difference.days}")
    print(f"timedelta: {datetime.timedelta(days=15)}")
    # Check if the difference is exactly one month
    one_month = datetime.timedelta(days=15)  # Assuming a month has 30 days
    if difference.days == one_month.days:
        return True
    else:
        return False