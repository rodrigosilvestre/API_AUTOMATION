import random
from datetime import datetime, timedelta
import faker
import pycountry


class RandomDataClass:
    def __init__(self):
        self.fake = faker.Faker()
        self.country_code = None

    def random_number_with_digits(self, digits=1):
        return self.fake.random_number(digits, True)

    def random_string(self, chars: object = 1, special_chars: object = False) -> object:
        if special_chars:
            return self.fake.password(chars, special_chars)
        else:
            return self.fake.pystr(chars, chars)

    def random_names(self, dot_separator=False, number_of_surnames=None, desired_length=None):
        names = self.fake.first_name_nonbinary()
        if number_of_surnames:
            for _ in range(number_of_surnames):
                names += f" {self.fake.last_name_nonbinary()}"
        if desired_length:
            for _ in range(desired_length):
                names += f" {self.fake.last_name_nonbinary()}"
            if len(names) > desired_length:
                names = names[:desired_length]
        if dot_separator:
            names = names.replace(" ", ".")
        return names

    def random_amount(self, min_amount=0, max_amount=999999.99):
        return round(random.uniform(min_amount, max_amount), 2)

    def random_emails(self):
        return self.fake.ascii_email()

    def random_alphasights_emails(self):
        return f"{self.random_names(True, 1)}@alphasights.com"

    def random_jobs(self):
        return self.fake.job()

    def get_formatted_datetime(self, days_from_now=0):
        datetime_now = datetime.now()
        final_datetime = datetime_now + timedelta(days=days_from_now)
        return str(final_datetime.isoformat()) + "Z"

    def get_formatted_date(self, days_from_today=0):
        date_today = datetime.now().date()
        final_date = date_today + timedelta(days=days_from_today)
        return str(final_date.isoformat())

    def random_swift(self):
        return self.fake.swift()

    def random_account_number(self):
        return self.fake.iban()

    def random_state(self, country_code):
        country = pycountry.countries.get(country_code)
        subdivisions = list(pycountry.subdivisions.get(country.alpha_2))
        state_codes = [subdivision.code for subdivision in subdivisions]
        state_code = random.choice(state_codes)
        return state_code.split("-")[-1]

    def random_passport(self):
        return self.fake.passport_number()

    def random_address(self):
        return self.fake.address().replace("\n", " ").split(",")[0]

    def random_city(self):
        return self.fake.city()

    def random_country(self):
        return self.fake.country()
