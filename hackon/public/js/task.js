frappe.ui.form.on('Task', {
  refresh: function(frm){
    frappe.db.get_single_value('Hackon Settings', 'maximum_team_score').then( maximum_team_score=>{
      frm.set_value('team_score_out_of', maximum_team_score);
    });
    frappe.db.get_single_value('Hackon Settings', 'maximum_participant_score').then( maximum_participant_score=>{
      frm.set_value('maximum_participant_score',maximum_participant_score);
    });
  },
});

frappe.ui.form.on('Software Tool Details',{
  weightage: function(frm, cdt, cdn){
    let d = locals[cdt][cdn];
    var total_weightage = 0
    frm.doc.software_tool_details.forEach(function(d){
      total_weightage += d.weightage;
    })
    frm.set_value('total_weightage',total_weightage)
  },
  software_tool_details_remove:function(frm){
      var total_weightage = 0
      frm.doc.software_tool_details.forEach(function(d){
        total_weightage += d.weightage;
      })
      frm.set_value("total_weightage",total_weightage)
    }
});
