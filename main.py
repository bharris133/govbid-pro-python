from database import SessionLocal
from models import ExampleModel

# Create a new session
db = SessionLocal()

# Example: Add a new record
new_record = ExampleModel(name="Sample Name")
db.add(new_record)
db.commit()

# Query the database
records = db.query(ExampleModel).all()
print(records)

# Close the session
db.close()
