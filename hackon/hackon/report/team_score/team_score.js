// Copyright (c) 2022, efeone and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Team Score"] = {
	"filters": [
		{
			"fieldname": "doc",
			"label": __("Document Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"ignore_user_permissions": 1,
			"get_query": function() {
				return {
					filters: {
						"name": ["in",["Team"]]
					}
				};
			}
		},

	]
};
