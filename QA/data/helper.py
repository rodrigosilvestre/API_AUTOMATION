from datetime import datetime


def print_assert(expected, received, extra_info=None):
    error_message = f"Expected: {expected} \n Received: {received} \n TimeStamp: {datetime.now().isoformat()}"
    if extra_info:
        error_message += f"\n\tExtra Info: {extra_info}"

    return error_message


def list_diferences(expected, received, extra_info=""):
    key = list(expected.keys())

    diff_list = []
    for item in key:
        if item == "type":
            expected[item] = expected[item].upper()
        if received.get(item) and expected[item] != received[item]:
            diff_list.append(
                {
                    "Expected": expected[item],
                    "Received": received[item],
                }
            )

    return diff_list + f"{extra_info}"
