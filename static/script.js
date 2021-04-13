const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const account = document.querySelector(".account_select");

const optionsList = document.querySelectorAll(".option");


selected.addEventListener("click", () => {
    optionsContainer.classList.toggle("active");
    document.getElementById('select').style.cssText = 'box-shadow: 0 0 12px #AAAAAA;';

});

optionsList.forEach(o => {

    o.addEventListener("click", () => {
        selected.innerHTML = o.querySelector("label").innerHTML;
        optionsContainer.classList.remove("active");
        document.getElementById('select').style.cssText = 'box-shadow: none';
    });

});

account.addEventListener("click", () => {

    document.getElementById('account').style.cssText = 'opacity: 1';

})

navigation.addEventListener("click", () => {

    navigation_block.classList.toggle("nav-active");
});

const navSlide = () => {

    const navigation = document.querySelector(".navigator-small");
    const navigation_block = document.querySelector(".navigator_second");

    navigation.addEventListener('click', () => {
        window.alert("clicked");

    });


};

var nav = document.getElementById('navigate');

function navigation() {

    const navigation_block = document.querySelector(".navigator_second");

    navigation_block.classList.toggle('nav-active');

}

function accountToggle() {

    let button = document.getElementById("account_button");

    let toggleStatus = button.dataset.status;

    const account = document.querySelector(".account");

    account.classList.toggle('active');
 
    switch (toggleStatus) {
        case "on":
            button.dataset.status = "off";
            button.style.color = "#c44e00";
            break;
        case "off":
            button.dataset.status = "on";
            button.style.color = "#FFFFFF";
            break;
    }
}






nav.onclick = function () {

    window.alert("clicked");
};

function validateCandidateForm() {

    var first_name = document.forms["candidate_form"]["first"].value;
    if (first_name == "") {
        alert("Name must be filled out");
        return false;
    }

    return true

}