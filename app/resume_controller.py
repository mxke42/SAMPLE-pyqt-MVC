
from app.resume_model import ResumeModel


class ResumeController:
    def __init__(self):
        self.model = ResumeModel()

    def reset(self):
        self.model.reset()

    def add_replacements(self, replacements):
        self.model.add_replacements(replacements)

    def remove_replacement(self, index):
        self.model.remove_replacement(index)

    def discard_edited(self, index):
        self.model.discard_edited(index)

    def handle_removal(self, item, replacements_list):
        index = getattr(item, 'index', None)
        if index is not None:
            self.remove_replacement(index)
            self.discard_edited(index) # discard from edited list, if there
        replacements_list.takeItem(replacements_list.row(item.list_item))

    def handle_generate_resume(self, replacements_list):
        replacements_list = self.request_replacements_list(replacements_list)
        status_message = self.model.generate_resume(replacements_list)
        return status_message

    def add_edited(self, index_edited):
        self.model.add_edited(index_edited)

    def request_replacements_list(self, replacements_list):
        return self.model.generate_replacements_list(replacements_list)

    def request_suggestions(self, job_description, action):
        self.reset()
        replacements, status_message = self.model.generate_suggestions(job_description, action)
        self.add_replacements(replacements)
        return replacements, status_message




