from QA.data.data_validator.validation_classes.base_validator import BaseValidator
from QA.data.helper import print_assert


class UserValidation(BaseValidator):
    def build_post_validator(self, context, data, response):
        for attr, value in context.data.items():
            assert str(response[attr]) == str(context.data[attr]), print_assert(
                context.data[attr],
                response[attr],
            )

    def build_get_validator(self, context, data, response):
        # Temporary Solution, you can extract the page number from the URI, exemple /api/users?page=2  --> Extract value 2 from page using regex or any other solution
        if "page" in response:
            expected_page = 2
            assert int(response["page"]) == expected_page, print_assert(
                    expected_page,
                    response["page"],
                )

        else:
            mock_id = 2
            assert int(response["data"]["id"]) == mock_id, print_assert(
                mock_id,
                response["id"],
            )
