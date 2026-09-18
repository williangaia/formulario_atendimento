const form = document.querySelector("#satisfaction-form");
const submitButton = document.querySelector("#submit-button");
const errorMessage = document.querySelector("#error-message");
const surveyScreen = document.querySelector("#survey-screen");
const thankYouScreen = document.querySelector("#thank-you-screen");
const answerInputs = document.querySelectorAll("input[name='answer']");

answerInputs.forEach((input) => {
    input.addEventListener("change", () => {
        submitButton.disabled = false;
        errorMessage.textContent = "";
    });
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const selected = document.querySelector("input[name='answer']:checked");

    if (!selected) {
        errorMessage.textContent = "Selecione uma opção para continuar.";
        return
    }

    submitButton.disabled = true;
    submitButton.textContent = "Enviando...";
    errorMessage.textContent = "";

    try {
        const response = await fetch("/api/satisfaction", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ answer: selected.value })
        });
    } catch (error) {
        errorMessage.textContent = "Não foi possível enviar. Tente novamente.";
        submitButton.disabled = false;
        submitButton.textContent = "Confirmar resposta";
    }
});