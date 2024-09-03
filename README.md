# Chat Application

A real-time chat application built with Django, Django Channels, and Redis.

## Local Setup

Follow these steps to set up the application locally:

### 1. Prerequisites

- Ensure you have Docker installed on your machine.
- Make sure Redis is not running locally if you plan to use Docker for Redis.

### 2. Environment Variables

Create a `.env` file in the root directory of the project and populate it with the following environment variables. Use the `.env(example)` file as a reference for the format.

```toml
# django conf
DEBUG=False
SECRET_KEY=<secret_key>
ALLOWED_HOSTS=<allowed_hosts>
CSRF_TRUSTED_ORIGINS=<csrf_trusted_origins>
CORS_ALLOWED_ORIGINS=<cors_allowed_origins>

# jwt signing
JWT_SIGNING_KEY=<jwt_signing_key>

# redis
REDIS_URI=<redis_uri>
```

### 3. Building and Running the Application
Use the provided build.sh script to build and run the web service in Docker:
```commandline
sh build.sh
```

You can set the `detached_mode` variable to `true` to run the container in detached mode:
```commandline
detached_mode=true sh build.sh
```

`Note:` If you have Redis installed and running locally, make sure to stop the Redis service before starting the Docker container to avoid conflicts. You can stop Redis with the following command:
```commandline
service redis stop
```

### 4. Accessing the Application
Once the application is running, you can access it through your web browser at the address specified in your Docker setup (usually http://localhost:8000).