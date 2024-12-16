
from PyQt5.QtWidgets import (QVBoxLayout, QWidget,
                             QTextEdit, QComboBox,
                             QPushButton, QLabel,
                             QListWidget, QListWidgetItem,
                             QHBoxLayout, QRadioButton)

from app.resume_controller import ResumeController
from PyQt5.QtCore import pyqtSignal
from app.utils import style_generate_resume_button
from app.constants import DROPDOWN_ITEMS



class ResumeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ResumeController()

        self.setWindowTitle("Resume Tailoring Tool")
        self.layout = QVBoxLayout()

        # Instructions label
        self.instructions = QLabel("Paste the job description below and press 'Generate Resume'")
        self.layout.addWidget(self.instructions)

        # Text box for job description
        self.text_box = QTextEdit(self)
        self.text_box.setPlaceholderText("Paste the job description here...")
        self.layout.addWidget(self.text_box)
        self.text_box.setLineWrapMode(QTextEdit.WidgetWidth)

        # Get suggestions button
        self.get_suggestions_button = QPushButton("Generate Suggestions", self)
        self.get_suggestions_button.clicked.connect(self.get_suggestions)  # Connect button to function
        self.layout.addWidget(self.get_suggestions_button)

        # Generate resume button
        self.generate_resume_button = QPushButton("Generate Resume", self)
        self.generate_resume_button.clicked.connect(self.generate_resume_clicked)  # Connect button to function
        self.layout.addWidget(self.generate_resume_button)
        self.generate_resume_button.setEnabled(False)  # Initially disable the button
        style_generate_resume_button(self.generate_resume_button)

        # Dropdown for actions
        self.action_dropdown = QComboBox(self)
        self.action_dropdown.addItems(DROPDOWN_ITEMS)  # Add options here
        self.action_dropdown.currentIndexChanged.connect(self.handle_action_selection)  # Connect selection event
        self.layout.addWidget(self.action_dropdown)
        self.action = self.action_dropdown.currentText()

        # Status label
        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        # List widget for replacements
        self.replacements_list = QListWidget()
        self.layout.addWidget(self.replacements_list)
        self.replacements_list.setWordWrap(True)

        # Set layout
        self.setLayout(self.layout)

    def handle_action_selection(self, index):
        # Check which action was selected
        self.action = self.action_dropdown.currentText()

    def get_suggestions(self):
        """Delegate processing to the controller."""
        job_description = self.text_box.toPlainText()
        if not job_description.strip():
            self.status_label.setText("Error: Job description cannot be empty.")
            return
        # reset list
        self.replacements_list.clear()

        replacements, status_message = self.controller.request_suggestions(job_description, self.action)
        self.populate_list(replacements, status_message)  # make ui

    def populate_list(self, replacements, status_message):
        """Populate the replacements list in the UI."""
        for i, replacement in enumerate(replacements):
            # Create and configure a QListWidgetItem
            list_item = QListWidgetItem(self.replacements_list)
            list_item.index = i  # Store index as a custom attribute

            # Create a custom widget for the replacement
            custom_widget = ReplacementItemWidget(replacement, i, list_item)

            # Connect widget signals to the appropriate UI methods
            custom_widget.clicked.connect(lambda widget: self.remove_suggestion(widget))
            custom_widget.edited.connect(self.add_edited)

            # Add the widget to the list
            self.replacements_list.setItemWidget(list_item, custom_widget)
            list_item.setSizeHint(custom_widget.sizeHint())
        self.status_label.setText(status_message)
        self.generate_resume_button.setEnabled(True)  # Enable the button after suggestions are generated

    def remove_suggestion(self, item):
        """Remove the clicked suggestion from the list and replacements."""
        self.controller.handle_removal(item, self.replacements_list)
        self.generate_resume_button.setEnabled(True)  # Enable the button after suggestions are generated

    def add_edited(self, index_edited):
        self.controller.add_edited(index_edited)

    def generate_resume_clicked(self):
        status_message = self.controller.handle_generate_resume(self.replacements_list)
        self.generate_resume_button.setEnabled(False)
        self.status_label.setText(status_message)


class ReplacementItemWidget(QWidget):
    clicked = pyqtSignal(object)  # Signal to emit with associated context
    edited = pyqtSignal(int)

    def __init__(self, replacement, index, list_item, parent=None):
        super().__init__(parent)
        # Main layout for the widget
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra spacing

        self.index = index
        self.list_item = list_item

        # Vertical layout for the "Replace" and "With" rows
        text_layout = QVBoxLayout()

        # Replace row
        replace_layout = QHBoxLayout()
        replace_static_label = QLabel("Replace:")  # Non-editable label
        replace_static_label.setWordWrap(True)  # Ensure label text wraps
        self.replace_statement = QTextEdit(replacement.get("replace", ""))  # Editable multi-line field
        self.replace_statement.setWordWrapMode(1)  # Enable word wrapping
        self.replace_statement.setFixedHeight(75)  # Adjust height as needed
        self.replace_statement.setReadOnly(True)
        replace_layout.addWidget(replace_static_label)
        replace_layout.addWidget(self.replace_statement)

        # With row
        with_layout = QHBoxLayout()
        with_static_label = QLabel("    -> With:")  # Non-editable label
        with_static_label.setWordWrap(True)  # Ensure label text wraps
        self.replace_with_editable = QTextEdit(replacement.get("replace_with", ""))  # Editable multi-line field
        self.replace_with_editable.setWordWrapMode(1)  # Enable word wrapping
        self.replace_with_editable.setFixedHeight(75)  # Adjust height as needed
        self.replace_with_editable.textChanged.connect(self.on_with_editable_changed)
        with_layout.addWidget(with_static_label)
        with_layout.addWidget(self.replace_with_editable)

        # Add "Replace" and "With" rows to the text layout
        text_layout.addLayout(replace_layout)
        text_layout.addLayout(with_layout)

        # Radio button for the entire pair
        self.radio_button = QRadioButton()
        self.radio_button.toggled.connect(self.on_radio_button_toggled)

        # Add text layout and radio button to the main layout
        main_layout.addLayout(text_layout)
        main_layout.addWidget(self.radio_button)

        # Set the layout for the widget
        self.setLayout(main_layout)

    def on_radio_button_toggled(self, checked):
        #print("click radio button")
        self.clicked.emit(self)

    def on_with_editable_changed(self):
        # Emit the clicked signal, passing context if needed
        #print("text field edited")
        self.edited.emit(self.index)
