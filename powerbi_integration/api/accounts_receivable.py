import frappe
from frappe.utils import nowdate
from erpnext.accounts.report.accounts_receivable.accounts_receivable import execute

@frappe.whitelist(allow_guest=True)
def accounts_receivable_powerbi():
    """
    Custom Accounts Receivable API for Power BI
    Structured based on AR Ageing report format.
    """

    filters = {
        "company": frappe.defaults.get_user_default("Company"),
        "report_date": nowdate(),
        "ageing_based_on": "Due Date",
    }

    try:
        columns, data = execute(filters)

        final_data = []

        for row in data:
            # Convert row to dict
            if isinstance(row, (list, tuple)):
                row_dict = {col.get("fieldname"): val for col, val in zip(columns, row)}
            elif isinstance(row, dict):
                row_dict = row
            else:
                continue

            # Transform into clean structure for Power BI
            formatted_row = {
                "date": row_dict.get("posting_date"),
                "due_date": row_dict.get("due_date"),
                "age_days": row_dict.get("age") or row_dict.get("ageing_days"),

                "reference_type": row_dict.get("voucher_type"),
                "reference_name": row_dict.get("voucher_no"),

                "customer": row_dict.get("party"),
                "remarks": row_dict.get("remarks") or row_dict.get("customer_name"),

                "invoiced_amount": row_dict.get("invoiced") or row_dict.get("invoice_amount"),
                "paid_amount": row_dict.get("paid_amount"),
                "credit_note": row_dict.get("credit_note"),

                "outstanding_amount": row_dict.get("outstanding") or row_dict.get("outstanding_amount"),
            }

            final_data.append(formatted_row)

        return {
            "status": "success",
            "report_date": filters["report_date"],
            "data": final_data
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Power BI AR API Error")
        return {"status": "error", "message": str(e)}