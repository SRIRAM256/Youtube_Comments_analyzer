document.getElementById("analyzeButton").addEventListener("click", function() {
    // You can use fetch or messaging to send data to the background script or perform analysis
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      const tab = tabs[0];
      chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: getYouTubeComments
      });
    });
  });
  
  function getYouTubeComments() {
    const comments = [];
    //add youtube api key and retriev comments respect to video id
    //return to backend js file to analyze the comments
    return comments;
  }
  