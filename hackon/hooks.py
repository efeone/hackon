from . import __version__ as app_version

app_name = "hackon"
app_title = "Hackon"
app_publisher = "efeone"
app_description = "Frappe app to facilitate Hackathon Events"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@efeone.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hackon/css/hackon.css"
# app_include_js = "/assets/hackon/js/hackon.js"

# include js, css files in header of web template
# web_include_css = "/assets/hackon/css/hackon.css"
# web_include_js = "/assets/hackon/js/hackon.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "hackon/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Project" : "public/js/project.js",
	"Task" : "public/js/task.js",
	"Project Template" : "public/js/project_template.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hackon.install.before_install"
# after_install = "hackon.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "hackon.uninstall.before_uninstall"
# after_uninstall = "hackon.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hackon.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways
#
permission_query_conditions = {
	"Participant": "hackon.hackon.utils.get_permission_query_conditions_for_participant",
	"Event Request": "hackon.hackon.utils.get_permission_query_conditions_for_event_request",
}
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

has_website_permission = {
	"Participant": "hackon.hackon.web_form.participant_registration.participant_registration.has_website_permission",
	"Event Request": "hackon.hackon.web_form.new_event_request.new_event_request.has_website_permission",
}

doc_events = {
	"Task":{
		'validate':'hackon.hackon.utils.validate_task_score',
		'after_insert': 'hackon.hackon.utils.project_template',
		'on_update':[
			'hackon.hackon.utils.update_team_score_to_project',
			'hackon.hackon.utils.update_team_score_to_team'
			],
		'before_save': 'hackon.hackon.utils.update_participant_score'
	},
	"Event":{
       'validate': [
	       'hackon.hackon.utils.validation_of_starting_date',
		   'hackon.hackon.utils.validation_of_Registration_date'
	   ]
   }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
#	"all": [
#		"hackon.tasks.all"
#	],
	"daily": [
	     "hackon.hackon.utils.event_scheduler"
	]
#	"hourly": [
#		"hackon.tasks.hourly"
#	],
#	"weekly": [
#		"hackon.tasks.weekly"
#	]
#	"monthly": [
#		"hackon.tasks.monthly"
#	]
}

# Testing
# -------

# before_tests = "hackon.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "hackon.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "hackon.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

fixtures = [
		{"dt": "Role","filters": [["name", "in", ['Participant', 'Super Admin', 'Judge','Team Lead', 'Mentor', 'Host Organizer', 'Event Requester']]]},
		{"dt": "Custom DocPerm","filters": [["role", "in", ['Participant', 'Super Admin', 'Judge','Team Lead', 'Mentor', 'Host Organizer', 'Event Requester']]]},
		{"dt": "Workflow State", "filters": [["name", "in", ["Approved by Mentor", "Draft", "Approved by Judges", "Completed","Draft","Pending review","Approved","Rejected"]]]},
		{"dt": "Workflow", "filters": [["name", "in", ["Task Workflow","Event Request Workflow"]]]},
		{"dt": "Energy Point Rule", "filters": [["name", "in", ["On Task Completion"]]]},
		{"dt": "Web Page", "filters": [["name", "in", ["events", "event-view", "event-requests", "sign-up","hackon-dashboard"]]]},
		{"dt": "Website Sidebar", "filters": [["name", "in", ["Participant Portal"]]]}

	]

standard_portal_menu_items = [
	{"title": "Participant Registration", "route": "/participant-registration", "reference_doctype": "Participant", "role": "Participant"},
]

# website_route_rules = [
# 	{"from_route": "/login", "to_route": "/sign-up"},
# ]

required_apps = ['frappe', 'erpnext']


# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"hackon.auth.validate"
# ]
