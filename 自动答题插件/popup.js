// console.log("this is popup js");
const btn = document.getElementById("btn");

btn.addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true,
  });
  // console.log("active tab", tab);
  const res = await chrome.tabs.sendMessage(tab.id, {
    isSearching: "true",
  });
  // do something with response here, not outside the function
  console.log(res);
});
