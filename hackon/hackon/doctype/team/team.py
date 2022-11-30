# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.mapper import *
from frappe.model.document import Document
from hackon.hackon.utils import create_notification_log

class Team(Document):
	def validate(self):
		self.check_team_lead()
	def check_team_lead(self):
		if frappe.db.exists('Participant',  {'team_lead':0 , 'team':self.name}):
			participant_doc = frappe.get_last_doc('Participant', filters = {'team_lead':0, 'team':self.name})
			frappe.db.set_value('Participant', participant_doc.name,'team_lead',1)


@frappe.whitelist()
def change_team_lead(new_team_lead, name):
	username = False
	email_content = "You're assigned as Team Lead"
	subject = "Team Lead Changed"
	if new_team_lead:
		username = frappe.db.get_value('Participant', new_team_lead, 'user')
	if frappe.db.exists('Team', name):
		doc = frappe.get_doc('Team', name)
		email_content = email_content + ' for Team : '+ doc.team_name
		if doc.team_lead:
			frappe.db.set_value('Participant', doc.team_lead, 'team_lead', 0)
			frappe.db.set_value('Participant', new_team_lead, 'team_lead', 1)
		doc.team_lead = new_team_lead
		doc.save()
		if username:
			create_notification_log(subject, username, email_content, doc.doctype, doc.name)
		return True

@frappe.whitelist()
def create_project_custom_button(source_name, target_doc = None):
	doc = get_mapped_doc(
        'Team',
        source_name,
        {
        'Team': {
        'doctype': 'Project',
        }
        })
	return doc

@frappe.whitelist()
def mentor_user_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT
            u.name
        FROM
            `tabUser` u ,
            `tabHas Role` r
        WHERE
            u.name = r.parent and
            u.name != 'Administrator' and
            r.role = 'Mentor' and
            u.enabled = 1 and
            u.name like %s
    """, ("%" + txt + "%"))
