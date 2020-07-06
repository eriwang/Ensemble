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

export function ajaxGet(url, data)
{
    return $.ajax(url, {
        'data': data,
        'method': 'GET',
        'processData': true
    });
}

export function ajaxPost(url, data)
{
    return ajaxJsonBody(url, data, 'POST');
}

export function ajaxPut(url, data)
{
    return ajaxJsonBody(url, data, 'PUT');
}

export function ajaxDelete(url, data)
{
    return ajaxJsonBody(url, data, 'DELETE');
}

function ajaxJsonBody(url, data, method)
{
    return $.ajax(url, {
        'contentType': 'application/json',
        'data': JSON.stringify(data),
        'method': method,
        'processData': false
    });
}
