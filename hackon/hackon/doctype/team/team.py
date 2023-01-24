# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.mapper import *
from frappe.model.document import Document
from frappe import _
from hackon.hackon.utils import change_user_role

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
		self.validate_team_score()
		self.total_active_members = len(self.participants)
		score = 0
		for participant in self.participants:
			if participant.participant_score:
				score += participant.participant_score
		if score:
			self.team_score = float(score)

	def validate_team_score(self):
		if self.team_score and self.maximum_team_score:
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
		doc_name.save()
		if doc_name.team_lead:
			frappe.db.set_value('Participant',doc_name.team_lead,'team_lead',0)
			doc_name.team_lead = new_team_lead
			frappe.db.set_value('Participant',new_team_lead,'team_lead',1)
			user_id = frappe.db.get_value('Participant', new_team_lead, 'user')
			change_participant_to_team_lead(user_id)
			doc_name.save()
		frappe.db.commit()
		return True

def change_participant_to_team_lead(user_id):
	if frappe.db.exists('Role Profile', 'Team Lead'):
		change_user_role(user_id, 'Team Lead')

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


@frappe.whitelist()
def create_mentor_user(full_name, email_id, team_name):
	''' Method to create Mentor user '''
	user_doc = frappe.new_doc('User')
	user_doc.email = email_id
	user_doc.first_name = full_name
	user_doc.send_welcome_email = 0
	if frappe.db.exists('Module Profile', 'Hackon'):
		user_doc.module_profile = 'Hackon'
	if frappe.db.exists('Role Profile', 'Mentor'):
		user_doc.role_profile_name = 'Mentor'
	user_doc.save(ignore_permissions=True)
	if team_name:
		frappe.db.set_value('Team', team_name, 'mentor', user_doc.name )
	return True
