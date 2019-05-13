$(document).ready(function () {
    $(function () {
        $('#from_time').datetimepicker({
        	format: "DD/MM/YYYY",
            useCurrent: false
        });
    });
     $(function () {
        $('#to_time').datetimepicker({
        	format: "DD/MM/YYYY",
            useCurrent: false
        });
    });
    $('#example').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    } );
});