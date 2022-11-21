// Copyright (c) 2022, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team', {
	refresh: function(frm) {
    frm.add_custom_button('Create Project', () => {
      frappe.model.open_mapped_doc({
                        method: 'hackon.hackon.doctype.team.team.create_project_custom_button',
                        frm: cur_frm,
                    })
    })

	}
});
