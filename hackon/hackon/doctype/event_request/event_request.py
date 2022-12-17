# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from hackon.hackon.utils import change_user_role

class EventRequest(Document):
	def on_update_after_submit(self):
		if self.workflow_state == 'Approved':
			create_event(self.name)
			if frappe.db.exists('Role Profile', 'Host Organizer'):
				change_user_role(self.owner, 'Host Organizer')

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
