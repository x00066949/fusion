from os import environ
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


logger = logging.getLogger()
logger.setLevel(logging.INFO)



def get_db():
    """Setting up database connection session
    Returns a Cockroach db session for running queries against cockroach db running in same cluster
    """
    db_user=environ["DB_USER"]
    db_password=environ["DB_PASSWORD"]

    logging.info("connecting to db")    
    db_uri="cockroachdb://"+db_user+":"+db_password+"@my-release-cockroachdb-public.default.svc.cluster.local:26257/movies"

    #in a real production environment, i'd opt for ssl cert auth (over username+password auth) in which case, the uri would be:
    #db_uri="cockroachdb://my-release-cockroachdb-public.default.svc.cluster.local:26257/movies?sslmode=require&sslrootcert=/cockroach/cockroach-certs/client.root.crt&sslcert=/cockroach/cockroach-certs/ca.crt&sslkey=/cockroach/cockroach-certs/client.root.key"

    try:        
        engine = create_engine(db_uri, pool_size=10)
    except Exception as e:
        logging.info("Failed to connect to database.")
        logging.info(f"{e}")

    logging.info("connected to db")

    Session=sessionmaker(bind=engine,autocommit=False,autoflush=False)
    return Session()

