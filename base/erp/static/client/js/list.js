$(function () {
	const is_superuser = document.getElementById("is_superuser").value;

	$("#data").DataTable({
		responsive: true,
		autoWidth: false,
		destroy: true,
		deferRender: true,
		ajax: {
			url: window.location.pathname,
			type: "POST",
			data: {
				action: "searchdata",
			},
			dataSrc: "",
			headers: {
				"X-CSRFToken": csrftoken,
			},
		},
		columns: [
			{ data: "id" },
			{ data: "names" },
			{ data: "surnames" },
			{ data: "ci" },
			{ data: "gender.name" },
			{ data: "score" },
			{ data: "id" },
		],
		columnDefs: [
			{
				targets: [-1],
				class: "text-center",
				orderable: false,
				render: function (data, type, row) {
					if (is_superuser == "True") {
						var buttons =
							'<a href="/erp/client/update/' +
							row.id +
							'/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
						buttons +=
							'<a href="/erp/client/delete/' +
							row.id +
							'/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
						return buttons;
					} else {
						var buttons =
							'<a href="#" class="btn btn-danger btn-xs btn-flat">X</a> ';
						return buttons;
					}
				},
			},
		],
		initComplete: function (settings, json) {},
	});
});
