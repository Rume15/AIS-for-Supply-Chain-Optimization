import streamlit as st
import time
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.firecrawl import FirecrawlTools
import openai


import time
import io
import sys
import os
import re
import logging
from dotenv import load_dotenv
load_dotenv()
openai.api_key=os.getenv("OPENAI_API_KEY")

# Suppress unnecessary logging
logging.basicConfig(level=logging.ERROR)

# Pass firecrawl api
firecrawl_tools = FirecrawlTools(api_key=os.getenv("FIRECRAWL_API_KEY"))


agent = Agent(
    name="health assistant",
    model=Gemini(id="gemini-2.0-flash-exp"),
    instructions=[
        "You are a health assistant agent specializing in providing information on symptoms and remedies for various diseases.",
        "Use only trusted health resources like MedlinePlus, WebMD, NIH, Harvard Health Publishing, and Mayo Clinic for gathering information.",
        "When a user asks about a disease, provide possible symptoms, and suggest remedies or treatment options based on the information from these trusted sources.",
        "Always prioritize accuracy and relevance to the user's query.",
        "Ensure that you provide remedies that are general and supported by reputable health sources.",
        "Avoid offering specific medical advice or treatments and recommend consulting a healthcare professional for personalized care.",
        "Format your response in a clear and easy-to-understand manner, highlighting key information.",
    ],
    tools=[firecrawl_tools],
)


def clean_output(raw_text):
    """
    Remove ANSI escape sequences and unnecessary logs from the output.
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', raw_text)
    return clean_text.strip()


# Streamlit app layout
st.title("Health Assistant")
st.write("You got any health related question I gat you!")

# Input field for the user query
query = st.text_input("Enter your query:")

# Button to trigger the agent's response
if st.button("Get Response") and query:
    with st.spinner("Fetching response..."):
        try:
            # Capture the response from the agent
            import io
            import sys

            captured_output = io.StringIO()
            sys.stdout = captured_output  # Redirect stdout temporarily
            try:
                agent.print_response(query)
            finally:
                sys.stdout = sys.__stdout__  # Restore stdout

            # Clean up and display the response
            raw_response = captured_output.getvalue()
            clean_response = clean_output(raw_response)
            st.success("Here's what I found:")
            st.write(clean_response)
        except Exception as e:
            st.error("Sorry, an error occurred while fetching the response.")
            st.write(f"Error details: {e}")
