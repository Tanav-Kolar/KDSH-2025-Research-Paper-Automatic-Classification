import os
from pathlib import Path
from pdfminer.high_level import extract_text

# Get file paths from the data folder.
def get_pdf_files(directory):
    """
    Get a list of all PDF files in the specified directory and its subdirectories.
    """
    pdf_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files


data_folder = Path("Data")
pdf_files = get_pdf_files(data_folder)

# Extract text from each PDF file and save it to a text file.
for pdf_file in pdf_files:
    text = extract_text(pdf_file)
    text_file_path = pdf_file.replace('.pdf', '.txt')
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

 # Create a corresponding folder structure in Data/raw_text and save the extracted text.
    raw_text_folder = Path("Data/raw_text")
    raw_text_folder.mkdir(parents=True, exist_ok=True)

for pdf_file in pdf_files:
    relative_path = Path(pdf_file).relative_to(data_folder)
    text_file_path = raw_text_folder / relative_path.with_suffix('.txt')
    text_file_path.parent.mkdir(parents=True, exist_ok=True)
    text = extract_text(pdf_file)
    with open(text_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

