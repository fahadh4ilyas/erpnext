# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import json

import frappe
from frappe.utils.nestedset import NestedSet, get_root_of

from erpnext.utilities.transaction_base import delete_events


class Division(NestedSet):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company: DF.Link
		division_name: DF.Data
		disabled: DF.Check
		is_group: DF.Check
		lft: DF.Int
		old_parent: DF.Data | None
		parent_division: DF.Link | None
		rgt: DF.Int
	# end: auto-generated types

	nsm_parent_field = "parent_division"

	def autoname(self):
		root = get_root_of("Division")
		if root and self.division_name != root:
			self.name = get_abbreviated_name(self.division_name, self.company)
		else:
			self.name = self.division_name

	def validate(self):
		if not self.parent_division:
			root = get_root_of("Division")
			if root:
				self.parent_division = root

	def before_rename(self, old, new, merge=False):
		# renaming consistency with abbreviation
		if frappe.get_cached_value("Company", self.company, "abbr") not in new:
			new = get_abbreviated_name(new, self.company)

		return new

	def on_update(self):
		if not (frappe.local.flags.ignore_update_nsm or frappe.flags.in_setup_wizard):
			super().on_update()

	def on_trash(self):
		super().on_trash()
		delete_events(self.doctype, self.name)


def on_doctype_update():
	frappe.db.add_index("Division", ["lft", "rgt"])


def get_abbreviated_name(name, company):
	abbr = frappe.get_cached_value("Company", company, "abbr")
	new_name = f"{name} - {abbr}"
	return new_name


@frappe.whitelist()
def get_children(doctype, parent=None, company=None, is_root=False, include_disabled=False):
	if isinstance(include_disabled, str):
		include_disabled = json.loads(include_disabled)
	fields = ["name as value", "is_group as expandable"]
	filters = {}

	if company == parent:
		filters["name"] = get_root_of("Division")
	elif company:
		filters["parent_division"] = parent
		filters["company"] = company
	else:
		filters["parent_division"] = parent

	if frappe.db.has_column(doctype, "disabled") and not include_disabled:
		filters["disabled"] = False

	return frappe.get_all("Division", fields=fields, filters=filters, order_by="name")


@frappe.whitelist()
def add_node():
	from frappe.desk.treeview import make_tree_args

	args = frappe.form_dict
	args = make_tree_args(**args)

	if args.parent_division == args.company:
		args.parent_division = None

	frappe.get_doc(args).insert()
