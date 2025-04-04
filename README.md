# Propylon Document Manager Assessment
The Propylon Document Management Technical Assessment is a web application consisting of:
* A Django/DRF API backend for document management.
* A React frontend for user interaction.

---
This project is designed as a bootstrap for implementing specific features outlined in the assignment.
The following documentation provides setup instructions, development guidance, and additional info for understanding
and extending the implementation.

---
## Features
### File Storage
* Upload files of any type and name.
* Store files at specified URLs with versions.
* Retrieve any version of a file via query parameters.
### Authentication and Permissions
* Only authenticated users can interact with the system. 
* Users cannot access files uploaded by other users.
### Content Addressable Storage
* Retrieval of files using a unique content hash (CAS mechanism).
### Admin Interface
* Manage users, files, and versions through Django's admin panel.
### Unit Testing
* Test coverage for backend.

---
## Getting Started
### Backend API
The backend is built with Django and Django Rest Framework (DRF).
It uses SQLite as the default database and provides essential utilities via Makefile for ease of development.

#### Prerequisites
Python 3.11 is required. Make sure it's installed and added to the system path before proceeding.

#### Setup and Run
Build the virtual environment:
```bash
    make build
```

#### Load sample data
```bash
    make fixtures
```

#### Start the development server

```bash
    make serve
```
The API will run on http://localhost:8001

#### Run Tests
To run the Pytest test suite you can run the command:
```bash
    make test
```

---
### Changes Made
Ensure the `DJANGO_SETTINGS_MODULE` in `manage.py` points to:
```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "propylon_document_manager.site.settings.local")
```

### Frontend Client Development
The frontend is built with React using the Create React App framework. It has been tested with Node v18.19.0.

#### Setup and Run
Ensure you have Node.js installed. You can use nvm to manage Node versions.
Navigate to the frontend directory:
```bash
    cd client/doc-manager
```

Install dependencies:
```bash
    npm install
```

Start the React development server:
```bash
npm start
```

The React client will run on http://localhost:3000 by default.

#### Additional Notes
N/A

### Testing
**Backend Tests:** Run the backend test suite with:
```bash
    make test
```

**Frontend Tests:** To be implemented

---
### Project Highlights
* Modular Design: Separation of concerns between the API backend and the React frontend.
* Authentication: Powered by django-allauth, supporting secure login and user management.
* Custom User Model: Uses email as the unique identifier.
* Admin Interface: Manage users and file versions directly via the Django admin.

---
### Known Issues and Future Improvements
N/A

---
### References
* [Django/DRF Documentation](https://www.django-rest-framework.org/)
* [Create React App Documentation](https://create-react-app.dev/)
* [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django)

---
### License
This project is for assessment purposes and no additional license is provided.
