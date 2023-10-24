from datetime import datetime, timedelta

from odoo import Command
from odoo.tests import TransactionCase


class TestPartnerShowPartnerRentals(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResPartner = cls.env["res.partner"]
        cls.BikeRent = cls.env["bike.rent"]
        cls.bank = cls.ResPartner.create(
            [
                {
                    "name": "Rich Bank LLC",
                    "is_company": True,
                    "child_ids": [Command.create({"name": "Jan Kowalski"})],
                }
            ]
        )

    def get_bank_and_employee_domains(self, employee=None):
        return map(
            lambda partner: partner.action_show_partner_rental()["domain"],
            (self.bank, self.bank.child_ids or employee),
        )

    def test_01_no_rentals(self):
        for domain in self.get_bank_and_employee_domains():
            self.assertEqual(self.BikeRent.search(domain), self.BikeRent, domain)

    def test_02_bank_and_employee_rental(self):
        # CASE 1: only employee has rental record
        # WHEN
        employee_rental = self.BikeRent.create(
            [
                {
                    "partner_id": self.bank.child_ids.id,
                    "rent_start": (now := datetime.now()),
                    "rent_stop": now + timedelta(days=20),
                }
            ]
        )
        # THEN (both bank and employee should be able to see the record)
        for domain in self.get_bank_and_employee_domains():
            self.assertEqual(
                self.BikeRent.search(domain),
                employee_rental,
                f"Case 1: domain {domain}",
            )
        # CASE 2 both employee and bank have rental records
        # WHEN
        bank_rental = self.BikeRent.create(
            [
                {
                    "partner_id": self.bank.id,
                    "rent_start": (now := datetime.now()),
                    "rent_stop": now + timedelta(days=10),
                }
            ]
        )
        # THEN
        for domain, result in zip(
            self.get_bank_and_employee_domains(),
            (bank_rental + employee_rental, employee_rental),
        ):
            self.assertEqual(
                self.BikeRent.search(domain), result, f"Case 2: domain {domain}"
            )
        # CASE 3: employee and bank are no longer connected
        # WHEN
        employee = self.bank.child_ids
        employee.write({"parent_id": [Command.unlink(self.bank.id)]})
        # THEN
        self.assertTrue(
            employee.parent_id == self.bank.child_ids == self.ResPartner,
            "Case 3 parent has not been unlinked.",
        )
        for domain, result in zip(
            self.get_bank_and_employee_domains(employee), (bank_rental, employee_rental)
        ):
            self.assertEqual(
                self.BikeRent.search(domain), result, f"Case 3: domain {domain}"
            )
