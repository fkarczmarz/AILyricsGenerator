function openSideMenu() {
  $("#sideMenu").attr("class", "side-menu open");
}

function hideSideMenu() {
  $("#sideMenu").attr("class", "side-menu");
}

function formatDateString(isoString) {
  const date = new Date(isoString);

  // Extract the day, month, and year from the Date object
  const day = String(date.getDate()).padStart(2, "0");
  const month = String(date.getMonth() + 1).padStart(2, "0"); // getMonth() is zero-based
  const year = date.getFullYear();

  return `${day}.${month}.${year}`;
}
