const defVal = "Выбрать сортировку:";

(function ($) {
    "use strict";

    const body = document.querySelector("body");
    body.classList.add("body");

    const phoneBtn = document.querySelector(".phoneBtn");
    const burger = document.querySelector(".phoneBtn span");
    const phoneMenu = document.querySelector(".phoneMenu");
    let isOpen = false;

    phoneBtn.addEventListener("click", phoneHandler);

    function phoneHandler() {
        if (!isOpen) {
            phoneMenu.style.height = "320px";

            burger.classList.add("open");

            isOpen = true;
        } else if (isOpen) {
            phoneMenu.style.height = "0px";

            burger.classList.remove("open");

            isOpen = false;
        }
    }

    const sort_date = document.getElementById("sort_date");
    const sort_name = document.getElementById("sort_name");

    const filteredTextDate = document.getElementById("is_filter_on_date")?.value;
    const filteredTextName = document.getElementById("is_filter_on_alphabet")?.value;

    onChageForSelect(sort_date);
    onChageForSelect(sort_name);

    setValueForSelectWhenFiltered(sort_date, filteredTextDate);
    setValueForSelectWhenFiltered(sort_name, filteredTextName);

    checkIfWeHaveSelectedOptionAndBlockIt(sort_date, sort_name);
    DropFiltersF(sort_date, sort_name);

    BlockSelectForUseOneSelect(sort_date, sort_name);
    BlockSelectForUseOneSelect(sort_name, sort_date);

    $(function () {
        $("#scroll_bottom").click(function () {
            $("html, body").animate(
                {scrollTop: $(document).height() - $(window).height()},
                600
            );
            return false;
        });
    });

    let isOpenFilter = false;
    const filterContainer = $(".filterContainer");
    const btnShowFilt = $(".showFilter");

    btnShowFilt.on("click", (e) => {
        filterContainer.slideDown();
        btnShowFilt.text("Скрыть фильтры");
        btnShowFilt.removeClass("btn-success");
        btnShowFilt.addClass("btn-danger");

        if (isOpenFilter) {
            isOpenFilter = false;

            filterContainer.slideUp();
            btnShowFilt.text("Показать фильтры");

            btnShowFilt.addClass("btn-success");
            btnShowFilt.removeClass("btn-danger");
            return;
        }

        isOpenFilter = true;
    });
})($);

function onChageForSelect(elem) {
    const opts = elem?.querySelectorAll("option");
    if (elem)
        elem.addEventListener("change", (e) => {
            for (let i of opts) {
                if (i.innerText === e.target.value) {
                    i.setAttribute("selected", "selected");

                    break;
                } else {
                    i.removeAttribute("selected");
                }
            }
        });
}

function DropFiltersF(first, second) {
    const dropFilters = document.getElementById("dropFilters");
    const firstOptions = first.querySelectorAll("option");
    const secondOptions = second.querySelectorAll("option");

    dropFilters.addEventListener("click", (e) => {
        e.preventDefault();

        for (let i of firstOptions) {
            if (i.innerText === defVal) {
                i.setAttribute("selected", "selected");
            }

            i.removeAttribute("selected");
        }
        first.removeAttribute("disabled");

        for (let i of secondOptions) {
            if (i.innerText === defVal) {
                i.setAttribute("selected", "selected");
            }

            i.removeAttribute("selected");
        }
        second.removeAttribute("disabled");

        checkIfWeHaveSelectedOptionAndBlockIt(first, second);
    });
}

function checkIfWeHaveSelectedOptionAndBlockIt(first, second) {
    const val1 = first?.value;
    const val2 = second?.value;

    if (val1 !== defVal) {
        second.setAttribute("disabled", "disabled");
    } else {
        first.removeAttribute("disabled");
    }

    if (val2 !== defVal) {
        first.setAttribute("disabled", "disabled");
    } else {
        second.removeAttribute("disabled");
    }
}

function setValueForSelectWhenFiltered(select, filteredText) {
    const options = select?.querySelectorAll("option");

    if (options)
        for (let i of options) {
            if (i.textContent === filteredText) {
                i.setAttribute("selected", "selected");
                break;
            }
        }
}

function BlockSelectForUseOneSelect(usingSelect, blockingSelect) {
    if (!usingSelect && !blockingSelect) {
        throw new Error(`blockingSelect & usingSelect is not defined`);
    }

    usingSelect.addEventListener("click", (e) => {
        let val = e.target.value;
        let optionDef = usingSelect.querySelectorAll("option")[0];

        if (optionDef.textContent !== val) {
            blockingSelect.setAttribute("disabled", "disabled");
        } else if (optionDef.textContent === val) {
            blockingSelect.removeAttribute("disabled");
        }
    });
}

;(() => {
    const modals = [...document.querySelectorAll('.js-modal')];
    const modalsBtn = [...document.querySelectorAll('.js-modal-btn')];
    const closeModalsBtn = [...document.querySelectorAll('.js-close')];

    modals.map(modal => {
        modalsBtn.map(btn => {
            btn.addEventListener('click', () => {
                const btnModalIdx = btn.getAttribute("data-modal-num");
                const modalId = modal.id;

                if (+modalId === +btnModalIdx) {
                    toggleModal(modal)
                }
            })
        })

        document.addEventListener('click', (ev) => {
            if (ev.target.classList.contains('js-open')) {
                const modalId = modal.id;
                if (+modalId === +ev.target.id) {
                    toggleModal(modal)
                }
            }
        })

        closeModalsBtn.map(btn => {
            btn.addEventListener('click', () => {
                const modalId = modal.id;
                const btnModalIdx = btn.getAttribute("data-modal-num");

                if (+modalId === +btnModalIdx) {
                    toggleModal(modal)
                }
            })
        })
    })

    function toggleModal(modal) {
        const keyframes = [
            {opacity: 0},
            {opacity: 1},
        ]
        const isOpen = modal.classList.contains('js-open');
        modal.classList[!isOpen ? 'add' : 'remove']('js-open');

        modal.style.display = !isOpen ? 'flex' : 'none';

        modal.animate(!isOpen && keyframes || keyframes.reverse());
        modal.style.opacity = !isOpen ? '1' : '0';

        document.body.style.overflow = !isOpen ? 'hidden' : 'visible';
    }
})
();

;(function () {
    let funcToDown = () =>
        $("html, body").animate(
            {scrollTop: $(document).height() - 900},
            300
        );

    let href = location.href;
    if (href) {
        let query = href?.split("?")[1]?.split("=") || [];
        let isNeedToGoDown = query.length
            ? (() => {
                let done = query.find((i) => i === "addComposition");

                return done === "addComposition";
            })()
            : false;

        if (isNeedToGoDown) {
            funcToDown();
        }
    }
})();
