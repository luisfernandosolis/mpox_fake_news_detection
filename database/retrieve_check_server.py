
from .kg_neo4j.neo4j_service import MpoxKgNeo4J
from .vectordb_qdrant.qdrant_service import QdrantDatabase

def get_new_check_fact(query) -> dict:
    mpox_kg = MpoxKgNeo4J()
    mpox_vdb = QdrantDatabase()


    ## return news and content from database
    try:
        new_info = mpox_kg.query_kg(query) # return list of dict
        #print(new_info)
    except Exception as e:
       print(e)
    
    new_check_result=[]
    for new in new_info:
        try:
            ## verify if the new is fact or now
            score_and_justification = mpox_vdb.check_information(new_info=new["abstract"])
        except:
            score_and_justification = {"score":0.0, "justification":"We can't check the fact of the new, sorry!"}
        new["score"] = score_and_justification["score"]
        new["justification"] = score_and_justification["justification"]
        new_check_result.append(new)

    print("len: ",len(new_check_result))
    #print(new_check_result)
    for i in new_check_result:
        print(i.keys())
    return new_check_result

query="MATCH (n:News) RETURN n LIMIT 3;"
get_new_check_fact(query)










