# Author: Aleksander Milinkevich. Copyright: Versada UAB.
# See LICENSE and COPYRIGHT files for details.
{
    "name": "Bike Rent",
    "version": "16.0.1.0.0",
    "summary": "Bike Rent",
    "license": "LGPL-3",
    "author": "Versada",
    "website": "https://www.versada.eu",
    "category": "Services",
    "depends": [
        # odoo
        "sale_management",
    ],
    "data": [
        "security/bike_rent_security.xml",
        "security/ir.model.access.csv",
        "security/bike_product_security.xml",
        "views/bike_rent.xml",
        "views/bike_rent_menus.xml",
        "views/product_template.xml",
        "views/product_product.xml",
        "views/res_partner.xml",
        "views/sale_order.xml",
        "report/sale_order.xml",
    ],
    "demo": ["demo/product_product.xml", "demo/bike_rent.xml"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
