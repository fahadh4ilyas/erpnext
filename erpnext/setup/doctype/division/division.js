// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on("Division", {
	onload: function (frm) {
		frm.set_query("parent_division", function () {
			return { filters: [["Division", "is_group", "=", 1]] };
		});
	},
	refresh: function (frm) {
		// read-only for root division
		if (!frm.doc.parent_division && !frm.is_new()) {
			frm.set_read_only();
			frm.set_intro(__("This is a root division and cannot be edited."));
		}
	},
	validate: function (frm) {
		if (frm.doc.name == "All Divisions") {
			frappe.throw(__("You cannot edit root node."));
		}
	},
});
