# Auto Email IP

This project automatically checks the public IP address (both IPv4 and IPv6) of your machine and sends an email notification if the IP address changes. It also logs the IP address changes and clears the log file every 24 hours.

## Features

- Check public IPv4 and IPv6 addresses from multiple sources.
- Send email notifications when the IP address changes.
- Log IP address changes and errors.

## Requirements

- Python 3.x

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/Geek-Roc/auto-public-net
    cd auto-public-net
    ```

2. Configure the email settings in auto_email_ip.py:

    ```python
    host = 'smtp.***.com'
    port = 465
    sender = '***@***.***'
    receiver = ['***@***.***', '***@***.***', '***@***.***']
    pwd = '***'  # Password
    ```

3. Run the script:
    ```sh
    python3 auto_email_ip.py
    ```

## Logging

The script logs messages to auto_email_ip.log. 
The log file is cleared every 24 hours.

## Acknowledgements

This project is based on the original repository: [auto-public-net](https://github.com/Geek-Roc/auto-public-net). Thank you to the original author for their work.

## License

This project is licensed under the MIT License. See the LICENSE file for details.