# Emotorad-StealthLink

# StealthLink

## Project Overview

StealthLink is a backend service designed for identity reconciliation. It consolidates contact information across multiple identities, making it possible to recognize and link the same individual despite varying contact details. This project handles JSON payloads containing "email" and "phoneNumber" fields and provides a flexible linking mechanism that dynamically adjusts the contact structure based on overlapping information.

### Key Features

1. **Identity Reconciliation**: StealthLink identifies overlapping contact details and links them while maintaining individual records when necessary.
2. **Dual Contact Role Management**: The service can switch a contact's role between "primary" and "secondary" as new information surfaces, enabling seamless merging.
3. **Dynamic Response**: Returns consolidated contact details, including `primaryContactId`, all associated `emails`, `phoneNumbers`, and `secondaryContactIds`.

## Project Structure

```
StealthLink/
├── app.py               # Main application file with FastAPI setup and endpoints
├── database.py          # Database models and session management
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## Requirements

To run StealthLink, you’ll need:
- **Python 3.7+**
- **FastAPI** for the web framework
- **SQLAlchemy** for ORM-based database management
- **SQLite** as the default database (can be switched in `database.py` if needed)

Install dependencies by running:
```bash
pip install -r requirements.txt
```

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/StealthLink.git
cd StealthLink
```

### 2. Set Up the Database
StealthLink uses SQLite by default. Run the following command to initialize the database schema:
```bash
python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### 3. Run the Application
Start the FastAPI application using Uvicorn:
```bash
uvicorn app:app --reload
```

The server should now be running at `http://127.0.0.1:8000`.

### 4. API Usage

#### Endpoint: `/identify`

- **Method**: `POST`
- **Description**: Processes incoming requests to identify or consolidate contacts.
- **Request Body**: JSON containing `email` and/or `phoneNumber`.
  - Example:
    ```json
    {
        "email": "example@domain.com",
        "phoneNumber": "1234567890"
    }
    ```

- **Response**:
  - `primaryContactId`: The unique ID of the primary contact.
  - `emails`: A list of all associated emails.
  - `phoneNumbers`: A list of all associated phone numbers.
  - `secondaryContactIds`: IDs of contacts linked to the primary contact.

Example Response:
```json
{
    "primaryContactId": 1,
    "emails": ["example@domain.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": [2, 3]
}
```

## Code Explanation

### `app.py`

The main file, `app.py`, defines the FastAPI application and the `/identify` endpoint. This endpoint performs the following operations:
1. **Fetch Matching Contacts**: Looks up existing contacts based on the `email` or `phoneNumber` in the request.
2. **Create or Link Contacts**:
   - If no matches are found, it creates a new `primary` contact.
   - If a match is found, it either links the new details to an existing primary contact or creates a secondary contact if the new information does not fully match any existing entry.
3. **Dynamic Role Switching**: When overlapping contacts are identified, the system automatically determines and adjusts the role of contacts as primary or secondary.

### `database.py`

This file handles:
- **Database Models**: Defines the `Contact` table structure using SQLAlchemy.
- **Session Management**: Manages database sessions and connections.

The `Contact` model contains:
- `id`: Unique identifier for each contact.
- `email` and `phoneNumber`: Contact information fields.
- `linkedId`: If a contact is secondary, this field links it to a primary contact.
- `linkPrecedence`: Defines if a contact is "primary" or "secondary."
- `createdAt`, `updatedAt`, and `deletedAt`: Timestamps for record management.

### Edge Cases and Testing

StealthLink includes handling for scenarios such as:
- Requests with no existing contacts.
- Multiple requests matching different subsets of contacts.
- Cases where contacts need to dynamically switch from primary to secondary roles.
- Redundant entries to ensure data integrity.

To test, use any HTTP client (e.g., `curl`, Postman) and send requests with various `email` and `phoneNumber` combinations. Ensure the returned structure follows the rules and contains accurate links.

### Future Improvements

1. **Error Handling**: Implement custom error messages and codes for different scenarios (e.g., invalid inputs, database errors).
2. **Performance Optimization**: Introduce caching for frequently requested contacts and optimize SQL queries.
3. **Extended Testing**: Add unit tests and integration tests for greater robustness and reliability.

