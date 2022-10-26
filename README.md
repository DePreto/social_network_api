# TODO временное состояние

env.py: 

POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=app

PGADMIN_DEFAULT_EMAIL = test@mail.ru
PGADMIN_DEFAULT_PASSWORD = password
PGADMIN_LISTEN_PORT=8080

PRE_START_PATH=/src/app/prestart.sh

app: localhost:5000
pgadmin: localhost:8080
db: localhost:5432