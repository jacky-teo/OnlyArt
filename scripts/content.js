
function showError(message) {
        // Hide the table and button in the event of error
        $('#searchField').hide();
        // Display an error under the main container
        $('#error').text("Creator not found") 
    }

    $('#search').click(async() => { 
        if($('#contentTable > tr')){
            $('#contentTable > tr').remove()
        }

        var rows = "";

        $('#contentTable').show()
        
        var creatorID = sessionStorage.getItem('CreatorID');  
        var serviceURL = "http://127.0.0.1:5003/content/" + creatorID;
        var deleteURL = 'http://127.0.0.1:5003/delete/'
        var updateURL = 'http://127.0.0.1:5003/update/'
        try {
            const response =
            await fetch(
                serviceURL, { method: 'GET' } // Get information from request
            );
            const result = await response.json(); // Get the results
            console.log(result)
            if (response.status == 200) {
                // success case
                var contents = result.data; //the array is in cont within data of contents
                // console.log(contents)
                // the returned result
                // for loop to setup all table rows with obtained Content data
                var counter =0;
                for (const content of contents) {
                    eachRow ="<td>" + content.POSTID + "</td>" +
                            "<td>" + content.CREATORID + "</td>" +
                            "<td>" + content.DESCRIPTION + "</td>" +
                            "<td> <img src='" + result.urls[counter] + "'  width='100' height='100'></td>"+
                            "<td>" + content.POST_DATE + "</td>" +
                            "<td>" + content.modified + "</td>" +
                            // "<td>"+ "<a href='./update.html?postID="+content.POSTID +"'"+">"+ "</td>"+ // IM UNSURE T__T
                            "<td> <a href='"+ deleteURL +  content.POSTID+ "'>Delete</a></td>";
                   rows += "<tr>" + eachRow + "</tr>";
                   counter ++
                }
                    // add all the rows to the table
                    $('#contentTable').append(rows);
                } else if (response.status == 404) {
                    // No content
                    showError(result.message);
                } else {
                    // unexpected outcome, throw the error
                    throw response.status;
                }
            } catch (error) {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                showError
    ('There is a problem retrieving content data, please try again later.<br />' + error);
            } // error
    });