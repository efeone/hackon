frappe.ui.form.on('Task', {
  refresh: function(frm){
    frappe.db.get_single_value('Hackon Settings', 'maximum_team_score').then( maximum_team_score=>{
      frm.set_value('team_score_out_of', maximum_team_score);
    });
    frappe.db.get_single_value('Hackon Settings', 'maximum_participant_score').then( maximum_participant_score=>{
      frm.set_value('maximum_participant_score',maximum_participant_score);
    });
  }
});
