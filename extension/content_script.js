
document.addEventListener("DOMContentLoaded", function() {

const btn=document.getElementById("analyzebtn");
btn.addEventListener("click",analyzeComments);


function analyzeComments() {
  // Get the active YouTube tab

  const btn=document.getElementById("analyzebtn");
  btn.disabled=true;
  btn.innerHTML="Analyzing...";

  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const tab = tabs[0];
    const url = new URL(tab.url);

    // Extract the video ID from the URL
    const videoId = url.searchParams.get("v");
    if (!videoId) {
      alert("Not a valid YouTube video URL.");
      btn.disabled=false;
      btn.innerHTML="Analyze comments";
      return;
    }

    // Send video ID to Python backend via a POST request
    fetch(`http://127.0.0.1:5000/analyze/${videoId}`)
    .then((data) => {
      console.log(data)
        const piechart=document.createElement('img');
        piechart.src=`http://127.0.0.1:5000/analyze/${videoId}`;
        piechart.alt="Pie Chart";
        piechart.width="500";
        piechart.height="500";
        console.log("piechart recieved");
        const res=document.getElementById('result');
        res.appendChild(piechart);
        btn.disabled=false;
        btn.innerHTML="Analyze comments";
      })
      .catch((error) => {
        console.error("Error fetching comments:", error);
        alert("Error fetching comments. Check the backend server.");
        btn.disabled=false;
        btn.innerHTML="Analyze comments";
      });

      
  });
}

});