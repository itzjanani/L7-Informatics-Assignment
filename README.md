
# L7-Informatics-Assignment

A Flask-based web application to track daily expenses, manage category-wise budgets, and generate monthly financial reports. This repository is part of the L7 Informatics Internship Assignment.

### 🔹 Full Application Walkthrough  
[![Watch the Full Demo](https://raw.githubusercontent.com/itzjanani/L7-Informatics-Assignment/refs/heads/main/demo/Overall%20Flow%20of%20the%20Website.png))](https://youtu.be/mKalzQkTQmY)

### 🔹 Email Alert Functionality  
[![Watch Email Alert Demo](https://img.youtube.com/vi/VIDEO_ID_2/0.jpg)](https://youtu.be/Wf00dvAKbz0)

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Setup & Execution](#repository-setup--execution)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Application Features](#application-features)
- [Edge Case Handling](#edge-case-handling)
- [Coding Standards](#coding-standards)
- [Evaluation Notes](#evaluation-notes)
- [Demo Walkthrough](#demo-walkthrough)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Project Overview

This application enables individual users to:

- Log daily expenses with category and date.
- Set category-wise monthly budgets.
- Automatically track spending against budgets.
- View monthly summary reports.
- Handle common edge cases (e.g., invalid inputs, budget breaches).
- Focus on backend logic using Python and Flask (minimal front-end).

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

## Application Features

- Expense Logging: Input expense amount, category, and date.
- Budget Management: Set and manage monthly budgets per category.
- Monthly Reports: Summarize spending per category vs. budget.
- Spending Alerts: Notify when spending exceeds budget limits.
- Minimal UI: Clean and functional HTML interface.

## Edge Case Handling

- Validation for negative or zero expense amounts.
- Error messages for missing or invalid form inputs.
- Duplicate entries handled and aggregated correctly.
- Alerts when spending goes over budget.
- Graceful handling of 404 and other route errors.

## Coding Standards

- Adheres to Python's PEP8 standards.
- Clean and modular Flask code.
- Functions are named clearly with comments where needed.
- Backend-focused with logically structured routes and validations.

## Evaluation Notes

- This is a public GitHub repository as required by the L7 Informatics assignment.
- Evaluators can simply clone the repo and follow this README to run the app.
- Focus has been placed on backend functionality and edge case handling.
- Minimal time was spent on CSS and front-end design, as per instructions.
- All key features and validations are documented above for easy scoring.

## Demo Walkthrough

- Open the browser and go to `http://127.0.0.1:5000/` after running the app.
- Use the registration page to create a user account.
- Login and begin adding expenses under different categories.
- Set a monthly budget under the “Set Monthly Budget” section.
- Add group expenses by creating a group and adding members, then log shared expenses to see automatic splitting.
- View all expenses and budgets in structured tables on the dashboard.

## Future Enhancements

- Add password encryption and secure session management.
- Introduce email notifications for low budget alerts.
- Add chart visualizations (e.g., pie and bar charts) for spending insights.
- Allow exporting data to CSV or PDF reports.
- Improve mobile responsiveness and styling.

## Contributing

This repository is maintained by Janani as part of the L7 Informatics Internship. While direct contributions are not open, suggestions and feedback are welcome via GitHub Issues.
