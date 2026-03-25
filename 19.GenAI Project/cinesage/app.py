import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing import List, Optional
import json

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

# -----------------------------
# Define schema
# -----------------------------
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

# -----------------------------
# Parser
# -----------------------------
parser = PydanticOutputParser(pydantic_object=Movie)

# -----------------------------
# Prompt Template
# -----------------------------
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

# -----------------------------
# Model
# -----------------------------
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Movie Info Extractor 🎬", layout="wide")

st.title("🎬 Movie Information Extractor")
st.write("Paste a movie description and extract structured data like a wizard 🧙‍♂️")

# Input box
user_input = st.text_area("Enter Movie Description:", height=200)

# Button
if st.button("Extract Information"):

    if user_input.strip() == "":
        st.warning("Please enter a movie description first.")
    else:
        try:
            # Format prompt
            formatted_prompt = prompt.format(paragraph=user_input)

            # Invoke model
            response = model.invoke(formatted_prompt)

            # Parse output
            parsed_output = parser.parse(response.content)

            result = parsed_output.model_dump()

            # Display JSON
            st.subheader("📦 Structured Output")
            st.json(result)

            # Optional UI Enhancements
            if result.get("poster_url"):
                st.image(result["poster_url"], width=200)

            st.subheader("📝 Summary")
            st.write(result.get("short_summary"))

        except Exception as e:
            st.error("Something went wrong while processing.")
            st.exception(e)