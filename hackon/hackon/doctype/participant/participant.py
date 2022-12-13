# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import *
from frappe import _

class Participant(Document):
	def on_submit(self):
		self.fetch_participant_name()
	def fetch_participant_name(self):
		team_members = frappe.get_doc('Team', self.team)
		team_members.append("participants", {
			"participant": self.name
		})
		team_members.save()


@frappe.whitelist()
def validate_team(team):
	'''Method to disable the team from participant if team reached  maximum allowed team members'''
	team_doc = frappe.get_doc('Team', team)
	if team_doc.maximum_allowed_team_members == team_doc.total_active_members:
		frappe.throw(title = _('ALERT !!'),
		msg = _('Team has the maximum number of members permitted !')
		)
