import { data } from "./data.js";

function searchAnswer(arr) {
  return new Promise((resolve) => {
    let answer = [];

    for (let i = 0; i < arr.length; i++) {
      answer.push([0]);
    }
    resolve(answer);
  });
}
// console.log("data", data);
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // 2. A page requested user data, respond with a copy of `user`
  if (message.origin === "content") {
    searchAnswer(message.questions).then((res) => sendResponse(res));
    return true;
  }
});
