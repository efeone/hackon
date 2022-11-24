import frappe

@frappe.whitelist()
def project_template(doc, method = None):
    if doc.project:
        template = frappe.db.get_value('Project', doc.project, 'project_template')
        if template:
            template_doc = frappe.get_doc('Project Template', template)
            if template_doc.tasks:
                for task in template_doc.tasks:
                    if doc.subject == task.subject and task.response:
                        doc.response = task.response
                        if task.url:
                            doc.url = task.url
                        elif task.attachment:
                            doc.attachment = task.attachment
                        elif task.data:
                            doc.data = task.data
                        else:
                            doc.text = task.text
                doc.save()

@frappe.whitelist()
def update_team_score_to_project(doc, method):
    if doc.project:
        team_score = get_total_team_score(doc.project) - frappe.db.get_value('Task', doc.name, 'team_score') + doc.team_score
        frappe.db.set_value('Project', doc.project, 'team_score', team_score)
        frappe.db.commit()

@frappe.whitelist()
def update_team_score_to_team(doc, method):
    if doc.project:
        team = frappe.db.get_value('Project', doc.project, 'team')
        if team:
            team_score = get_total_team_score(doc.project) - frappe.db.get_value('Task', doc.name, 'team_score') + doc.team_score
            frappe.db.set_value('Team', team, 'team_score', team_score)
            frappe.db.commit()

@frappe.whitelist()
def get_total_team_score(project):
    query = """
        SELECT
            IFNULL(SUM(team_score),0) as total_task_score
        FROM
            tabTask
        WHERE
            project = %(project)s

    """
    doc_list = frappe.db.sql(query.format(),{ 'project' : project }, as_dict = 1)
    return (doc_list[0].total_task_score)
