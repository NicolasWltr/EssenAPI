var text = document.getElementById('textfield');

var xhr = new XMLHttpRequest();
xhr.open('GET', "http://127.0.0.1:5000/getter/getsave");
xhr.setRequestHeader("token", 'nivanprpquß24723h780cnß2n1n')
xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
        let response = xhr.responseText;

        if (response === "declined") {
            window.location.href = 'IDNotPresent'
            return;
        }

        text.innerHTML = xhr.responseText;
    } else {
        console.log('error')
    }
}
xhr.send();

function save() {
    var text = document.getElementById("textfield").innerHTML;

    var xhr = new XMLHttpRequest();

    xhr.open('POST', "http://127.0.0.1:5000/setter/setsave?input=" + text);
    xhr.setRequestHeader("token", 'nivanprpquß24723h780cnß2n1n');

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            let response = xhr.responseText;

            if (response === "declined") {
                window.location.href = 'IDNotPresent'
                return;
            }

            text.innerHTML = xhr.responseText;
            window.location.href = 'start';
        } else {
            console.log('error')
        }
    }
    xhr.send();
}