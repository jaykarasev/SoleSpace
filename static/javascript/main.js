// document.getElementById("search-icon").addEventListener("click", function () {
//   const searchContainer = document.querySelector(".search-container");
//   const searchInput = document.getElementById("search-input");

//   searchContainer.classList.toggle("expanded");

//   if (searchContainer.classList.contains("expanded")) {
//     searchInput.focus();
//   }
// });

// Search Icon Toggle
document.getElementById("search-icon").addEventListener("click", function () {
  const searchContainer = document.querySelector(".search-container");
  const searchInput = document.getElementById("search-input");

  searchContainer.classList.toggle("expanded");

  if (searchContainer.classList.contains("expanded")) {
    searchInput.focus();
  }
});

// Toggle Closet and Wishlist with AJAX and Icon Update
document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelectorAll(".add-to-closet, .add-to-wishlist")
    .forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent the default form submission behavior

        const sneakerId = this.dataset.sneakerId;
        const url = this.dataset.actionUrl;
        const isClosetAction = this.classList.contains("add-to-closet");

        console.log(
          `Action: ${
            isClosetAction ? "Adding to Closet" : "Adding to Wishlist"
          }, Sneaker ID: ${sneakerId}`
        );

        // Perform the AJAX request
        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.message) {
              const parentDiv = this.closest(".sneaker-actions");
              console.log("Parent div found:", parentDiv);

              const messageElement = parentDiv.querySelector("p");
              if (messageElement) {
                messageElement.innerText = data.message; // Show status message if <p> exists
              } else {
                console.log(
                  "Message <p> element not found in .sneaker-actions div."
                );
              }

              // Swap icons based on the action
              console.log("Updating icon colors based on action.");
              if (isClosetAction) {
                parentDiv.querySelector(".icon-closet-image").src =
                  "/static/images/closet_icon_red.png?v=1";
                parentDiv.querySelector(".icon-wishlist-image").src =
                  "/static/images/wishlist_icon.png?v=1";
              } else {
                parentDiv.querySelector(".icon-wishlist-image").src =
                  "/static/images/wishlist_icon_red.png?v=1";
                parentDiv.querySelector(".icon-closet-image").src =
                  "/static/images/closet_icon.png?v=1";
              }
            }
          })
          .catch((error) => console.error("Error:", error));
      });
    });
});
