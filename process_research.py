import openai
import os
import glob
from langchain import PromptTemplate


# Get the names of the research files
def get_txt_filenames(folder_name):
    cwd = os.getcwd()
    txt_pattern = os.path.join(cwd, folder_name, "*.txt")
    txt_filepaths = [file for file in glob.glob(txt_pattern, recursive=True)]
    return txt_filepaths


# Function to read PDF files and extract text
def read_txts(txt_files):
    file_contents = []
    for txt_file in txt_files:
        with open(txt_file, "rb") as file:
            lines = file.readlines()
            file_contents.append(lines)
    return file_contents


# Function to summarize a given research paper
def summarize_paper(paper_content, chunk_size=3000):
    chunks = [
        paper_content[i : i + chunk_size]
        for i in range(0, len(paper_content), chunk_size)
    ]
    summarized_points = []
    citation = ""

    for chunk in chunks:
        prompt = f"""Answer the questions based on the context below. If the
question cannot be answered using the information provided, answer
with "I don't know".

Context: Large Language Models (LLMs) have been the source of many breakthroughs in AI. 
They have the potential to revolutionize many fields ranging from research science to business. 
An astute researcher is currently investigating the applications of large language models
for irrigation scheduling based on big data and remote sensing inspired by the following partial research paper: \n
{chunk}

Question 1: Produce an in-line citation for this paper using the APA 6th format according to citation best practices.

Question 2: Produce bullet points that capture the main arguments and insights of this part of the paper.

Answer: """

        chunk_length = len(chunk_size)
        prompt_len = len(prompt)
        max_tokens = 4096 - len(prompt)

        response = openai.Completion.create(
            engine="text-curie-001",
            prompt=prompt,
            max_tokens=4096 - len(prompt),  # Reserve enough tokens for the response
            n=1,
            stop=None,
            temperature=0.7,
        )

        answers = response.choices[0].text.strip().split("\n")

        if not citation:
            citation = answers[0].strip()

        summarized_points.extend(answers[1:])

    # Select only 10 bullet points for the summary
    summary_points = summarized_points[:10]

    # Add the in-line citation generated by the model as the first point
    summary_points.insert(0, citation)

    with open("summary.txt", "a", encoding="utf-8") as file:
        file.write(summary_points)

    return "\n".join(summary_points)


# Function to generate new material based on the input research papers
def generate_research_output(summaries):
    pt = PromptTemplate()

    pt.add_question(
        "Based on these summaries, what new research insights can be derived?"
    )
    pt.add_instruction(
        "Write an abstract for a scientific paper on the applications of Large Language models in Irrigation scheduling:"
    )
    pt.add_data("\n".join(summaries))

    prompt = pt.compile_prompt()

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.3,
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
