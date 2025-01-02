# Atom Chat ⚛️
![Atom Chat](https://raw.githubusercontent.com/nickAnhel/FastAPI-Atom-Chat/refs/heads/main/images/image.png)
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

Linux
```bash
# Create virtual env
python3 -m venv .venv

# Activate it
source .venv/bin/activate
```
Windows
```cmd
# Create virtual env
py -m venv .venv

# Activate it
.venv\Scripts\activate
```

Go to the `server` directory.

Install project dependencies. They will be required to run tests and a script to fill the database with test data.
```bash
 # Install project dependencies
poetry install
```

Create a `certs` directory and navigate in it.
```bash
# Create a dir to store the keys
md certs
cd certs
```

Create private and public encryption keys.

Linux
```bash
# Create a private key
openssl genrsa -out private.pem 2048

# Create a public key
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```
Windows
```bash
# Create a private key
"C:\Program Files\Git\usr\bin\openssl.exe" genrsa -out private.pem 2048

# Create a public key
"C:\Program Files\Git\usr\bin\openssl.exe" rsa -in private.pem -outform PEM -pubout -out public.pem
```

Go back to the `server` directory and create the configuration files `.dev.env` and `.test.env` and fill them with your data guided by the files `.dev.env.example` and `.test.env.example`.

Go to the root directory of the project and start it using `docker`.
```bash
# Run project
docker compose up --build
```
# Launching on Windows
If you have an error in the `atom_chat_server` container and it says something like `Database '<your database name>' does not exists`, try to recreate the script `pg-scripts/create_dbs.sh` with the same content and restart the project.
# Tests
To run the tests, navigate to the `server` directory and execute the `pytest -v` command, specifying the `tests` directory.
```bash
# Run tests in verbose mode
pytest -v ./tests
```
# Filling with test data
To run the script to fill the database with test data, navigate to the `api` directory and run the script `fill_db.py`.

It will create three users `user1`, `user2` and `user3`, with the password `atom1234`. It will also create three chats `chat1`, `chat2` and `chat3`.
