$(document).ready(function () {
$("#surveyor-list").select2({
		placeholder: "Surveyors"
	});
	$("#vehicle-list").select2({
		placeholder: "Select a vehicle"
	});
	$(function () {
		$('#survey-time').datetimepicker({
            useCurrent: false,
             viewMode: 'years',
            sideBySide: true
        });
	});

$('#confirmsurveyModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#confirmSurveyButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});

	});

$('#sendquoteModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#sendquoteButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

$('#approvemoveModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#approveMoveButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

$('#confirmpaymentModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#confirmpaymentButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

$('#propertydetailsModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#editPropertyButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

$('#delightformModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#delightformButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

$('#customerdetailsModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#customerdetailsButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

$('#confirmMoveModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#confirmMoveButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

$('#raiseBookingOrderModal').on('show.bs.modal', function (event) {
		var modal = $(this);
		modal.find('#raiseBookingOrderButton').on('click', function () {
			var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
	});
	});

});





