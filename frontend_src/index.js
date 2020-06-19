import $ from 'jquery';

$(document).ajaxError((event, jqXHR, settings, exception) => {
    const errorText = `"${settings.type}" request to URL "${settings.url}" failed ` +
                        `with status ${jqXHR.status}, "${exception}"`;
    console.error(errorText);
    if (jqXHR.hasOwnProperty('responseJSON'))
    {
        console.error(jqXHR.responseJSON['error']);
    }
});

$(document).ready(() => {
    $('#file-upload').change(uploadFile);
    $('#merge-files').click(mergeFiles);
});

function uploadFile()
{
    console.log('uploading file');
    let fileUploadInput = $('#file-upload');
    fileUploadInput.prop('disabled', true);
    let formData = new FormData();
    formData.append('file', fileUploadInput[0].files[0]);

    // TODO: clear the file from the input
    $.ajax('/track', {
        'data': formData,
        'method': 'POST',
        'processData': false,
        'contentType': false
    })
        .done(() => {
            fileUploadInput.prop('disabled', false);
            console.log('upload complete');
        })
        .fail(() => {
            fileUploadInput.prop('disabled', false);
            console.error('upload failed');
        });
}

function mergeFiles()
{
    console.log('merge files');
    let mergeFilesButton = $('#merge-files');
    mergeFilesButton.prop('disabled', true);
    $.ajax('/merge', { 'method': 'POST' })
        .done(() => {
            mergeFilesButton.prop('disabled', false);
            console.log('files merged successfully');
        })
        .fail(() => {
            mergeFilesButton.prop('disabled', false);
            console.error('file merge failed');
        });
}
