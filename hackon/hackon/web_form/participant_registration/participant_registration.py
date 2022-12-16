from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):
	
	context.show_sidebar = True

	if frappe.db.exists("Participant", {"user": frappe.session.user}):
		participant = frappe.get_doc("Participant", {"user": frappe.session.user})
		context.doc = participant
		frappe.form_dict.new = 0
		frappe.form_dict.name = participant.name

def get_participant():
	return frappe.get_value("Participant", {"user": frappe.session.user}, "name")

def has_website_permission(doc, ptype, user, verbose=True):
	if doc.name == get_participant():
		return True
	else:
		return False
