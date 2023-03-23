import openai
import process_research as research
import datetime
import os
import sys


# Set your OpenAI API key
openai.api_key = "Insert Open-AI Key"

folder_name = "research_files"
pdf_filenames = research.get_txt_filenames(folder_name)

# Read and extract text from PDF research papers
paper_contents = research.read_txts(pdf_filenames)

research_output = research.process_papers(paper_contents)
print(research_output)


# Get the current date and time
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Format the research_output entry with date, time, and additional information
entry = f"---\nDate: {formatted_datetime}\n\n{research_output}\n\n"

# Append the research_output entry to a text file in the current working directory
with open("research_output_log.txt", "a") as file:
    file.write(entry)
