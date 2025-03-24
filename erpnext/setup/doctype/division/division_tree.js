frappe.treeview_settings["Division"] = {
	ignore_fields: ["parent_division"],
	get_tree_nodes: "erpnext.setup.doctype.division.division.get_children",
	add_tree_node: "erpnext.setup.doctype.division.division.add_node",
	filters: [
		{
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			label: __("Company"),
		},
	],
	breadcrumb: "HR",
	root_label: "All Divisions",
	get_tree_root: true,
	menu_items: [
		{
			label: __("New Division"),
			action: function () {
				frappe.new_doc("Division", true);
			},
			condition: 'frappe.boot.user.can_create.indexOf("Division") !== -1',
		},
	],
	onload: function (treeview) {
		treeview.make_tree();
	},
};
