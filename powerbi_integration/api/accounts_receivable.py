import frappe
from frappe.utils import nowdate

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

    try:
        report = frappe.desk.query_report.run(
            report_name="Accounts Receivable",
            filters=filters,
            user=frappe.session.user
        )

        columns = report.get("columns", [])
        data = report.get("result", [])

        final_data = []

        for row in data:

            # Handle dict rows
            if isinstance(row, dict):
                row_dict = row
            else:
                row_dict = {}
                for col, value in zip(columns, row):
                    fieldname = col.get("fieldname") or col.get("label")
                    fieldname = fieldname.replace(" ", "_").lower()
                    row_dict[fieldname] = value

            # Skip unwanted rows (headers / totals)
            if not row_dict.get("voucher_no"):
                continue

            final_data.append({
                "posting_date": row_dict.get("posting_date"),
                "due_date": row_dict.get("due_date"),
                "age": row_dict.get("age") or row_dict.get("ageing_days"),
                "voucher_type": row_dict.get("voucher_type"),
                "voucher_no": row_dict.get("voucher_no"),
                "customer": row_dict.get("customer_name") or row_dict.get("party"),
                "remarks": row_dict.get("remarks"),
                "invoiced": row_dict.get("invoiced"),
                "paid": row_dict.get("paid"),
                "credit_note": row_dict.get("credit_note"),
                "outstanding": row_dict.get("outstanding"),
            })

        # CRITICAL FIX
        frappe.local.response.clear()
        frappe.local.response.update({
            "type": "json",
            "data": final_data
        })

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Power BI AR Error")
        frappe.throw(str(e))