# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.mapper import *
from frappe.model.document import Document
from frappe import _

class Team(Document):
	def after_insert(self):
		if frappe.session.user == self.owner:
			if frappe.db.exists('Participant', {'user' : frappe.session.user}):
				participant_doc = frappe.get_doc('Participant', {'user' : frappe.session.user})
				participant_doc.team_lead = 1
				participant_doc.save()
				frappe.db.set_value('Team', self.name, 'team_lead', participant_doc.name)
				frappe.db.commit()

	def validate(self):
		self.validation_of_team_score()
		self.total_active_members = len(self.participants)
		score = 0
		for participant in self.participants:
			if participant.participant_score:
				score += participant.participant_score
		if score:
			self.team_score = float(score)

	def validation_of_team_score(self):
		if self.team_score > self.maximum_team_score:
			frappe.throw(title = _('ALERT !!'),
				msg = _('Team Score Greater than Maximum Team Score..!')
			)


	def on_update(self):
		if not self.team_lead:
			set_team_lead_if_not_set(self.name)

@frappe.whitelist()
def change_team_lead(new_team_lead, name):
	if frappe.db.exists('Team', name):
		doc_name = frappe.get_doc('Team',name)
		doc_name.team_lead = new_team_lead
		doc_name.save()
		if doc_name.team_lead:
			frappe.db.set_value('Participant',doc_name.team_lead,'team_lead',0)
			doc_name.team_lead = new_team_lead
			frappe.db.set_value('Participant',new_team_lead,'team_lead',1)
			doc_name.save()
		return True

@frappe.whitelist()
def create_project_custom_button(source_name, target_doc = None):
	doc = get_mapped_doc(
        'Team',source_name,{
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

def set_team_lead_if_not_set(team):
	''' Method to set Team Lead in Team if not set'''
	owner = frappe.db.get_value('Team', team, 'owner')
	if frappe.db.exists('Participant', { 'user' : owner }):
		participant_doc = frappe.get_doc('Participant', { 'user' : owner })
		participant_doc.team_lead = 1
		participant_doc.save()
		frappe.db.set_value('Team', team, 'team_lead', participant_doc.name)
		frappe.db.commit()

def get_permission_query_conditions_for_team(user):
	if not user:
		user = frappe.session.user
	user_roles = frappe.get_roles(user)
	if user == "Administrator" or "Host Organizer" in user_roles:
		return None
	elif "Mentor" in user_roles:
		conditions = '(`tabTeam`.`_assign` like "%{user}%") OR(`tabTeam`.`mentor` = "{user}")'.format(user = user)
		return conditions
