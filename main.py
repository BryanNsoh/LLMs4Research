import openai
import PyPDF2
import os
import process_research as research
import datetime

# Set your OpenAI API key
openai.api_key = "your_openai_api_key_here"

folder_path = "./research_files"
pdf_filenames = research.get_pdf_filenames(folder_path)

# Read and extract text from PDF research papers
paper_contents = [research.read_pdf(pdf_filenames[index]) for index in range(0, len(pdf_filenames))]

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