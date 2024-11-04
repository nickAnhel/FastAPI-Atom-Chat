# Atom Chat ⚛️
![Atom Chat](https://raw.githubusercontent.com/nickAnhel/FastAPI-Atom-Chat/refs/heads/main/images/screen.png)
**Atom Chat** is a platform where users can chat in open or private chats. Users can create their own chats, either personal or shared, and join existing communities to exchange thoughts and ideas with people who share their interests.
# Requirements
To start a project, you need to have a number of installed programs and utilities:
- `poetry`
- `python3.12`
- `docker` and `docker-compose`
- `git`
# Local Launching
To run a project on a local machine, follow the steps described below.

First, clone the repository with the project into a pre-created directory. Then go to the `FastAPI-Atom-Chat` directory.

```bash
# Clone repository
git clone https://github.com/nickAnhel/FastAPI-Atom-Chat.git

# Go to new dir FastAPI-Atom-Chat
cd FastAPI-Atom-Chat
```

Create and activate a virtual environment.

```bash
# Create virtual env
python3 -m venv .venv

# Activate it
source .venv/bin/activate
```

Go to the `server` directory.

Install project dependencies. They will be required to run tests and a script to fill the database with test data.

```bash
 # Install project dependencies
poetry install
```

Create private and public encryption keys.

```bash
# Create a dir to store the keys
md certs
cd certs

# Create a private key
openssl genrsa -out private.pem 2048

# Create a public key
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```

Go back to the `server` directory and create the configuration files `.dev.env` and `.test.env` and fill them with your data guided by the files `.dev.env.example` and `.test.env.example`.

Go to the `client/atom_chat` directory and install all frontend dependencies.

```bash
# Go to frontend dir
cd client/atom_chat

# Install all dependencies
npm install
```

Go to the root directory of the project and start it using `docker`.

```bash
# Run project
docker compose up --build
```
# Tests
To run the tests, navigate to the `server` directory and execute the `pytest -v` command, specifying the `tests` directory.

```bash
# Run tests in verbose mode
pytest -v ./tests
```
# Filling with test data
To run the script to fill the database with test data, navigate to the `api` directory and run the script `fill_db.py`.