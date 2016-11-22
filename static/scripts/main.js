// Stephanie Frankian and Elizabeth Kuszmaul
// main.js


// Credit to http://stackoverflow.com/questions/19578111/how-to-add-clone-form-fields-using-jquery-and-increment-ids-and-names
// For helping us figure out how to clone form fields!

$(document).ready(function(){
	var time_index = 0;
	var location_index = 0;
	// If the time button is clicked
	$("#add_time").click(function(){
		time_index++;
		// Cloning and making the new field visible
		$(this).parent().before($("#time_form").clone().attr("id","time_form" + time_index));
		$("#time_form" + time_index).css("display","inline");
		$("#time_form" + time_index + " :input").each(function(){
			// Making the name and id use the clone's number	
			$(this).attr("name",$(this).attr("name") + time_index);
			$(this).attr("id",$(this).attr("id") + time_index);
		    });
		// Removing a time field
		$("#remove_time" + time_index).click(function(){
			$(this).closest("div").remove();
		    });
	}); 
    
	// If the location button is clicked
	$("#add_location").click(function(){
		location_index++;
		// Cloning and making the new field visible
		$(this).parent().before($("#location_form").clone().attr("id","location_form" + location_index));
		$("#location_form" + location_index).css("display","inline");
		$("#location_form" + location_index + " :input").each(function(){
			// Making the name and id use the clone's number	
			$(this).attr("name",$(this).attr("name") + location_index);
			$(this).attr("id",$(this).attr("id") + location_index);
		    });
		// Removing a location field
		$("#remove_location" + location_index).click(function(){
			$(this).closest("div").remove();
		    });
	}); 
    
       
 });