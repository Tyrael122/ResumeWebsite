
document.addEventListener("DOMContentLoaded", function () {

    let inputField = document.getElementById("sourceText");

    inputField.addEventListener("input", function () {

        let lang_from = document.getElementById("lang_from");
        let lang_to = document.getElementById("lang_to");

        lang_from = lang_from.options[lang_from.selectedIndex].value;
        lang_to = lang_to.options[lang_to.selectedIndex].value;

        fetch('/translator',
            {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: inputField.value, lang_from: lang_from, lang_to: lang_to })
            })
            .then((response) => response.text())
            .then(responseText => {

                let outputText = document.getElementById("outputText");

                outputText.innerHTML = responseText;
            });
    });

    if (screen.width < 600) {
        let div = document.getElementById("translatorArea");
        div.className = "";
    }
});