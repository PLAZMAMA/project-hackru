def format_date(date):
    # Get the day and add the appropriate suffix
    day = date.day
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    formatted_date = date.strftime(f"%A, %B {day}{suffix} %Y")
    return formatted_date
