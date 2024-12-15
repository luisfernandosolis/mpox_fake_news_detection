import os
from dotenv import load_dotenv
from langchain.graphs import Neo4jGraph
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from langchain.chains import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
neo4j_url = os.environ.get("NEO4J_URL")
neo4j_username = os.environ.get("NEO4J_USERNAME")
neo4j_password = os.environ.get("NEO4J_PASSWORD")


# Function to remove 'a.' prefix from dictionary keys
def remove_prefix_from_keys(data):
    new_data = []
    for item in data:
        new_item = {key.replace('a.', '').replace("l.",""): value for key, value in item.items()}
        new_data.append(new_item)
    return new_data

class MpoxKgNeo4J():
    def __init__(self) -> None:
        self.graph = Neo4jGraph( url=neo4j_url,  username=neo4j_username,  password=neo4j_password)
    
    def scrape_information(self, url):
        # Step 1: Send a GET request to the webpage you want to scrape
        response = requests.get(url)

        # Step 2: Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 3: Extract the data you need
        
        # You can extract other elements by their tag, class, id, etc.
        # Example: Get all paragraph elements
        data_scrapped = ""
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            data_scrapped+=paragraph.text + "\n"
        
        
        return data_scrapped
    def query_kg(self,query):
        
        ##Query that we can first convert input user in this
        #query = "MATCH (n:News) RETURN n LIMIT 25;"

        ## trnansform query in cypher
        cypher_chain = GraphCypherQAChain.from_llm(
            graph=self.graph,
            cypher_llm=ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-0125"),
            qa_llm=ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo-0125"),
            validate_cypher=True,
            verbose=True,
            allow_dangerous_requests=True,
            return_intermediate_steps=True
        )
        eq = query + " .- Consider this: for the new, return the url,label,the country, the virus, and the abstract. Return the TOP 5 news"

        response =  cypher_chain.invoke({"query": eq})

        Query_Cypher = response['intermediate_steps'][0]["query"]

        response = self.graph.query(
            Query_Cypher
        )

        response_news = remove_prefix_from_keys(response)


        #response_news = self.graph.query(query)

        ##scrape urls
        
        data_result=[]

        # for new in response_news:
        #     url= new["n"]["url"]
        #     content = self.scrape_information(url)
        #     new_content ={
        #         "url":url,
        #         "content":content
        #     }
        #     data_result.append(new_content)


        # #data_temp = pd.DataFrame(data_result)
        # #data_temp.to_csv("data_temp_result_kg.csv", index=False)
        return response_news

if __name__=="__main__":
    kg_database = MpoxKgNeo4J()
    
    ## get news irls
    news_information = kg_database.query_kg(query="MATCH (n:News) RETURN n LIMIT 25;")
    ## print info
    print(news_information)
    


