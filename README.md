# Project Setup Notes

## Google Docs API (Doc Manager)

### Set Up Google Cloud Console
- Created a new project named **"Resume Automation"**.
- Enabled the following APIs:
  - **Google Docs API**
  - **Google Drive API**
- Generated a `credentials.json` file for service account authentication.

### Grant Access to Google Doc
- Shared the specified Google Doc with the email associated with the service account (found in `credentials.json`).

### Obtain Google Doc ID
- Extracted the Google Doc ID from the URL of the document:

  Example URL: `https://docs.google.com/document/d/<DOC_ID>/edit`

- Stored the `DOC_ID` for use in the program.

### Document Automation
- Added a function to dynamically manage and process the Google Doc:
  - Apply changes.
  - Export as PDF.
  - Restore content.
  - Export page 2 of resume as pdf
  - Combine pdfs

## OpenAI Integration

### OpenAI API Access
- Logged into OpenAI using **email**.
- Generated an API key for use in the project.

### ChatGPT Integration
- Configured ChatGPT API (**gpt-4o-mini**) for generating resume line replacements based on job descriptions.
- Designed a prompt structure to:
  - Analyze job descriptions.
  - Suggest no more than three replacements.
  - Output results in JSON format.

### Environment Variables
- Stored the OpenAI API key in `.env.local` for secure access.

## User Interface (UI)

### GUI Development
- Built a **PyQt5 GUI** for the project:
  - **Text Input:** A field to paste job descriptions.
  - **Button:** A "Generate Resume" button to trigger the automation process.
  - **Status Label:** Displays processing status and errors.

### Functionality
- Connected the GUI to:
  - **OpenAI API** (for generating replacements).
  - **Google Docs API** (to update and export the resume).
- Added error handling for invalid inputs and API issues.

### Bug Fixes
- Resolved issues with window resizing when input text was long.
- Ensured that paths (e.g., for credentials and environment files) dynamically resolve using a helper function (`resolve_path`).

## Bash Script (Automation)

### File Monitoring
- Wrote a bash script to monitor the directory for the creation of `Updated_Resume.pdf`.

### File Management
- Upon detecting a new `Updated_Resume.pdf`:
  - Moves the new PDF to a specified folder.
  - Archives older resume files being replaced.

### Triggering
- Script runs in the background and seamlessly integrates with the automated process.

## Workflow Summary

1. Paste a job description into the GUI.
2. Click the **"Generate Resume"** button.
3. The program:
   - Queries ChatGPT for replacements.
   - Updates the Google Doc.
   - Exports the updated resume as a PDF.
4. The bash script:
   - Detects the new `Updated_Resume.pdf`.
   - Moves the file and manages archives.
5. The original Google Doc content is restored.
