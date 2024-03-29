// Copyright (c) 2022, efeone and contributors
// For license information, please see license.txt

frappe.ui.form.on('Team', {
	refresh: function(frm) {
		if(frm.is_new()){
      frappe.db.get_single_value('Hackon Settings', 'maximum_team_score').then( maximum_team_score=>{
        frm.set_value('maximum_team_score', maximum_team_score);
      });
      frappe.db.get_single_value('Hackon Settings', 'maximum_allowed_team_members').then( maximum_allowed_team_members=>{
        frm.set_value('maximum_allowed_team_members', maximum_allowed_team_members);
      });
		}
		set_filters(frm);
		let roles = frappe.user_roles;
		if(roles.includes("Participant") && !frm.is_new()){
			frm.add_custom_button ("Change Team Lead", () => {
				new_team_lead(frm);
			});
		}
		if(!frm.is_new()){
			frm.add_custom_button('Create Project', () => {
				frappe.model.open_mapped_doc({
					method: 'hackon.hackon.doctype.team.team.create_project_custom_button',
					frm: cur_frm
				});
			});
		}
	},
	create_mentor: function(frm){
		if(!frm.doc.mentor){
				create_mentor(frm);
		}
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
							options: 'Participant',
							"get_query": function () {
								return {
									filters: {
										team: frm.doc.name,
									}
								};
							}
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

function create_mentor(frm){
	 let d = new frappe.ui.Dialog({
    	title: 'Change Team Lead',
	    fields: [
	        {
	            label: 'Full Name',
	            fieldname: 'full_name',
	            fieldtype: 'Data'
	        },
					{
	            label: 'Email Id',
	            fieldname: 'email_id',
	            fieldtype: 'Data',
							options: 'Email'
	        }
	    ],
			primary_action_label: 'Create',
		  primary_action(values) {
				 d.hide();
				 if (values){
					 frappe.call({
						 method: 'hackon.hackon.doctype.team.team.create_mentor_user',
						 args:{
							 		'full_name' : values.full_name,
									'email_id' : values.email_id,
									'team_name': frm.doc.name
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

function set_filters(frm){
	frm.set_query("participant", "participants", function(doc) {
		return {
			filters: { 'team': doc.name }
		};
	});
	frm.set_query('mentor', function() {
		return {
				query : 'hackon.hackon.doctype.team.team.mentor_user_query',
		}
	});
}
