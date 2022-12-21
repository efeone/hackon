import frappe
from frappe.utils import *
from frappe import _

@frappe.whitelist()
def project_template(doc, method = None):
    if doc.project:
        template = frappe.db.get_value('Project', doc.project, 'project_template')
        if template:
            template_doc = frappe.get_doc('Project Template', template)
            if template_doc.tasks:
                for task in template_doc.tasks:
                    if doc.subject == task.subject and task.response:
                        doc.response = task.response
                        if task.url:
                            doc.url = task.url
                        elif task.attachment:
                            doc.attachment = task.attachment
                        elif task.data:
                            doc.data = task.data
                        else:
                            doc.text = task.text
                doc.save()

@frappe.whitelist()
def update_team_score_to_project(doc, method):
    if doc.project:
        team_score = get_total_team_score(doc.project) - frappe.db.get_value('Task', doc.name, 'team_score') + doc.team_score
        frappe.db.set_value('Project', doc.project, 'team_score', team_score)
        frappe.db.commit()

@frappe.whitelist()
def update_team_score_to_team(doc, method):
    if doc.project:
        team = frappe.db.get_value('Project', doc.project, 'team')
        if team:
            team_score = get_total_team_score(doc.project) - frappe.db.get_value('Task', doc.name, 'team_score') + doc.team_score
            frappe.db.set_value('Team', team, 'team_score', team_score)
            frappe.db.commit()

@frappe.whitelist()
def get_total_team_score(project):
    query = """
        SELECT
            IFNULL(SUM(team_score),0) as total_task_score
        FROM
            tabTask
        WHERE
            project = %(project)s
    """
    doc_list = frappe.db.sql(query.format(),{ 'project' : project }, as_dict = 1)
    return (doc_list[0].total_task_score)


#Validation of Events#
@frappe.whitelist()
def event_scheduler():
    '''Method to validate event based on date'''
    events = frappe.db.get_all('Event', filters = {'status': 'Open'})
    if events:
        today = getdate(frappe.utils.today())
        for event in events:
            event_doc = frappe.get_doc('Event', event.name)
            due_date = getdate(event_doc.ends_on)
            if due_date < today:
                change_event_status(event_doc)

def change_event_status(doc):
    '''method to change the status of event
       args: doc:event document
    '''
    frappe.db.set_value(doc.doctype, doc.name, 'status', 'Closed')
    frappe.db.commit()

@frappe.whitelist()
def create_notification_log(subject, for_user, email_content, document_type, document_name):
    notification_doc = frappe.new_doc('Notification Log')
    notification_doc.subject = subject
    notification_doc.type = 'Mention'
    notification_doc.for_user = for_user
    notification_doc.email_content = email_content
    notification_doc.document_type = document_type
    notification_doc.document_name = document_name
    notification_doc.save()
    frappe.db.commit()

@frappe.whitelist()
def update_participant_score(doc, method = None):
    if doc.participant:
        frappe.db.set_value('Participant', doc.participant, 'participant_score', doc.total_weightage_earned + doc.team_score)
        team_doc = frappe.get_doc('Team', doc.team)
        teamscore = 0
        for participant_details in team_doc.participants:
            if participant_details.participant == doc.participant:
                participant_details.participant_score = doc.total_weightage_earned + doc.team_score
        team_doc.save()

@frappe.whitelist()
def get_software_tool_weightage(software_tool):
    weightage = frappe.db.get_value('Software Tool', software_tool, 'weightage') if frappe.db.get_value('Software Tool', software_tool, 'weightage') else 0
    return weightage

@frappe.whitelist()
def get_software_tool_weightage_from_task(software_tool, task):
    weightage = 0
    task_doc = frappe.get_doc('Task', task)
    for tool in task_doc.software_tool_details:
        if software_tool == tool.software_tool:
            weightage = tool.weightage
    return weightage
# validate of Task score #
@frappe.whitelist()
def validation_of_task_score(doc, method = None):
    if doc.team_score > doc.maximum_participant_score:
        frappe.throw(title = _('ALERT !!'),
        msg = _('Task Score Greater than Maximum Participant Score !')
        )
def get_permission_query_conditions_for_participant(user):
    if not user:
        user = frappe.session.user

    user_roles = frappe.get_roles(user)
    if user == "Administrator" or "Host Organizer" in user_roles:
        return None
    else:
        conditions = '(`tabParticipant`.`_assign` like "%{user}%") OR(`tabParticipant`.`owner` = "{user}")'.format(user = user)
        return conditions

def get_permission_query_conditions_for_event_request(user):
    if not user:
        user = frappe.session.user

    user_roles = frappe.get_roles(user)
    if user == "Administrator":
        return None
    else:
        conditions = '(`tabEvent Request`.`_assign` like "%{user}%") OR(`tabEvent Request`.`owner` = "{user}")'.format(user = user)
        return conditions

def change_user_role(user, role_profile):
    ''' Method to change Role of an User'''
    if frappe.db.exists('User', user):
        user_doc = frappe.get_doc('User', user)
        user_doc.role_profile_name = role_profile
        user_doc.save()
@frappe.whitelist()
def validation_of_starting_date(doc, method = None):
    if doc.registration_ends_on >= doc.starts_on :
        frappe.throw(title = _('ALERT !!'),
        msg = _('Set Valid Start Date !')
        )
