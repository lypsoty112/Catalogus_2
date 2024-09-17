import io
import re
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_core.messages.ai import AIMessage
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers.fix import OutputFixingParser
from pydantic import BaseModel, Field
import dotenv

dotenv.load_dotenv()

PROMPT = """
You are tasked with writing Python code to answer a specific question using a provided DataFrame. Your goal is to create a function that processes the data and returns either a DataFrame or a Plotly figure as the answer.

Here's the question you need to answer:
<question>
{question}
</question>

The DataFrame you'll be working with has the following structure:
<df_info>
{df_info}
</df_info>

Your task is to fill in the following Python function:

```python
import pandas as pd
import plotly
def answer_question(df: pd.DataFrame) -> pd.DataFrame | plotly.graph_objs.Figure:
    # YOUR CODE GOES HERE
```

When writing your code, please follow these guidelines:
1. You can only use the pandas and plotly libraries, which are already imported.
2. Your function should take a pandas DataFrame as input and return either a pandas DataFrame or a plotly.graph_objs.Figure as output. It can't return both.
3. Make sure your code directly answers the given question using the provided data.
4. If the question requires data manipulation, use appropriate pandas functions.
5. If the question asks for a visualization, create a suitable Plotly figure.
6. Comment your code to explain the logic behind your solution.
7. You have a preference for visualisations above dataframes.
8. If you're returning a single value, provide just a dataframe with a single row.

IMPORTANT: Before writing the code, write down your thought process.

After writing your code, format your answer according to these instructions:
<format_instructions>

Provide the python code between these <CODE> </CODE> tags.

</format_instructions>

<example response>

<CODE>
import pandas as pd
import plotly
def answer_question(df: pd.DataFrame) -> pd.DataFrame | plotly.graph_objs.Figure:
    return df

</CODE>

</example response>

Remember to strictly follow the format instructions provided above when presenting your code solution. Do not include any additional text or explanations outside of the specified format.

Output:
I think..
"""


class Response(BaseModel):
    thoughts: str = Field(description="Write down your thoughts here before performing the task.")
    python_code: str = Field(description="Provide python code here that should be added to the method.")
llm = ChatOpenAI(
    temperature=.2,
    model_name="gpt-4o"
)
parser = PydanticOutputParser(
    pydantic_object=Response
)


parser = OutputFixingParser.from_llm(
    llm=llm,
    parser=parser
)

template = PromptTemplate.from_template(
    template=PROMPT,
    partial_variables={
    }
)


chain = template | llm

def call_llm(question: str, df: pd.DataFrame):
    buf = io.StringIO()
    df.info(buf=buf)
    df_info = buf.getvalue()
    answer: AIMessage = chain.invoke({
        "question": question,
        "df_info": df_info
    })

    # Get anything between <CODE> & </CODE>
    pattern = r"<CODE>(.*?)<\/CODE>"
    print(answer.content)
    code_block = re.findall(pattern, answer.content, re.DOTALL)
    if code_block:
        single_string_code = code_block[0].strip()  # Replaces line breaks with \n
        return single_string_code

    return ""