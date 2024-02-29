function extractAndConcatenateWords(jsonObj) {
  let concatenatedString = '';

  function traverseAndCollectWords(obj) {
      if (Array.isArray(obj)) {
          // If it's an array, iterate through its elements
          obj.forEach(element => {
              traverseAndCollectWords(element);
          });
      } else if (typeof obj === 'object' && obj !== null) {
          // If it's an object, iterate through its properties
          Object.keys(obj).forEach(key => {
              if (key === 'word' && typeof obj[key] === 'string') {
                  // If the key matches and its value is a string, concatenate it
                  concatenatedString += obj[key] + ' '; // Adding a space for separation
              } else {
                  // Otherwise, continue traversing
                  traverseAndCollectWords(obj[key]);
              }
          });
      }
  }

  // Start traversing the JSON object
  traverseAndCollectWords(jsonObj);

  // Return the concatenated string, trimming any trailing space
  return concatenatedString.trim();
}

function populate(jsonObj) {
  let concatenatedString = '';

  function traverseAndCollectWords(obj) {
      if (Array.isArray(obj)) {
          // If it's an array, iterate through its elements
          obj.forEach(element => {
              traverseAndCollectWords(element);
          });
      } else if (typeof obj === 'object' && obj !== null) {
          // If it's an object, iterate through its properties
          Object.keys(obj).forEach(key => {
              if (key === 'word' && typeof obj[key] === 'string') {
                  // If the key matches and its value is a string, concatenate it
                  concatenatedString += obj[key] + ' '; // Adding a space for separation
              } else {
                  // Otherwise, continue traversing
                  traverseAndCollectWords(obj[key]);
              }
          });
      }
  }

  // Start traversing the JSON object
  traverseAndCollectWords(jsonObj);

  // Return the concatenated string, trimming any trailing space
  return concatenatedString.trim();
}

fetch("http://192.168.50.97:8080/words.json")
  .then(response => response.json())
  .then(data => {
    obj = extractAndConcatenateWords(data);
    document.getElementById('transcribed_paragraph').innerHTML = obj;
   });

  const table = document.getElementById('registerTable');
  const row = document.createElement('tr');
  row.innerHTML = `
  <td>
  #${1}
  </td>
  <td>
  ${2}
  </td>
  <td>
  (${3}, ${4})
  </td>`;
  // You could also do the same for the cells and inputs
  table.appendChild(row);

// // const result = extractAndConcatenateWords(obj);
// console.log(obj.count); // Output: "Hello World Foo Bar End