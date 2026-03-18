import frappe
from frappe.utils import nowdate
from frappe.desk.query_report import run

@frappe.whitelist(allow_guest=True)
def accounts_receivable_powerbi():
    """
    Clean Accounts Receivable API for Power BI
    Returns ONLY actual data rows (no headers, no metadata)
    """

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
        report = run(
            report_name="Accounts Receivable",
            filters=filters,
            user=frappe.session.user
        )

        data = report.get("result", [])

        final_data = []

        for row in data:

            # ✅ CASE 1: Row is dict (new ERPNext versions)
            if isinstance(row, dict):

                # Skip summary/invalid rows
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

            # ✅ CASE 2: Row is list (older ERPNext / mixed format)
            elif isinstance(row, list):

                # 🔥 CRITICAL: Skip header rows
                if len(row) > 0 and row[0] == "voucher_type":
                    continue

                # 🔥 Ensure valid data row
                if len(row) < 11:
                    continue

                final_data.append({
                    "voucher_type": row[0],
                    "voucher_no": row[1],
                    "customer": row[2],
                    "posting_date": row[4],
                    "remarks": row[6],
                    "invoiced": row[7],
                    "paid": row[8],
                    "credit_note": row[9],
                    "outstanding": row[10],
                    "due_date": row[19] if len(row) > 19 else None,
                })

        # ✅ RETURN CLEAN DATA (Power BI friendly)
        return final_data

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Power BI AR API Error")
        frappe.throw(str(e))