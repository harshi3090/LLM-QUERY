from langchain_huggingface import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables
load_dotenv()

# Neo4j connection details
uri = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')

# Initialize Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

# Define a function to query Neo4j
def query_neo4j(query):
    with driver.session() as session:
        result = session.run(query)
        return [record.data() for record in result]

# Define a function to sanitize the Cypher query
def sanitize_query(cypher_query):
    # Basic sanitation to remove unwanted text
    if "Cypher Query:" in cypher_query:
        cypher_query = cypher_query.split("Cypher Query:")[-1].strip()
    return cypher_query

# Set up Hugging Face pipeline
hf_pipeline = pipeline("text2text-generation", model="facebook/bart-large-cnn")
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# Define the revised prompt template
template = """


User Query: {user_query}

Cypher Query:
"""

# Initialize LangChain components
prompt = PromptTemplate(template=template, input_variables=["user_query"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

# Function to process a natural language query and execute it against Neo4j
def process_query(user_query):
    # Generate Cypher query using LLM
    cypher_query = llm_chain.run({"user_query": user_query}).strip()
    print(f"Generated Cypher Query: {cypher_query}")

    # Sanitize the query
    cypher_query = sanitize_query(cypher_query)
    
    # Execute the Cypher query against Neo4j
    results = query_neo4j(cypher_query)
    return results

# Example usage
user_query = "What is the ReleaseDate of The Union?"
results = process_query(user_query)

print("Query Results:")
for result in results:
    print(result)

# Close Neo4j driver
driver.close()
