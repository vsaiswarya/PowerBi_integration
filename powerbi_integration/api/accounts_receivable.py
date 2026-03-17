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
            # Convert list → dict using report columns
            row_dict = {}

            for col, value in zip(columns, row):
                fieldname = col.get("fieldname") or col.get("label")
                fieldname = fieldname.replace(" ", "_").lower()
                row_dict[fieldname] = value

            # Keep ONLY fields matching your report screenshot
            formatted_row = {
                "date": row_dict.get("posting_date"),
                "age_days": row_dict.get("age"),
                "reference": f"{row_dict.get('voucher_type')} {row_dict.get('voucher_no')}",
                "remarks": row_dict.get("customer_name") or row_dict.get("party"),
                "invoiced_amount": row_dict.get("invoiced"),
                "paid_amount": row_dict.get("paid"),
                "credit_note": row_dict.get("credit_note"),
                "outstanding_amount": row_dict.get("outstanding"),
            }

            final_data.append(formatted_row)

        # Return clean JSON for Power BI
        frappe.response["type"] = "json"
        frappe.response["result"] = final_data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Power BI AR Exact Report Error")
        frappe.throw(str(e))