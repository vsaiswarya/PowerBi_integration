import frappe
from frappe.utils import nowdate
from erpnext.accounts.report.accounts_receivable.accounts_receivable import execute


@frappe.whitelist()
def accounts_receivable_powerbi(
    company=None,
    report_date=None,
    customer=None
):
    """
    Power BI friendly Accounts Receivable API
    Returns clean JSON with all report fields
    """

    # Default filters
    filters = {
        "company": company or frappe.defaults.get_user_default("Company"),
        "report_date": report_date or nowdate(),
        "ageing_based_on": "Due Date",
    }

    if customer:
        filters["customer"] = customer

    try:
        columns, data = execute(filters)

        result = []

        for row in data:
            row_dict = {}

            for col, val in zip(columns, row):
                # Use fieldname if exists, else label
                fieldname = col.get("fieldname") or col.get("label")

                # Clean fieldname (remove spaces)
                fieldname = fieldname.replace(" ", "_").lower()

                row_dict[fieldname] = val

            result.append(row_dict)

        return result

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Power BI AR API Error")
        return {"error": str(e)}