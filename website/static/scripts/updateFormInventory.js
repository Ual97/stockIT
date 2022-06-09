window.addEventListener('load', function() {
  const elements = document.getElementsByClassName('updateButton');
  for (let element of elements) {
    element.addEventListener('click', async function () { //asyc function which allows make await returns
      document.querySelector('.Invisible').classList.replace('Invisible', 'update');
      // await in fetch return which with wait to conclude the request to then return the json obj
      const data = await (await fetch(`/inventory/${element.id}`)).json()
      // filling form with corresponding item data:
      document.querySelector("#updateForm").setAttribute("action", `/inventory/${element.id}`);
      const id = document.querySelector("#idUpdate");
      id.appendChild(document.createTextNode(data.id));
      document.querySelector("#nameUpdate").setAttribute("value", data.name);
      const branches = document.querySelector("#branchesUpdate");
      for (let i = 0; data.ownerBranches[i]; i++) {
        const option = document.createElement("option");
        option.setAttribute("value", data.ownerBranches[i]);
        option.appendChild(document.createTextNode(data.ownerBranches[i]));
        option.setAttribute("value", data.ownerBranches[i]);
        if (data.ownerBranches[i] === data.branch) {
          option.setAttribute("selected", "selected");
        }
        branches.appendChild(option);
      }
      document.querySelector("#quantityUpdate").setAttribute("value", data.quantity);
      document.querySelector("#costUpdate").setAttribute("value", data.cost);
      document.querySelector("#priceUpdate").setAttribute("value", data.price);
      document.querySelector("#expiryUpdate").setAttribute("value", data.expiry);
      document.querySelector("#qty_reservedUpdate").setAttribute("value", data.qty_reserved);
      document.querySelector("#qr_barcodeUpdate").setAttribute("value", data.qr_barcode);
      function cancel() {
        document.querySelector('.update').classList.replace('update', 'Invisible')
        branches.innerHTML = "";
        id.innerHTML = "";
      }
      const cancelButton = document.querySelector("#cancelButtonUpdate")
      cancelButton.addEventListener("click", cancel);
    });
  };
});