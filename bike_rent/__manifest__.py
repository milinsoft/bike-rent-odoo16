# Author: Aleksander Milinkevich. Copyright: Versada UAB.
# See LICENSE and COPYRIGHT files for details.
{
    "name": "Bike Rent",
    "version": "16.0.1.0.0",
    "summary": "Bike Rent",
    "license": "LGPL-3",
    "author": "Versada",
    "website": "https://www.versada.eu",
    "category": "Uncategorized",
    "depends": [
        # odoo
        "base"
    ],
    "data": ["security/ir.model.access.csv", "views/bike_rent.xml", "views/bike_rent_menus.xml"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
