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
