from newspaper import Article
import pandas as pd

data = pd.read_csv("/content/bquxjob_17581d95_19226b21740.csv")

# Function to extract content from a single URL
def extract_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text  # This will contain the full text of the article
    except Exception as e:
        return f"Failed to extract article: {str(e)}"

data["new_content"] = data["url"].apply(lambda x: extract_article_content(x))


clean_data = data.loc[(data["new_content"]!="")]
clean_data

clean_data.loc[~clean_data["new_content"].str.contains("Failed")]
clean_data.to_csv("data_mpox_gdelt_latam.csv", index=False)

## after we use chatpgt for extract the rest of tye columns for get "Final_Mpox_Data_Adjusted.csv".
## based on the KG structure described in neo4j