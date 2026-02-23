function dismissAlert() {
  document.querySelector("#alert-container")?.classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", function (event) {
  setTimeout(() => {
    dismissAlert();
  }, 3000);
});
