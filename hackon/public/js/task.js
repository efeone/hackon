frappe.ui.form.on('Task', {
  refresh: function(frm){
    if(frm.is_new()){
      frappe.db.get_single_value('Hackon Settings', 'maximum_team_score').then( maximum_team_score=>{
        frm.set_value('team_score_out_of', maximum_team_score);
      });
      frappe.db.get_single_value('Hackon Settings', 'maximum_participant_score').then( maximum_participant_score=>{
        frm.set_value('maximum_participant_score', maximum_participant_score);
      });
    }
    frm.set_query("participant", function() {
  		return {
  			filters: { 'team': frm.doc.team }
  		};
  	});
    var tools_can_be_used = [];
    frm.doc.software_tool_details.forEach(function(d){
      tools_can_be_used.push(d.software_tool);
    })
    cur_frm.get_field('tools_used').get_query = function(){
			return {
				filters: {'name': ['in', tools_can_be_used ]}
			}
		};
  },
  software_tool:function(frm){
    update_software_tool_weightage(frm);
    var total_weightage = 0
    frm.doc.software_tool_details.forEach(function(d){
      total_weightage += d.weightage;
    })
    frm.set_value('total_weightage', total_weightage)
  },
  tools_used:function(frm){
    update_used_software_tool_weightage(frm);
    var total_weightage_earned = 0
    frm.doc.used_software_tool_details.forEach(function(d){
      total_weightage_earned += d.weightage;
    })
    frm.set_value('total_weightage_earned', total_weightage_earned)
  }
});

frappe.ui.form.on('Software Tool Details',{
  weightage: function(frm, cdt, cdn){
    let d = locals[cdt][cdn];
    var total_weightage = 0
    frm.doc.software_tool_details.forEach(function(d){
      total_weightage += d.weightage;
    })
    frm.set_value('total_weightage', total_weightage)
  },
  software_tool_details_remove:function(frm){
    var total_weightage = 0;
    frm.doc.software_tool_details.forEach(function(d){
      total_weightage += d.weightage;
    })
    frm.set_value("total_weightage", total_weightage)
  }
});

let update_software_tool_weightage = function (frm) {
	let software_tool = frm.doc.software_tool;
	let software_tool_length = frm.doc.software_tool.length;
  let software_tool_details_length = 0
  if(frm.doc.software_tool_details){
    software_tool_details_length = frm.doc.software_tool_details.length;
  }
	if (software_tool_length > software_tool_details_length) {
    frm.clear_table('software_tool_details')
    frm.doc.software_tool.forEach(software_tool => {
      frappe.call({
        method: 'hackon.hackon.utils.get_software_tool_weightage',
        args: {
          'software_tool':software_tool.software_tool
        },
        callback: (r) => {
          if (r.message) {
            let software_tool_table = frm.add_child('software_tool_details');
            software_tool_table.software_tool = software_tool.software_tool
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
				software_tools.push(software_tool.software_tool)
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
				if(!software_tools.includes(table[i].software_tool)) {
					cur_frm.get_field('software_tool_details').grid.grid_rows[i].remove();
				}
			}
			cur_frm.refresh_field('software_tool_details');
}

let update_used_software_tool_weightage = function (frm) {
	let tools_used = frm.doc.tools_used;
	let tools_used_length = frm.doc.tools_used.length;
  let used_software_tool_details_length = 0
  if(frm.doc.used_software_tool_details){
    used_software_tool_details_length = frm.doc.used_software_tool_details.length;
  }
	if (tools_used_length > used_software_tool_details_length) {
    frm.clear_table('used_software_tool_details')
    frm.doc.tools_used.forEach(tools_used => {
      frappe.call({
        method: 'hackon.hackon.utils.get_software_tool_weightage_from_task',
        args: {
          'software_tool': tools_used.software_tool,
          'task': frm.doc.name
        },
        callback: (r) => {
          if (r.message) {
            let used_software_tool_table = frm.add_child('used_software_tool_details');
            used_software_tool_table.software_tool = tools_used.software_tool
            used_software_tool_table.weightage = r.message
            frm.refresh_field('used_software_tool_details')
          }
        }
      })
    });
	}
	else if (tools_used_length < used_software_tool_details_length) {
		if (tools_used_length) {
			tools_used_length = frm.doc.tools_used.length
			let tools_used = []
			frm.doc.tools_used.forEach(tool_used => {
				tools_used.push(tool_used.software_tool)
			});
			delete_row_from_used_software_tool_table(tools_used)
      tools_used = frm.doc.tools_used
			tools_used_length = frm.doc.tools_used.length
		}
		else {
			frm.clear_table('used_software_tool_details')
			frm.refresh_field('used_software_tool_details')
		}
	}
}

let delete_row_from_used_software_tool_table = function (tools_used) {
  let table = cur_frm.doc.used_software_tool_details || [];
  let i = table.length;
  while (i--) {
    if(!tools_used.includes(table[i].software_tool)) {
      cur_frm.get_field('used_software_tool_details').grid.grid_rows[i].remove();
    }
  }
  cur_frm.refresh_field('used_software_tool_details');
}
