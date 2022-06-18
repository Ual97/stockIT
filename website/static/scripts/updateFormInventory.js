window.addEventListener('load', function () {
  const elements = document.getElementsByClassName('updateButton');
  for (let element of elements) {
    element.addEventListener('click', async function () { //asyc function which allows make await returns
      document.querySelector('.Invisible').classList.replace('Invisible', 'update');
      // await in fetch return which with wait to conclude the request to then return the json obj
      const data = await (await fetch(`/product/${element.id}`)).json()
      // filling form with corresponding item data:
      document.querySelector("#updateForm").setAttribute("action", `/product/${element.id}`);
      const id = document.querySelector("#idUpdate");
      id.appendChild(document.createTextNode(data.id));
      nameTxt = document.querySelector("#nameUpdate");
      nameTxt.appendChild(document.createTextNode(data.name));
      document.querySelector(`#qr_barcodeUpdate${data.qr_barcode}`).setAttribute("selected", 'selected');
      document.querySelector("#descrptionUpdate").setAttribute("value", data.description);
      function cancel() {
        document.querySelector('.update').classList.replace('update', 'Invisible')
        id.innerHTML = "";
      }
      const cancelButton = document.querySelector("#cancelButtonUpdate")
      cancelButton.addEventListener("click", cancel);
    });
  };
});