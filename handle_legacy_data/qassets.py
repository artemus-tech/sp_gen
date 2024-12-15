def parse_q_range(input_string):
    # Extract the part inside the square brackets
    prefix, range_part = input_string.split("[")
    range_part = range_part.rstrip("]")  # Remove the closing bracket

    # Split the range into minimum and maximum
    qmin, qmax = range_part.split(",")

    # Construct the desired output string
    result = f"{prefix}min={qmin}_qmax={qmax}"
    return result


import re


def replace_q_range_in_text(large_text):
    # Define the regex pattern to find q[min,max]
    pattern = r"q\[(\d+(\.\d+)?),(\d+(\.\d+)?)\]"

    # Define the replacement format using captured groups
    replacement = r"qmin=\1_qmax=\3"

    # Replace all matches with their transformed format
    result = re.sub(pattern, replacement, large_text)
    return result


# Example usage
large_text = "This is some text with the range q[0.02,5.0] embedded in it. Another range q[1.5,10.0] exists too."
output = replace_q_range_in_text(large_text)
print(output)
