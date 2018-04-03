


$(document).ready(function(){

/***** drag and drop ********/
var dropper = document.getElementById('deposer');
dropper.addEventListener('dragover', function(e) {
    e.preventDefault(); // Annule l'interdiction de drop
     dropper.style.borderColor = '#33CCFF';
     dropper.getElementsByClassName('bigTxt')[0].style.color='#33CCFF';
     dropper.querySelector('i').style.color='#33CCFF';
});

dropper.addEventListener('dragenter', function(e) {

    

});

dropper.addEventListener('dragleave', function() {
          dropper.style.borderColor = '#ddd';
          dropper.getElementsByClassName('bigTxt')[0].style.color='#ccc';
          dropper.querySelector('i').style.color='#ddd';
});

dropper.addEventListener('drop', function(e) {
    e.preventDefault(); // Cette méthode est toujours nécessaire pour éviter une éventuelle redirection inattendue

    process_selected(e.dataTransfer.files);
        
    dropper.style.borderColor = '#ddd';
    dropper.getElementsByClassName('bigTxt')[0].style.color='#ccc';
    dropper.querySelector('i').style.color='#ddd';
});



    // setup session cookie data. This is Django-related
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // end session cookie data setup.

    var fileItemList = []

    function process_selected(selectedFiles){
        
        $.each(selectedFiles, function(index, item){
            
            var myFile = verifyVideo(item)
            if (myFile){
                uploadFile(myFile)
            } else {
                alert("Some files are invalid uploads.")
            }
        })
        $(this).val('');


    }

	// auto-upload on file input change.
	$(document).on('change','.upload-video', function(event){
        var selectedFiles = $(this).prop('files');
         process_selected(selectedFiles)
	    });

        function uploadComplete(file){
            alert(file.order)
            var itemList = $('.uploading-queue')


        }

	function verifyVideo(file){
	    // verifies the file extension is one we support.
	    var extension = file.name.split('.').pop().toLowerCase(); //file.substr( (file.lastIndexOf('.') +1) );
	    switch(extension) {
	        case 'mov':
	        case 'mp4':
	        case 'mpeg4':
	        case 'avi':
            case 'webm':
	            return file

	        default:
	            //snotAllowedFiles.push(file)
	            return null
	    }
	}
    
    function constructFormData(data, fileItem) {
		var contentType = fileItem.type
		var filename = data.filename
		//var repsonseUser = data.user
		var keyPath = 'www/' + '/' + filename
		// var keyPath = policyData.file_bucket_path
		var fd = new FormData()
		fd.append('key', keyPath + filename);
		// fd.append('acl','private');
		fd.append('Content-Type', contentType);
		fd.append("uuid", data.uuid)
		fd.append('filename', filename);
		fd.append('file', fileItem);
		return fd
	}

    function displayItems(fileItemList){
        var itemList = $('.uploading-queue')
        itemList.html("")
        $.each(fileItemList, function(index, obj){
            var item = obj.file
            var id_ = obj.id
            var order_ = obj.order
            // <div class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width: 10%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100">25%</div>
            var close_html=' <button type="button" class="close" aria-label="Close" data-id="' + id_ + '"> <span aria-hidden="true">&times;</span> </button>'
            var html_ = '<div class="progress">' + 
              '<div class = "progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width:' + item.progress + '%" aria-valuenow="' + item.progress + '" aria-valuemin="0" aria-valuemax="100">' + item.progress + '%</div></div>'
            itemList.append('<div id="'+ order_ +'"> <h6> <span class="badge badge-pill badge-primary align-top">' + order_ + " </span> " + item.name + close_html +"</h6>" + html_ + "</div><hr/>")

        })
    }

    function uploadFile(fileItem){
        var data = {
            // add to setting url to simplify editing
		url:'http://ss.dcm-ovs.com:8080/upload/',
        };

        $.ajax({
            type:"POST",
            data: { // TODO: send to server side file name and maybe md5 of file also type mime and size
                filename: fileItem.name
            },
            url: "/upload/",
            dataType : "json",
            success: function(revievedData){
                    alert("success: "+ revievedData.uuid)
                    data.uuid = revievedData['uuid']
                    // data.uuid = '4513f29b-ee91-4656-86de-70e8aca88959'
                    // data.uuid = $.parseJSON(revievedData)[0].fields.uuid
            },
            error: function(data){
                alert("An error occured, please try again later")
            }
        }).done(function(){
            // construct the needed data
            var fd = constructFormData(data, fileItem)

            // use XML http Request to Send ss. 
            var xhr = new XMLHttpRequest()

            // construct callback for when uploading starts
            xhr.upload.onloadstart = function(event){
                var inLoadingIndex = $.inArray(fileItem, fileItemList)
                if (inLoadingIndex == -1){
                    // Item is not loading, add to inProgress queue
                    newLoadingItem = {
                        file: fileItem,
                        id: data.uuid,
                        order: fileItemList.length + 1
                    }
                    fileItemList.push(newLoadingItem)
                  }
                fileItem.xhr = xhr
            }

            // Monitor upload progress and attach to fileItem.
            xhr.upload.addEventListener("progress", function(event){
                if (event.lengthComputable) {
                 var progress = Math.round(event.loaded / event.total * 100);
                    fileItem.progress = progress
                    displayItems(fileItemList)
                    console.log("progress = "+ progress)
                }
            })
           
           function readBody(xhr) {
                var data;
                if (!xhr.responseType || xhr.responseType === "text") {
                    data = xhr.responseText;
                
                } else if (xhr.responseType === "document") {
                    data = xhr.responseXML;

                } else {
                    data = xhr.response;
              
                }
                return data;
            }
            function getfile(item){

                return item.file.name == fileItem.name
            }

            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4) {
                    var item = fileItemList.find(getfile);
   
                    itemhtml = $('.uploading-queue > #'+item.order+' > .progress')
                    
                    switch (xhr.status){
                        case 200:
                            itemhtml.replaceWith( '<div class="alert alert-success" role="alert">This video was successfully uploaded </div>' )
                            break;
                        case 413:
                            itemhtml.replaceWith( '<div class="alert alert-danger" role="alert">Error, file too large ! </div>' )
                            break;
                        case 415:
                            itemhtml.replaceWith( '<div class="alert alert-danger" role="alert">Error, Unsupported Media Type !</div>' )
                            break;

                    }
                    console.log(readBody(xhr));
                }
            }



            xhr.open('POST', data.url , true);
            xhr.send(fd);
 })
}});