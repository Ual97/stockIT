async function consult(code_content, path) {
  if (code_content) {
    const data = await (await fetch(`/${path}/${code_content}`)).json()
    console.log(data);
    console.log(code_content);

    if (path === 'inventory') {

      $('#InvisibleBarcode').modal('show');
      tableName = document.querySelector('#nameBarcode');
      tableName.appendChild(document.createTextNode(data.name));
      const tableQuantity = document.querySelector('#quantityBarcode');
      tableQuantity.appendChild(document.createTextNode(data.quantity));
      const tableDescription = document.querySelector('#descriptionBarcode');
      tableDescription.appendChild(document.createTextNode(data.description));
      document.querySelector('#qr_barcodeBarcode').setAttribute('src', `/static/images/${data.qr_barcode}.${code_content}.png`);
    }
    else if (path === 'profits') {
      const updclass = document.querySelector('.InvisibleBarcode');
      console.log(updclass);
      updclass.setAttribute('class', '');

      const tr = document.querySelector("#trBarcode");

      for (item of data) {
        tdName = document.createElement('td');
        tdName.appendChild(document.createTextNode(item.name));
        tr.appendChild(tdName);
        tdProfit = document.createElement('td');
        tdProfit.appendChild(document.createTextNode(item.profit));
        tr.appendChild(tdProfit);
        tdQuantity = document.createElement('td');
        tdQuantity.appendChild(document.createTextNode(item.quantity));
        tr.appendChild(tdQuantity);
        tdBranch = document.createElement('td');
        tdBranch.appendChild(document.createTextNode(item.branch));
        tr.appendChild(tdBranch);
        tdDate = document.createElement('td');
        tdDate.appendChild(document.createTextNode(item.date));
        tr.appendChild(tdDate);
        tdDescription = document.createElement('td');
        tdDescription.appendChild(document.createTextNode("show description"));
        tdDescription.setAttribute("value", item.description)
        tr.appendChild(tdDescription);
        tdDescription = document.createElement('img');
        tdDescription.setAttribute("src", `/static/images/${item.qr_barcode}.${code_content}.png`)
        tr.appendChild(tdDescription);
      }

    } 
    else {
      document.querySelector('#nameBarcode').value = data.name;
      branches = document.querySelector('#branchBarcode');
      for (branch of data.branches) {
        option = document.createElement('option');
        option.setAttribute('value', branch);
        branches.appendChild(option)
      }
      
    }
    
  }
  else {
    alert("Code is not registered")
  }
}

Dynamsoft.DBR.BarcodeReader.license = 'DLS2eyJoYW5kc2hha2VDb2RlIjoiMTAxMTI4MTMxLVRYbFhaV0pRY205cSIsIm9yZ2FuaXphdGlvbklEIjoiMTAxMTI4MTMxIn0=';
let scanner = null;
async function scannerF(obj) {
  scanner = await Dynamsoft.DBR.BarcodeScanner.createInstance();
  scanner.onFrameRead = results => {
    if (results[0]) {
      const code_content = results[0].barcodeText;
      consult(code_content, obj.id);
      scanner.hide();
    }

  };
  scanner.onUnduplicatedRead = (txt, result) => { };
  await scanner.show();
};
