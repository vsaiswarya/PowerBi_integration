import frappe
from frappe.utils import nowdate
from erpnext.accounts.report.accounts_receivable.accounts_receivable import execute

@frappe.whitelist(allow_guest=True)
def accounts_receivable_powerbi():
    """
    Returns ERPNext Accounts Receivable report in a JSON-ready format
    suitable for Power BI.
    """
    filters = {
        "company": frappe.defaults.get_user_default("Company"),
        "report_date": nowdate(),
        "ageing_based_on": "Due Date",
    }

    try:
       
        columns, data = execute(filters)

        fieldnames = [
            (col.get("fieldname") or col.get("label")).replace(" ", "_").lower()
            for col in columns
        ]

        final_data = []

        for row in data:
            # If row is a list/tuple of values
            if isinstance(row, (list, tuple)):
                row_dict = {fn: val for fn, val in zip(fieldnames, row)}
            # If row is already a dict
            elif isinstance(row, dict):
                row_dict = {
                    k.replace(" ", "_").lower(): v
                    for k, v in row.items()
                }
            else:
                continue  

            final_data.append(row_dict)

        return final_data 

    except Exception as e:
        # Log error in ERPNext
        frappe.log_error(frappe.get_traceback(), "Power BI AR API Error")
        return {"error": str(e)}