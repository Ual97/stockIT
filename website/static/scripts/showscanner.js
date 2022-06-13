Dynamsoft.DBR.BarcodeReader.license = 'DLS2eyJoYW5kc2hha2VDb2RlIjoiMTAxMTI4MTMxLVRYbFhaV0pRY205cSIsIm9yZ2FuaXphdGlvbklEIjoiMTAxMTI4MTMxIn0=';
let scanner = null;
async function scannerF () {
  scanner = await Dynamsoft.DBR.BarcodeScanner.createInstance();
  scanner.onFrameRead = results => { 
    if (results) {
      const data = await (await fetch(`/inventory/${results.barcodeText}`)).json();
      if (!data)
        () => {
          let flag;
          if (confirm("The code is not registred")) {
            flag = 1;
          } else {
            flag = null;
          }
          if (!flag) {
            scanner.hide();
          }
      }
      else {
        id = document.querySelector('#idBarcode');
        id.appendChild(document.createTextNode(data.id));
        document.querySelector('#nameBarcode').setAttribute('value', data.name);
        document.querySelector('#branchBarcode').setAttribute('value', data.branch);
        document.querySelector('#quantityBarcode').setAttribute('value', data.quantity);
        document.querySelector('#costBarcode').setAttribute('value', data.cost);
        document.querySelector('#priceBarcode').setAttribute('value', data.price);
        document.querySelector('#expiryBarcode').setAttribute('value', data.expiry);
        document.querySelector('#qty_reservedBarcode').setAttribute('value', data.qty_reserved);
        document.querySelector('#qr_barcodeBarcode').setAttribute('value', data.qr_barcode);
      }
    }
  
  };
  scanner.onUnduplicatedRead = (txt, result) => { };
  await scanner.show();
};