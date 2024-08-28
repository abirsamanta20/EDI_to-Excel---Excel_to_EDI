import datetime

# Define your ISA dictionary
# header_dictionary = {
#     'sender_id': '571099948',
#     'receiver_id': '481244306',
#     'Internal_ctrl_No': '000179621',
#     'group_control_number': '100549',
#     'industry_identifier_code': '005010X220A1'


# }


medicare_dictionary = {
    'referrence_identification': 'S20240205170014'
}

common_parts_of_transaction = {
    'Author Info Qualifier': '00',
    'Author Information': ' ',
    'Security Info Qualifier': '00',
    'Security Information': ' ',
    'Interchange Sender Id Qualifier': '30',
    'Interchange Sender Id': '571099948',
    'Interchange Receiver Id Qualifier': '30',
    'Interchange Receiver Id': '481244306',
    'Interchange Date': '240205',
    'Interchange Time': '1718',
    'Inter Control Version Number': '00501',
    'Inter Control Number': '000179621',
    'Acknowledgment Requested': '1',
    'Interchange Usage Indicator': 'P',
    'Functional Id Code': 'BE',
    'Group Control Number': '100549',
    'Implementation Convention Reference': '005010X220A1',
    'Transaction Set Purpose Code': '00',
    'Transaction Set Reference Number': 'S20240205170014',
    'Transaction Date': '20240205',
    'Transaction Time': '170014',
    'Time Zone Code': 'ET',
    'Action Code': '2',
    'Vendor Name': 'Benefitfocus.com, Inc.',
    'Vendor Id Code Qualifier': 'FI',
    'Vendor Id': '571099948'
}

# current_datetime = datetime.datetime.now()
# isa_dictionary['date'] = current_datetime.strftime("%Y-%m-%d")  
# isa_dictionary['time'] = current_datetime.strftime("%H:%M:%S")  


# print(isa_dictionary)
