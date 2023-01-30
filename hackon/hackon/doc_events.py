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

@frappe.whitelist()
def set_user_permission(doc, method):
    '''Method to set User Permissions for team'''
    if doc.team:
        team_doc = frappe.get_doc('Team', doc.team)
        for participant in team_doc.participants:
            user = frappe.db.get_value('Participant', participant.participant, 'user')
            if user:
                if not frappe.db.exists('User Permission', {'user':user, 'allow':'Project', 'for_value':doc.project}):
                    user_permission = frappe.new_doc('User Permission')
                    user_permission.user = user
                    user_permission.allow = 'Project'
                    user_permission.for_value = doc.project
                    user_permission.save(ignore_permissions=True)

@frappe.whitelist()
def set_user_permission_for_user(doc, method):
    '''Method to set User Permissions for user on user creation'''
    if doc.name:
        user_roles = frappe.get_roles(doc.name)
        if (("Host Organizer" in user_roles) or ("Super Admin" in user_roles)):
            if frappe.db.exists('User Permission', {'user':doc.name, 'allow':'User', 'for_value':doc.name}):
                user_permission = frappe.get_doc('User Permission', {'user':doc.name, 'allow':'User', 'for_value':doc.name})
                user_permission.delete()
        elif user_roles:
            if not frappe.db.exists('User Permission', {'user':doc.name, 'allow':'User', 'for_value':doc.name}):
                user_permission = frappe.new_doc('User Permission')
                user_permission.user = doc.name
                user_permission.allow = 'User'
                user_permission.for_value = doc.name
                user_permission.save(ignore_permissions=True)
