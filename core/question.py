from langchain_experimental.tools import PythonAstREPLTool
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.openai_tools import JsonOutputKeyToolsParser

def run_csv_question_chain(question: str, locals: dict):
    
    tool = PythonAstREPLTool(locals=locals)

    llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")

    llm_with_tool = llm.bind_tools(tools=[tool], tool_choice=tool.name)

    df_template = """\`\`\`python
    {df_name}.head().to_markdown()
    >>> {df_head}
    \`\`\`"""

    df_context = "\n\n".join(
        df_template.format(df_head=_df.head().to_markdown(), df_name=df_name)
        for _df, df_name in [(locals["heads"], "heads"), (locals["items"], "items")]
    )

    system = f"""You have access to a number of pandas dataframes. \
    Here is a sample of rows from each dataframe and the python code that was used to generate the sample:

    {df_context}

    Given a user question about the dataframes, write the Python code to answer it. \
    Don't assume you have access to any libraries other than built-in Python ones and pandas. \
    Make sure to refer only to the variables mentioned above."""

    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])

    parser = JsonOutputKeyToolsParser(key_name=tool.name, first_tool_only=True)
    chain = prompt | llm_with_tool | parser | tool

    try:
        result = chain.invoke({"question": question})
        return result
    except Exception as e:
        return f"❌ Ocorreu um erro ao tentar responder sua pergunta. Detalhes técnicos: {str(e)}"