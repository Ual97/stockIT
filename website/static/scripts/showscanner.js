async function consult(code_content) {
  if (!isNaN(code_content)) {
    const data = await (await fetch(`/inventory/${code_content}`)).json();
    document.getElementsByClassName('InvisibleBarcode')[0].classList.replace('InvisibleBarcode', 'barcode')
    id = document.querySelector('#idBarcode');
    id.appendChild(document.createTextNode(data.id));
    code_name = document.querySelector('#nameBarcode');
    code_name.appendChild(document.createTextNode(data.name));
    code_branch = document.querySelector('#branchBarcode');
    code_branch.appendChild(document.createTextNode(data.branch));
    code_quantity = document.querySelector('#quantityBarcode');
    code_quantity.appendChild(document.createTextNode(data.quantity));
    code_cost = document.querySelector('#costBarcode');
    code_cost.appendChild(document.createTextNode(data.cost));
    code_price = document.querySelector('#priceBarcode');
    code_price.appendChild(document.createTextNode(data.price));
    code_expiry = document.querySelector('#expiryBarcode');
    code_expiry.appendChild(document.createTextNode(data.expiry));
    code_reserved = document.querySelector('#qty_reservedBarcode');
    code_reserved.appendChild(document.createTextNode(data.qty_reserved));
    document.querySelector('#qr_barcodeBarcode').setAttribute('src', `../images/${data.id}.png`);
    function cancel() {
      document.querySelector('.barcode').classList.replace('barcode', 'InvisibleBarcode')
      id.innerHTML = "";
      code_name.innerHTML = "";
      code_branch.innerHTML = "";
      code_quantity.innerHTML = "";
      code_cost.innerHTML = "";
      code_price.innerHTML = "";
      code_expiry.innerHTML = "";
      code_reserved.innerHTML = "";
    }
    const cancelButton = document.querySelector("#cancelButtonBarcode")
    cancelButton.addEventListener("click", cancel);
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
