from fastapi import Depends
from app.services import transcript_service, chunk, vector_db, embedding_service

class QueryService:
    def __init__(self, embedding_service: embedding_service.EmbeddingService, vector_db_service: vector_db.VectorDBService):
        self.embedding_service = embedding_service
        self.vector_db_service = vector_db_service

    def retrieve_context(self, question: str, top_k: int=5, video_id: str=None):
        try:
            print(f"Embedding query: {question}")
            query_vector = self.embedding_service.embed_texts([question])[0]
            if not query_vector:
                raise ValueError("Embedding service returned no data")

            print(f"retrieving documents: {query_vector}")
            result = self.vector_db_service.query_documents(query_vector, top_k=top_k, video_id=video_id)
            
            return result
        
        except Exception as e:
            print(f"Error in Retrieval Pipeline: {e}")
            return []
        
def get_query_service(embedding_service: embedding_service.EmbeddingService = Depends(embedding_service.get_embedding_service),
                          vector_db_service: vector_db.VectorDBService = Depends(vector_db.get_vector_db_service)
                          ):
        return QueryService(embedding_service=embedding_service, vector_db_service=vector_db_service)

        