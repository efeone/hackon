# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from hackon.hackon.utils import change_user_role
from frappe import _

class EventRequest(Document):
	def validate(self):
		self.validate_registration_date()
		self.validate_registration_end_date()

	def on_update(self):
		if self.workflow_state == 'Approved':
			create_event(self.name)
			if frappe.db.exists('Role Profile', 'Host Organizer'):
				change_user_role(self.owner, 'Host Organizer')

	def validate_registration_date(self):
		''' Method to validate Registration ending date against event starting date '''
		if self.registration_ends_on > self.starts_on :
			frappe.throw(
				title = _('ALERT !!'),
				msg = _('The deadline for registration should come before the event itself..!')
			)

	def validate_registration_end_date(self):
		if self.registration_ends_on < self.registration_starts_on :
			frappe.throw(
				title = _('ALERT !!'),
				msg = _('The registration end date should be greater than the registration start date....!')
			)

def create_event(source_name, target_doc = None):
	''' Method to Create Event from Event Request'''
	target_doc = get_mapped_doc("Event Request", source_name,{
    	"Event Request": {
    		"doctype": "Event",
    			"field_map":{
    			},
    		}
    	},
	target_doc)
	target_doc.save()
	frappe.db.commit()
