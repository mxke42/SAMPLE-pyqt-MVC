from app.suggestion_generator import generate_replacements, generate_concise_description
from app.doc_manager import process_resume
from app.utils import resolve_path
from app.file_manager import process_new_resume

from PyQt5.QtCore import QObject, pyqtSignal


class ResumeModel(QObject):
    data_changed = pyqtSignal(set)  # Signal to notify when the data changes

    def __init__(self):
        super().__init__()
        self._edited_list = set()  # Internal storage for edited indices
        self._replacements = {}

    def reset(self):
        self.clear_replacements()
        self.clear_edited()

    @staticmethod
    def generate_suggestions(job_description, action):
        """Handle the business logic for processing a job description."""
        replacements =[]
        try:
            # Get the paths
            resume_path = resolve_path("resources/resume_text")

            # 1) distill job description
            distilled_description = generate_concise_description(job_description)

            # 2) generate replacements
            replacements = generate_replacements(resume_path, distilled_description, action)

            status_message = "suggestions generated"
        except Exception as e:
            # Handle errors
            status_message = f"Error: {str(e)}"

        return replacements, status_message

    @staticmethod
    def generate_resume(replacements):
        try:
            output_pdf_path = resolve_path("Updated_Resume.pdf")
            process_resume(replacements, output_pdf_path)  # new pdf added to project repo
            process_new_resume()  # move resume to correct location, save old resume
            status_message = "resume generated"
        except Exception as e:
            status_message = f"Error: {str(e)}"

        return status_message

    ### replacements related
    def add_replacements(self, replacements):
        for i, replacement in enumerate(replacements):
            self.add_replacement(i, replacement)

    def add_replacement(self, index, replacement):
        self._replacements[index] = replacement

    def remove_replacement(self, index):
        del self._replacements[index]

    def clear_replacements(self):
        self._replacements.clear()

    def get_replacements(self):
        return self._replacements

    def fetch_updated_replacement(self, index, widget):
        self._replacements[index]["replace_with"] = widget.replace_with_editable.toPlainText()

    def generate_replacements_list(self, list_widget):
        replacements_list = []
        for key in self._replacements:  # replacements looks like {0: {"replace": "", "replace_with": ""}, 1: {}, ...}
            if self.edited_contains(int(key)):
                for row in range(list_widget.count()):
                    list_item = list_widget.item(row)  # Get the QListWidgetItem
                    custom_widget = list_widget.itemWidget(list_item)  # Get the associated ReplacementItemWidget

                    if custom_widget and custom_widget.index == int(key):  # Match the desired key
                        self.fetch_updated_replacement(int(key), custom_widget)  # Process the widget
                        break  # Stop iterating once the correct widget is found
                replacements_list.append(self._replacements[int(key)])
            else:
                # Key is not edited append the original entry
                replacements_list.append(self._replacements[int(key)])

        return replacements_list

    ## edited_list related
    def add_edited(self, index):
        """Add an index to the edited list."""
        self._edited_list.add(index)
        self.data_changed.emit(self._edited_list)  # Notify listeners

    def discard_edited(self, index):
        """Remove an index from the edited list."""
        self._edited_list.discard(index)
        self.data_changed.emit(self._edited_list)  # Notify listeners

    def edited_contains(self, index):
        """Check if an index is in the edited list."""
        return index in self._edited_list

    def clear_edited(self):
        """Clear all indices."""
        self._edited_list.clear()
        self.data_changed.emit(self._edited_list)

    def get_all(self):
        """Get the current set of edited indices."""
        return self._edited_list
