# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt
import unittest

import frappe
from frappe.tests import IntegrationTestCase

IGNORE_TEST_RECORD_DEPENDENCIES = ["Leave Block List"]


class TestDivision(IntegrationTestCase):
	def test_remove_division_data(self):
		doc = create_division("Test Division")
		frappe.delete_doc("Division", doc.name)


def create_division(division_name, parent_division=None):
	doc = frappe.get_doc(
		{
			"doctype": "Division",
			"is_group": 0,
			"parent_division": parent_division,
			"division_name": division_name,
			"company": frappe.defaults.get_defaults().company,
		}
	).insert()

	return doc
