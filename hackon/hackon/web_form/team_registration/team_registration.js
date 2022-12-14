frappe.ready(function() {
  frappe.web_form.after_load = () => {
    filter_events();
  }

  function filter_events() {
    var api_url = 'api/resource/Event?filters=[["Event","status","=","Open"]]';
    $.ajax({
    	type: 'GET',
    	url: api_url,
    	success: function(result) {
    		var options = [];
    		for (var i = 0; i < result.data.length; i++) {
    			options.push({
    				'label': result.data[i].name,
    				'value': result.data[i].name
    			});
    		}
    		var field = frappe.web_form.get_field("event");
    		field._data = options;
    		field.refresh();
    	}
    });
  };
});
