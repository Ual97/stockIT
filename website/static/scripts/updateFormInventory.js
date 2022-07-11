window.addEventListener('load', function () {
  const elements = document.getElementsByClassName('updateButton');
  for (let element of elements) {
    element.addEventListener('click', async function () { //asyc function which allows make await returns
      $('#InvisibleProduct').modal('show');
      // await in fetch return which with wait to conclude the request to then return the json obj
      console.log(`\n\nel clickeado${element.id}\n`)
      const data = await (await fetch(`/product/${element.id}`)).json()
      // filling form with corresponding item data:
      console.log(`\n\ndiccionario\n`)
      console.log(data)
      document.querySelector("#updateForm").setAttribute("action", `/product/${element.id}`);
      nameTxt = document.querySelector("#nameUpdate");

      console.log("khe loceee")
      if (nameTxt.firstChild){
        console.log(nameTxt.firstChild.length)
      }
      console.log("bolas")
      console.log(data.name)
      if (nameTxt.firstChild) {
        nameTxt.removeChild(nameTxt.firstChild)
      }
      nameTxt.appendChild(document.createTextNode(data.name));
      console.log(nameTxt)
      console.log(`adasdasd${data.description}`);
      document.querySelector(`#qr_barcodeUpdate${data.qr_barcode}`).setAttribute("selected", 'selected');
      document.querySelector("#descriptionUpdate").setAttribute("value", data.description);
    });
  };
});