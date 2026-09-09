(() => {
    const form = document.querySelector("[data-invite-form]");
    if (!form) {
        return;
    }

    const input = form.querySelector('input[name="username"]');
    const list = form.querySelector("#invite-suggestions");
    const feedback = form.querySelector("[data-invite-feedback]");
    let options = [];
    let activeIndex = -1;
    let requestId = 0;
    let timer;

    const closeList = () => {
        list.hidden = true;
        input.setAttribute("aria-expanded", "false");
        input.removeAttribute("aria-activedescendant");
        activeIndex = -1;
    };

    const setFeedback = (message) => {
        feedback.textContent = message;
    };

    const renderOptions = (results) => {
        options = results;
        list.replaceChildren();
        results.forEach((result, index) => {
            const option = document.createElement("div");
            option.id = `invite-option-${index}`;
            option.className = "invite-suggestion";
            option.setAttribute("role", "option");
            option.dataset.username = result.username;
            option.textContent = result.username;
            option.addEventListener("mousedown", (event) => {
                event.preventDefault();
                selectOption(index);
            });
            list.appendChild(option);
        });
        list.hidden = results.length === 0;
        input.setAttribute("aria-expanded", String(results.length > 0));
        setFeedback(results.length ? `${results.length} clients available.` : "No eligible clients match.");
    };

    const highlightOption = (index) => {
        activeIndex = index;
        list.querySelectorAll("[role=option]").forEach((option, optionIndex) => {
            const active = optionIndex === index;
            option.classList.toggle("is-active", active);
            option.setAttribute("aria-selected", String(active));
        });
        if (index >= 0) {
            input.setAttribute("aria-activedescendant", `invite-option-${index}`);
        } else {
            input.removeAttribute("aria-activedescendant");
        }
    };

    const selectOption = (index) => {
        const selected = options[index];
        if (!selected) {
            return;
        }
        input.value = selected.username;
        closeList();
        setFeedback(`${selected.username} selected.`);
        input.focus();
    };

    const loadSuggestions = async () => {
        const value = input.value.trim();
        if (!value.startsWith("@")) {
            closeList();
            return;
        }
        const currentRequest = ++requestId;
        setFeedback("Loading eligible clients...");
        try {
            const response = await fetch(
                `${form.dataset.suggestionsUrl}?q=${encodeURIComponent(value)}`,
                { headers: { Accept: "application/json" } }
            );
            if (!response.ok || currentRequest !== requestId) {
                throw new Error("Suggestions could not be loaded.");
            }
            const data = await response.json();
            renderOptions(data.results);
        } catch (error) {
            if (currentRequest !== requestId) {
                return;
            }
            closeList();
            setFeedback(error.message);
        }
    };

    input.addEventListener("input", () => {
        window.clearTimeout(timer);
        timer = window.setTimeout(loadSuggestions, 180);
    });

    input.addEventListener("keydown", (event) => {
        if (list.hidden) {
            if (event.key === "Escape") {
                closeList();
            }
            return;
        }
        if (event.key === "ArrowDown") {
            event.preventDefault();
            highlightOption((activeIndex + 1) % options.length);
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            highlightOption((activeIndex - 1 + options.length) % options.length);
        } else if (event.key === "Enter" && activeIndex >= 0) {
            event.preventDefault();
            selectOption(activeIndex);
        } else if (event.key === "Escape") {
            event.preventDefault();
            closeList();
        }
    });

    input.addEventListener("blur", () => {
        window.setTimeout(closeList, 150);
    });
})();
