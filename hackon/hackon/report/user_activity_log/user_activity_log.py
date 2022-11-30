# Copyright (c) 2022, efeone and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		_("Participant") + ":Link/Participant:300",
		_("Participant score") + ":Float:250",
		_("Task Progress") + ":Percent:250"
		]
	return columns
def get_data(filters):
	data = []
	query = """
		SELECT
			p.name,
			p.participant_score,
			t.progress

		FROM
			`tabTask` as t,
			`tabParticipant` as p
		"""
	doclist = frappe.db.sql(query, as_dict = 1)
	if doclist:
		for doc in doclist:
			row = [
				doc.name,
				doc.participant_score,
				doc.progress
			]
			data.append(row)
	return data
