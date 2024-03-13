let example_name;

function submit(input) {
  fetch(`http://127.0.0.1:8080/${input}/answer.json`)
   .then(response => response.json())
   .then(data => {
     populate_table(data, document.getElementById('matchTable'), input);
    });
    

  var container = document.getElementById("finalVideoWrapper");
  container.innerHTML = "";
  var video = document.createElement('video');
  video.src = `http://127.0.0.1:8080/${input}/image_video.mp4`;
  video.width = 1000;
  video.setAttribute("controls","controls")
  container.appendChild(video);
  video.style.border = '1px solid red';

  var container = document.getElementById("comparisonVideoWrapper");
  container.innerHTML = "";
  var video = document.createElement('video');
  video.src = `http://127.0.0.1:8080/${input}/merged.mp4`;
  video.width = 1600;
  video.setAttribute("controls","controls")
  container.appendChild(video);
  video.style.border = '1px solid red';
}

function populate_table(jsonObj, table, input) {
  table.innerHTML = `<thead>
      <tr>    
            <th>Index</th>
            <th>Lecture</th>
            <th>Slide Region</th>
            <th>Justification</th>
        </tr>
      </thead>`;  
  
  //const regex = 'The most relevant sentence on the slide is: (.*)\.';

  console.log(jsonObj)
  //Segment \d+: "(.*?)"
  const regex = ': "(.*?)"';
  const matches = [...jsonObj.matchAll(regex)];
  let num_segments = matches.length;
  console.log(matches.length);

  const regex2 = '(?<=: "(.*?)" ).*'
  const matches2 = [...jsonObj.matchAll(regex2)];
  console.log(matches2.length);

  for (var idx = 0; idx < num_segments; idx++){
    const row = document.createElement('tr');
    row.innerHTML = `
    <td>
    #${idx}
    </td>
    <td>
    ${matches[idx][1]}
    </td>
    <td>
    <img src = "http://127.0.0.1:8080/${input}/cropped_boxes/${idx}.jpg" style="max-height:150px; max-width:400px; height:auto; width:auto;">
    </td>
    <td>
    Segment ${matches2[idx][0]}
    </td>`;
    // You could also do the same for the cells and inputs
    table.appendChild(row);    
  }
  // jsonObj.forEach(obj => {
  //       const row = document.createElement('tr');
  //       row.innerHTML = `
  //       <td>
  //       #${idx}
  //       </td>
  //       <td>
  //       ${idx}
  //       </td>
  //       <td>
  //       NA
  //       </td>
  //       <td id>
  //       NA
  //       </td>`;
  //       // You could also do the same for the cells and inputs
  //       table.appendChild(row);
  //       idx += 1;
  // });
    
  }

submit("149_2_14_table");
