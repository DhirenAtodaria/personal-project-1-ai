import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")
DEBUG = ENVIRONMENT == "dev"
HOST = '0.0.0.0' if ENVIRONMENT == "prod" else 'localhost'
MONGO_DB = "mongodb+srv://dhiren:someRandomPassword@macrocluster-wjiuw.mongodb.net/test?retryWrites=true&w=majority"
