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

def flag_one_month_to_date(date_str, dias=30):
    target_date = date_str

    print(date_str)
    print(datetime.datetime.now())
    # Calculate the difference between the target date and the current date
    difference = target_date - datetime.datetime.now()
    print(f"difference: {difference.days}")
    print(f"timedelta: {datetime.timedelta(days=int(dias))}")
    # Check if the difference is exactly one month
    target_difference = datetime.timedelta(days=int(dias))
    if difference.days == target_difference.days:
        return True
    else:
        return False