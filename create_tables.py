from database import Base, engine
from models import ExampleModel

# Create all tables
Base.metadata.create_all(bind=engine)
