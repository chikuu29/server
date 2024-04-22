from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from NLP_Model.nlp_for_find_job import findtoptenjobforresume
# from NLP_Model.nlp_for_find_resume import findtoptenresumeforjob
from db.mongo import db
import bcrypt
import threading
from services.commonService import *
 
 
class JobResumeDynamicQuery(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def get(self, request):
        try:
            query = request.data.get('query')
            collection = request.data.get('collection')
            projection = request.data.get('projection')
            if not query or  not collection or  not projection:
                return Response({"error": "Please provide  query/collection/projection"}, status=status.HTTP_400_BAD_REQUEST)
            self.collection = db[collection]
           
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
            collection = request.data.get('collection')
            if not document or  not collection:
                return Response({"error": "Please provide a document/collection to insert"}, status=status.HTTP_400_BAD_REQUEST)
           
            self.collection = db[collection]
            # Insert document into MongoDB
            result = self.collection.insert_one(document)
            return Response({"message": "Document inserted successfully", "inserted_id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
    def put(self, request):
        try:
            query = request.data.get('query')
            update = request.data.get('update')
            collection = request.data.get('collection')
            if not query or not update or  not collection:
                return Response({"message": "Please provide both query and update fields and collection"}, status=status.HTTP_400_BAD_REQUEST)
           
            self.collection = db[collection]
            # Update document in MongoDB
            result = self.collection.update_one(query, update)
            print(f"hii",result)
            return Response({"message": "Document updated successfully", "modified_count": result.modified_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
    def patch(self, request):
        try:
            query = request.data.get('query')
            update = request.data.get('update')# use set keyword in update parameter data
            collection = request.data.get('collection')
            if not query or not update or  not collection:
                return Response({"error": "Please provide both query and update fields and collection"}, status=status.HTTP_400_BAD_REQUEST)
           
            # Update document in MongoDB
           
            collection = request.data.get('collection')
            result = self.collection.update_one(query, update)
            if result.matched_count == 0:  # If no document matched the query
                return Response({"message": "No document matched the query"}, status=status.HTTP_404_NOT_FOUND)
            elif result.modified_count == 0:  # If no document was actually modified
                return Response({"message": "No document was updated"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Document updated successfully", "modified_count": result.modified_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request):
        try:
            query = request.data.get('query')
            collection = request.data.get('collection')
            if not query or  not collection:
                return Response({"error": "Please provide a query/collection"}, status=status.HTTP_400_BAD_REQUEST)
           
            self.collection = db[collection]
            # Delete document from MongoDB
            result = self.collection.delete_one(query)
            return Response({"message": "Document deleted successfully", "deleted_count": result.deleted_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
       



class getJobPost(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
    def post(self, request):
        try:
            query = request.data.get('query')
            collection = request.data.get('collection')
            projection = request.data.get('projection')
            if   not collection:
                return Response({"error": "Please provide a collection Name"}, status=status.HTTP_400_BAD_REQUEST)
           
            self.collection = db[collection]
            # Insert document into MongoDB
            result = self.collection.find(query, projection)
            list_cursor = list(result)
            serialized_result = []
            for item in list_cursor:
                item['_id'] = str(item['_id'])  # Convert ObjectId to string
                serialized_result.append(item)

            if serialized_result:
                return Response(serialized_result, status=status.HTTP_200_OK)
            else:
                print("No documents found")
                return Response([], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
 
    

class JobResumeAggregationQuery(APIView):
    def post(self, request):
        try:
            pipeline = request.data.get('pipeline')
            collection = request.data.get('collection')
            if not pipeline or not collection:
                return Response({"error": "Please provide a pipeline and collection"}, status=status.HTTP_400_BAD_REQUEST)
           
            self.collection = db[collection]
           
            # Run aggregation query
            result = self.collection.aggregate(pipeline)
           
            # Convert aggregation result to a list and return
            list_result = list(result)
            if len(list_result) > 0:
                return Response(list_result, status=status.HTTP_200_OK)
            else:
                print("No documents found")
                return Response([], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class getallResume(APIView):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
     def get(self, request):
        try:
           
            self.collection = db["resume"]
           
            # Execute MongoDB query with projection
            # result = self.collection.find({}, {})
            # listCursor = list(result)
            result = self.collection.find({}, {})
            # result = self.collection.find(query, projection)
            list_cursor = list(result)
            serialized_result = []
            for item in list_cursor:
                item['_id'] = str(item['_id'])  # Convert ObjectId to string
                serialized_result.append(item)

            if serialized_result:
                path ='./csv_files/resume.csv',
                columnsKeys = ["name", "objective", "education", "work_experience", "certifications", "skills", "languages", "interests", "references", "resume_id", "email", "resumeCreatedBy", "createdAt"]
                csv_thread = threading.Thread(target=jsonTocsv, args=(serialized_result,path,columnsKeys))
                csv_thread.start()
                return Response(serialized_result, status=status.HTTP_200_OK)
            else:
                print("No documents found")
                return Response([], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
 


class getallJob(APIView):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
     def get(self, request):
        try:
           
            self.collection = db["job_post"]
            # Execute MongoDB query with projection
            # result = self.collection.find({}, {})
            # listCursor = list(result)
            result = self.collection.find({}, {})
            # result = self.collection.find(query, projection)
            list_cursor = list(result)
            serialized_result = []
            for item in list_cursor:
                item['_id'] = str(item['_id'])  # Convert ObjectId to string
                serialized_result.append(item)

            if serialized_result:
                path ='./csv_files/job.csv',
                columnsKeys = ["job_posting", "location", "position_type", "project_title", "project_description", "key_responsibilities", "qualifications", "application_process", "university_name", "job_id", "createdAt", "createdBy"]
                csv_thread = threading.Thread(target=jsonTocsv, args=(serialized_result,path,columnsKeys))
                csv_thread.start()
                return Response(serialized_result, status=status.HTTP_200_OK)
            else:
                print("No documents found")
                return Response([], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
 





# class getTopTenJobPost(APIView):
#       def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#       def post(self,request):
#         try:
           
#             self.collection = db["job_post"]
#             resume_id = request.data.get('resume_id')
#             # Execute MongoDB query with projection
#             # result = self.collection.find({}, {})
#             # listCursor = list(result)
#             print("resume_id",resume_id)
#             if not resume_id:
#                 return Response({"message": "resume_id For Run NLP"}, status=status.HTTP_400_BAD_REQUEST)
#             # result = self.collection.find({}, {})


#             print(f"Callinf NLP Model")

#             nlpResponce=findtoptenjobforresume(resume_id)
#             print(nlpResponce)
#             if nlpResponce and nlpResponce['success']:
#                job_ids = [entry['job_id'] for entry in nlpResponce['result'] if entry.get('job_id')]
#             else:
#                 return Response({"message": "NLP RUN UNSUCCESSFULL", "nlpresponce": nlpResponce, "success": False},
#                                 status=status.HTTP_200_OK)

#             print(f"data", job_ids)
#             result = self.collection.find({"job_id": {"$in": job_ids}})
#             list_cursor = list(result)
#             serialized_result = []
#             for item in list_cursor:
#                 item['_id'] = str(item['_id'])  # Convert ObjectId to string
#                 serialized_result.append(item)

#             if serialized_result:
#                 return Response({"message": "NLP RUN SUCCESSFULL", "nlpresponce": nlpResponce, "matchData": serialized_result,
#                                 "success": True}, status=status.HTTP_200_OK)
#             else:
#                 print("No documents found")
#                 return Response({"message": "NLP RUN SUCCESSFULL", "nlpresponce": nlpResponce, "matchData": serialized_result,
#                                 "success": True}, status=status.HTTP_200_OK)

#             # result = self.collection.find(query, projection)
#             # list_cursor = list(result)
#             # serialized_result = []
#             # for item in list_cursor:
#             #     item['_id'] = str(item['_id'])  # Convert ObjectId to string
#             #     serialized_result.append(item)

#             # if serialized_result:
#             #     return Response(serialized_result, status=status.HTTP_200_OK)
#             # else:
#             #     print("No documents found")
#             #     return Response([], status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"message": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
          
 


 
# class getTopTenJobResume(APIView):
#       def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#       def post(self,request):
#         try:
           
#             self.collection = db["resume"]
#             job_id = request.data.get('job_id')
#             # Execute MongoDB query with projection
#             # result = self.collection.find({}, {})
#             # listCursor = list(result)
#             print("job_id",job_id)
#             if not job_id:
#                 return Response({"message": "Job_id For Run NLP"}, status=status.HTTP_400_BAD_REQUEST)
#             # result = self.collection.find({}, {})


            
#             nlpResponce=findtoptenresumeforjob(job_id)
#             print(nlpResponce)
#             if nlpResponce and nlpResponce['success']:
#                resume_ids = [entry['resume_id'] for entry in nlpResponce['result'] if entry.get('resume_id')]
#             else:
#                 return Response({"message": "NLP RUN UNSUCCESSFULL", "nlpresponce": nlpResponce, "success": False},
#                                 status=status.HTTP_200_OK)

#             print(f"data", resume_ids)
#             result = self.collection.find({"resume_id": {"$in": resume_ids}})
#             list_cursor = list(result)
#             serialized_result = []
#             for item in list_cursor:
#                 item['_id'] = str(item['_id'])  # Convert ObjectId to string
#                 serialized_result.append(item)

#             if serialized_result:
#                 return Response({"message": "NLP RUN SUCCESSFULL", "nlpresponce": nlpResponce, "matchData": serialized_result,
#                                 "success": True}, status=status.HTTP_200_OK)
#             else:
#                 print("No documents found")
#                 return Response({"message": "NLP RUN SUCCESSFULL", "nlpresponce": nlpResponce, "matchData": serialized_result,
#                                 "success": True}, status=status.HTTP_200_OK)

#             # result = self.collection.find(query, projection)
#             # list_cursor = list(result)
#             # serialized_result = []
#             # for item in list_cursor:
#             #     item['_id'] = str(item['_id'])  # Convert ObjectId to string
#             #     serialized_result.append(item)

#             # if serialized_result:
#             #     return Response(serialized_result, status=status.HTTP_200_OK)
#             # else:
#             #     print("No documents found")
#             #     return Response([], status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"message": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class syncAllResumeJobs(APIView):
    def get(self, request):
        try:
            getallResume.get(self, request)
            getallJob.get(self, request)
            return Response({"message": "synced successfully",'success':True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "An error occurred: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)  
 
          
 