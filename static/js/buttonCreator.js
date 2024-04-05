var xhr = new XMLHttpRequest();
xhr.open('GET', "http://walternicolas.de/api/getAllAvailableAPICalls")
xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
        let apiCalls = JSON.parse(xhr.responseText);
        createButtons(apiCalls);
    } else {
        // console.error('Error making ' + apiCall.name + ' API call:', xhr.statusText);
    }
};


xhr.send();
function createButtons(apiCalled) {
    var buttonContainer = document.getElementById('buttonContainer');

    buttonContainer.style.display = 'flex';

    apiCalled.forEach(function (apiCall) {

        var button = document.createElement('button');

        buttonContainer.appendChild(button);

        button.textContent = apiCall.name;
        button.type = "button";
        button.className = 'custom-button load-store';

        button.addEventListener('click', function () {
            if (apiCall.type === "site") {
                window.location.href = apiCall.url;
            } else {
                var xhr = new XMLHttpRequest();

                xhr.open('GET', apiCall.url);

                xhr.setRequestHeader('Token', '1074473')

                xhr.onload = function () {
                    appendToOutput(xhr.responseText);
                };

                xhr.ontimeout = function () {
                    appendToOutput("PC ist nicht erreichbar oder Aus!");
                }

                xhr.onerror = function () {
                    appendToOutput(('Error making ' + apiCall.name + ' API call:' + xhr.statusText));
                };

                xhr.send();
            }
        });

        buttonContainer.appendChild(button);
    });
}

function loadSave() {
    window.location.href = "load";
}

function createNew() {
    window.location.href = "createID";
}

function deleteID() {
    window.location.href = "deleteID";
}

function appendToOutput(Resp) {
    var outputfield = document.getElementById('output');

    var datetime = new Date();

    var date = datetime.toDateString();
    var time = datetime.toTimeString().split(' ')[0];

    var formatted = date + ' ' + time;

    if (outputfield.innerHTML === '<br>') {
        outputfield.innerHTML = formatted + ': ' + Resp;
    }else {
        outputfield.innerHTML = formatted + ': ' + Resp + '<br>' + outputfield.innerHTML;
    }

}