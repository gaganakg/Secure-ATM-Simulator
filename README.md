# Secure ATM Simulator

This is a Secure ATM Simulator implemented in Python, providing real-time interactive banking features, OTP authentication, and SMS notifications. The simulator ensures a secure and user-friendly banking experience.

## Features

- **Login and Registration:** Users can log in to existing accounts or register new ones.

- **Withdrawal:** Perform cash withdrawals from your account securely.

- **Deposit:** Deposit funds into your account using the provided options.

- **Transaction History:** View a detailed history of your transactions.

- **Check Balance:** Quickly check your account balance.

- **Change PIN:** Change your PIN for added security.

- **Account-to-Account Transfer:** Transfer funds between accounts securely.

- **OTP Authentication:** Enhance security with one-time password (OTP) authentication.

- **SMS Notifications:** Receive SMS notifications for transactions and account updates.

## Setup

1. Install the required dependencies:

    ```bash
    pip install twilio mysql-connector-python rich
    ```

2. Configure Twilio credentials:

    - Replace `number_twilio`, `account_sid`, and `auth_token` with your Twilio phone number, account SID, and authentication token.

3. Set up MySQL database:

    - Install MySQL and create a database named "ATM".
    - Update `mydb` connection parameters in the script (host, user, password) accordingly.

4. Run the ATM simulator:

    ```bash
    python SecureATMSimulator.py

    ```

## Usage

1. Choose between login and registration.
2. Follow the prompts to perform transactions securely.
3. Explore the different banking functionalities.

## Requirements

- Python
- twilio
- mysql-connector-python
- rich
- colorama

## Contributors

- Gagana K G
- Chandana Priya Peddibhotla
- C ujwal


