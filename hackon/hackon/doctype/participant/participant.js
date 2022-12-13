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
  	});
		frm.set_query('team', () => {
			return {
				filters: {
					event : frm.doc.event
				 }
			 }
	 });

 },
  team :function(frm){
		frappe.call({
			method: 'hackon.hackon.doctype.participant.participant.validate_team' ,
			args : {
				   'team' : frm.doc.team
			},
		})
	}
});
