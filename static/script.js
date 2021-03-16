const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");

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

nav.onclick = function () {

    window.alert("clicked");
};