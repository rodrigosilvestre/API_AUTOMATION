import datetime

from QA.data.random_data_class import RandomDataClass

"""
BaseObject class is used to generate a base object based on the object_template provided.
Any specific data type that you wish to have generated, has to be added here
"""


class BaseObject:
    def generate_object(self, context, object_template, parsed_data):
        """
        This function will iterate over an object template, created in one of the object classes,
        and set the configurations for given field, depending on what was received from Parsed data.
        Setting the required fields, and values to be generated for each field.
        """
        # Initialize an empty dictionary to store the generated object
        base_object = {}

        # Iterate over each attribute and its corresponding value in the object_template
        for attr, value in object_template.items():
            # Check if the payload_type in parsed_data is "optional_data"
            if parsed_data.get("payload_type") == "optional_data":
                # If true, update the attribute in object_template to be required
                object_template[attr].update({"required": True})

            # If argument is "with" or "without", update the attribute to be required or not
            if parsed_data.get("argument") in ["with", "without"]:
                if parsed_data.get("argument") == "with":
                    required = True
            else:
                required = False
            # Check if there are field specifications for the current attribute
            if parsed_data.get("field_specifications"):
                field_specifications = next(
                    (field for field in parsed_data.get("field_specifications") if field["field_name"] == attr),
                    None,
                )
                if field_specifications:
                    object_template[attr].update({"required": required})

            # Initialize an empty dictionary for the current attribute in the base_object
            base_object[attr] = {}

            # If no field specifications are provided, set the default value for the attribute based on its data type
            if not object_template[attr].get("default"):
                object_template[attr].update({"default": object_template[attr]["type"]})

            # Check if there are field specifications for the current attribute
            if parsed_data.get("field_specifications"):
                field_specifications = next(
                    (field for field in parsed_data.get("field_specifications") if field["field_name"] == attr),
                    None,
                )
                # Check if there are field specifications for the current attribute
                if field_specifications:
                    if field_specifications.get("value"):
                        # Update the attribute's default value with the specified value
                        object_template[attr].update({"default": field_specifications.get("value")})

            # Update the base_object with the current attribute and its specifications
            base_object.update({attr: object_template[attr]})

        # Return the final generated object by updating fields
        return self.assemble_payload(context, base_object, parsed_data)

    def assemble_payload(self, context, object_template, parsed_data):
        """
        This function will iterate over the updated object_template, call the set_field_value function
        and generate the final payload.
        """
        base_object = {}

        for attr, value in object_template.items():
            if value.get("required"):
                base_object[attr] = {}
                base_object[attr] = self.set_field_value(context, value, object_template[attr]["default"])

        return base_object


    def set_field_value(self, context, value, field_specifications):
        """
        This function will generate the value for the given field, it contains a set of pre-defined
        values for each data type, most come from the RandomDataClass.
        You can also set specific enums, so that the value will be generated from the given enum instead of being
        a string of the enum's name.
        """
        rdc = RandomDataClass()
        generated_value = ""
        specification = None

        if field_specifications:
            specification = field_specifications

        if type(specification) == bool:
            generated_value = specification
        elif type(specification) == int:
            generated_value = specification
        elif specification in ["false", "False"]:
            generated_value = False
        elif specification in ["true", "True"]:
            generated_value = True
        elif value["type"] is None or value["type"] == "none":
            generated_value = None
        elif specification == "none":
            generated_value = None
        elif specification == "upper_Limit":
            if value["type"] in ["integer", "float"]:
                generated_value = value["max_value"]
                if "string" in value["type"]:
                    generated_value = str(generated_value)
            elif value["type"] == "string":
                generated_value = rdc.random_string(value["max_length"])
            elif value["type"] == "name":
                generated_value = rdc.random_names(False, None, value["max_length"])
            else:
                generated_value = rdc.random_string(value["max_length"])

        elif specification == "lower_Limit":
            if value["type"] in ["integer", "float"]:
                generated_value = value["min_value"]
                if "string" in value["type"]:
                    generated_value = str(generated_value)
            elif value["type"] == "string":
                generated_value = rdc.random_string(value["min_length"])
            elif value["type"] == "name":
                generated_value = rdc.random_names(False, None, value["min_length"])
            else:
                generated_value = rdc.random_string(value["min_length"])

        elif specification == "exceeding":
            if value["type"] in ["integer", "float"]:
                generated_value = value["max_value"] + 1
                if "string" in value["type"]:
                    generated_value = str(generated_value)
            elif value["type"] == "string":
                generated_value = rdc.random_string(value["max_length"] + 1)
            elif value["type"] == "swift":
                generated_value = rdc.random_swift() + "1"
            elif value["type"] == "password":
                generated_value = rdc.random_string(value["max_length"] + 1, True)
            else:
                generated_value = rdc.random_string(value["max_length"] + 1)

        elif specification == "below":
            if value["type"] in ["integer", "float"]:
                generated_value = value["min_value"] - 1
                if "string" in value["type"]:
                    generated_value = str(generated_value)
            elif value["type"] == "password":
                generated_value = rdc.random_string(value["min_length"] - 1, False)
            elif value["type"] == "string":
                generated_value = rdc.random_string(value["min_length"] - 1)
            else:
                generated_value = rdc.random_string(value["min_length"] - 1)

        elif specification == "string":
            generated_value = rdc.random_string(value["min_length"] + 6)

        elif "integer" in str(specification):
            generated_value = rdc.random_number_with_digits(value["min_length"] + 6)
            if "string" in value["type"]:
                generated_value = str(generated_value)

        elif "float" in str(specification):
            generated_value = rdc.random_amount(value["min_value"], value["max_value"] + 100)
            if "negative" in str(specification):
                generated_value = -generated_value
            if "string" in value["type"]:
                generated_value = str(generated_value)

        elif specification == "name":
            generated_value = rdc.random_names(False, None, value["min_length"] + 10)

        elif specification == "email":
            generated_value = rdc.random_emails()

        elif specification == "alphaemails":
            generated_value = rdc.random_alphasights_emails()

        elif specification == "password":
            generated_value = rdc.random_string(value["min_length"], True)

        elif specification == "job":
            generated_value = rdc.random_jobs()

        elif specification == "datetime" in specification and "datetime" in value["type"]:
            time_delta = {
                "datetime_tomorrow": 1,
                "datetime_yesterday": -1,
                "datetime_fortnight": 14,
                "date": 0,
            }
            generated_value = rdc.get_formatted_datetime(time_delta[specification])

        elif "date" in specification and "date" in value["type"]:
            time_delta = {
                "date_tomorrow": 1,
                "date_yesterday": -1,
                "date_fortnight": 14,
                "date": 0,
            }
            today = datetime.datetime.now()
            if today.weekday() == 4:
                time_delta["date_tomorrow"] = 3
            generated_value = rdc.get_formatted_date(time_delta[specification])

        elif specification == "country_code":
            generated_value = "US"

        elif specification == "state":
            generated_value = rdc.random_state("US")

        elif specification == "account_number":
            generated_value = rdc.random_account_number()

        elif specification == "address":
            generated_value = rdc.random_address()

        elif specification == "passport":
            generated_value = rdc.random_passport()

        elif specification == "swift":
            generated_value = rdc.random_swift()

        elif specification == "city":
            generated_value = rdc.random_city()

        elif specification == "country":
            generated_value = rdc.random_country()

        elif specification == "empty":
            if "list" in value["type"]:
                generated_value = []
            elif "string" in value["type"]:
                generated_value = ""
            elif "integer" in value["type"]:
                generated_value = 0
            elif "float" in value["type"]:
                generated_value = 0.0
        else:
            generated_value = specification

            if "list" in value["type"]:
                if type(specification) is not list:
                    generated_value = [generated_value]
            if "dict" in value["type"]:
                if type(specification) is not dict:
                    generated_value = {generated_value: generated_value}
            elif "string" in value["type"]:
                generated_value = str(generated_value)
            elif "integer" in value["type"]:
                generated_value = int(generated_value)
            elif "float" in value["type"]:
                generated_value = float(generated_value)

        return generated_value
