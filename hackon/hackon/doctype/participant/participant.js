// Copyright (c) 2022, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant', {
	refresh : function(frm){
		frm.set_df_property('team_lead', 'read_only', frm.is_new() ? 0 : 1);
    frm.set_query('event', () => {
    return {
        filters: {
            status : 'Open'
        }
    }
  })
 }

});
