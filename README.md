# Illicit-Services-Enum-Script

This script generates a URL with GET parameters based on the provided arguments and fetches records from the Illicit Services API. It helps you search and filter email addresses based on various parameters such as first name, last name, username, phone number, address, etc. It also supports filtering emails by domain and limiting the number of requests. 

The script uses the API from the following site:

Illicit Services
- https://search.illicit.services/

Blog Post
- [Unveiling OSINT Techniques: Exploring LinkedIn, Illicit Services, and Dehashed for Information Gathering](https://whiteknightlabs.com/2023/04/15/unveiling-osint-techniques-exploring-linkedin-illicit-services-and-dehashed-for-information-gathering/)

Requirements
To run the script, you need to install the following Python packages:

- argparse
- requests
You can install these packages using pip:

```bash
pip install argparse requests
```

## Usage
To run the program, use the following command format:

```bash
python3 illicit-services.py --email test@example.com --max-requests 2 --email_domain example.com
```

### Command Line Arguments

The script supports the following command line arguments:

```bash
--first-name: First name
--last-name: Last name
--email: Email address
--username: Username
--phone: Phone number
--address: Address
--license-plate: License plate number
--vin: VIN
--city: City
--state: State
--zip: Zip code
--max-requests: Maximum number of requests (default: 3)
--proxy: Proxy URL (e.g., http://proxy.example.com:8080)
--email_domain: Filter emails by domain
--output_file: CSV file to store the JSON data
```
