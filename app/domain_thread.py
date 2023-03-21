import threading
from database_manager import DatabaseManager
import json
from get_whois_data import process_domain,send_email

class DomainThread(threading.Thread):
    threads = {}
    def __init__(self, domain):
        threading.Thread.__init__(self)
        self.domain = domain

    def run(self):
        try: 
            with DatabaseManager('db.sqlite3') as conn:
                # Check if there is a record for this domain in the database
                query = 'SELECT * FROM whois_records WHERE domain = ?'
                cursor =  conn.execute(query,(self.domain,))
                result = cursor.fetchone()
            
                data = process_domain(self.domain)

                if result is None:
                    # Insert a new record into the database
                    q = '''INSERT INTO whois_records (domain,createdDate,updatedDate,expiresDate,
                    registrantName,registrantEmail,administrativeContact,technicalContact,
                    contactEmail) VALUES (?,?,?,?,?,?,?,?,?)'''
                    cursor = conn.execute(q,data)
                    cursor.commit()
                    if cursor is None:
                            print('Whois record was not inserted')
                else:
                    # Compare the WHOIS data with the previous day's data
                    if data[1] != result[1] or data[2] != result[2] or data[3] != result[3] or data[4] != result[4] or data[5] != result[5] or data[6] != result[6] or data[7] != result[7] or data[8] != result[8]:
                            # Update the record in the database with the new WHOIS data
                        q = '''UPDATE whois_records 
                                SET 
                                    createdDate = ? ,
                                    updatedDate = ? , 
                                    expiresDate = ? , 
                                    registrantName = ? ,
                                    registrantEmail = ? , 
                                    administrativeContact = ? ,
                                    technicalContact = ? , 
                                    contactEmail = ?
                                WHERE 
                                    domain = ?'''
                        cursor = conn.execute(q,(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],self.domain,))
                        conn.commit()
                        if cursor is None:
                            print('Whois record was not updated')

                        message = json.dumps({
                            "whoisCreatedDate": data[1],
                            "whoisUpdatedDate": data[2],
                            "whoisExpiresDate": data[3],
                            "registrantName": data[4],
                            "emails": {
                            "registrant": data[5],
                            "administrativeContact": data[6],
                            "technicalContact": data[7],
                            "contactEmail": data[8]		 
                            },
                            "domainName": data[0]
                        }, separators=(',', ':'), skipkeys = True,
                         allow_nan = True,
                         indent = 6)                      
                        send_email(self.domain, message)

            del DomainThread.threads[self.domain]

        except Exception as e:
            raise Exception("Domain Thread error: ", e)

    def schedule(self):
        if self.domain not in DomainThread.threads:
            # Create new thread only if one doesn't already exist for this domain
            thread = threading.Thread(target=self.run)
            thread.start()
            DomainThread.threads[self.domain] = thread

        #threading.Timer(60, self.schedule).start()
        threading.Timer(86400, self.schedule).start()