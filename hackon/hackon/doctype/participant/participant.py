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
		if self.team:
			validate_team(self.team)

	def on_update(self):
		self.set_participant_to_team()

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

@frappe.whitelist()
def validate_team(team):
    '''Method to validate the team from participant if team reached  maximum allowed team members'''
    team_doc = frappe.get_doc('Team', team)
    if team_doc.maximum_allowed_team_members == team_doc.total_active_members:
        frappe.throw(title = 'ALERT !!', msg = 'Team has the maximum number of members permitted !')
