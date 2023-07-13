from datetime import datetime
from dateutil.parser import parse

output = "2023-07-13T19:42:29.056052354Z"
parsed_output = parse(output)
formatted_output = parsed_output.strftime("%Y-%m-%d %H:%M:%S")

print(formatted_output)