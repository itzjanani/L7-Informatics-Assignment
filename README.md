
# L7-Informatics-Assignment

A Flask-based web application to track daily expenses, manage category-wise budgets, and generate monthly financial reports. This repository is part of the L7 Informatics Internship Assignment.

### 🔹 Full Application Walkthrough  
[![Watch the Full Demo](https://raw.githubusercontent.com/itzjanani/L7-Informatics-Assignment/refs/heads/main/demo/Overall%20Flow%20of%20the%20Website%20(1).png)](https://youtu.be/mKalzQkTQmY)

### 🔹 Email Alert Functionality  
[![Watch Email Alert Demo](https://raw.githubusercontent.com/itzjanani/L7-Informatics-Assignment/refs/heads/main/demo/email-alert.png)](https://youtu.be/Wf00dvAKbz0)

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Setup & Execution](#repository-setup--execution)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Demo Walkthrough](#demo-walkthrough)
- [Contributing](#contributing)

## Project Overview

This application enables individual users to:

- Log daily expenses with category and date.
- Set category-wise monthly budgets.
- Automatically track spending against budgets.
- Send Email alerts if expenses > 90% monthly allocated budget.
- Handle common edge cases (e.g., invalid inputs, user not found, and so on).
- Focus on backend logic using Python and Flask (minimal front-end).
- Create groups and split group expenses like splitwise.

## Repository Setup & Execution

### 1. Clone the Repository

```bash
git clone https://github.com/itzjanani/L7-Informatics-Assignment.git
cd L7-Informatics-Assignment
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Packages

All required Python dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4. Run the Flask Application

```bash
python app.py
```

You will have your own instance of your local sql db created inside the folder named instances in which the db name is called expenses (expenses.db)

Visit the following URL in your browser to interact with the application:

```
http://127.0.0.1:5000/
```

## Folder Structure

```bash
L7-Informatics-Assignment/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Required Python packages
├── templates/
│   └── index.html         # Basic HTML interface
│   └── login.html         # Basic HTML interface to login
│   └── register.html      # Basic HTML interface to register or sign up
├── utils/
│   └── email_alerts.py    # Basic SMTP server to send Emails  
└── README.md              # Project documentation
```

## Requirements

Below are the dependencies used in this project:

```ini
Flask==2.2.5
```

To update or regenerate this file:

```bash
pip freeze > requirements.txt
```

## Demo Walkthrough

- Open the browser and go to `http://127.0.0.1:5000/` after running the app.
- Use the registration page to create a user account.
- Login and begin adding expenses under different categories.
- Set a monthly budget under the “Set Monthly Budget” section.
- Add group expenses by creating a group and adding members, then log shared expenses to see automatic splitting.
- View all expenses and budgets in structured tables on the dashboard.

## Contributing

This repository is maintained by Janani as part of the L7 Informatics Internship assignment.
