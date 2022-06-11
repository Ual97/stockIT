Dynamsoft.DBR.BarcodeReader.license = 'DLS2eyJoYW5kc2hha2VDb2RlIjoiMTAxMTI4MTMxLVRYbFhaV0pRY205cSIsIm9yZ2FuaXphdGlvbklEIjoiMTAxMTI4MTMxIn0=';
let scanner = null;
async function scannerF () {
  scanner = await Dynamsoft.DBR.BarcodeScanner.createInstance();
  scanner.onFrameRead = results => { 
    if (results) {
      const data = await (await fetch(`/inventory/${results.barcodeText}`)).json()
      if (!data)
        () => {
          let flag;
          if (confirm("The code is not registred")) {
            flag = 1;
          } else {
            flag = null;
          }
          if (!flag) {
            scanner.hide()
          }
      }
    }
  
  };
  scanner.onUnduplicatedRead = (txt, result) => { };
  await scanner.show();
};