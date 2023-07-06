import requests
import base64

url = 'https://checkout.paycom.uz/base64(m=649d672a94aff0d52dbda578;ac.test=195;a=5000)'

# Extract the Base64-encoded part from the URL
encoded_data = url.split('base64(', 1)[1].split(')', 1)[0]

# Decode the Base64-encoded data using 'latin-1' encoding
decoded_data = base64.b64decode(encoded_data).decode('latin-1')

# Append the decoded data as a query parameter
full_url = f"{url.split('base64(')[0]}?data={decoded_data}"

# Send the HTTP GET request
response = requests.get(full_url)

# Process the response as needed
print(response.text)
