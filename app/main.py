from database_manager import DatabaseManager
from domain_thread import DomainThread
import yaml

def init_database():
    try:
        """Initialize the database and create the table if it doesn't exist"""
        with DatabaseManager('db.sqlite3') as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS whois_records(
                    domain TEXT PRIMARY KEY,
                    createdDate TEXT,
                    updatedDate TEXT,
                    expiresDate TEXT,
                    registrantName TEXT,
                    registrantEmail TEXT, 
                    administrativeContact TEXT, 
                    technicalContact TEXT,
                    contactEmail TEXT
                );''')
            conn.commit()

    except Exception as e:
        raise Exception("Failed to create table", e)

def main():
    init_database()
    with open('domains.yml', 'r') as f:
        domains = yaml.safe_load(f)

    for domain in domains['domains']:
        thread = DomainThread(domain)
        thread.schedule()

if __name__ == "__main__":
         main()