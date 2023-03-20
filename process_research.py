import openai
import PyPDF2
import os
import glob
from langchain import PromptBuilder


# Get the names of the research files
def get_pdf_filenames(folder_path):
    pdf_pattern = os.path.join(os.getcwd(folder_path), '*.pdf')
    pdf_filepaths = [file for file in glob.glob(pdf_pattern, recursive=True)]
    return pdf_filepaths

folder_path = 'path/to/your/folder'
pdf_filenames = get_pdf_filenames(folder_path)
print(pdf_filenames)


# Function to read PDF files and extract text
def read_pdf(pdf_files):
    text = ""
    for pdf_file in pdf_files:
        with open(pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfFileReader(file)
            for page in range(pdf_reader.numPages):
                text += pdf_reader.getPage(page).extractText()
    return text


# Function to generate text with OpenAI API
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Function to summarize a given research paper
def summarize_paper(paper_content):
    pb = PromptBuilder()
    
    pb.add_question("What is the main objective of this research paper?")
    pb.add_instruction("Develop an appropriate in-line citation for this research paper:")
    pb.add_instruction("Summarize the following research paper in 2-3 sentences:")
    pb.add_instruction("Produce five points that capture the main arguments and insights of this paper")
    pb.add_data(paper_content)
    
    prompt = pb.compile_prompt()
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    summary = response.choices[0].text.strip()
    return summary


# Function to generate new material based on the input research papers
def generate_research_output(summaries):
    pb = PromptBuilder()
    
    pb.add_question("Based on these summaries, what new research insights can be derived?")
    pb.add_instruction("Write as abstract for a scientific paper on the applications of Large Language models in Irrigation scheduling:")
    pb.add_data("\n".join(summaries))
    
    prompt = pb.compile_prompt()
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.7,
    )

    output = response.choices[0].text.strip()
    return output


def process_papers(paper_contents):
    summaries = []

    for paper_content in paper_contents:
        summary = summarize_paper(paper_content)
        summaries.append(summary)

    research_output = generate_research_output(summaries)
    return research_output
