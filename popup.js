const statusEl = document.getElementById('status');
const downloadBtn = document.getElementById('download');
const btnText = document.getElementById('btn-text');
const spinner = document.getElementById('spinner');

downloadBtn.addEventListener('click', async () => {
  statusEl.textContent = "Downloading...";
  statusEl.className = "downloading";

  downloadBtn.disabled = true;
  spinner.style.display = "inline-block";
  btnText.style.display = "none";

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const videoUrl = tab.url;

  if (!videoUrl.includes("youtube.com/watch")) {
    statusEl.textContent = "Please open a Youtube page.";
    statusEl.className = "error";
    downloadBtn.disabled = false;
    spinner.style.display = "none";
    btnText.style.display = "inline";
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: videoUrl })
    });

    if (!response.ok) throw new Error("No Response.");

    statusEl.textContent = "Download triggered! Check your folder. 🎉";
    statusEl.className = "done";

  } catch (error) {
    statusEl.textContent = "Error: " + error.message;
    statusEl.className = "error";
  } finally {
    downloadBtn.disabled = false;
    spinner.style.display = "none";
    btnText.style.display = "inline";

    setTimeout(() => {
      statusEl.textContent = "";
      statusEl.className = "";
    }, 4000);
  }
});
