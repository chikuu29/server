import pymongo
try:
    # Try to establish a connection to MongoDB
    client = pymongo.MongoClient("mongodb+srv://cchiku1999:4WqX3s8paabc2y4o@cluster0.sklu9w7.mongodb.net/?retryWrites=true&w=majority")
    db = client['myMongoDB']
    # Check if the connection is successful
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    # If an exception occurs, print the error message
    print("An error occurred:", e)
