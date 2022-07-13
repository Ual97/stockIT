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
    }
    else if (path === 'profits') {
      $('#InvisibleBarcode').modal('show');
      const table = document.querySelector('#tableBarcode');
      for (item of data) {
        const tr = document.createElement('tr');
        tr.setAttribute('id', 'trBarcode')
        const td_name = document.createElement('td');
        td_name.appendChild(document.createTextNode(item.name));
        tr.appendChild(td_name);
        const td_profit = document.createElement('td');
        td_profit.appendChild(document.createTextNode(item.profit));
        tr.appendChild(td_profit);
        const td_quantity = document.createElement('td');
        td_quantity.appendChild(document.createTextNode(item.quantity));
        tr.appendChild(td_quantity);
        const td_branch = document.createElement('td');
        td_branch.appendChild(document.createTextNode(item.branch));
        tr.appendChild(td_branch);
        const td_date = document.createElement('td');
        td_date.appendChild(document.createTextNode(item.date));
        tr.appendChild(td_date);
        const td_description = document.createElement('td');
        td_description.appendChild(document.createTextNode(item.description));
        tr.appendChild(td_description);
        table.appendChild(tr);
      }
    } 
    else {
      $('#InvisibleBarcode').modal('show');
      const name = document.querySelector('#nameBarcode');
      if (name.firstChild) {
        name.removeChild(name.firstChild)
      }
      name.value = data.name;
      name.appendChild(document.createTextNode(data.name));
      branches = document.querySelector('#branchBarcode');
      for (branch of data.branches) {
        option = document.createElement('option');
        option.setAttribute('value', branch);
        option.appendChild(document.createTextNode(branch))
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
