import logging
import requests
import psycopg2
from psycopg2 import sql
from typing import Optional
import json
import time

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database connection settings
DB_SETTINGS = {
    'dbname': 'user_database',
    'user': 'db_user',
    'password': 'db_password',
    'host': 'localhost',
    'port': 5432
}

# Third-Party API settings
API_ENDPOINT = "https://thirdpartyapi.com/share"

class UserData:
    """Encapsulates user data such as name, email, DOB, and bank account details."""
    def __init__(self, name: str, email: str, dob: str, bank_account: str):
        self.name = name
        self.email = email
        self.dob = dob
        self.bank_account = bank_account

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "dob": self.dob,
            "bank_account": self.bank_account
        }

class DatabaseClient:
    """Handles database interactions."""
    def __init__(self):
        self.conn = self.connect()

    def connect(self):
        try:
            logger.info("Connecting to database...")
            conn = psycopg2.connect(**DB_SETTINGS)
            logger.info("Database connection established.")
            return conn
        except psycopg2.DatabaseError as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def save_user_data(self, user_data: UserData):
        try:
            with self.conn.cursor() as cur:
                insert_query = sql.SQL(
                    """INSERT INTO user_data (name, email, dob, bank_account) 
                    VALUES (%s, %s, %s, %s)"""
                )
                cur.execute(insert_query, (user_data.name, user_data.email, user_data.dob, user_data.bank_account))
                self.conn.commit()
                logger.info(f"User data for {user_data.name} saved to database.")
        except Exception as e:
            logger.error(f"Failed to save user data to database: {e}")
            self.conn.rollback()

    def close(self):
        self.conn.close()
        logger.info("Database connection closed.")

class ThirdPartyAPIClient:
    """Handles interactions with third-party services."""
    def __init__(self, api_url: str):
        self.api_url = api_url

    def share_user_data(self, user_data: UserData) -> Optional[requests.Response]:
        try:
            logger.info(f"Sending user data for {user_data.name} to third-party service...")
            response = requests.post(self.api_url, json=user_data.to_dict())
            if response.status_code == 200:
                logger.info(f"Successfully shared user data for {user_data.name}.")
                return response
            else:
                logger.warning(f"Failed to share user data. Status code: {response.status_code}")
                return None
        except requests.RequestException as e:
            logger.error(f"Error while sending user data: {e}")
            return None

class UserDataSystem:
    """System responsible for managing user data operations."""
    def __init__(self):
        self.db_client = DatabaseClient()
        self.api_client = ThirdPartyAPIClient(API_ENDPOINT)

    def handle_user_data(self, user_data: UserData):
        try:
            # Save user data to database
            self.db_client.save_user_data(user_data)
            
            # Share user data with third-party service
            response = self.api_client.share_user_data(user_data)

            # Log result to file
            if response and response.status_code == 200:
                self.log_user_data_to_file(user_data, "Successfully shared with third-party")
            else:
                self.log_user_data_to_file(user_data, "Failed to share with third-party")
        except Exception as e:
            logger.error(f"Unexpected error during user data handling: {e}")
        finally:
            self.db_client.close()

    def log_user_data_to_file(self, user_data: UserData, status: str):
        """Log the user data operation result to a file."""
        log_entry = {
            "timestamp": time.time(),
            "name": user_data.name,
            "email": user_data.email,
            "dob": user_data.dob,
            "bank_account": user_data.bank_account,
            "status": status
        }
        try:
            with open("user_data_log.json", "a") as log_file:
                log_file.write(json.dumps(log_entry) + "\n")
                logger.info(f"Logged user data operation for {user_data.name} to file.")
        except IOError as e:
            logger.error(f"Failed to write user data log to file: {e}")

if __name__ == "__main__":
    # Example usage
    try:
        user_data = UserData(name="John Doe", email="john.doe@example.com", dob="1990-01-01", bank_account="1234567890")
        user_data_system = UserDataSystem()
        user_data_system.handle_user_data(user_data)
    except Exception as e:
        logger.error(f"Fatal error in system: {e}")
