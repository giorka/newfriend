from pymongo import MongoClient

from server.settings import MONGO_HOST

client: MongoClient = MongoClient(MONGO_HOST)
db = client['newFriend']

registration_queue = db['registrationQueue']
registration_queue.create_index('expirationTime', expireAfterSeconds=0)
