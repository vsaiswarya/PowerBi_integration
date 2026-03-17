import frappe

@frappe.whitelist()
def task_management_report():

    data = frappe.db.sql("""
        SELECT
            t.name AS task_id,
            t.subject AS task_name,
            t.type AS task_type,
            t.priority,
            t.status,
            t.project,
            p.project_name,
            p.project_type,
            t.issue,
            i.subject AS issue_name,
            i.opening_date AS issue_date,
            t.customer,
            t.exp_start_date AS expected_start_date,
            t.exp_end_date AS expected_end_date,
            t.expected_time AS expected_hours,
            t.completed_on,
            t.actual_time AS actual_hours,
            t.is_milestone,
            t.sales_order,
            t.description AS remark,
            t.owner
        FROM `tabTask` t
        LEFT JOIN `tabProject` p
            ON t.project = p.name
        LEFT JOIN `tabIssue` i
            ON t.issue = i.name
        ORDER BY t.modified DESC
    """, as_dict=True)

    return data