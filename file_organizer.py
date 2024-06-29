import os
import re
import shutil
from PyPDF2 import PdfReader

def extract_text_from_first_page(pdf_path):
    """
    Extracts text from the first page of a PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        if len(reader.pages) > 0:
            first_page = reader.pages[0]
            text = first_page.extract_text()
            return text
    return ""

def extract_text_from_doc(doc_path):
    """
    Extracts text from a DOC file (for simplicity, we'll assume it's a DOCX file).
    """
    try:
        import docx
    except ImportError:
        raise ImportError("Please install python-docx to handle DOC files.")
    
    doc = docx.Document(doc_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text_from_txt(txt_path):
    """
    Extracts text from a TXT file.
    """
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def generate_new_filename(text, file_path):
    """
    Generates a new filename based on extracted text.
    This example extracts the first line of text and sanitizes it for use as a filename.
    """
    # Extract the first line or a pattern that is significant for the filename
    first_line = text.split('\n')[0]
    
    # Sanitize the first line to be a valid filename
    # Windows does not allow the following characters in filenames: \ / : * ? " < > |
    new_filename = re.sub(r'[\\/:*?"<>|]', '', first_line).strip()
    new_filename = '_'.join(new_filename.split())
    
    # Get the extension of the original file
    extension = os.path.splitext(file_path)[1]
    
    # Ensure the new filename has the original file extension
    new_filename += extension
    
    # Construct the full new path
    directory = os.path.dirname(file_path)
    new_path = os.path.join(directory, new_filename)
    
    return new_path

def rename_file(file_path, extract_text_function):
    """
    Renames the given file based on its content.
    """
    # Extract text from the file using the provided function
    text = extract_text_function(file_path)
    
    # Generate a new filename based on the extracted text
    new_path = generate_new_filename(text, file_path)
    
    # Rename the file if the new filename is different
    if file_path != new_path:
        os.rename(file_path, new_path)
        print(f'Renamed "{file_path}" to "{new_path}"')
    else:
        print(f'No renaming needed for "{file_path}"')

    return new_path  # Return the new path for further processing

def organize_files_by_extension(path):
    """
    Organizes files by their extensions and renames PDF, DOC, and TXT files based on their content.
    """
    if not os.path.exists(path):
        print("The provided path does not exist.")
        exit(1)

    files = os.listdir(path)

    for file in files:
        full_file_path = os.path.join(path, file)

        if os.path.isfile(full_file_path):
            filename, extension = os.path.splitext(file)
            extension = extension[1:].lower()

            if not extension:
                continue

            if extension in ['pdf', 'doc', 'docx', 'txt']:
                rename_file_prompt = input(f"Do you want to rename the file '{file}' based on its content? (yes/no): ").strip().lower()
                if rename_file_prompt == 'yes':
                    if extension == 'pdf':
                        new_file_path = rename_file(full_file_path, extract_text_from_first_page)
                    elif extension in ['doc', 'docx']:
                        new_file_path = rename_file(full_file_path, extract_text_from_doc)
                    elif extension == 'txt':
                        new_file_path = rename_file(full_file_path, extract_text_from_txt)
                else:
                    new_file_path = full_file_path
            else:
                new_file_path = full_file_path  # No renaming needed

            extension_dir = os.path.join(path, extension)
            if not os.path.exists(extension_dir):
                os.makedirs(extension_dir)

            shutil.move(new_file_path, os.path.join(extension_dir, os.path.basename(new_file_path)))

    print("Files have been organized by their extensions.")

# Prompt the user to enter the path
path = input("Enter Path (e.g., C:\\Users\\YourUsername\\Documents or /home/yourusername/documents): ")

organize_files_by_extension(path)
