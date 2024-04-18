from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from db.mongo import db
import bcrypt
from services.commonService import *


class JobResumeDynamicQuery(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection = db['your_collection_name']

    def get(self, request):
        try:
            query = request.data.get('query')
            projection = request.data.get('projection')
            if not query:
                return Response({"error": "Please provide a query"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Execute MongoDB query with projection
            result = self.collection.find(query, projection)
            listCursor = list(result)
            if len(listCursor) >0:
                return Response(listCursor, status=status.HTTP_200_OK)
            else:
                print("No documents found")
                return Response([], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            document = request.data.get('document')
            if not document:
                return Response({"error": "Please provide a document to insert"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Insert document into MongoDB
            result = self.collection.insert_one(document)
            return Response({"message": "Document inserted successfully", "inserted_id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            query = request.data.get('query')
            update = request.data.get('update')
            if not query or not update:
                return Response({"error": "Please provide both query and update fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Update document in MongoDB
            result = self.collection.update_one(query, update)
            return Response({"message": "Document updated successfully", "modified_count": result.modified_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        # Similar to PUT, you can implement patch method for partial updates
        pass

    def delete(self, request):
        try:
            query = request.data.get('query')
            if not query:
                return Response({"error": "Please provide a query"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Delete document from MongoDB
            result = self.collection.delete_one(query)
            return Response({"message": "Document deleted successfully", "deleted_count": result.deleted_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)