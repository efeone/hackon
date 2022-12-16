from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):

	context.show_sidebar = True

	if frappe.db.exists("Event Request", {"owner": frappe.session.user}):
		event_request = frappe.get_doc("Event Request", {"owner": frappe.session.user})
		context.doc = event_request
		frappe.form_dict.new = 0
		frappe.form_dict.name = event_request.name

def get_event_request():
	return frappe.get_value("Event Request", {"owner": frappe.session.user}, "name")

def has_website_permission(doc, ptype, user, verbose=True):
	if doc.name == get_event_request():
		return True
	else:
		return False
