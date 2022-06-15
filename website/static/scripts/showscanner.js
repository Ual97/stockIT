async function consult(code_content) {
  if (!isNaN(code_content)) {
    const data = await (await fetch(`/inventory/${code_content}`)).json()    
    console.log(data);
    console.log(code_content);
    
    document.querySelector('.InvisibleBarcode').setAttribute('class', 'barcode');    
    

    tableName = document.querySelector('#nameBarcode');
    tableName.appendChild(document.createTextNode(data.name));
    tableBranch = document.querySelector('#branchBarcode');
    tableBranch.appendChild(document.createTextNode(data.branch));
    tableQuantity = document.querySelector('#quantityBarcode');
    tableQuantity.appendChild(document.createTextNode(data.quantity));
    tableCost = document.querySelector('#costBarcode');
    if (data.cost) {
      const textCost = document.createTextNode(data.cost);
      tableCost.appendChild(textCost);
    }
    tablePrice = document.querySelector('#priceBarcode');
    if (data.price) {
      const textPrice = document.createTextNode(data.price);
      tablePrice.appendChild(textPrice);
    }
    tableExpiry = document.querySelector('#expiricy');
    if (data.expiry) {
      const textExpiry = document.createTextNode(data.expiry);
      tableExpiry.appendChild(textExpiry);
    }
    tableQty = document.querySelector('#qty_reservedBarcode');
    if (data.qty_reserved) {
      const textQty = document.createTextNode(data.qty_reserved);
      tableQty.appendChild(textQty);
    }
    document.querySelector('#qr_barcodeUpdate').setAttribute('src', `/static/images/${code_content}.png`);

    updateButton = document.querySelector('#updateButtonBarcode');
    updateButton.addEventListener('click', function () {

      document.querySelector('#tableBarcode').setAttribute('class', 'Invisible');
      document.querySelector('#tableBarcodeUpdate').setAttribute('class', '');

      // filling form with corresponding item data:
      document.querySelector("#updateFormBarcode").setAttribute("action", `/inventory/${code_content}`);
      const id = document.querySelector("#idUpdate");
      id.appendChild(document.createTextNode(data.id));
      document.querySelector("#nameBarcodeUpdate").setAttribute("value", data.name);
      const branches = document.querySelector("#branchesBarcodeUpdate");
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
      document.querySelector("#quantityBarcodeUpdate").setAttribute("value", data.quantity);
      document.querySelector("#costBarcodeUpdate").setAttribute("value", data.cost);
      document.querySelector("#priceBarcodeUpdate").setAttribute("value", data.price);
      document.querySelector("#expiryBarcodeUpdate").setAttribute("value", data.expiry);
      document.querySelector("#qty_reservedBarcodeUpdate").setAttribute("value", data.qty_reserved);
      document.querySelector(`#qr_barcodeBarcodeUpdate${data.qr_barcode}`).setAttribute("selected", 'selected');
      function cancel() {
        document.querySelector('#tableBarcodeUpdate').setAttribute('class', 'Invisible')
        branches.innerHTML = "";
        id.innerHTML = "";
      }
      const cancelButton = document.querySelector("#cancelButtonUpdate")
      cancelButton.addEventListener("click", cancel);

      

    });
  }
  else {
    alert("Code is not registered")
  }
}

Dynamsoft.DBR.BarcodeReader.license = 'DLS2eyJoYW5kc2hha2VDb2RlIjoiMTAxMTI4MTMxLVRYbFhaV0pRY205cSIsIm9yZ2FuaXphdGlvbklEIjoiMTAxMTI4MTMxIn0=';
let scanner = null;
async function scannerF() {
  scanner = await Dynamsoft.DBR.BarcodeScanner.createInstance();
  scanner.onFrameRead = results => {
    if (results[0]) {
      const code_content = results[0].barcodeText;
      console.log(code_content)
      consult(code_content);
      scanner.hide();
    }

  };
  scanner.onUnduplicatedRead = (txt, result) => { };
  await scanner.show();
};
