formatting = '0.00 сум'.replace('сум', '').replace(',', '')
formatted_output = f'{float(formatting) * 100:.2f}'
print(formatted_output == '0.00')
