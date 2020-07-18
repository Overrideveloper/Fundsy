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
3. Navigate to the `backend` directory.
4. Create a `.env` file.
5. Use the `.env.sample` file in the directory to add the required environment variables:<br>
   - JWT_SECRET => Secret for signing json web tokens
   - ADMIN_NAME => Name of administrator
   - ADMIN_PASSWORD => Password of administrator
   - ADMIN_USERNAME => Username of administrator
   - MIN_WITHDRAWAL => Minimum amount withdrawable<br>
    
    The `ADMIN_NAME`, `ADMIN_PASSWORD` and `ADMIN_USERNAME` will be used to create an admin user at first run. These credentials are to be used to log in as an administrator to the application<br>
   **NOTE**: `ADMIN_PASSWORD` should not be **less than 7 alphanumeric characters**
6. Navigate to the `frontend` directory.
7. Create a `.env` file.
8. Use the `.env.sample` file in the directory to add the required environment variable:<br>
   - VUE_APP_MIN_WITHDRAWAL => Minimum amount withdrawable (This should match MIN_WITHDRAWAL in `backend/.env`)
9. Navigate to the root of the directory
9. Run `docker-compose up`
10. Open `http://<YOUR_MACHINE_IP>:8081` in your browser. You should to see the application running.
11. The backend server will be running at `http://<YOUR_MACHINE_IP>:8100`.
12. You can also access the pgAdmin interface at `http://<YOUR_MACHINE_IP>:5050`.<br>
    The login credentials for the pgAdmin interface in the `docker-compose.yml` file in the `environment` section under the `pgadmin` service.

Note: There is currently no documentation for the backend (API) due to the time constraints. Sorry!