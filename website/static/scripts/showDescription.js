function showDescription(obj) {

    const description = obj.getAttribute("value");
    console.log(description);
    const idTag = obj.getAttribute("id");
    textNode = document.querySelector('#productDescriptionText');
    textNode.innerHTML = description;
    function close() {
        textNode.innerHTML = "";
    }
}