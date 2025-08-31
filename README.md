# Propylon Document Manager Assessment
The Propylon Document Management Technical Assessment is a web application consisting of:
* A Django/DRF API backend for document management.
* A React frontend for user interaction.
---
## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Backend API](#backend-api)
  - [Frontend Client Development](#frontend-client-development)
  - [Testing](#testing)
  - [Managing the app](#managing-the-app)
  - [API Endpoints](#api-endpoints)
  - [Debugging (Development Only)](#debugging-development-only)
  - [Admin Interface](#admin-interface)
  - [Project Highlights](#project-highlights)
  - [Known Issues and Future Improvements](#known-issues-and-future-improvements)
  - [References](#references)

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
This command will load sample data into the database, including a superuser account.
Follow the prompt for the superuser credentials.
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

Copy the `.env.example` file to `.env` and set the `REACT_APP_API_URL` to point to the backend API:
```bash
    cp .env.example .env
```

Start the React development server:
```bash
npm start
```

The React client will run on http://localhost:3000 by default.

---
## Testing
**Backend Tests:** Run the backend test suite with:
```bash
    make test
```

---
## Managing the app

### API Endpoints
The API endpoints are defined in the `urls.py` file of the Django app. The main endpoints include:

#### Admin Interface
- **URL:** `/admin/`
- **Description:** Access the admin panel for managing models.

#### File Versions API
- **Base URL:** `/api/file_versions/`
- **Description:** Endpoints for managing file versions.

#### Actions:
- **GET** `/api/file_versions/`
  - List all file versions.
  - Optional: Filter by `file_path` (e.g., `/api/file_versions/?file_path=/example/path`).
- **GET** `/api/file_versions/<id>/`
  - Retrieve a specific file version by `id`.
- **POST** `/api/file_versions/`
  - Create a new file version.
  - **Request Body:** 
    - `file_name` (string)
    - `file_path` (string)
    - `file` (file)
- **Permissions:** Authenticated users only.

### Authentication
**Session-Based Authentication**
- **URL:** `/api-auth/` 
- **Description:** Login and session authentication endpoints provided by DRF.
- **Token-Based Authentication**
- **URL:** `/auth-token/`
- **Description:** Obtain tokens for secure API requests.

### Debugging (Development Only)
**Debug Toolbar**
- **URL:** `/__debug__/`
- **Description:** Debugging interface available during development.

### Admin Interface
The Django admin interface is available at:
```
http://localhost:8001/admin
```
Login with the superuser credentials created during the setup.

---
## Project Highlights
* Modular Design: Separation of concerns between the API backend and the React frontend.
* Authentication: Powered by django-allauth, supporting secure login and user management.
* Custom User Model: Uses email as the unique identifier.
* Admin Interface: Manage users and file versions directly via the Django admin.
* File Uploads: Supports file uploads with versioning.

---
## Known Issues and Future Improvements
File uploads are currently prohibited to be with the same file name and same content.
This is a limitation of the current implementation. Future improvements could include:
* Implementing a more robust file versioning system.
* Addition of unit tests for the frontend.
* Implementation of a more user-friendly file upload interface.
* Enhancement of error handling and user feedback in the frontend.
* Implementation of a more sophisticated authentication mechanism (e.g., JWT).
* Addition of a more comprehensive API documentation.
* Implementation of a caching mechanism for file retrieval to improve performance.
* Integration with a cloud storage solution for file management.
* Implementation of a search functionality for files.
* Improvement of the UI/UX for better user experience.

---
## References
* [Django/DRF Documentation](https://www.django-rest-framework.org/)
* [Create React App Documentation](https://create-react-app.dev/)
* [Cookiecutter Django](https://github.com/cookiecutter/cookiecutter-django)

---
## License
This project is for assessment purposes and no additional license is provided.
