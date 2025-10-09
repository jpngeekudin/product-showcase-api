from pymongo import AsyncMongoClient

client = AsyncMongoClient('localhost', 27017)
db = client.get_database('evaluasi-sharing-session')
user_collection = db.get_collection('users')
product_collection = db.get_collection('products')