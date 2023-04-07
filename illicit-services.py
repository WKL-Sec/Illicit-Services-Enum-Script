import argparse
import requests
import sys

def format_phone_number(phone_number):
    characters_to_remove = {'-', '.', '(', ')'}
    return ''.join(char for char in phone_number if char not in characters_to_remove)


def fetch_emails(base_url, email_addresses, headers, proxies, args):
    all_emails = set(email_addresses)

    #print('New email addresses found:')
    request_count = 0
    for email in email_addresses:
        if request_count >= args.max_requests:
            print(f'Maximum limit of {args.max_requests} requests reached.')
            break

        target_url = f'{base_url}emails={email}'
        response = requests.get(target_url, headers=headers, proxies=proxies)
        response.raise_for_status()

        data = response.json()
        for record in data['records']:
            if 'emails' in record:
                new_email = record['emails'][0]
                if new_email not in all_emails:
                    if not args.email_domain or (args.email_domain and new_email.split('@')[-1] == args.email_domain):
                        all_emails.add(new_email)
                        #print(new_email)
        request_count += 1

    print('All email addresses:')
    for email in all_emails:
        print(email)

def main():
    parser = argparse.ArgumentParser(description='Script to generate a URL with GET parameters based on provided arguments and fetch records.')
    parser.add_argument('--first-name', help='First name')
    parser.add_argument('--last-name', help='Last name')
    parser.add_argument('--email', help='Email address')
    parser.add_argument('--username', help='Username')
    parser.add_argument('--phone', help='Phone number')
    parser.add_argument('--address', help='Address')
    parser.add_argument('--license-plate', help='License plate number')
    parser.add_argument('--vin', help='VIN')
    parser.add_argument('--city', help='City')
    parser.add_argument('--state', help='State')
    parser.add_argument('--zip', help='Zip code')
    parser.add_argument('--max-requests', type=int, default=10, help='Maximum number of requests (default: 3)')
    parser.add_argument('--proxy', help='Proxy URL (e.g., http://proxy.example.com:8080)')
    parser.add_argument('--email_domain', type=str, help='Filter emails by domain')
    parser.add_argument('--output_file', type=str, help='CSV file to store the JSON data')


    args = parser.parse_args()

    if not any(vars(args).values()):
        raise ValueError('At least one argument is required.')

    # Format phone number if provided
    if args.phone:
        args.phone = format_phone_number(args.phone)

    base_url = 'https://search.illicit.services/records?wt=json&'

    arg_key_map = {
        'first_name': 'firstName',
        'last_name': 'lastName',
        'email': 'emails',
        'username': 'usernames',
        'phone': 'phoneNumbers',
        'address': 'address',
        'license_plate': 'VRN',
        'vin': 'vin',
        'city': 'city',
        'state': 'state',
        'zip': 'zipCode'
    }

    query_params = '&'.join(f'{arg_key_map[key]}={value}' for key, value in vars(args).items() if key in arg_key_map and value)

    # Check the number of GET parameters
    num_params = query_params.count('&') + 1
    if num_params > 5:
        print("Error: The target URL does not support more than 5 GET parameters. Please reduce the number of arguments.")
        sys.exit(1)

    target_url = f'{base_url}{query_params}'
    print(f'Generated URL: {target_url}')

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    proxies = {'http': args.proxy, 'https': args.proxy} if args.proxy else None

    response = requests.get(target_url, headers=headers, proxies=proxies)
    response.raise_for_status()

    # Parse JSON data
    data = response.json()

    email_addresses = list(set(record['emails'][0] for record in data['records'] if 'emails' in record))

    if args.email_domain:
        email_addresses = [email for email in email_addresses if email.split('@')[-1] == args.email_domain]

    all_emails = set(email_addresses)

    fetch_emails(base_url, email_addresses, headers, proxies, args)

 

if __name__ == '__main__':
    main()