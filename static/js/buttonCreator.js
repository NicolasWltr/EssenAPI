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
                    console.log("hi")
                    console.log(xhr.responseText);
                    appendToOutput(xhr.responseText);
                };

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

    outputfield.innerHTML = outputfield.innerHTML + Resp;

}