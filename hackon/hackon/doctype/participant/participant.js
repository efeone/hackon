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
	 if(frm.is_new() || !frm.doc.maximum_participant_score){
		 frappe.db.get_single_value('Hackon Settings', 'maximum_participant_score').then( maximum_participant_score=>{
			 frm.set_value('maximum_participant_score', maximum_participant_score);
		 });
	 }
 },

	team :function(frm){
	     frappe.call({
	         method: 'hackon.hackon.doctype.participant.participant.validate_team' ,
	         args : {
	                    'team' : frm.doc.team
	         },
	     })
	 },
});
