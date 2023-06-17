from datetime import datetime

class Newsletter:

    def __init__(self) -> None:
        # get current month and year
        current_datetime = datetime.now()

        current_month = current_datetime.month
        current_year = current_datetime.year
        current_day = current_datetime.date().day

        formatted_month = f"{current_month:02}"
        formatted_year = f"{current_year}"

        # create the filename
        filename = f"{formatted_month}-{formatted_year}-newsletter"
        self.filename = filename
        self.month = formatted_month
        self.year = formatted_year
        self.day = current_day