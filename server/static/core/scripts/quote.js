$(document).ready(function () {
	$("#quote-item-list").select2({
		placeholder: "Select an item"
	});

  $(function () {
    $('#move-time').datetimepicker({
            useCurrent: false
        });
  });


$('#editQuoteItemModal').on('show.bs.modal', function (event) {
  var link = $(event.relatedTarget) // Button that triggered the modal
  var item = link.data('item') // Extract info from data-* attributes
  var action = link.data('action');
  var id = link.data('id');
  var units = link.data('units');
  var cost = link.data('cost');
  console.log(id)
  var modal = $(this);
  modal.find('#quote_id').val(id);
  modal.find('#cost').val(cost);
  modal.find('#quote_item').val(item);
  modal.find('#units').val(units); 
  modal.find('#editModalSurveyItemButton').on('click', function () {
  	var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
})
})

$('#editTotalCBMModal').on('show.bs.modal', function (event) {
  var link = $(event.relatedTarget) // Button that triggered the modal
  // Extract info from data-* attributes
  var action = link.data('action');
  var id = link.data('id');
  var units = link.data('units');
  var cost = link.data('cost');
  console.log(id)
  var modal = $(this);
  modal.find('#quote_id').val(id);
  modal.find('#cost').val(cost);
  modal.find('#units').val(units); 
  modal.find('#editModalSurveyItemButton').on('click', function () {
  	var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
})
})



$('#deleteQuoteItemModal').on('show.bs.modal', function (event) {
  var link = $(event.relatedTarget) // Button that triggered the modal
  var item = link.data('item') // Extract info from data-* attributes
  var id = link.data('id');
  console.log(id);
  var modal = $(this);
  modal.find('#quote_id').val(id);
  modal.find('#deleteModalSurveyItemButton').on('click', function () {
  	var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
})
})
});