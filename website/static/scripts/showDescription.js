function showDescription(obj) {

    description = obj.getAttribute("value");
    console.log(description);
    descriptionDiv = document.querySelector("#InvisibleDescription");
    descriptionDiv.classList.replace("Invisible", "description");
    textNode = document.querySelector('#productDescriptionText');
    textNode.innerHTML = description;
    function close() {
        document.querySelector("#InvisibleDescription").classList.replace("description", "Invisible");
        textNode.innerHTML = "";
    }
    const closeButton = document.querySelector("#closeProductDescription");
    closeButton.addEventListener("click", close);
}