import frappe
from frappe.utils import *
from frappe import _

@frappe.whitelist()
def get_total_task_score(project):
    ''' Method to get sum of Task Score in Tasks by Project'''
    query = """
        SELECT
            IFNULL(SUM(task_score),0) as total_task_score
        FROM
            tabTask
        WHERE
            project = %(project)s
    """
    doc_list = frappe.db.sql(query.format(),{ 'project' : project }, as_dict = 1)
    return (doc_list[0].total_task_score)

@frappe.whitelist()
def daily_event_scheduler():
    '''Method to change Event Status based on Date via daily Scheduler'''
    events = frappe.db.get_all('Event', filters = {'status': 'Open'})
    if events:
        today = getdate(frappe.utils.today())
        for event in events:
            starts_on = getdate(frappe.db.get_value('Event', event.name, 'starts_on')) if frappe.db.get_value('Event', event.name, 'starts_on') else 0
            ends_on = getdate(frappe.db.get_value('Event', event.name, 'ends_on')) if frappe.db.get_value('Event', event.name, 'ends_on') else 0
            if ends_on and ends_on < today:
                change_event_status(event.name, 'Closed')
            if starts_on and starts_on >= today:
                change_event_status(event.name, 'Started')

def change_event_status(docname, status):
    '''method to change the status of event
       args: doc:event document
    '''
    frappe.db.set_value('Event', docname, 'status', status)
    frappe.db.commit()

@frappe.whitelist()
def create_notification_log(subject, for_user, email_content, document_type, document_name):
    ''' Method to Create Notification Log '''
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
def update_participant_score(doc):
    ''' Method to add score from task to Team as participant Score '''
    if doc.participant:
        doc.total_weightage_earned = doc.total_weightage_earned if doc.total_weightage_earned else 0
        doc.task_score = doc.task_score if doc.task_score else 0
        frappe.db.set_value('Participant', doc.participant, 'participant_score', doc.total_weightage_earned + doc.task_score)
        team_doc = frappe.get_doc('Team', doc.team)
        for participant_details in team_doc.participants:
            if participant_details.participant == doc.participant:
                participant_details.participant_score = doc.total_weightage_earned + doc.task_score
        team_doc.save()

@frappe.whitelist()
def get_software_tool_weightage(software_tool):
    ''' Method to fetch Software Tool weightage from Software Tool Master '''
    weightage = frappe.db.get_value('Software Tool', software_tool, 'weightage') if frappe.db.get_value('Software Tool', software_tool, 'weightage') else 0
    return weightage

@frappe.whitelist()
def get_software_tool_weightage_from_task(software_tool, task):
    ''' Method to get Software Tool weightage from Task '''
    weightage = 0
    task_doc = frappe.get_doc('Task', task)
    for tool in task_doc.software_tool_details:
        if software_tool == tool.software_tool:
            weightage = tool.weightage
    return weightage

def validate_task_score(doc):
    ''' Method to validate Task Score Limit in Task'''
    if doc.task_score and doc.maximum_participant_score:
        if float(doc.task_score) > float(doc.maximum_participant_score):
            frappe.throw(
                title = _('ALERT !!'),
                msg = _('Task Score is Greater than Maximum Participant Score !')
            )

def get_permission_query_conditions_for_participant(user):
    ''' Permission query conditions for Participant users'''
    if not user:
        user = frappe.session.user

    user_roles = frappe.get_roles(user)
    if user == "Administrator" or "Host Organizer" in user_roles:
        return None
    else:
        conditions = '(`tabParticipant`.`_assign` like "%{user}%") OR(`tabParticipant`.`owner` = "{user}")'.format(user = user)
        return conditions

def get_permission_query_conditions_for_event_request(user):
    ''' Permission query conditions for Event Request'''
    if not user:
        user = frappe.session.user

    user_roles = frappe.get_roles(user)
    if user == "Administrator" or 'Super Admin' in user_roles:
        return None
    else:
        conditions = '(`tabEvent Request`.`_assign` like "%{user}%") OR(`tabEvent Request`.`owner` = "{user}")'.format(user = user)
        return conditions

def change_user_role(user, role_profile):
    ''' Method to change Role of an User'''
    if frappe.db.exists('User', user) and frappe.db.exists('Role Profile', role_profile):
        user_doc = frappe.get_doc('User', user)
        user_doc.role_profile_name = role_profile
        user_doc.save()

def validate_starts_on_date(doc):
    ''' Method to validate Registration Date and Starts on Date of Event '''
    if doc.starts_on and doc.registration_ends_on:
        if getdate(doc.registration_ends_on) > getdate(doc.starts_on):
            frappe.throw(
                title = _('ALERT !!'),
                msg = _('Event Registration end date should be before Starts on date!')
            )

def validate_registration_date(doc):
    ''' Method to validate Registration Dates of Event '''
    if doc.registration_starts_on and doc.registration_ends_on:
        if get_datetime(doc.registration_starts_on) > get_datetime(doc.registration_ends_on):
            frappe.throw(
                title = _('ALERT !!'),
                msg = _('The Registration end date should be greater than the Registration start date...!!')
            )
