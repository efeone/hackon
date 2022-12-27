import frappe
from frappe import _
from frappe.utils import *
from hackon.hackon.utils import *

@frappe.whitelist()
def task_after_insert(doc, method):
    '''Method for Task after_insert event. Will setup Task from Template'''
    if doc.project:
        project_template = frappe.db.get_value('Project', doc.project, 'project_template')
        if project_template:
            template_doc = frappe.get_doc('Project Template', project_template)
            if template_doc.tasks:
                for task_template in template_doc.tasks:
                    if doc.subject == task_template.subject:
                        task_template_doc = frappe.get_doc('Task', task_template.task)
                        doc.response = task_template_doc.response
                        doc.software_tool = task_template_doc.software_tool
                        doc.software_tool_details = task_template_doc.software_tool_details
                        doc.total_weightage = task_template_doc.total_weightage
                doc.save()

@frappe.whitelist()
def validate_task(doc, method):
    ''' Method for validation in Task'''
    validate_task_score(doc)

@frappe.whitelist()
def task_before_save(doc, method):
    ''' Method for before_save event in Task'''
    update_participant_score(doc)

@frappe.whitelist()
def validate_event(doc, method):
    '''Method for validations in Event'''
    validate_registration_date(doc)
    validate_starts_on_date(doc)
