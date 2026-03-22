const footerTranslations = {
    en: {
        get_in_touch: "Get In Touch",
        company: "Company",
        support: "Support",
        contact: "Contact",
        feedback: "Feedback",
        privacy: "Privacy Policy",
        terms: "Terms and Conditions",
        payments: "Payments"
    },
    hi: {
        get_in_touch: "संपर्क करें",
        company: "कंपनी",
        support: "सहायता",
        contact: "संपर्क",
        feedback: "प्रतिक्रिया",
        privacy: "गोपनीयता नीति",
        terms: "नियम और शर्तें",
        payments: "भुगतान"
    },
    mr: {
        get_in_touch: "संपर्क साधा",
        company: "कंपनी",
        support: "सहाय्य",
        contact: "संपर्क",
        feedback: "अभिप्राय",
        privacy: "गोपनीयता धोरण",
        terms: "अटी व शर्ती",
        payments: "देयके"
    }
};

function applyFooterLanguage(lang) {
    localStorage.setItem("footer_lang", lang);
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (footerTranslations[lang] && footerTranslations[lang][key]) {
            el.innerText = footerTranslations[lang][key];
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const savedLang = localStorage.getItem("footer_lang") || "en";
    applyFooterLanguage(savedLang);

    const selector = document.getElementById("languageSwitcher");
    selector.value = savedLang;
    selector.addEventListener("change", e => {
        applyFooterLanguage(e.target.value);
    });
});
