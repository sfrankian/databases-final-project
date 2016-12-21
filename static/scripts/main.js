// Stephanie Frankian and Elizabeth Kuszmaul
// main.js


// Credit to http://stackoverflow.com/questions/19578111/how-to-add-clone-form-fields-using-jquery-and-increment-ids-and-names
// For helping us figure out how to clone form fields!

$(document).ready(function() {
	var row_index=0;
	var table = document.getElementById("form_table");
	$("#add_row").click(function(){
		row_index++;
		var input = document.createElement("input");
		input.type = "text";
		
		var row = table.insertRow(-1);
		var col0 = row.insertCell(0);
		var col1 = row.insertCell(1);
		var col2 = row.insertCell(2);
		
	
		var newDate = document.createElement("input");
		//newDate.type = "input";
		$(newDate).attr('className','pickDate').attr('name','date'+row_index).appendTo(col0);
		$(newDate).datepicker({ dateFormat: "yy-mm-dd" });
			
		input.name = "time" + row_index;
		col1.appendChild(input);
		
		$(input).clone().prop('name','location'+row_index).appendTo(col2);
		
	});
	
	$("#remove_row").click(function(){
		if(row_index > 0) {
			document.getElementById("form_table").deleteRow(-1);
			row_index--;
		}
		
	
	});
});
