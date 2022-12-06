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
		_("Team") + ":Link/Team:200",
		_("Team Score") + ":Data:150",
		_("Percent Complete") + ":Data:200"
		]
	return columns

def get_data(filters):
	data = []
	query = """
		SELECT
			t.name,
			t.team_score,
			p.percent_complete

		FROM
			`tabTeam` as t,
			`tabProject` as p
		WHERE
			p.team = t.name
		"""
	doclist = frappe.db.sql(query.format(**{}), as_dict = 1)
	if doclist:
		for doc in doclist:
			row = [
				doc.name,
				doc.team_score,
				doc.percent_complete
			]
			data.append(row)
	return data
