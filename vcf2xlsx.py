import os
import pandas as pd

version = '1.0.0'


def extract_field(line):
    # Extract field name and value from a line
    if ':' in line:
        parts = line.split(':', 1)
        field = parts[0].strip()
        value = parts[1].strip()
        return field, value
    return None, None

def extract_email_type(line):
    # Extract email type from a line
    if 'type=' in line:
        parts = line.split(';')
        email_type = [p.split('=')[1] for p in parts[1:]]
        return email_type
    return None

def extract_phone_type(line):
    # Extract phone type from a line
    if 'type=' in line:
        parts = line.split(';')
        phone_type = [p.split('=')[1] for p in parts[1:]]
        return phone_type
    return None

def convert_phone_number(phone_number):
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone_number))

    # Handle phone numbers starting with "1"
    if digits.startswith('1'):
        digits = digits[1:]        
        
    # Extract the area code and the remaining digits
    area_code = digits[:3]
    remaining_digits = digits[3:]

    # Format the phone number with hyphens
    formatted_number = f"{area_code}-{remaining_digits[:3]}-{remaining_digits[3:]}"

    return formatted_number

        
def vcf_to_excel(input_directory, output_file):
    vcf_files = [f for f in os.listdir(input_directory) if f.endswith('.vcf')]
    contacts = []

    # Define the desired column order
    column_order = [
        'query', 'ranking', 'fullname', 'url', 'email', 'user', 'phone', 'ip', 'business',
        'fulladdress', 'city', 'state', 'zip', 'country', 'note', 'aka', 'dob', 'gender',
        'info', 'misc', 'lastname', 'firstname', 'middlename', 'friend', 'otherurls',
        'otherphones', 'otheremails', 'case', 'sosfilenumber', 'president', 'sosagent',
        'managers', 'dnsdomain', 'dstip', 'srcip', 'content', 'referer', 'osurl',
        'titleurl', 'pagestatus'
    ]

    for vcf_file in vcf_files:
        # print('vcf_file = %s' %(vcf_file)) # temp 
        with open(os.path.join(input_directory, vcf_file), 'rb') as file:
        # with open(os.path.join(input_directory, vcf_file), 'r', encoding='utf-8') as file:
            content = file.read()

            encodings = ['utf-8', 'latin-1']
            for encoding in encodings:
                try:
                    lines = content.decode(encoding).splitlines()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                print(f"Cannot decode file: {vcf_file}")
                continue   

            contact = {'VCF File': vcf_file}
            for line in lines:
                line = line.strip()
                field, value = extract_field(line)
                if field == 'FN':
                    contact['fullname'] = value
                    contact['info'] = vcf_file  # Assign the file name to 'info'
                elif "TEL" in line:
                    if 'TEL' in line:
                        contact['query'] = value
                        phone = value
                        phone = convert_phone_number(phone)
                        contact['phone'] = phone
                        contact['misc'] = extract_phone_type(line)
                        contact['info'] = vcf_file  # Assign the file name to 'info'
                        
                elif "EMAIL" in line:
                    if field.startswith('EMAIL'):
                        contact['email'] = value
                        contact['misc'] = extract_email_type(line)
                elif field == 'N':
                    name_parts = value.split(';')
                    contact['lastname'] = name_parts[0].strip()
                    contact['firstname'] = name_parts[1].strip()
                elif field == 'NICKNAME':
                    contact['aka'] = value
                elif field == 'NOTE':
                    contact['note'] = value
                elif "displayname=" in line:
                    fullname = ''

                    # Splitting the line based on the '=' character
                    split_line = field.split('=')

                    # Retrieving the value after the '=' character
                    fullname = split_line[1]

                    # fullname = field
                    fullname = line.split('=')[1]
                   
                    
                    contact['url'] = value
                    if ':' in value:
                        url = value.split(':')[1]
                        if 'facebook.com' in url:
                            user = url.split('facebook.com')[1] # .replace('//')
                            if '/' in user:
                                user = user.replace('/', '')
                            contact['user'] = user
                            print(user)                    
                    
                elif "BDAY" in line:
                    contact['dob'] = value    # task               
                elif field == 'ORG':
                    contact['business'] = value                   
                elif "X-SOCIALPROFILE" in line:
                     contact['content'] = line
                     if 'x-user=' in line:
                        user = field
                        # user = field.lstrip('x-user=')
                        # user = user.rstrip(';')
                        contact['user'] = user

            contacts.append(contact)

    df = pd.DataFrame(contacts)

    df['ranking'] = '5 - VCF contact'

    # Add missing columns with blank names
    missing_columns = [col for col in column_order if col not in df.columns]
    for column in missing_columns:
        df[column] = ""

    # Reorder the columns according to column_order
    df = df[column_order]
    df.to_excel(output_file, index=False)
    print(f"Contacts converted and saved to {output_file}")

print('converting phone contacts (*.vcf) to excel')
print('.vcf files should be placed in a Logs sub folder')


# Usage example
input_directory = 'Logs'
output_file = 'contacts_Apple.xlsx'
vcf_to_excel(input_directory, output_file)
