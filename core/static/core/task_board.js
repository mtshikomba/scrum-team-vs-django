(() => {
    const csrfToken = document.cookie
        .split(";")
        .map((cookie) => cookie.trim())
        .find((cookie) => cookie.startsWith("csrftoken="))
        ?.split("=")[1];

    const setFeedback = (section, message, isError = false) => {
        const feedback = section.querySelector("[data-task-feedback]");
        feedback.textContent = message;
        feedback.classList.toggle("task-feedback--error", isError);
    };

    const updateLaneCount = (lane) => {
        const count = lane.querySelector(".task-count");
        const tasks = lane.querySelectorAll("[data-task-card]").length;
        count.textContent = `${tasks} task${tasks === 1 ? "" : "s"}`;
    };

    const updateLaneEmptyState = (lane) => {
        const hasTasks = lane.querySelectorAll("[data-task-card]").length > 0;
        const emptyState = lane.querySelector("[data-lane-empty]");
        if (hasTasks) {
            emptyState?.remove();
        } else if (!emptyState) {
            lane.insertAdjacentHTML(
                "afterbegin",
                '<p class="task-lane__empty" data-lane-empty>No tasks here yet.</p>'
            );
        }
    };

    const moveCard = async (card, targetLane, select, section) => {
        const previousLane = card.closest(".task-lane__dropzone");
        const previousStatus = card.dataset.status;
        const nextStatus = targetLane.dataset.status;
        if (previousStatus === nextStatus) {
            select.value = previousStatus;
            return;
        }

        select.disabled = true;
        card.classList.add("task-card--pending");
        setFeedback(section, "Saving task status...");
        try {
            const response = await fetch(select.dataset.statusUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken,
                },
                body: new URLSearchParams({ status: nextStatus }),
            });
            if (!response.ok) {
                throw new Error("The task status could not be saved.");
            }
            const result = await response.json();
            card.dataset.status = result.status;
            select.dataset.currentStatus = result.status;
            select.value = result.status;
            targetLane.appendChild(card);
            updateLaneCount(previousLane.closest(".task-lane"));
            updateLaneCount(targetLane.closest(".task-lane"));
            updateLaneEmptyState(previousLane);
            updateLaneEmptyState(targetLane);
            card.classList.remove("task-card--pending");
            setFeedback(section, `Task moved to ${result.label}.`);
        } catch (error) {
            select.value = previousStatus;
            card.classList.remove("task-card--pending");
            setFeedback(section, error.message, true);
        } finally {
            select.disabled = false;
        }
    };

    document.querySelectorAll(".task-section").forEach((section) => {
        section.addEventListener("click", (event) => {
            const toggle = event.target.closest("[data-task-view]");
            if (!toggle) {
                return;
            }
            const selectedView = toggle.dataset.taskView;
            section.querySelectorAll("[data-task-view]").forEach((button) => {
                const isSelected = button.dataset.taskView === selectedView;
                button.classList.toggle("is-selected", isSelected);
                button.setAttribute("aria-pressed", String(isSelected));
            });
            section.querySelectorAll("[data-task-view-panel]").forEach((panel) => {
                panel.hidden = panel.dataset.taskViewPanel !== selectedView;
            });
            setFeedback(section, `${selectedView === "lanes" ? "Lanes" : "List"} view selected.`);
        });

        section.addEventListener("change", (event) => {
            const select = event.target.closest("[data-task-move]");
            if (!select) {
                return;
            }
            const card = select.closest("[data-task-card]");
            const targetLane = section.querySelector(
                `.task-lane__dropzone[data-status="${select.value}"]`
            );
            moveCard(card, targetLane, select, section);
        });

        section.addEventListener("dragstart", (event) => {
            const card = event.target.closest("[data-task-card]");
            if (card) {
                event.dataTransfer.setData("text/task-id", card.dataset.taskId);
                card.classList.add("task-card--dragging");
            }
        });

        section.addEventListener("dragend", (event) => {
            event.target.closest("[data-task-card]")?.classList.remove("task-card--dragging");
        });

        section.querySelectorAll(".task-lane__dropzone").forEach((lane) => {
            lane.addEventListener("dragover", (event) => {
                event.preventDefault();
                lane.classList.add("task-lane__dropzone--active");
            });
            lane.addEventListener("dragleave", () => {
                lane.classList.remove("task-lane__dropzone--active");
            });
            lane.addEventListener("drop", (event) => {
                event.preventDefault();
                lane.classList.remove("task-lane__dropzone--active");
                const card = section.querySelector(
                    `[data-task-card][data-task-id="${event.dataTransfer.getData("text/task-id")}"]`
                );
                if (card) {
                    moveCard(card, lane, card.querySelector("[data-task-move]"), section);
                }
            });
        });
    });
})();
