from QA.data.data_validator.validation_classes.register_validation import RegisterValidation
from QA.data.data_validator.validation_classes.user_validation import UserValidation
from QA.data.helper import print_assert


class DataValidation:
    def response_status_code(self, context, status_code):
        response_status_code = context.response.status_code
        assert response_status_code == int(status_code), print_assert(
            status_code, response_status_code, f"\n{context.response.text}"
        )

    def check_message_response(self, context, data_validation):
        #
        # This function will select the correct data validator based on the received data
        #
        try:
            response = context.response.json()
        except AttributeError:
            response = context.response
        except ValueError:
            response = "No Data"

        object_name = data_validation

        if "user" in object_name.lower():
            validator = UserValidation()
        elif "register" in object_name.lower():
            validator = RegisterValidation()

        else:
            raise NotImplementedError(f"'{object_name}' validator not yet implemented on data_validation_class.py")

        validator.validate(context, data_validation, response)