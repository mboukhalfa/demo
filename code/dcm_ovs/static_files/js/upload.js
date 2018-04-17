$(document).ready(function () {
let ss_url = "http://ss.dcm-ovs.com:8080"
    /***** drag and drop ********/
    let dropper = document.getElementById('deposer');
    dropper.addEventListener('dragover', function (e) {
        e.preventDefault(); // Annule l'interdiction de drop
        dropper.style.borderColor = '#33CCFF';
        dropper.getElementsByClassName('bigTxt')[0].style.color = '#33CCFF';
        dropper.querySelector('i').style.color = '#33CCFF';
    });

    dropper.addEventListener('dragenter', function (e) {


    });

    dropper.addEventListener('dragleave', function () {
        dropper.style.borderColor = '#ddd';
        dropper.getElementsByClassName('bigTxt')[0].style.color = '#ccc';
        dropper.querySelector('i').style.color = '#ddd';
    });

    dropper.addEventListener('drop', function (e) {
        e.preventDefault(); // Cette méthode est toujours nécessaire pour éviter une éventuelle redirection inattendue

        process_selected(e.dataTransfer.files);

        dropper.style.borderColor = '#ddd';
        dropper.getElementsByClassName('bigTxt')[0].style.color = '#ccc';
        dropper.querySelector('i').style.color = '#ddd';
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
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // end session cookie data setup.

    let fileItemList = []
    let ordering = 0;
    let fileItemListname = []

    function process_selected(selectedFiles) {

        $.each(selectedFiles, function (index, item) {
            var inLoadingIndex = $.inArray(item.name, fileItemListname)
            if (inLoadingIndex == -1) {
                fileItemListname.push(item.name)

                var myFile = verifyVideo(item)
                if (myFile) {
                    uploadFile(myFile)
                } else {
                    alert("Some files are invalid uploads.")
                }
            } else {
                alert(item.name + "already exist!")
            }
        })

    }

    // auto-upload on file input change.
    $(document).on('change', '.upload-video', function (event) {
        var selectedFiles = $(this).prop('files');
        process_selected(selectedFiles)
    });


    $(document).on('click', '.close', function (event) {

        var inLoadingIndex = $.inArray($(this).clone().parent().children().remove().end().text(), fileItemListname)
        fileItemListname.splice(inLoadingIndex, 1);
        fileItemList.splice(inLoadingIndex, 1);
        $(this).closest('div').html("");
    });


    function verifyVideo(file) {
        // verifies the file extension is one we support.
        var extension = file.name.split('.').pop().toLowerCase(); //file.substr( (file.lastIndexOf('.') +1) );
        switch (extension) {
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


    function arafile(fileItem) {

        return fileItemList.find(function (item) {
            return item.file.name == fileItem.name;
        });
    }

    function arafileHtml(item) {

        return $('.uploading-queue > #' + item.order + ' > .progress');
    }


    function displayItem(obj) {
        var itemList = $('.uploading-queue')
        let item = obj.file;
        let id_ = obj.id;
        let order_ = obj.order;

        let close_html = ' <button type="button" class="close" aria-label="Close" data-id="' + id_ + '"> <span aria-hidden="true">&times;</span> </button>'
        let html_ = '<div class="progress">' +
            '<div class = "progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width:0%" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">0%</div></div>'
        itemList.append('<div id="' + order_ + '"> <h6> <span class="badge badge-pill badge-primary align-top">' + order_ + " </span> " + item.name + close_html + "</h6>" + html_ + "<hr/></div>")
    }

    function processDisplay(fileItem) {
        let obj = arafile(fileItem);
        let fh = arafileHtml(obj);
        fh.html("");
        var item = obj.file

        var html_ = '<div class = "progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style="width:' + item.progress + '%" aria-valuenow="' + item.progress + '" aria-valuemin="0" aria-valuemax="100">' + item.progress + '%</div>'
        fh.html(html_)

    }

    function uploadFile(fileItem) {
        var data = {
            // add to setting url to simplify editing
            url: ss_url+'/upload/',
        };

        $.ajax({
            type: "POST",
            data: { // TODO: send to server side file name and maybe md5 of file also type mime and size
                filename: fileItem.name
            },
            url: "/upload/",
            dataType: "json",

            success: function (revievedData) {
                data.uuid = revievedData['uuid']
            },
            error: function (data) {
                alert("An error occurred, please try again")
            }
        }).done(function () {


                let interval = null;
                // construct the needed data
                var fd = constructFormData(data, fileItem)

                // use XML http Request to Send ss.
                var xhr = new XMLHttpRequest()


                /* generate random progress-id */
                let progress_uuid = "";
                for (i = 0; i < 32; i++) {
                    progress_uuid += Math.floor(Math.random() * 16).toString(16);
                }
                /* patch the data include the progress-id */
                data.url += "?X-Progress-ID=" + progress_uuid;

                console.log(data.url)
                xhr.open('POST', data.url, true);
                xhr.setRequestHeader('uuid', data.uuid);
                xhr.send(fd);


                // Item is not loading, add to inProgress queue


                newLoadingItem = {
                    file: fileItem,
                    id: data.uuid,
                    order: ++ordering,
                }

                fileItemList.push(newLoadingItem)
                displayItem(newLoadingItem)
                fileItem.xhr = xhr


                function fetch(progress_uuid) {
                    let req = new XMLHttpRequest();
                    req.open("GET", ss_url+"/progress", true);
                    req.setRequestHeader("X-Progress-ID", progress_uuid);
                    req.onreadystatechange = function () {
                        if (req.readyState == 4) {
                            if (req.status == 200) {

                                /* poor-man JSON parser */
                                var upload = JSON.parse(req.responseText);


                                if (upload.state == 'starting') {
                                    console.log('starting')

                                    setTimeout(function () {
                                        fetch(progress_uuid);
                                    }, 200);


                                }
                                /* change the width if the inner progress-bar*/
                                if (upload.state == 'uploading') {


                                    console.log('uplo')
                                    w = Math.floor(100 * upload.received / upload.size);
                                    if (w !== fileItem.progress && w < 100) {
                                        fileItem.progress = w
                                        processDisplay(fileItem);
                                        setTimeout(function () {
                                            fetch(progress_uuid);
                                        }, 500);
                                        console.log("progress = " + w)
                                    } else {
                                        setTimeout(function () {
                                            fetch(progress_uuid);
                                        }, 1000);
                                    }
                                }
                                /* we are done, stop the interval */
                                if (upload.state == 'done') {
                                    let item = arafile(fileItem);
                                    let itemhtml = arafileHtml(item);
                                    fileItem.progress = 100
                                    processDisplay(fileItem);
                                    itemhtml.replaceWith('<div class="alert alert-success" role="alert">This video was successfully uploaded </div>')

                                    window.clearTimeout(interval);
                                }
                                /* we are done, stop the interval */
                                if (upload.state == 'error') {
                                    let item = arafile(fileItem);
                                    let itemhtml = arafileHtml(item);


                                    switch (upload.status) {
                                        case 403:
                                            itemhtml.replaceWith('<div class="alert alert-danger" role="alert">Error, Permission denied  </div>')
                                            break;
                                        case 413:
                                            itemhtml.replaceWith('<div class="alert alert-danger" role="alert">Error, file too large ! </div>')
                                            break;
                                        case 415:
                                            itemhtml.replaceWith('<div class="alert alert-danger" role="alert">Error, Unsupported Media Type !</div>')
                                            break;
                                        default:
                                            itemhtml.replaceWith('<div class="alert alert-danger" role="alert">Error, file too large ! </div>')
                                            break;

                                    }
                                    console.log("error  " + upload.status)
                                    window.clearTimeout(interval);
                                }
                            }
                        }
                    }
                    req.send(null);
                }

                /* call the progress-updater every 1000ms */

                fetch(progress_uuid);

            }
        )
    }
})
;