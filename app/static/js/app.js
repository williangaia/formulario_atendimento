"use strict";

const form = document.querySelector("#satisfaction-form");
const submitButton = document.querySelector("#submit-button");
const errorMessage = document.querySelector("#error-message");
const surveyScreen = document.querySelector("#survey-screen");
const thankYouScreen = document.querySelector("#thank-you-screen");
const answerInputs = document.querySelectorAll(
    "input[name='answer']"
);
const optionCards = document.querySelectorAll(".option-card");

if (
    !form ||
    !submitButton ||
    !errorMessage ||
    !surveyScreen ||
    !thankYouScreen
) {
    throw new Error(
        "Elementos obrigatórios do formulário não foram encontrados."
    );
}

answerInputs.forEach((input) => {
    input.addEventListener("change", () => {
        optionCards.forEach((card) => {
            card.classList.remove("selected");
        });

        input.closest(".option-card").classList.add("selected");

        submitButton.disabled = false;
        errorMessage.textContent = "";
    });
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const selected = document.querySelector(
        "input[name='answer']:checked"
    );

    if (!selected) {
        errorMessage.textContent =
            "Selecione uma opção para continuar.";
        return;
    }

    submitButton.disabled = true;
    submitButton.textContent = "Enviando...";
    errorMessage.textContent = "";

    try {
        const response = await fetch("/api/satisfaction/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                answer: selected.value,
            }),
        });

        const data = await response.json();

        if (!response.ok || data.success !== true) {
            throw new Error(
                data.detail ||
                data.message ||
                "Falha ao enviar a resposta."
            );
        }

        surveyScreen.hidden = true;
        thankYouScreen.hidden = false;

        window.setTimeout(() => {
            form.reset();

            optionCards.forEach((card) => {
                card.classList.remove("selected");
            });

            thankYouScreen.hidden = true;
            surveyScreen.hidden = false;

            submitButton.disabled = true;
            submitButton.textContent = "Enviar resposta";
        }, 3000);
    } catch (error) {
        console.error(error);

        errorMessage.textContent =
            "Não foi possível enviar. Tente novamente.";

        submitButton.disabled = false;
        submitButton.textContent = "Enviar resposta";
    }
});