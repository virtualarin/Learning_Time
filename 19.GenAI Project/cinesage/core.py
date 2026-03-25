from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional
from langchain_google_genai import ChatGoogleGenerativeAI

# Define schema
class Movie(BaseModel):
    title: str
    type: str
    genre: List[str]
    release_year: Optional[int]
    key_people: List[str]
    rating: Optional[float]
    key_entities: List[str]
    themes: List[str]
    setting: Optional[str]
    notable_features: List[str]
    poster_url: Optional[str]
    short_summary: str

# Parser
parser = PydanticOutputParser(pydantic_object=Movie)

# Load API key
load_dotenv()

# Prompt template
prompt = PromptTemplate(
    template="""
You are an expert information extraction system.

Extract structured movie information from the given paragraph.

{format_instructions}

Paragraph:
{paragraph}
""",
    input_variables=["paragraph"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

# Input
input_text = input("Enter the movie description: ")

# Format prompt
formatted_prompt = prompt.format(paragraph=input_text)

# Invoke model
response = model.invoke(formatted_prompt)

# Parse output
parsed_output = parser.parse(response.content)

# Print structured result
print(parsed_output.model_dump_json(indent=4))