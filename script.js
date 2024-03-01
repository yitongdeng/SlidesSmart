function populate_text(jsonObj, textbox) {
  let concatenatedString = '';

  jsonObj.forEach(obj => {
    Object.keys(obj).forEach(key => {
      if (key === 'word' && typeof obj[key] === 'string') {
          // If the key matches and its value is a string, concatenate it
          concatenatedString += obj[key] + ' '; // Adding a space for separation
      }
    });
    
  });

  // Return the concatenated string, trimming any trailing space
  textbox.innerHTML = concatenatedString.trim();
}

function populate_table(jsonObj, table) {
  let idx = 0;
  jsonObj.forEach(obj => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>
        #${idx}
        </td>
        <td>
        ${obj["words"]}
        </td>
        <td>
        ${Math.round(obj["start"]*1000)/1000}
        </td>
        <td>
        ${Math.round(obj["end"]*1000)/1000}
        </td>`;
        // You could also do the same for the cells and inputs
        table.appendChild(row);
        idx += 1;
  });
    
  }

fetch("http://192.168.50.97:8080/words.json")
  .then(response => response.json())
  .then(data => {
    obj = populate_text(data, document.getElementById('transcribed_paragraph'));
   });

fetch("http://192.168.50.97:8080/segments_processed.json")
   .then(response => response.json())
   .then(data => {
     obj = populate_table(data, document.getElementById('registerTable'));
    });

  // const table = document.getElementById('registerTable');
  // const row = document.createElement('tr');
  // row.innerHTML = `
  // <td>
  // #${1}
  // </td>
  // <td>
  // ${2}
  // </td>
  // <td>
  // (${3}, ${4})
  // </td>`;
  // // You could also do the same for the cells and inputs
  // table.appendChild(row);

// // const result = extractAndConcatenateWords(obj);
// console.log(obj.count); // Output: "Hello World Foo Bar End