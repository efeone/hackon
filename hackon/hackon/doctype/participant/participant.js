// Copyright (c) 2022, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Participant', {
	refresh : function(frm){
    frm.set_query('event', () => {
    return {
        filters: {
            status : 'Open'
        }
    }
  })
 }
});
