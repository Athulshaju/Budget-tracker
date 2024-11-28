Personal Budget Tracker with Authentication and RBAC
Project Overview
This project is a web-based personal budget tracker built using the Django framework. It allows users to manage their financial data securely with features like dynamic dashboards, authentication, and role-based access control (RBAC). The project demonstrates secure system design principles by implementing authentication, authorization, and RESTful APIs.

Features
Authentication: User registration, login, and logout with secure session management.
Role-Based Access Control (RBAC): Role-specific permissions (e.g., Admin, Regular User) to control access to resources.
Dynamic Dashboard: Displays income, expenses, and EMIs, with filtering options for recent transactions.
RESTful APIs: CRUD operations for managing financial data, secured with token-based authentication.
Swagger API Documentation: Interactive documentation for API testing and integration.
Postman Tested: Endpoints tested using Postman for reliability.
Technologies Used
Backend: Django, Django REST Framework
Database: SQLite (default) / PostgreSQL (optional for production)
Authentication: Token-based (Django Rest Framework SimpleJWT)
API Documentation: Swagger/OpenAPI
Tools: Postman for API testing
Getting Started
Prerequisites
Ensure you have the following installed on your system:

Python 3.8+
Pip (Python package manager)
Virtualenv (recommended)
Git
Setup and Installation
Clone the Repository

bash
Copy code
git clone <repository-url>
cd budget-tracker
Create a Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Apply Migrations

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a Superuser (Admin Account)

bash
Copy code
python manage.py createsuperuser
Run the Development Server

bash
Copy code
python manage.py runserver
Access the Application

Open your browser and navigate to: http://127.0.0.1:8000/
API endpoints are accessible at: http://127.0.0.1:8000/api/
Environment Variables
Create a .env file in the root directory and configure the following:

env
Copy code
SECRET_KEY=<your-secret-key>
DEBUG=True
DATABASE_URL=<your-database-url>  # Optional for production
Testing the APIs
Use Postman or Swagger to test the API endpoints.
Swagger URL: http://127.0.0.1:8000/swagger/
Ensure you authenticate by obtaining a token from the /api/token/ endpoint.
License
This project is licensed under the MIT License.

Contact
For any queries or contributions, reach out to:
Athul
[Your Email Address]

Future Enhancements
Integration with third-party authentication systems (OAuth).
Adding expense category analytics.
Deploying on a cloud platform like AWS or Heroku.
