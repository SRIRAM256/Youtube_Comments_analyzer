document.getElementById("analyzeButton").addEventListener("click", function () {
  // Get the active YouTube tab
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const tab = tabs[0];
    const url = new URL(tab.url);

    // Extract the video ID from the URL
    const videoId = url.searchParams.get("v");
    if (!videoId) {
      alert("Not a valid YouTube video URL.");
      return;
    }

    // Send video ID to Python backend via a POST request
    fetch("http://127.0.0.1:5000/fetch-comments", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ videoId: videoId }),
    })
    .then((data) => {
        const piechart=document.createElement('img');
        piechart.src="http://127.0.0.1:5000/fetch-comments";
        piechart.alt="Pie Chart";
        piechart.width="500";
        piechart.height="500";

        console.log("piechart recieved");
        const res=document.getElementById('result');
        res.appendChild(piechart);
      })
      .catch((error) => {
        console.error("Error fetching comments:", error);
        alert("Error fetching comments. Check the backend server.");
      });
  });
});
