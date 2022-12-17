// Copyright (c) 2022, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Event Request', {
	refresh: function(frm) {
		if(frm.is_new() || !frm.doc.maximum_allowed_team){
			frappe.db.get_single_value('Hackon Settings', 'maximum_allowed_team').then( maximum_allowed_team=>{
	      frm.set_value('maximum_allowed_team', maximum_allowed_team);
	    });
		}
	}
});
