# Event Manager App

## Backend Setup

### Python Virtual Environment

In the project root directory create a Python virtual environment with the command

```python3 -m venv venv```

and activate it using

```source venv/bin/activate```

or, using Windows,

```.\venv\Scripts\activate```.

Install all required dependencies using

```pip install -r requirements.txt```

### Application Database

Init the application database with

```python3 manage.py migrate```

### Run backend server

Execute the backend application using

```python3 manage.py run```

Your backend server will be running at `http://localhost:8000/` and you can access
the API documentation at `http://localhost:8000/swagger/`.

## Client Setup

Enter the frontend project directory

```cd frontend```

and install all required dependencies running

```npm install```

Start the frontend dev server with

```npm start```.

You can now access the Event Manager App frontend at `http://localhost:3000`.