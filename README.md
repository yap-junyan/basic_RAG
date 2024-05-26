#### A RAG Pipeline with Gemini Pro

A pipeline that stores PDF documents in a vector store [ChromaDB](https://www.trychroma.com/) and does document retrieval before sending off to Gemini to process the context and provide us with a suitable response. 

Reranking with a cross-encoder was used to rerank the documents to hopefully provide a more accurate answer by first selecting better documents to use as context for the LLM.
