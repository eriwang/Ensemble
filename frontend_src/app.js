import $ from 'jquery';
import React from 'react';
import ReactDOM from 'react-dom';

class App extends React.Component
{
    constructor(props)
    {
        super(props);
        this.state = {
            'isUploadDisabled': false,
            'isMergeDisabled': false
        };

        this.fileInput = React.createRef();
    }

    handleFileUploadChange = () =>
    {
        this.setState({'isUploadDisabled': true});

        let formData = new FormData();
        formData.append('file', this.fileInput.current.files[0]);

        // TODO: clear the file from the input
        $.ajax('/track', {
            'data': formData,
            'method': 'POST',
            'processData': false,
            'contentType': false
        })
            .done(() => {
                this.setState({'isUploadDisabled': false});
                console.log('upload complete');
            })
            .fail(() => {
                this.setState({'isUploadDisabled': false});
                console.error('upload failed');
            });
    }

    mergeFiles = () =>
    {    
        console.log('merge files');
        this.setState({'isMergeDisabled': true});
        $.ajax('/merge', { 'method': 'POST' })
            .done((response) => {
                this.setState({'isMergeDisabled': false});
                
                console.log('files merged successfully');
                let searchParams = new URLSearchParams();
                searchParams.set('is_merged', true);
                searchParams.set('filename', response.filename);
                
                window.location.href = `/download?${searchParams.toString()}`;
            })
            .fail(() => {
                this.setState({'isMergeDisabled': false});
                console.error('file merge failed');
            });  
    }

    render()
    {
        return (
            <div>
                <h1>Ensemble Mini</h1>
                <input type="file" id="file-upload" accept="audio/wav, audio/mp3" ref={this.fileInput}
                    onChange={this.handleFileUploadChange} disabled={this.state.isUploadDisabled}/>
                <button id="merge-files" disabled={this.state.isMergeDisabled} onClick={this.mergeFiles}>
                    Merge Songs
                </button>
            </div>
        );
    }
}

ReactDOM.render(<App />, document.getElementById('app'));
