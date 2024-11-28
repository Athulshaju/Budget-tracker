# Personal Budget Tracker
## Project Overview

This project is a web-based personal budget tracker built using the Django framework. It allows users to manage their financial data securely with features like dynamic dashboards, authentication, and role-based access control (RBAC). The project demonstrates secure system design principles by implementing authentication, authorization, and RESTful APIs.

## Features
* Authentication: User registration, login, and logout with secure session management.
* Role-Based Access Control (RBAC): Role-specific permissions (e.g., Admin, Regular User) to control access to resources.
* Dynamic Dashboard: Displays income, expenses, and EMIs, with filtering options for recent transactions.
* RESTful APIs: CRUD operations for managing financial data, secured with token-based authentication.
* Swagger API Documentation: Interactive documentation for API testing and integration.
* Postman Tested: Endpoints tested using Postman for reliability.

## Technologies Used
* Backend: Django, Django REST Framework
* Database: SQLite (default) / PostgreSQL (optional for production)
* Authentication: Token-based (Django Rest Framework SimpleJWT)
* API Documentation: Swagger/OpenAPI
* Tools: Postman for API testing
## Getting Started
Prerequisites
Ensure you have the following installed on your system:

* Python 3.8+
* Pip (Python package manager)
* Virtualenv (recommended)
* Git
* Setup and Installation
* Clone the Repository

```bash
git clone https://github.com/Athulshaju/Budget-tracker.git
cd budget-tracker
```
Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```
Install Dependencies


```bash
pip install -r requirements.txt
```
Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```
Run the Development Server

```bash
python manage.py runserver
Access the Application
```
Open your browser and navigate to: http://127.0.0.1:8000/





Contact
For any queries or contributions, reach out to:
Athul Shaju
athul.shaju4@gmail.com

## Future Enhancements
- Integration with third-party authentication systems (OAuth).
- Adding expense category analytics.
- Deploying on a cloud platform like AWS or Heroku.