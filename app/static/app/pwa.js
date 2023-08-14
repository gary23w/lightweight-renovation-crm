if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("/static/service-worker.js")
      .then(function (registration) {
        console.log(
          "Service Worker registered with scope:",
          registration.scope
        );
      })
      .catch(function (error) {
        console.error("Service Worker registration failed:", error);
      });
  });
} else {
  alert("Your browser does not support service workers.");
}

let deferredPrompt;

window.addEventListener("beforeinstallprompt", function (event) {
  // Prevent the default browser prompt from showing
  event.preventDefault();

  // Store the event for later use
  deferredPrompt = event;

  // Show your custom installation button
  console.log("beforeinstallprompt fired");
  showInstallButton();
});

function showInstallButton() {
  // Show your custom installation button and handle the click event
  const installButton = document.getElementById("install-pwa");
  installButton.style.display = "block";
  installButton.addEventListener("click", installPWA);
}

function installPWA() {
  alert("Trying to install the WebView.");

  if (navigator && navigator.standalone) {
    // iOS standalone mode
    alert('To install this app, tap "Share" and then "Add to Home Screen."');
  } else if (
    window &&
    window.matchMedia("(display-mode: standalone)").matches
  ) {
    // Android standalone mode
    alert("This app is already installed.");
  } else if (deferredPrompt) {
    // PWA installation
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(function (choiceResult) {
      if (choiceResult.outcome === "accepted") {
        alert("App installed successfully!");
      } else {
        alert("App installation canceled.");
      }
      // Reset the deferredPrompt variable
      deferredPrompt = null;
    });
  }
}
