**Relevant directory structure**

```
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── dev_requirements.txt
├── init_db.py
├── run_queue.py
├── runserver.py
├── alembic.ini.example
├── dedupe.stop
├── api
│   ├── app_config.py
│   ├── local.py.example
│   └── secrets.py.example
├── scripts
│   └── init-dedupeapi.sh
└── tests
    └── docker-compose.yml
```

Run the app: `docker-compose up --build`

**`Dockerfile`**

```Dockerfile
FROM python:3.4
LABEL maintainer "DataMade <info@datamade.us>"
RUN apt-get update
RUN apt-get install -y python-pip
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./dev_requirements.txt /app/dev_requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r dev_requirements.txt
COPY . /app
```

**`docker-compose.yml`**

```docker-compose.yml
version: '3'

services:
  app:
    image: dedupeio
    container_name: dedupe-service
    restart: always
    build: .
    ports:
      - 5000:5000
    depends_on:
      - postgres
      - redis
    volumes:
      - .:/app
      - ${PWD}/api/local.py.example:/app/api/local.py
      - ${PWD}/api/secrets.py.example:/app/api/secrets.py
      - dedupe-tmp:/tmp
    command: python runserver.py --host 0.0.0.0

  queue:
    container_name: dedupe-queue
    restart: always
    image: dedupeio:latest
    depends_on:
      - migration
    volumes:
      - .:/app
      - ${PWD}/api/local.py.example:/app/api/local.py
      - ${PWD}/api/secrets.py.example:/app/api/secrets.py
      - dedupe-tmp:/tmp
    command: python run_queue.py

  migration:
    container_name: dedupe-migration
    image: dedupeio:latest
    depends_on:
      - app
    volumes:
      - .:/app
      - ${PWD}/api/local.py.example:/app/api/local.py
      - ${PWD}/alembic.ini.example:/app/alembic.ini
    command: bash -c "python init_db.py && alembic upgrade head"

  postgres:
    container_name: dedupe-postgres
    restart: always
    image: postgres:9.6
    volumes:
      - db-data:/var/lib/postgresql/data
      - ${PWD}/scripts/init-dedupeapi.sh:/docker-entrypoint-initdb.d/10-init.sh
      - ${PWD}/dedupe.stop:/usr/share/postgresql/9.6/tsearch_data/dedupe.stop
    ports:
      - 32001:5432

  redis:
    container_name: dedupe-redis
    restart: always
    image: redis:latest
    ports:
      - 6379:6379

volumes:
  db-data:
  dedupe-tmp:
```

Run the tests: `docker-compose -f docker-compose.yml -f tests/docker-compose.yml run app`

**tests/docker-compose.yml**

```docker-compose.yml
version: '3'

services:
  app:
    restart: "no"
    environment:
      - TEST_DATABASE_URL=postgresql+dedupe://postgres@postgres:5432/dedupe_test
      - REDIS_HOST=redis
    volumes:
      # Multi-value fields are concatenated, i.e., this file will be mounted
      # in addition to the files and directories specified in the root
      # docker-compose.yml
      - ${PWD}/alembic.ini.example:/app/alembic.ini
    command: pytest -sxv
```
