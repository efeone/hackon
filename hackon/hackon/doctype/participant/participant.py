# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import *

class Participant(Document):
	def on_submit(self):
		self.fetch_participant_name()
	def fetch_participant_name(self):
		team_members = frappe.get_doc('Team', self.team)
		team_members.append("participants", {
			"participant": self.name
		})
		team_members.save()
