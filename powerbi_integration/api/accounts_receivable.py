import frappe
from frappe.utils import nowdate
from erpnext.accounts.report.accounts_receivable.accounts_receivable import execute


@frappe.whitelist()
def accounts_receivable_powerbi():

    filters = {
        "company": frappe.defaults.get_user_default("Company"),
        "report_date": nowdate(),
        "ageing_based_on": "Due Date",
    }

    try:
        result = execute(filters)

        columns = result[0]
        data = result[1]

        final_data = []

        for row in data:
            row_dict = {}

            for col, val in zip(columns, row):
                fieldname = col.get("fieldname") or col.get("label")
                fieldname = fieldname.replace(" "import frappe
from frappe.utils import nowdate
from erpnext.accounts.report.accounts_receivable.accounts_receivable import execute

@frappe.whitelist()
def accounts_receivable_powerbi():
    filters = {
        "company": frappe.defaults.get_user_default("Company"),
        "report_date": nowdate(),
        "ageing_based_on": "Due Date",
    }

    try:
        columns, data = execute(filters)

        # Get actual fieldnames from columns
        fieldnames = [col.get("fieldname") or col.get("label") for col in columns]

        final_data = []

        for row in data:
            # If row is a list of values
            if isinstance(row, (list, tuple)):
                row_dict = {fn.replace(" ", "_").lower(): val for fn, val in zip(fieldnames, row)}
            # If row is already a dict
            elif isinstance(row, dict):
                row_dict = {k.replace(" ", "_").lower(): v for k, v in row.items()}
            else:
                continue

            final_data.append(row_dict)

        return final_data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Power BI AR API Error")
        return {"error": str(e)}, "_").lower()

                row_dict[fieldname] = val

            final_data.append(row_dict)

        return final_data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Power BI AR API Error")
        return {"error": str(e)}