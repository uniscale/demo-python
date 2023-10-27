# Demo solution Python backend

## How to run

### Create and Activate a Virtual Environment (venv)

It's recommended to use a virtual environment to isolate project dependencies. Follow these steps:

On macOS and Linux:
```bash
python -m venv env
source env/bin/activate
```

On Windows (Command Prompt):
```bash
python -m venv env
.\env\Scripts\activate
```

### Install Dependencies

```bash
pip install --extra-index-url https://{username}:{password}@sdk.uniscale.com/api/packages/{organisation}/pypi/simple -r requirements.txt
```
This command will install all the required dependencies for the program. Replace `{username}` and `{password}` with information
from `Demo company`.

### Run program
Here's how you can run the program:

Start the services:
```bash
python account.py
```
```bash
python messages.py
```

These will run each service on their own servers.

## How to use

Send backend action request to `/api/service-to-module/{featureId}`. Port 5298 for account service and port 5192 for messages.