import requests

# Function to interact with Gemini LLM
def query_gemini_llm(prompt):
    api_key = "AIzaSyDvnfCqBshGrTF2zi6UcUgluioS4StLHoA"  # Replace with your actual API key
    url = "https://api.googleapis.com/v1/gemini:generateText"

    headers = {
        "Authorization": f"Bearer {api_key}"
        
    }

    data = {
        "prompt": prompt,
        "max_tokens": 80
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Attempt to parse the response as JSON
        response_data = response.json()
        return response_data.get('generated_text', '')

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Print the HTTP error
        print("Response content:", response.content)  # Print the response content for further inspection
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")  # Print the request error
    except ValueError:
        print("Response is not in JSON format. Response content:")
        print(response.content)  # Print the raw content of the response

    return None  # Return None or some default value in case of an error

# Function to convert natural language to Cypher using LLM
def convert_to_cypher(natural_query):
  
    prompt = f"Convert the following natural language query to a Cypher query for a Neo4j movie database: '{natural_query}'"
    
    cypher_query = query_gemini_llm(prompt)
    
    if cypher_query:
        return cypher_query.strip()
    else:
        return "Failed to generate Cypher query."

# Example usage
natural_query = "return cast of movies called Twisters"
cypher_query = convert_to_cypher(natural_query)
print(cypher_query)
