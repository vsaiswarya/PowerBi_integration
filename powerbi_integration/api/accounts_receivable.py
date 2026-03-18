import frappe
from frappe.utils import nowdate
from frappe.desk.query_report import run

@frappe.whitelist(allow_guest=True)
def accounts_receivable_powerbi():

    filters = {
        "company": frappe.defaults.get_user_default("Company"),
        "report_date": nowdate(),
        "ageing_based_on": "Due Date",
        "range1": 30,
        "range2": 60,
        "range3": 90,
        "range4": 120,
    }

    report = run(
        report_name="Accounts Receivable",
        filters=filters,
        user=frappe.session.user
    )

    data = report.get("result", [])

    final_data = []

    for row in data:

        if isinstance(row, dict):

            if not row.get("voucher_no"):
                continue

            final_data.append({
                "posting_date": row.get("posting_date"),
                "due_date": row.get("due_date"),
                "age": row.get("age") or row.get("ageing_days"),
                "voucher_type": row.get("voucher_type"),
                "voucher_no": row.get("voucher_no"),
                "customer": row.get("customer_name") or row.get("party"),
                "remarks": row.get("remarks"),
                "invoiced": row.get("invoiced"),
                "paid": row.get("paid"),
                "credit_note": row.get("credit_note"),
                "outstanding": row.get("outstanding"),
            })

    # 🔥 KEY FIX (NO message wrapper)
    frappe.local.response.clear()
    frappe.local.response.update({
        "type": "json",
        "data": final_data
    })