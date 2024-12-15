from qdrant_client import QdrantClient
import os 
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel, Field
from langchain.vectorstores import Qdrant

load_dotenv()

QDRANT_CLOUD_URL = os.environ.get("QDRANT_CLOUD_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

# Define your desired data structure.
class NewsChecker(BaseModel):
    score: str = Field(description="a score between 0 and 1, where 1 means the news is completely true and closer to 0 means it is false", default=0)
    justification: str = Field(description="a justification about the score", default="Ninguna")

class QdrantDatabase():
    def __init__(self) -> None:
        self.client = QdrantClient(url=QDRANT_CLOUD_URL,api_key=QDRANT_API_KEY)
        self.vector_store = Qdrant(client=self.client,collection_name="mpox_collection",embeddings=OpenAIEmbeddings(model="text-embedding-3-small"))

    def retrieve_information(self, query):
        context = self.vector_store.similarity_search(query=query, k=5)
        return context
    def check_information(self,new_info):

        fact_information = " ".join([i.page_content for i in self.retrieve_information(query=new_info)])
        parser = PydanticOutputParser(pydantic_object=NewsChecker)
        template = """
            You are an expert information verification assistant. I am going to provide you with a set of verified facts that are considered true. Then I will provide you with a news story and your task will be to compare the facts in the news with the true information provided, and determine how true the news is on a scale of 0 to 1, where 0 means the news is completely false and 1 means it is completely false. completely true. Provide your evaluation by briefly explaining the reasons for your score, and justify why you assigned that truthfulness number.
            ### Verified information:
            {fact_information}

            ### News to evaluate:
            {new_information}

            ### Expected result:
            - **Veracity score(0 a 1):**
            - **Scoring reason:**
            - **Scoring justification:**
            {format_instructions}
        """
        prompt = PromptTemplate(
            template=template,
            input_variables=["new_information","fact_information"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        model = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.5)

        # And a query intended to prompt a language model to populate the data structure.
        prompt_and_model = prompt | model
        output = prompt_and_model.invoke({"new_information":new_info, "fact_information":fact_information})
        result = parser.invoke(output)
        print("#"*50)
        print(result)
        news_fact_score = {
            "score":result.score,
            "justification":result.justification
        }
        return news_fact_score

if __name__=="__main__":

    qdrant = QdrantDatabase()
    
    print("*"*10)
    new_information="""
        Title of the page: Esquema das joias movimentou R$ 6,8 mi; Bolsonaro recebeu dinheiro vivo, diz PF
        Ex-presidente Jair Bolsonaro é indiciado pela PF no caso das joias
        Moraes retira sigilo do inquérito das joias e manda PGR se manifestar
        DÃª a sua opiniÃ£o! O Correio tem um espaÃ§o na ediÃ§Ã£o impressa para publicar a opiniÃ£o dos leitores pelo e-mail sredat.df@dabr.com.br
        RepÃ³rter de polÃ­tica, setorista do Supremo Tribunal Federal (STF). Vencedor do PrÃªmio CNT de Jornalismo, possuÃ­ passagens pelo SBT, Record/R7 e estÃ¡ entre os jornalistas mais influentes do Twitter no Brasil.
        Formada em Jornalismo pela UFSM, no RS, onde pesquisou sobre Jornalismo Internacional, focado em AmÃ©rica Latina. JÃ¡ trabalhou com Cultura, Entretenimento, Redes Sociais, GÃªnero e Minorias Sociais.
    """
    res = qdrant.check_information(new_info=new_information)
    print(res)
    