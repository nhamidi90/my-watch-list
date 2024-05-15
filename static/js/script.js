document.addEventListener('DOMContentLoaded', function() {

    // navbar 
    let navbar = document.querySelectorAll('.sidenav');
    M.Sidenav.init(navbar);

    // Dropdown menu 
    let dropdown = document.querySelectorAll('select');
    M.FormSelect.init(dropdown);

    // status dropdown 
    let drop = document.querySelectorAll('.dropdown-trigger');
    M.Dropdown.init(drop);

    // Modal
    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);

    // Carousel
    let carousel = document.querySelectorAll('.carousel');
    M.Carousel.init(carousel);

    // Star rating 
    let star = document.querySelectorAll('input.star');
    let showValue = document.querySelector('#rating-value');

    for (let i = 0; i < star.length; i++) {
	    star[i].addEventListener('click', function() {
		    i = this.value;

		showValue.innerHTML = i + " out of 10";
	});
    
    // Custom materialize validation 
    validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = "border-bottom: 1px solid #4caf50; box-shadow: 0 1px 0 0 #4caf50;";
        let classInvalid = "border-bottom: 1px solid #f44336; box-shadow: 0 1px 0 0 #f44336;";
        let selectValidate = document.querySelector("select.validate");
        let selectWrapperInput = document.querySelector(".select-wrapper input.select-dropdown");
        if (selectValidate.hasAttribute("required")) {
            selectValidate.style.cssText = "display: block; height: 0; padding: 0; width: 0; position: absolute;";
        }
        selectWrapperInput.addEventListener("focusin", (e) => {
            e.target.parentNode.addEventListener("change", () => {
                ulSelectOptions = e.target.parentNode.childNodes[1].childNodes;
                for (let i = 0; i < ulSelectOptions.length; i++) {
                    if (ulSelectOptions[i].className == "selected" && ulSelectOptions[i].hasAttribute != "disabled") {
                        e.target.style.cssText = classValid;
                    }
                }
            });
        });
        
        selectWrapperInput.addEventListener("click", (e) => {
            ulSelectOptions = e.target.parentNode.childNodes[1].childNodes;
            for (let i = 0; i < ulSelectOptions.length; i++) {
                if (ulSelectOptions[i].className == "selected" && ulSelectOptions[i].hasAttribute != "disabled" && ulSelectOptions[i].style.backgroundColor == "rgba(0, 0, 0, 0.03)") {
                    e.target.style.cssText = classValid;
                } else {
                    e.target.addEventListener("focusout", () => {
                        if (e.target.parentNode.childNodes[3].hasAttribute("required")) {
                            if (e.target.style.borderBottom != "1px solid rgb(76, 175, 80)") {
                                e.target.style.cssText = classInvalid;
                            }
                        }
                    });
                }
            }
        });
    }
}

    // Show/hide drama tables 
    allShows = document.getElementById("all-shows")
    planToWatch = document.getElementById("plan-to-watch")
    currentlyWatching = document.getElementById("currently-watching")
    completed = document.getElementById("completed")
    dropped = document.getElementById("dropped")

    menuAll = document.getElementById("menu-all").addEventListener("click", showAllShows)
    menuPlanToWatch = document.getElementById("menu-plan-to-watch").addEventListener("click", showPlanToWatch)
    menuCurrentlyWatching = document.getElementById("menu-currently-watching").addEventListener("click", showCurrentlyWatching)
    menuCompleted = document.getElementById("menu-completed").addEventListener("click", completedDramas)
    menuDropped = document.getElementById("menu-dropped").addEventListener("click", showDropped)

    function showAllShows() {
        allShows.classList.remove('nodisplay')
        planToWatch.classList.add('nodisplay')
        currentlyWatching.classList.add('nodisplay')
        completed.classList.add('nodisplay')
        dropped.classList.add('nodisplay')
    }

    function showPlanToWatch() {
        allShows.classList.add('nodisplay')
        planToWatch.classList.remove('nodisplay')
        currentlyWatching.classList.add('nodisplay')
        completed.classList.add('nodisplay')
        dropped.classList.add('nodisplay')
    }

    function showCurrentlyWatching() {
        allShows.classList.add('nodisplay')
        planToWatch.classList.add('nodisplay')
        currentlyWatching.classList.remove('nodisplay')
        completed.classList.add('nodisplay')
        dropped.classList.add('nodisplay')
    }

    function completedDramas() {
        allShows.classList.add('nodisplay')
        planToWatch.classList.add('nodisplay')
        currentlyWatching.classList.add('nodisplay')
        completed.classList.remove('nodisplay')
        dropped.classList.add('nodisplay')
    }

    function showDropped() {
        allShows.classList.add('nodisplay')
        planToWatch.classList.add('nodisplay')
        currentlyWatching.classList.add('nodisplay')
        completed.classList.add('nodisplay')
        dropped.classList.remove('nodisplay')
    }
//     let status = document.getElementById('status');
//     let episodesWatched = document.getElementById('number-of-eps');
//     status.addEventListener('click', showElement);

// function showElement(status, episodesWatched){
//         if (status.value === "Currently Watching") {
//             revealElement(episodesWatched);
//         }
//     }

//     function revealElement(episodesWatched) {
//         episodesWatched.classList.remove("nodisplay")
//     }

});

