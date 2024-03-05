let example_name;

function submit(input) {
  fetch(`http://127.0.0.1:8080/${input}/segments_processed.json`)
   .then(response => response.json())
   .then(data => {
     obj = populate_table(data, document.getElementById('registerTable'));
    });

  fetch(`http://127.0.0.1:8080/${input}/captions.json`)
    .then(response => response.json())
    .then(data => {
      obj = populate_caption_table(data, document.getElementById('captionTable'), input);
     });

  fetch(`http://127.0.0.1:8080/${input}/segments_processed.json`)
     .then(response => response.json())
     .then(data => {
       obj = populate_match_table_1(data, document.getElementById('matchTable'));
      });
  
  populate_match_table_2()

  var container = document.getElementById("finalVideoWrapper");
  container.innerHTML = "";
  var video = document.createElement('video');
  video.src = `http://127.0.0.1:8080/${input}/image_video.mp4`;
  video.width = 1000;
  video.setAttribute("controls","controls")
  container.appendChild(video);
  video.style.border = '1px solid red';

  var container2 = document.getElementById("textVideoWrapper");
  container2.innerHTML = "";
  var video2 = document.createElement('video');
  video2.src = `http://127.0.0.1:8080/${input}/text_video.mp4`;
  video2.width = 1000;
  video2.setAttribute("controls","controls")
  container2.appendChild(video2);
  video2.style.border = '1px solid red';

  var DINO_proposal = document.getElementById("DINOproposal");
  DINO_proposal.src = `http://127.0.0.1:8080/${input}/region_preds.jpg`;
  var OCR_proposal = document.getElementById("OCRproposal");
  OCR_proposal.src = `http://127.0.0.1:8080/${input}/OCR_preds.jpg`;
  var Final_proposal = document.getElementById("Finalproposal");
  Final_proposal.src = `http://127.0.0.1:8080/${input}/pruned.jpg`;
}

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

function populate_caption_table(jsonObj, table, input) {
  let idx = 0;
  jsonObj.forEach(obj => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>
        #${idx}
        </td>
        <td>
        <img src = "http://127.0.0.1:8080/${input}/proposed_regions/${idx}.jpg" style="max-height:150px; max-width:400px; height:auto; width:auto;">
        </td>
        <td>
        ${obj}
        </td>`;
        // You could also do the same for the cells and inputs
        table.appendChild(row);
        idx += 1;
  });
    
  }

  function populate_match_table_1(jsonObj, table) {
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
          NA
          </td>
          <td id = "testID">
          NA
          </td>`;
          // You could also do the same for the cells and inputs
          table.appendChild(row);
          idx += 1;
    });
      
    }

  function populate_match_table_2() {
    testCell = document.getElementById('testID');
    testCell.innerHTML = "LKR 100";
  }

submit("149_2_14_table")
