import gradio as gr
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.core import PromptTemplate
import os

PERSIST_DIR = "./storage"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader("data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)

# Query Engine
query_engine = index.as_query_engine(response_mode="tree_summarize")

new_summary_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "As an employee specialized in customer service, your main role is to assist users by answering questions based on the context"
    "You are here to ensure that users receive accurate and helpful responses to their inquiries, making their experience smooth and satisfactory."
    "If you don't know something, tell the customer that you don't have the information yet and that it will be updated later."
    "Answer in the same language as the query"
    "Query: {query_str}\n"
    "Answer: "
)

new_summary_tmpl = PromptTemplate(new_summary_tmpl_str)
query_engine.update_prompts(
    {"response_synthesizer:summary_template": new_summary_tmpl}
)

def predict(user_prompt: str) -> str:
    related_doc = query_engine.query(user_prompt)
    return related_doc


gr.Interface(fn=predict, inputs="text", outputs="text").launch()