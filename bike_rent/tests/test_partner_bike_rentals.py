from odoo import Command

from .common import TestBikeRentCommon


class TestPartnerShowPartnerRentals(TestBikeRentCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_rich_bank = cls.ResPartner.create(
            [
                {
                    "name": "Rich Bank LLC",
                    "is_company": True,
                    "child_ids": [Command.create({"name": "Jan Kowalski"})],
                }
            ]
        )
        cls.partner_jan = cls.partner_rich_bank.child_ids

    @classmethod
    def _get_rental_domain(cls, partner):
        return partner.action_show_partner_rental()["domain"]

    def get_rentals(self, partner):
        return self.BikeRent.search(self._get_rental_domain(partner))

    @classmethod
    def get_rent_search_err_msg(cls, partner):
        return f"Wrong {partner.name} Rentals search result"

    @classmethod
    def get_rent_count_err_msg(cls, partner):
        return f"{partner.name} has incorrect rent_count"

    def test_01_no_rentals(self):
        company_rentals = self.get_rentals(self.partner_rich_bank)
        employee_rentals = self.get_rentals(self.partner_jan)
        self.assertTrue(company_rentals == employee_rentals == self.BikeRent)

    def test_02_employee_has_rental(self):
        # GIVEN
        employee_rental = self.create_rent(20, self.partner_jan)
        # WHEN
        company_rentals = self.get_rentals(self.partner_rich_bank)
        employee_rentals = self.get_rentals(self.partner_jan)
        # THEN
        self.assertEqual(
            company_rentals,
            employee_rental,
            self.get_rent_search_err_msg(self.partner_rich_bank),
        )
        self.assertEqual(
            employee_rentals,
            employee_rental,
            self.get_rent_search_err_msg(self.partner_jan),
        )
        self.assertEqual(
            len(employee_rentals),
            self.partner_rich_bank.rent_count,
            self.get_rent_count_err_msg(self.partner_rich_bank),
        )
        self.assertEqual(
            len(employee_rentals),
            self.partner_jan.rent_count,
            self.get_rent_count_err_msg(self.partner_jan),
        )

    def test_03_company_and_employee_have_rental(self):
        # GIVEN
        employee_rental = self.create_rent(20, self.partner_jan)
        company_rental = self.create_rent(10, self.partner_rich_bank)
        # WHEN
        company_rentals = self.get_rentals(self.partner_rich_bank)
        employee_rentals = self.get_rentals(self.partner_jan)
        # THEN
        self.assertEqual(
            company_rentals,
            company_rental + employee_rental,
            self.get_rent_search_err_msg(self.partner_rich_bank),
        )
        self.assertEqual(
            employee_rentals,
            employee_rental,
            self.get_rent_search_err_msg(self.partner_jan),
        )
        self.assertEqual(
            len(company_rentals),
            self.partner_rich_bank.rent_count,
            self.get_rent_count_err_msg(self.partner_rich_bank),
        )
        self.assertEqual(
            len(employee_rental),
            self.partner_jan.rent_count,
            self.get_rent_count_err_msg(self.partner_jan),
        )

    def test_04_company_and_ex_employee_have_independent_rental(self):
        # GIVEN
        employee_rental = self.create_rent(20, self.partner_jan)
        company_rental = self.create_rent(10, self.partner_rich_bank)
        # WHEN
        partner_employee = self.partner_jan
        partner_employee.write(
            {"parent_id": [Command.unlink(self.partner_rich_bank.id)]}
        )
        # THEN
        self.assertTrue(
            partner_employee.parent_id
            == self.partner_rich_bank.child_ids
            == self.ResPartner,
            "Case 3 parent has not been unlinked.",
        )
        company_rentals = self.get_rentals(self.partner_rich_bank)
        employee_rentals = self.get_rentals(partner_employee)
        self.assertEqual(
            company_rentals,
            company_rental,
            self.get_rent_search_err_msg(self.partner_rich_bank),
        )
        self.assertEqual(
            employee_rentals,
            employee_rental,
            self.get_rent_search_err_msg(self.partner_jan),
        )
        self.assertEqual(
            len(company_rentals),
            self.partner_rich_bank.rent_count,
            self.get_rent_count_err_msg(self.partner_rich_bank),
        )
        self.assertEqual(
            len(employee_rentals),
            partner_employee.rent_count,
            self.get_rent_count_err_msg(partner_employee),
        )
