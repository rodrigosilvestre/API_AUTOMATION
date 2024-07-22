from QA.data.data_validator.validation_classes.base_validator import BaseValidator
from QA.data.helper import print_assert


class RegisterValidation(BaseValidator):
    def build_post_validator(self, context, data, response):
        expected_message = "Note: Only defined users succeed registration"
        assert str(response["error"]) == expected_message, print_assert(
            expected_message,
            response["error"],
        )

