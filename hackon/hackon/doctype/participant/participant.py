# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Participant(Document):
	def before_validate(self):
		if not self.team and self.new_team and self.event:
			if not frappe.db.exists('Team', self.new_team):
				maximum_allowed_team_members = frappe.db.get_single_value("Hackon Settings", "maximum_allowed_team_members")
				team_doc = frappe.new_doc('Team')
				team_doc.team_name = self.new_team
				team_doc.event = self.event
				team_doc.maximum_allowed_team_members = maximum_allowed_team_members
				team_doc.save()
				self.team = self.new_team

	def validate(self):
		if not self.maximum_participant_score:
			self.maximum_participant_score = frappe.db.get_single_value("Hackon Settings", "maximum_participant_score")

		if self.team:
			validate_team(self.team)

	def on_update(self):
		self.set_participant_to_team()
		self.assign_to_team_lead()

	def set_participant_to_team(self):
		''' Method to Add Participants to the Team'''
		if self.team:
			team_doc = frappe.get_doc('Team', self.team)
			participant_added = False
			if team_doc.participants:
				for participant in team_doc.participants:
					if participant.participant == self.name:
						participant_added = True
			if not participant_added:
				new_participant = team_doc.append('participants')
				new_participant.participant = self.name
				team_doc.save()

	def assign_to_team_lead(self):
		''' Method to set assign participant to team lead'''
		if self.team:
			team_lead = frappe.db.get_value('Team', self.team, 'team_lead')
			if team_lead:
				team_lead_user = frappe.db.get_value('Participant', team_lead, 'user')
				if team_lead_user:
					doc = frappe.new_doc('DocShare')
					doc.user = team_lead_user
					doc.share_doctype = 'Participant'
					doc.share_name = self.name
					doc.read = 1
					doc.write = 1
					doc.notify_by_email = 1
					doc.flags.ignore_validate = True
					doc.flags.ignore_permissions = True
					doc.save()
					frappe.db.commit()

@frappe.whitelist()
def validate_team(team):
    '''Method to validate the team from participant if team reached  maximum allowed team members'''
    team_doc = frappe.get_doc('Team', team)
    if team_doc.maximum_allowed_team_members == team_doc.total_active_members:
        frappe.throw(title = 'ALERT !!', msg = 'Team has the maximum number of members permitted !')
