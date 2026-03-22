document.getElementById("feedbackForm").addEventListener("submit", function (e) {
    e.preventDefault();

    let valid = true;

    const name = nameField();
    const email = value("email");
    const pkg = value("package");
    const rating = value("rating");
    const feedback = value("feedback");
    const review = value("review");

    clearErrors();

    if (!name) error("nameError", "Name is required");
    if (!email) error("emailError", "Email is required");
    if (!pkg) error("packageError", "Please select package");
    if (!rating) error("ratingError", "Rating required");
    if (feedback.length < 5) error("feedbackError", "Min 5 characters");
    if (review.length < 20) error("reviewError", "Review min 20 characters");

    function error(id, msg) {
        document.getElementById(id).textContent = msg;
        valid = false;
    }

    if (valid) {
        document.getElementById("successMsg").textContent =
            "Feedback submitted successfully ✔";

        document.getElementById("feedbackForm").reset();
    }
});

function value(id) {
    return document.getElementById(id).value.trim();
}

function nameField() {
    return document.getElementById("name").value.trim();
}

function clearErrors() {
    document.querySelectorAll(".error").forEach(e => e.textContent = "");
    document.getElementById("successMsg").textContent = "";
}
