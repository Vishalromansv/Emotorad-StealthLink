from fastapi import FastAPI, Depends, HTTPException  # FastAPI framework for building APIs
from sqlalchemy.orm import Session  # ORM session for database operations
from database import Contact, Base, engine, get_db  # Importing database models and utilities
from pydantic import BaseModel  # Pydantic models for request and response validation
from typing import List, Optional  # Type hinting for lists and optional fields
from datetime import datetime  # Used for timestamping records

# Initialize the database tables if they don’t already exist
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()

# Define the request body schema
class IdentifyRequest(BaseModel):
    email: Optional[str] = None  # Optional email field
    phoneNumber: Optional[str] = None  # Optional phone number field

# Define the response schema
class IdentifyResponse(BaseModel):
    primaryContactId: int  # ID of the primary contact
    emails: List[str]  # List of all associated emails
    phoneNumbers: List[str]  # List of all associated phone numbers
    secondaryContactIds: List[int]  # List of secondary contact IDs linked to primary

# Define the /identify endpoint, which processes contact information for identity reconciliation
@app.post("/identify", response_model=IdentifyResponse)
def identify_contact(request: IdentifyRequest, db: Session = Depends(get_db)):
    # Ensure at least one contact field (email or phone number) is provided
    if not request.email and not request.phoneNumber:
        raise HTTPException(status_code=400, detail="Either email or phone number is required.")

    # Step 1: Fetch any contacts in the database that match the provided email or phone number
    matching_contacts = db.query(Contact).filter(
        (Contact.email == request.email) | (Contact.phoneNumber == request.phoneNumber)
    ).all()

    # Step 2: Determine if a new primary contact is needed or link to existing ones
    if not matching_contacts:
        # If no existing contact matches, create a new primary contact
        new_contact = Contact(
            email=request.email,
            phoneNumber=request.phoneNumber,
            linkPrecedence="primary",  # Set as primary since no match was found
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)  # Refresh to get the generated ID

        # Return response with the new contact as primary
        return IdentifyResponse(
            primaryContactId=new_contact.id,
            emails=[new_contact.email] if new_contact.email else [],
            phoneNumbers=[new_contact.phoneNumber] if new_contact.phoneNumber else [],
            secondaryContactIds=[]
        )

    # Step 3: Process linked contacts by identifying the primary contact and collecting details
    primary_contact = min(
        [c for c in matching_contacts if c.linkPrecedence == "primary"],
        key=lambda c: c.createdAt
    )  # Choose the earliest primary contact
    emails = {c.email for c in matching_contacts if c.email}
    phone_numbers = {c.phoneNumber for c in matching_contacts if c.phoneNumber}
    secondary_contact_ids = [c.id for c in matching_contacts if c.linkPrecedence == "secondary"]

    # Step 4: Add new secondary contact if needed (i.e., a new combination of email and phone number)
    if not any(c.email == request.email and c.phoneNumber == request.phoneNumber for c in matching_contacts):
        new_secondary_contact = Contact(
            email=request.email,
            phoneNumber=request.phoneNumber,
            linkedId=primary_contact.id,  # Link to the primary contact
            linkPrecedence="secondary",  # Set as secondary
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        db.add(new_secondary_contact)
        db.commit()
        db.refresh(new_secondary_contact)  # Refresh to get the generated ID
        secondary_contact_ids.append(new_secondary_contact.id)

    # Step 5: Return a consolidated response including primary and secondary contacts
    return IdentifyResponse(
        primaryContactId=primary_contact.id,
        emails=list(emails),  # Unique list of emails associated with the contact
        phoneNumbers=list(phone_numbers),  # Unique list of phone numbers
        secondaryContactIds=secondary_contact_ids  # List of secondary contact IDs
    )
