document.addEventListener('DOMContentLoaded', async function () {
	$("#dataTable").DataTable();
	$(".form_select").chosen();
	ClassicEditor.create(document.querySelector("#description"), {
		language: "ar",
	});

	ClassicEditor.create(document.querySelector("#guidelines"), {
		language: "ar",
	});
});
