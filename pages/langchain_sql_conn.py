from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain import OpenAI, LLMChain, SQLDatabase, SQLDatabaseChain
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

from langchain.chains.sql_database.prompt import SQL_PROMPTS
import streamlit as st
import time


PROMPT_SUFFIX = """Only use the following tables:
{table_info}

Question: {input}"""
_snowflake_prompt = """You are a Snowflake Database expert. Given an input question, first create a syntactically correct Snowflake query to run, then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MariaDB. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURRENT_DATE() function to get the current date, if the question involves "today".

Use DATEADD( <date_or_time_part>, <value>, <date_or_time_expr> ) which Adds the specified value for the specified date or time part to a date, time, or timestamp.

Example:

SELECT l_shipdate, SUM(l_extendedprice) AS total_price, SUM(l_discount) AS total_discount
FROM lineitem WHERE l_shipdate <= dateadd('DAY', -90, CURRENT_DATE())
 GROUP BY l_shipdate ORDER BY l_shipdate DESC LIMIT 100000

"""


SNOWFLAKE_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template=_snowflake_prompt + PROMPT_SUFFIX,
)

QUERY_CHECKER = """
{query}
Double check the {dialect} query above for common mistakes, including:
- Using NOT IN with NULL values
- Using UNION when UNION ALL should have been used
- Using BETWEEN for exclusive ranges
- Data type mismatch in predicates
- Properly quoting identifiers
- Using the correct number of arguments for functions
- Casting to the correct data type
- Using the proper columns for joins

If there are any of the above mistakes, rewrite the query. If there are no mistakes, just reproduce the original query."""


query_checker_prompt = PromptTemplate(template=QUERY_CHECKER, input_variables=["query", "dialect"] )
st.set_page_config(page_title="Connect to Snowflake", page_icon="")

st.sidebar.header("SQL Generation with Langchain Demo")


st.markdown('''## Functionality
It is a toy example to connect to Snowflake and Query - code is using Langchain and Open AI.
This example uses following Langchain functionalities:

- Example Sets
- LLM Chain - Using OpenAI

Example Use Case:

1. Pricing Summary Report Query provide a summary pricing report for all line items shipped as of a given date. The date is within 90 days of the greatest ship date contained in the database.

2. Find which supplier can supply parts of size of 50 and type like BRASS in EUROPE  at minimum cost.


''')

def create_conn(sf_user, sf_pass, sf_org, sf_acc):
    with st.spinner(text="Snowflake Connection in progress..."):
        db = SQLDatabase.from_uri(f'snowflake://{sf_user}:{sf_pass}@{sf_org}-{sf_acc}/SNOWFLAKE_SAMPLE_DATA/TPCH_SF1')
    st.write("Snowflake Connection done...")
    return db

def call_llm(api_key_oi, db,input ):
    with st.spinner(text="LLM calls in progress..."):
        llm = OpenAI(temperature=0,
                     openai_api_key=api_key_oi,
                     )


        ####
        input_text = f"{input}\nSQLQuery:"
        table_info = db.get_table_info()
        prompt = SNOWFLAKE_PROMPT
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        llm_inputs = {
                    "input": input_text,
                    "top_k": 100000,
                    "dialect": db.dialect,
                    "table_info": table_info,
                    "stop": ["\nSQLResult:"],
                }


        sql_cmd = llm_chain.predict(**llm_inputs).strip().split(';')[0]



        query_checker_chain = LLMChain(llm=llm_chain.llm, prompt=query_checker_prompt)
        query_checker_inputs = {"query": sql_cmd,"dialect": db.dialect  }

        checked_sql_command: str = query_checker_chain.predict( **query_checker_inputs).strip()



    return sql_cmd, checked_sql_command

st.header("Snowflake TPC-H Schema")
st.image("https://www.researchgate.net/profile/Teodora-Buda/publication/315535249/figure/fig3/AS:667884921552938@1536247582935/The-TPC-H-database-schema.png")


SNOWFLAKE_USER = st.text_input(label= "SNOWFLAKE_USER",
               max_chars=None,
               key='SNOWFLAKE_USER',
               placeholder="Type Your SNOWFLAKE USER Here")
SNOWFLAKE_PASSWORD = st.text_input(label= "SNOWFLAKE_PASSWORD", type="password",
               max_chars=None,
               key='SNOWFLAKE_PASSWORD',
               placeholder="Type Your SNOWFLAKE_PASSWORD Here")
SNOWFLAKE_ORG_ID = st.text_input(label= "SNOWFLAKE_ORG_ID",
               max_chars=None,
               key='SNOWFLAKE_ORG_ID',
               placeholder="Type Your SNOWFLAKE_ORG_ID Here")
SNOWFLAKE_ACCOUNT = st.text_input(label= "SNOWFLAKE_ACCOUNT",  
               max_chars=None,
               key='SNOWFLAKE_ACCOUNT',
               placeholder="Type Your SNOWFLAKE_ACCOUNT Here")

if SNOWFLAKE_PASSWORD and SNOWFLAKE_USER and  SNOWFLAKE_ORG_ID and SNOWFLAKE_ACCOUNT:

    sdb = create_conn(SNOWFLAKE_USER, SNOWFLAKE_PASSWORD, SNOWFLAKE_ORG_ID, SNOWFLAKE_ACCOUNT)


    api_key_oi = st.text_input(label= "Open AI Key",
                               placeholder="Type Your Open AI API Key Here",
                               )


    input = st.text_input(label="Ask a Question")

    if sdb and api_key_oi and input:

        sql_cmd, checked_sql_command = call_llm(api_key_oi, sdb,input )

        st.markdown("### Raw SQL returned by LLM ")
        st.write(sql_cmd)


        st.markdown("### Re-written SQL by Query Checker ")
        st.write(checked_sql_command)



st.button("Re-run")
