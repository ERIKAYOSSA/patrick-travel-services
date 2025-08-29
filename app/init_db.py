from app.database.connection import engine, Base
from app.models.user import User
from app.models.flight import FlightBooking
from app.models.accommodation import Accommodation
from app.models.message import Message
from app.models.assistance_visa import AssistanceVisa
from app.models.school_admission import SchoolAdmission
from app.models.partner import Partner
from app.models.offer import Offer
from app.models.document import Document
from app.models.notification import Notification

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    

