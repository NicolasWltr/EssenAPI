var xhr = new XMLHttpRequest();
xhr.open('GET', "http://walternicolas.de/api/getAllAvailableAPICalls")
xhr.onload = function() {
    if (xhr.status >= 200 && xhr.status < 300) {
        let apiCalls = JSON.parse(xhr.responseText);
        createButtons(apiCalls);
    } else {
        console.error('Error making ' + apiCall.name + ' API call:', xhr.statusText);
    }
};

        // Define the behavior for error
xhr.onerror = function() {
    console.error('Error making ' + apiCall.name + ' API call:', xhr.statusText);
};

xhr.send();

// Get the container where buttons will be appended
var buttonContainer = document.getElementById('buttonContainer');

console.log(buttonContainer)
function createButtons(apiCalled) {
    console.log(apiCalled)
    apiCalled.forEach(function (apiCall) {
        var button = document.createElement('button');

        button.textContent = apiCall.name;
        button.className = 'custom-button';

        button.addEventListener('click', function () {
            if (apiCall.type === "site") {
                window.location.href = apiCall.url;
            } else {
                var xhr = new XMLHttpRequest();

                xhr.setRequestHeader('Token', '1074473')

                xhr.open('GET', apiCall.url);

                xhr.onload = function () {
                    if (xhr.status >= 200 && xhr.status < 300) {
                        console.log(apiCall.name + ' API call successful:', xhr.responseText, xhr);
                    } else {
                        console.error('Error making ' + apiCall.name + ' API call:', xhr.statusText);
                    }
                };

                xhr.onerror = function () {
                    console.error('Error making ' + apiCall.name + ' API call:', xhr.statusText);
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