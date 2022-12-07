frappe.ui.form.on('Task', {
  refresh: function(frm){
    frappe.db.get_single_value('Hackon Settings', 'maximum_team_score').then( maximum_team_score=>{
      frm.set_value('team_score_out_of', maximum_team_score);
    });
    frappe.db.get_single_value('Hackon Settings', 'maximum_participant_score').then( maximum_participant_score=>{
      frm.set_value('maximum_participant_score',maximum_participant_score);
    });
  },
  software_tool:function(frm){
    manage_software_tool(frm)
    var total_weightage = 0
    frm.doc.software_tool_details.forEach(function(d){
      total_weightage += d.weightage;
    })
    frm.set_value('total_weightage',total_weightage)
  }
});
  refresh:function(frm){
    if (frm.doc.maximum_team_score){
      frappe.db.get_single_value('Hackon Settings', 'maximum_team_score').then( maximum_team_score=>{
        frm.set_value('team_score_out_of', maximum_team_score);
      });
    }
    if (frm.doc.maximum_participant_score){
      frappe.db.get_single_value('Hackon Settings', 'maximum_participant_score').then( maximum_participant_score=>{
        frm.set_value('maximum_participant_score',maximum_participant_score);
      });
    }
  }
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
    },
    software_tool_details_add:function(frm){

    }
});
let manage_software_tool = function (frm) {
	let software_tool = frm.doc.software_tool
	let software_tool_length = frm.doc.software_tool.length
  let software_tool_details_length = 0
  if(frm.doc.software_tool_details){
    software_tool_details_length = frm.doc.software_tool_details.length
  }
	if (software_tool_length > software_tool_details_length) {
    frm.clear_table('software_tool_details')
    frm.doc.software_tool.forEach(software_tool => {
      frappe.call({
        method: 'hackon.hackon.utils.get_software_tool_weightage',
        args: {
          'software_tool':software_tool.task
        },
        callback: (r) => {
          if (r.message) {
            let software_tool_table = frm.add_child('software_tool_details');
            software_tool_table.software_tool_name = software_tool.task
            software_tool_table.weightage = r.message
            frm.refresh_field('software_tool_details')
          }
        }
      })
    });
	}
	else if (software_tool_length < software_tool_details_length) {
		if (software_tool_length) {
			software_tool_length = frm.doc.software_tool.length
			let software_tools = []
			frm.doc.software_tool.forEach(software_tool => {
				software_tools.push(software_tool.task)
			});
			delete_row_from_software_tool_table(software_tools)
      software_tool = frm.doc.software_tool
			software_tool_length = frm.doc.software_tool.length
		}
		else {
			frm.clear_table('software_tool_details')
			frm.refresh_field('software_tool_details')
		}
	}
}
let delete_row_from_software_tool_table = function (software_tools) {
			let table = cur_frm.doc.software_tool_details || [];
			let i = table.length;
			while (i--) {
				if(!software_tools.includes(table[i].software_tool_name)) {
					cur_frm.get_field('software_tool_details').grid.grid_rows[i].remove();
				}
			}
			cur_frm.refresh_field('software_tool_details');
}
