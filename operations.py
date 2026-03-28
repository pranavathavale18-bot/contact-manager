
from appwrite.id import ID
from appwrite.query import Query
from datetime import datetime
import hashlib

from appwrite_config import (
    get_databases,
    DATABASE_ID,
    USERS_COLLECTION_ID,
    CONTACTS_COLLECTION_ID
)


class ContactOperations:
    def __init__(self):
        self.db = get_databases()

    # -------------------------
    # USER REGISTER
    # -------------------------
    def register_user(self, username, password):
        try:
            users = self.db.list_documents(
                DATABASE_ID,
                USERS_COLLECTION_ID,
                [Query.equal("username", username)]
            )

            if users.total > 0:
                return False, "Username already exists"

            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            self.db.create_document(
                DATABASE_ID,
                USERS_COLLECTION_ID,
                ID.unique(),
                {
                    "username": username,
                    "password": hashed_password,
                    "created_at": datetime.utcnow().isoformat()
                }
            )

            return True, "User registered successfully"

        except Exception as e:
            return False, str(e)

    # -------------------------
    # LOGIN
    # -------------------------
    def authenticate_user(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            users = self.db.list_documents(
                DATABASE_ID,
                USERS_COLLECTION_ID,
                [
                    Query.equal("username", username),
                    Query.equal("password", hashed_password)
                ]
            )

            return users.total > 0

        except Exception:
            return False

    # -------------------------
    # GET CONTACTS
    # -------------------------
    def get_contacts(self, username):
        try:
            docs = self.db.list_documents(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                [
                    Query.equal("user_id", username),
                    Query.order_desc("date_added")
                ]
            )

            contacts = []

            for doc in docs.documents:
                contacts.append({
                    "id": doc["$id"],
                    "name": doc["name"],
                    "phone": doc["phone"],
                    "email": doc.get("email"),
                    "date_added": datetime.fromisoformat(doc["date_added"])
                })

            return contacts

        except Exception:
            return []

    # -------------------------
    # ADD CONTACT
    # -------------------------
    def add_contact(self, username, name, phone, email):
        try:
            existing = self.db.list_documents(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                [
                    Query.equal("user_id", username),
                    Query.equal("phone", phone)
                ]
            )

            if existing.total > 0:
                return False, "Phone number already exists"

            self.db.create_document(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                ID.unique(),
                {
                    "user_id": username,
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "date_added": datetime.utcnow().isoformat()
                }
            )

            return True, "Contact added successfully"

        except Exception as e:
            return False, str(e)

    # -------------------------
    # UPDATE CONTACT
    # -------------------------
    def update_contact(self, username, contact_id, name, phone, email):
        try:
            self.db.update_document(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                contact_id,
                {
                    "name": name,
                    "phone": phone,
                    "email": email
                }
            )

            return True, "Contact updated successfully"

        except Exception as e:
            return False, str(e)

    # -------------------------
    # DELETE CONTACT
    # -------------------------
    def delete_contact(self, username, contact_id):
        try:
            self.db.delete_document(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                contact_id
            )

            return True, "Contact deleted successfully"

        except Exception as e:
            return False, str(e)

    # -------------------------
    # SEARCH CONTACTS
    # -------------------------
    def search_contacts(self, username, search_term):
        try:
            results = []
            seen_ids = set()

            name_docs = self.db.list_documents(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                [
                    Query.equal("user_id", username),
                    Query.search("name", search_term)
                ]
            )

            phone_docs = self.db.list_documents(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                [
                    Query.equal("user_id", username),
                    Query.search("phone", search_term)
                ]
            )

            email_docs = self.db.list_documents(
                DATABASE_ID,
                CONTACTS_COLLECTION_ID,
                [
                    Query.equal("user_id", username),
                    Query.search("email", search_term)
                ]
            )

            all_docs = (
                name_docs.documents
                + phone_docs.documents
                + email_docs.documents
            )

            for doc in all_docs:
                if doc["$id"] not in seen_ids:
                    seen_ids.add(doc["$id"])
                    results.append({
                        "id": doc["$id"],
                        "name": doc["name"],
                        "phone": doc["phone"],
                        "email": doc.get("email"),
                        "date_added": datetime.fromisoformat(doc["date_added"])
                    })

            return results

        except Exception as e:
            print("Search error:", e)
            return []
```
