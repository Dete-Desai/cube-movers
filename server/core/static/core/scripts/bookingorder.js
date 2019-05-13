$(document).ready(function () {
	$('.download-pdf').click(function(){
		var doc = new jsPDF(); 
		doc.fromHTML($('#test').get(0), 15, 15, {
			'width': 170
		});

         doc.save('booking order');
	});
});