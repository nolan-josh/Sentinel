import time
import sys
from pymongo import MongoClient

"""
    Later on we want to use .watch() to be able to monitor changes to the database and to do this it requires mongodb having oplogs
    after running the client.admin.command below it:
        - Creates the oplog
        - Elects itself as PRIMARY (since it's the only member)
        - Enables change streams
    (We use this change streams later on to detect a change in the DB which leads to the agent being called - we coudl just call agent if we find a new alert and add 
    it to the alerts collection but this simulates the real world more closely)
    
    THIS FILE WAS WRITTEN BY CLAUDE ! THE PART WHERE I WANTED AI TO HELP SO I CAN SPEND MY TIME ON OTHER AREAS AND COME BACK TO LEARN LATER
"""

def init_replica_set():
    while True:
        try:
            client = MongoClient(
                "mongodb://mongoDB:27017",
                serverSelectionTimeoutMS=5000,
                directConnection=True  # This was the key fix. Without it pymongo tries to discover and validate a replica set before connecting, but the replica set doesn't exist yet at init time.
            )
            client.admin.command("ping")
            print("MongoDB is up, initialising replica set...", flush=True)
            
            result = client.admin.command({
                "replSetInitiate": {
                    "_id": "rs0",
                    "members": [{"_id": 0, "host": "mongoDB:27017"}]
                }
            })
            print(f"Replica set result: {result}", flush=True)
            print("Replica set initialised successfully", flush=True)
            break

        except Exception as e:
            error_msg = str(e)
            print(f"Error: {error_msg}", flush=True)
            
            # already initialised is fine - exit successfully
            if "already initialized" in error_msg or "AlreadyInitialized" in error_msg:
                print("Replica set already exists, skipping.", flush=True)
                break
                
            # MongoDB not ready yet - retry
            print("Retrying in 3 seconds...", flush=True)
            time.sleep(3)

if __name__ == "__main__":
    print("Starting replica set initialisation...", flush=True)
    init_replica_set()
    print("Done.", flush=True)
    sys.exit(0)