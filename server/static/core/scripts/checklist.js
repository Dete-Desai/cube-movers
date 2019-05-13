$(document).ready(function () {
	$("#existing-item-list").select2({
		placeholder: "Select an item"
	});
	$("#existing-room-list").select2({
		placeholder: "Select a room"
	});
	$("#new-room-list").select2({
		placeholder: "Select a room"
	});
	$("#edit-room-list").select2({
		placeholder: "Select a room"
	});
    $("#edit-item-list").select2({
    placeholder: "Select an item"
  });

    $("#modal-room-list").select2({
      });
    $("#modal-item-list").select2({
 
  });

$('#editModal').on('show.bs.modal', function (event) {
  var link = $(event.relatedTarget) // Button that triggered the modal
  var item = link.data('item') // Extract info from data-* attributes
  var action = link.data('action');
  var id = link.data('id');
  var volume = link.data('volume');
  var qty = link.data('qty');
  var room = link.data('room');


  var text = '<span class="glyphicon glyphicon-pencil"></span>' + ' Edit '
  var modal = $(this);
  modal.find('.modal-title').html(text);
  modal.find('#item_id').val(id);
  modal.find('#volume').val(volume);
  modal.find('#item_name').val(item);
  modal.find('#quantity').val(qty); 
  modal.find('#modal-room-list').select2("val", room);
  modal.find('#editModalSurveyItemButton').on('click', function () {
    var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
  })
})

$('#deleteModal').on('show.bs.modal', function (event) {
  var link = $(event.relatedTarget) // Button that triggered the modal
  var item = link.data('item') // Extract info from data-* attributes
  var id = link.data('id');

  var text = '<span class="glyphicon glyphicon-trash"></span>' + ' Delete '
  var modal = $(this);
  modal.find('#item_id').val(id);
  modal.find('.modal-title').html(text);
  modal.find('#deleteModalSurveyItemButton').on('click', function () {
  var $btn = $(this).button('loading')
    // business logic...
    // $btn.button('reset')
  })

})
});