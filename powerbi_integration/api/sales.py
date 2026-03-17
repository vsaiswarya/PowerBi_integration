import frappe

@frappe.whitelist()
def sales_invoice_summary(from_date=None, to_date=None, company=None, limit=100):
    filters = {}

    if from_date and to_date:
        filters["posting_date"] = ["between", [from_date, to_date]]
    elif from_date:
        filters["posting_date"] = [">=", from_date]
    elif to_date:
        filters["posting_date"] = ["<=", to_date]

    if company:
        filters["company"] = company

    return frappe.get_all(
        "Sales Invoice",
        fields=[
            "name",
            "posting_date",
            "customer",
            "customer_name",
            "company",
            "grand_total",
            "outstanding_amount",
            "status"
        ],
        filters=filters,
        limit_page_length=int(limit),
        order_by="posting_date desc"
    )