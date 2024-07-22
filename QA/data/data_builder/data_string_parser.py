import re


class DataStringParser:
    """
    This class is used to parse a data string in the following format:

    <payload_type> <argument>: <field_name> <parameter> <value>; <field_name_2>...;'

    It will extract all data specifications that will be used by the data builder class in order to specify what data to build.
    It returns all extracted fields in a dict format, as follows:

    data_structure = {
        "payload_type": "<str required>",
        "argument": "<str required>",
        "field_specifications": [
            {
                "field_name": "<str required>",
                "parameter": "<str optional>",
                "value": "<str optional>",
            }
        ]
    }
    """

    def __init__(self):
        """
        Enums are specified here for validation purposes, if a behavior is to be added at a later date, please add it here as well, otherwise the parser will throw error messages.
        """
        self.payload_type_enums = ["base_data", "optional_data"]
        self.argument_enums = ["with", "without"]
        self.parameter_enums = [
            "as",
            "exceeding",
            "below",
            "upper_limit",
            "lower_limit",
            "invalid",
            "empty",
            "updated",
        ]
        self.structure_error_message = (
            "{1}Please make sure you are following the data structure specified in the documentation: {0}\n"
            "{2}<payload_type> <argument>: <field_name> <parameter> <value>; <field_name_2>...;\n"
        )
        self.data_structure = {}

    def validate_payload_type(self, payload_type):
        for item in payload_type:
            assert item in self.payload_type_enums, (
                f"{item} is not a valid preset payload type\n"
                f"Valid payload types are: {self.payload_type_enums}\n\n{self.structure_error_message}"
            )

    def validate_argument(self, argument):
        for item in argument:
            assert item in self.argument_enums, (
                f"{item} is not a valid preset argument\n"
                f"Valid arguments are: {self.argument_enums}\n\n{self.structure_error_message}"
            )

    def validate_parameter(self, parameter):
        for item in parameter:
            assert item in self.parameter_enums, (
                f"{item} is not a valid preset parameter\n"
                f"Valid parameters are: {self.parameter_enums}\n\n{self.structure_error_message}"
            )

    def extract_payload_type(self, data):
        """
        This method extracts the payload type from the data string and validates it.
        """
        payload_type = re.findall(r"^\w+", data)
        self.validate_payload_type(payload_type)
        self.data_structure["payload_type"] = payload_type[0]

    def extract_argument(self, data):
        """
        This method extracts the argument from the data string and validates it.
        """
        argument = re.findall(r"\s(\w+)\:", data)
        self.validate_argument(argument)
        self.data_structure["argument"] = argument[0]
        self.data_structure["field_specifications"] = []

    def extract_field_specifications(self, data):
        """
        This method extracts the field specifications from the data string and validates it.
        Firstly it looks for the format of field specifications, if there is more than one in the data.
        If there is more than one, it will match the following pattern: '<field_name> <parameter> <value>;'
        and repeat until all field specifications are extracted.
        If there is only one field specification, it will match the following pattern:
        '<field_name> <parameter> <value>' and extract the field specification.
        After that the loop will extract the field name, parameter and value from each extracted string and save it to the data_structure dict if the value is present.
        """
        if "/" in data:
            field_specifications = re.findall(r"(\w* *\w* *\w*/*\w*);+", data)
        elif ";" in data:
            field_specifications = [
                                    "".join(item) for item in re.findall(r"(\w* *\w* *([-]?\d*\.\d+|[-+]?|\w)+);", data)
                                    ]
        else:
            field_specifications = [",".join(item) for item in
                                    re.findall(r"(\w* *\w* *([-]?\d*\.\d+|\d+|[-]?|\w)+)$", data)
                                    ]

        if not field_specifications or (not len(field_specifications)):
            raise IndexError(self.structure_error_message)

        for item in field_specifications:
            field_specifications_dict = {}

            field_name = re.findall(r"(\w+) *\w* *\w*", item)
            field_specifications_dict["field_name"] = field_name[0]

            parameter = re.findall(r"\w+ +(\w+) *", item)
            if len(parameter):
                self.validate_parameter(parameter)
                field_specifications_dict["parameter"] = parameter[0]

            fields = item.split(" ")
            if len(fields) > 1:
                value = fields[-1]
                field_specifications_dict["value"] = value

                if "/" in value:
                    value = value.split("/")
                    field_specifications_dict["value"] = value

            self.data_structure["field_specifications"].append(field_specifications_dict)

    def string_parser(self, data):
        try:
            if ":" in data:
                self.extract_payload_type(data)
                self.extract_argument(data)
                self.extract_field_specifications(data)
            else:
                self.validate_payload_type([data])
                self.data_structure["payload_type"] = data
            return self.data_structure
        except IndexError:
            raise IndexError(self.structure_error_message)
