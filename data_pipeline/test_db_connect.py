from pymongo import MongoClient
from config import settings

client = MongoClient(settings.MONGO_DATABASE_HOST)
db = client[settings.MONGO_DATABASE_NAME]

# 插入測試數據
test_collection = db.test_collection
test_document = {"name": "test"}
result = test_collection.insert_one(test_document)

print(f"Inserted document ID: {result.inserted_id}")

# 列出所有資料庫
db_list = client.list_database_names()
print("Databases:", db_list)

# 檢查資料庫是否存在
if settings.MONGO_DATABASE_NAME in db_list:
    print(f"Database {settings.MONGO_DATABASE_NAME} exists.")
else:
    print(f"Database {settings.MONGO_DATABASE_NAME} does not exist.")
