frappe.ui.form.on('Project', {
  refresh: function(frm){
    if(frm.is_new() && !frm.doc.team_score_out_of){
      frappe.db.get_single_value('Hackon Settings', 'maximum_team_score').then( maximum_team_score=>{
        frm.set_value('team_score_out_of', maximum_team_score);
      });
    }
    if(frm.is_new() && !frm.doc.participant_score_out_of){
      frappe.db.get_single_value('Hackon Settings', 'maximum_participant_score').then( maximum_participant_score=>{
        frm.set_value('participant_score_out_of', maximum_participant_score);
      });
    }
  }
});
