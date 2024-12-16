from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import time
from app.utils import resolve_path
from dotenv import load_dotenv
import os
from PyPDF2 import PdfMerger
# Setup Google Docs API authentication
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# Get the absolute path to the script directory
credentials_path = resolve_path('resources/credentials.json')

# Use the full path for credentials
creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

docs_service = build('docs', 'v1', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)


# Get the absolute path to the .env file
dotenv_path = resolve_path('.env.local')
load_dotenv(dotenv_path=dotenv_path)
google_doc_id = os.getenv("BASE_DOC_ID")
google_doc_id_p2 = os.getenv("PAGE_TWO_BASE_DOC_ID")


def apply_changes(doc_id, replacements):
    """Apply find-and-replace changes to the Google Doc."""
    requests = [
        {
            'replaceAllText': {
                'containsText': {'text': replacement['replace'], 'matchCase': True},  # Exact match required
                'replaceText': replacement['replace_with']  # Replace with this text
            }
        } for replacement in replacements
    ]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()


def restore_content(doc_id, replacements):
    """Revert the changes by restoring original text."""
    requests = [
        {
            'replaceAllText': {
                'containsText': {'text': replacement['replace_with'], 'matchCase': True},
                'replaceText': replacement['replace']
            }
        } for replacement in replacements
    ]
    docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()


def save_as_pdf(doc_id, output_name):
    """Save the Google Doc as a PDF."""
    request = drive_service.files().export(fileId=doc_id, mimeType='application/pdf')
    with open(output_name, 'wb') as pdf_file:
        pdf_file.write(request.execute())



def combine_pdfs(pdf1, pdf2, combined_output):
    """Combine two PDF files into one."""
    merger = PdfMerger()
    merger.append(pdf1)
    merger.append(pdf2)
    merger.write(combined_output)
    merger.close()
    print(f"Combined PDF saved as {combined_output}")


def process_resume(replacements, output_name):
    """Main function to modify, save, and revert the Google Doc."""
    # Step 1: Apply changes
    apply_changes(google_doc_id, replacements)

    # Step 2: Save as PDF page 1
    save_as_pdf(google_doc_id, output_name+"1")
    time.sleep(2)
    # Step 3: Restore original content
    restore_content(google_doc_id, replacements)

    # save page 2 pdf
    save_as_pdf(google_doc_id_p2, output_name+"2")

    combine_pdfs(output_name+"1", output_name+"2", output_name)
    time.sleep(1)


    #time.sleep(2)



    print(f"PDF saved as {output_name} and original content restored.")
