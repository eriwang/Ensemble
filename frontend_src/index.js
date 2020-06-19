import { test } from './upload.js';

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
    name();
    $('#submit-button').click(submitAccomplishmentForm);
    $.get('/all_accomplishments').done(populateAccomplishments);
});

function populateAccomplishments(data)
{
    console.log(data);
    for (let a of data['accomplishments'])
    {
        let htmlStr =   `<p data-id="${a['id']}">
                            ${a['date']}: ${a['description']}, is_planned=${a['is_planned']}, status=${a['status']}
                        </p>`;
        $('#accomplishments').append(htmlStr);
    }
}

function submitAccomplishmentForm()
{
    console.log('submitting');
    let data = {};
    for (let name_and_value of $('#add-accomplishment').serializeArray())
    {
        data[name_and_value['name']] = name_and_value['value'];
    }

    data['is_planned'] = (data['is_planned'] === 'true');
    data['status'] = parseInt(data['status']);
    console.log(data);
    $.ajax('/accomplishment', {  // TODO: abstract this out. this is ridiculous to get right
        'contentType': 'application/json',
        'data': JSON.stringify(data),
        'method': 'POST',
        'processData': false
    }).done(() => {
        console.log('done');
        $.get('/all_accomplishments').done(populateAccomplishments);
    });
}