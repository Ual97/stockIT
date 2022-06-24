async function consult(code_content) {
  if (code_content) {
    const data = await (await fetch(`/inventory/${code_content}`)).json()
    console.log(data);
    console.log(code_content);

    const updclass = document.querySelector('.InvisibleBarcode');
    console.log(updclass);
    updclass.setAttribute('class', '');


    tableName = document.querySelector('#nameBarcode');
    tableName.appendChild(document.createTextNode(data.name));
    const tableQuantity = document.querySelector('#quantityBarcode');
    tableQuantity.appendChild(document.createTextNode(data.quantity));
    const tableDescription = document.querySelector('#descriptionBarcode');
    tableDescription.appendChild(document.createTextNode('Show Description'));
    tableDescription.setAttribute('value', data.description); 
    document.querySelector('#qr_barcodeBarcode').setAttribute('src', `/ static/images/${data.qr_barcode}.${code_content}.png`);

    //exitButton = document.querySelector('#updateButtonBarcode');

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
      consult(code_content);
      scanner.hide();
    }

  };
  scanner.onUnduplicatedRead = (txt, result) => { };
  await scanner.show();
};
