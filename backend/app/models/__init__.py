from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from backend.app.models.db_models import Base

# This will be set from the app's config
engine = None
db_session = None

def init_db(app):
    """Initialize the database connection"""
    global engine, db_session
    
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = db_session.query_property()
    
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
        
    return db_session
