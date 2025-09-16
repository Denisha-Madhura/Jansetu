# JanSetu

## Software Pipeline

![Software Pipeline](.github/assets/workflow_pipeline.png)

A **Software Pipeline** describes how a project moves between its stages of publishing from local development. It is important as it gives a clear view as to what all steps a programmers code goes through before it gets **deployed to production**.

### The steps/nodes

1. **Local** : This is the actual development environment of a programmers where they make changes to the software's code.

2. **Pre Commit Hooks** : This is the first check before publishing code to a collaborative environment like *GitHub*. A *pre commit hook*, like its name suggests, runs before running running `git commit` automatically. It is a set of pre set commands that ensure that the code being written follows the standards set for that project. In our case we have three major *pre commit checks*.

	-  **Linting** : This step analyzes the code being added for any *programmatic and stylistic* errors.The programmatic and stylistic rules are preset per project defined generally by a *config file*. This allows one to catch any *known issues* before hand and hence saves debugging time. a good example would be *unused import* where redundant imports increase *software package size* and hence should be removed. **linting changes are manual**

	- **Formatting** : This step auto formats code to the *set standard* that is defined per project via a *config file*. A good example would be *tabs vs spaces*, where some developers prefer using tabs and some prefer spaces but the project to disallow ambiguity only allows *tabs*, and so all "space" code auto converts to tabs before being added. **formatting changes are automatic**

	- **Building** : This step your project is built *locally* so as to find any errors that may cause a *build time error* which if pushed could take down a *deployment*. A good example would be *not using .js after import files* which sometimes the *tsc* typescript compiler fails at during building.

3. **Github** : This is the main hub where your code lives on the cloud which allows for collaboration. *git* is version control, *github* is a cloud platform which powers git by storing code. *git* != *github*

4. **Workflows** : A workflow can be thought of simply as a *pre commit hook* but on the cloud, which also listens to some *event* and then performs some *steps*, automaticaly. In our case we only have like two *major steps*, which have their own *sub steps* but they are a little out of scope here.

	-  **Building** : Here our *entire* project software is built into (in our case) a singular **docker image**. Local building step helps prevent any errors from occurring during our main building step (this one).

	- **Publishing** : Here (in our case) the built *docker image* is published to **docker hub**. Docker hub is (just like github), a cloud storage for all docker images on the web that can be *pulled from*.

5. **Server** : This is a cloud computer where our actual project gets *deployed* from. The entire process of deployment is supported by tools like **docker-compose** and **watch tower**, where *docker compose* manages the structure of a *docker image* and *watch tower* listens to updates for a docker image.

6. **Internet** : Well this is a self explanatory node, this is when our software gets accessible to the users. A lot of pre-processing steps are involved here like, **reverse proxy**, **dns** etc

Every project will have its own *software pipeline*, but the above pipeline can be thought of as the most basic and rudimentary one which powers more complex pipelines.

## Backend

### Project Structure

```
backend/
    ├── src/
        ├── models/
            ├── __init__.py
            └── auth.py
        ├── routes/
            ├── __init__.py
            └── auth.py
        ├── utils/
            ├── jwt.py
            └── password.py
        ├── __init__.py
        ├── database.py
        └── main.py
    ├── .env.copy
    ├── .gitignore
    ├── .pre-commit-config.yaml
    ├── docker-compose.yaml
    ├── poetry.lock
    ├── pyproject.toml
    └── README.md
```

1. **`src/`**

This is the main _application folder_. Everything related to your backend lives here.

2. **`src/models/`**

Here your *database models* are defined. A *model* is how a table (or better said *data*) in your database will look like. It is written (in our case) via **SQLAlchemy** which is an **ORM** (object relational model), and *orm* basically abstracts our database queries for us so we dont have to spend time writing *raw SQL* (structured query language).

3. **`src/routes/`**

Here your *API endpoints* are defined. An *endpoint* can be thought of as a *URL* that is used to connect some sort of data from the *client* and the *server*. They are defined to be used via basic **internet protocols** like **POST** (used to push data onto the *server*, has a *request body* in which data to be processed can be added) and **GET** (used to fetch data from the *server*, does not support a *request body* and generally has *URL queries* to narrow down the fetch).

4. **`src/utils/`**

Here your *helper functions* are defined. A *helper function* is anything that doesn't directly act like an *endpoint* but is required to process data *over and over again*. For example (in our case) we have helper functions defined to **hash passwords**.

other files can be understood as *standard files* which build up the project. They have self explanatory names, and generally only deal with one functionality (as the name of the file suggests).

### How to add a new endpoint

1. Define your **route**

```py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session

router = APIRouter(prefix="/<router-name>", tags=["<router-tag>"])
```

- `prefix="/<router-name>"` : This sets a **base path** for all endpoints in this router. Meaning your *URL* will have this prefixed automatically. Example `/api/v1/<router-name>/{userId}` might be an *endpoint* to get a users data by user id.

- `tags=["<router-tag>"]` : Only for *documentation*. It is used to group all similar endpoints in your **swagger** documentation.

2. Define your **Endpoint Function**

```py
@router.get("/{id_}")
async def <function-name>(id_: int, session: AsyncSession = Depends(get_session)):
    ...
```

- `@router.get("/{id_}")` : This is a **python decorator** (a decorator can be thought of as a function wrapping another function). `get` defines the *method* of the endpoint (get, post etc) and `"/{id_}"` defines any URL queries, for example `GET api/v1/user/1` can be thought of as getting the data of a *user* with *id 1*.

3. Include the **router** in **main.py**

```py
from src.routes import <router-name>

app = FastAPI(title="Jansetu API")
app.include_router(<router-name>)
```

### How to run this project

1. Environment setup

	1. Copy the environment template:
	
	```bash
	cp .env.copy .env
	```

	2. Open `.env` and fill in your values:
	
	```bash
	DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/jansetu
	JWT_SECRET=supersecret
	```

2. Install Dependencies

```bash
poetry install
```

3. Run the application

```shell
poetry run uvicorn src.main:app --reload
```

### How to use swagger

FastAPI automatically generates an **interactive API documentation** using Swagger. You can use it to *explore endpoints, test requests, and see responses* without needing external tools like Postman.

1. Open **Swagger UI**

Once your app is running, go to:  [http://localhost:8000/docs](http://localhost:8000/docs)

2. Explore Endpoints

	- Endpoints are grouped by **tags** (e.g. `auth`, `users`).
	- Click on a section to expand and see available routes (`/signup`, `/signin`, etc.).


3. Try Out an Endpoint

	1. Click on an endpoint (e.g. `POST /auth/signup`).
	2. Click **“Try it out”**.
	3. Fill in the input fields (e.g. `email`, `password`).
	4. Press **“Execute”**.

	Swagger will:

	- Send the request to your API
	- Show the exact **curl request**
	- Display the **response JSON** from your backend

4. Authorize with JWT (if needed) for protected endpoints (lock at the side)

	1. Click the **“Authorize”** button at the top right.
	2. Enter your JWT token (usually `Bearer <token>`).
	3. Click **Authorize**.
