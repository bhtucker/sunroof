# Sunroof
Script for fetching and storing congressional data from the Sunlight Foundation.


## Requirements:
* Postgres 9.4 or above
** (assumed to be running locally and to have a database called `congress`)
* Python dependencies (see requirements.txt)

## Usage:

* sunroof.py brings in data from sunlight fdtn.
* Invoke like:
* `python  --query=documentary --end-date=2012-01-01`
	NB: There is currently no primary key enforcement, so dropdb & createdb between runs
		You'll need a real API_KEY in secrets.py to run

* `bill_count.sql` provides some per-sponsor information about the contents of the database:
	Invoke like:
	`psql -d congress < bill_count.sql `

### TODO:
	
* Move interaction out of command line and offer UI (would do via Flask)
* Implement relational and primary key enforcement in tables
* Separate DB logic from request logic
* Reorganize private config (API key, database URI if it had ACL) for security
* Create py.test suite for unit test coverage
** Use httpretty mocking for request testing
* Add Alembic for DB migration management