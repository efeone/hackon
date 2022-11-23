// Copyright (c) 2022, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team', {
	refresh: function(frm) {
		let roles = frappe.user_roles
    	if(roles.includes("Participant") && !frm.is_new()){
			frm.add_custom_button ("Change Team Lead", () => {
			new_team_lead(frm)
		})
	}
		frm.add_custom_button('Create Project', () => {
      frappe.model.open_mapped_doc({
                        method: 'hackon.hackon.doctype.team.team.create_project_custom_button',
                        frm: cur_frm,
        })
		})
}
 });

 function new_team_lead(frm){
	 let d = new frappe.ui.Dialog({
    	title: 'Change Team Lead',
	    fields: [
	        {
	            label: 'New Team Lead',
	            fieldname: 'new_team_lead',
	            fieldtype: 'Link',
							options: 'Participant'
	        }
	    ],
			primary_action_label: 'Save',
		  primary_action(values) {
				 d.hide();
				 if (values){
					 frappe.call({
						 method: 'hackon.hackon.doctype.team.team.change_team_lead',
						 args:{
							 		'new_team_lead' : values.new_team_lead,
									'name' : frm.doc.name
								},
						 callback:function(r){
							 if (r){
								 frm.reload_doc()
							 }
						 }
					 })
				 }
		   }
	  });
	  d.show();
	 }
