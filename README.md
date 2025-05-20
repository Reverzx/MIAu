# 📘 Automated Testing of the Contact List App (AQA Python) — MIAu

This repository contains a complete automation framework for testing the web application [**Contact List App**](https://thinking-tester-contact-list.herokuapp.com), developed as part of a graduation project in the field of **Automated Quality Assurance** (AQA) using Python.

---

## About the tested application

The **Contact List App** is a demo web-based contact management system that allows users to:

- Register and authorize (auth flow)
- Create, view, update, and delete contacts (CRUD)
- Work with contacts via both UI and REST API

---

## Tech Stack

| Category       | Tools & Libraries               |
|----------------|---------------------------------|
| Language       | Python 3.10+                    |
| Framework      | Pytest                          |
| UI Automation  | Selenium WebDriver              |
| API Automation | Requests, JSON chema validation |
| Architecture   | Page Object Model (POM)         |
| CI/CD          | GitHub Actions                  |
| Reporting      | Allure                          |
| Docs / Planning| Kaiten                          |

---

## 📂 Project Structure
```
MIAu/
├── .github
│   ├── workflows
│   │   ├── flake8.yaml
│   │   ├── ...
├── api_actions
│   │── add_contact_and_get_id.py
│   │── ...
├── pages
│   │── base_page.py
│   │── ...
├── test
│   ├── API
│   └── UI
├── test_data
├── conftest.py
├── requirements.txt 
├── .gitignore
└── README.md 
```

## How to install
1. Clone this repository: git clone <URL>
2. Create virtual environment, activate it: pip install virtualenv
3. Install dependencies: pip install -r requirements.txt

## How to run tests
1. All tests: pytest -v -s
2. API tests: pytest -v -s -m "api"
3. Regression suite: pytest -v -s -m "regression"
4. Expected failures (xfail): pytest -v -s -m "xfail"
5. UI tests: pytest -v -s -m "ui"

## CI/CD & Reports
To generate a report locally:

1. pytest --alluredir=allure-results 
2. allure serve allure-results
