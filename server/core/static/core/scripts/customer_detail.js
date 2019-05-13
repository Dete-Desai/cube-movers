$(document).ready(function () {
$('#customerdetailsModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#customerdetailsButton').on('click', function () {
			var $btn = $(this).button('Loading')
    // business logic...
    // $btn.button('reset')
	})
	})
$('#createInquiryModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#createInquiryButton').on('click', function () {
			var $btn = $(this).button('Loading')
    // business logic...
    // $btn.button('reset')
	})
	})
// $('.panel-body .collapse').collapse('show');
});





