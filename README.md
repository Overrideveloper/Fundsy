# Fundsy
Hello there! This, 'Fundsy", is my submission for kudy.io's fullstack developer test.

## Directories
There are two main directories in this project:
- `backend`: This houses the backend of this project.<br>
  The backend is built with Python, FastAPI, Postgres and Redis.

- `frontend`: This houses the frontend of the project.<br>
  The frontend is built with Vue 2 and Typescript.

## How to run
This "guide" assumes you have Docker on your machine.

1. Clone this repository.
2. Navigate to the root of the cloned repository.
3. Open the `docker-compose.yml` file.
4. Under the `environment` section of the `backend` service set the following environment variables:
   - JWT_SECRET
   - ADMIN_PASSWORD
   - ADMIN_USERNAME<br>
  The `ADMIN_PASSWORD` and `ADMIN_USERNAME` will be used to create an admin user at first run. These credentials are to be used to log in as an administrator to the application
5. Run `docker-compose up`
6. Open `http://localhost:8081` in your browser. You should to see the application running.
7. The backend server will be running at `http://localhost:8100`.

Note: There is currently no documentation for the backend (API) due to the time constraints. Sorry!