import frappe

@frappe.whitelist()
def timesheet_report():

    data = frappe.db.sql("""
        SELECT
            ts.name as id,
            ts.employee_name,
            ts.total_hours as total_working_hours,
            ts.customer,
            tsd.activity_type,
            tsd.project,
            tsd.task,
            tsd.from_time,
            tsd.to_time,
            tsd.hours as hrs,
            ts.owner
        FROM `tabTimesheet` ts
        LEFT JOIN `tabTimesheet Detail` tsd
        ON ts.name = tsd.parent
        ORDER BY ts.start_date DESC
    """, as_dict=True)

    return data