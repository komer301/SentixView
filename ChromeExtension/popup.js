// popup.js
document.addEventListener("DOMContentLoaded", function () {
  // Automatically get the video ID from the active tab
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    const videoId = extractVideoId(tabs[0].url);
    if (videoId) {
      analyzeSentiment(videoId);
    } else {
      console.error("Unable to extract video ID.");
      displayResult({ error: "Not on a Youtube Video" });
    }
  });

  const analyzeBtn = document.getElementById("analyzeBtn");

  analyzeBtn.addEventListener("click", function () {
    const videoId = document.getElementById("videoId").value;
    analyzeSentiment(videoId);
  });

  function analyzeSentiment(videoId) {
    const apiUrl = "http://127.0.0.1:5000/" + videoId;
    const resultDiv = document.getElementById("result");

    // Display loading spinner or some feedback to the user
    resultDiv.innerHTML = "Analyzing sentiment...";

    fetch(apiUrl)
      .then((response) => {
        console.log("Response status:", response.status);

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return response.json();
      })
      .then((data) => {
        console.log("Data received:", data);
        if (data.error) {
          throw new Error(`Sentiment analysis error: ${data.error}`);
        }
        displayResult(data);
      })
      .catch((error) => {
        console.error("Error:", error);
        resultDiv.innerHTML =
          error.message || "Failed to analyze sentiment. Please try again.";
      });
  }

  function displayResult(result) {
    console.log("Result received:", result);

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "";

    try {
      // Parse the result string into a JavaScript object
      const parsedResult = JSON.parse(result);

      if (parsedResult.error) {
        resultDiv.textContent = parsedResult.error;
      } else {
        resultDiv.innerHTML = `
            <p>Positive: ${parsedResult.positive.toFixed(0)}%</p>
            <p>Negative: ${parsedResult.negative.toFixed(0)}%</p>
            <p>Neutral: ${parsedResult.neutral.toFixed(0)}%</p>
          `;
      }
    } catch (error) {
      console.error("Error parsing result:", error);
      resultDiv.textContent = "Failed to parse result. Please try again.";
    }
  }

  function extractVideoId(url) {
    const match = url.match(/[?&]v=([^&]+)/);
    return match ? match[1] : null;
  }

  // ... rest of your code
});
