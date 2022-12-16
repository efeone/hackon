frappe.ready(function() {
  frappe.web_form.after_load = () => {
    filter_users();
    frappe.web_form.set_value('user', frappe.session.user);
    get_user_details();
    filter_events();
  }
  
  frappe.web_form.validate = () => {
    let email_id = frappe.web_form.get_value("email");
    var pattern = /^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,4}$/
    if(!email_id.match(pattern)){
      frappe.msgprint('Enter a Valid Email Address');
      return false;
    }
    let mobile_no = frappe.web_form.get_value("phone_no");
    var mob_no = /^\(?(\d{3})\)?[- ]?(\d{3})[- ]?(\d{4})$/
    if (!mobile_no.match(mob_no)){
      frappe.msgprint('Enter a Valid Mobile Number');
      return false;
    }
    return true;
  }

  function filter_users() {
    var options = [];
    options.push({
      'label': frappe.session.user,
      'value': frappe.session.user
    });
    var user_field = frappe.web_form.get_field("user");
    user_field._data = options;
    user_field.refresh();
  }

  function filter_events() {
    var api_url = 'api/resource/Event?filters=[["status","=","Open"],["published","=",1]]';
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

  function get_user_details(){
    user = frappe.session.user;
    if(user && user!='Guest'){
      var api_url = 'api/resource/User/'+ user;
      $.ajax({
        type: 'GET',
        url: api_url,
        success: function(result) {
          if(!frappe.web_form.get_value('email')){
            frappe.web_form.set_value('email', result.data.email );
          }
          if(!frappe.web_form.get_value('first_name')){
            frappe.web_form.set_value('first_name', result.data.first_name );
          }
          if(!frappe.web_form.get_value('full_name')){
            frappe.web_form.set_value('full_name', result.data.full_name );
          }
          if(!frappe.web_form.get_value('full_name')){
            frappe.web_form.set_value('full_name', result.data.full_name );
          }
        }
      });
    }
  }
});
