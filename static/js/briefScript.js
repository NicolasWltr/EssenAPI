function changeEnvelope(){
    envelope = document.getElementById("env")
    envelopeToHideKiss = document.getElementById("envToHideKiss")
    kiss = document.getElementById("kiss")

    envelope.classList.add('opened');
    envelope.src = 'https://cdn-icons-png.flaticon.com/128/10333/10333708.png'
    envelopeToHideKiss.classList.add('opened');
    envelopeToHideKiss.src = 'https://cdn-icons-png.flaticon.com/128/10333/10333708.png'

    kiss.classList.add('popup')
}