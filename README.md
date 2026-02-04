Requirements file
1. FastAPI
    - Web framework
    - To build API endpoints
2. sqlalchemy
    - Object relational mapper (ORM) for Python
    - To interact with PostgreSQL using Python instead of SQL Queries
3. psycopg2-binary
    - PostgreSQL driver for Python
    - Allows Python and SQLAlchemy to talk to PostgreSQL. Without it, SQLAlchemy can’t send queries to Postgres
4. uvicorn
    - An ASGI server (a web server for async Python apps)
    - Runs FastAPI app locally or in production

How they all work together
[User/browser] --> uvicorn (ASGI server)
                   --> FastAPI (routes & logic)
                        --> SQLAlchemy (ORM)
                             --> psycopg2-binary
                                  --> PostgreSQL database

