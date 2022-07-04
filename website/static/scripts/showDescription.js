function showDescription(obj) {

    const description = obj.getAttribute("value");
    console.log(description);
    descriptionDiv = document.querySelector("#InvisibleDescription");
    const idTag = obj.getAttribute("id");
    if (idTag !== "descriptionBarcode")
    {    
        descriptionDiv.classList.replace("Invisible", "description");
    }
    else
    {
        descriptionDiv.setAttribute("class", "");
    }
    textNode = document.querySelector('#productDescriptionText');
    textNode.innerHTML = description;
    function close() {
        if (idTag !== "descriptionBarcode")
    {    
        document.querySelector("#InvisibleDescription").classList.replace("description", "Invisible");
    }
    else
    {
        descriptionDiv.setAttribute("class", "InvisibleDescription");
    }
    
        textNode.innerHTML = "";
    }
    const closeButton = document.querySelector("#closeProductDescription");
    closeButton.addEventListener("click", close);
}