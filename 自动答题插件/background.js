import Judgment from "./TestDatabase/Judgment.js";
import MultiChoice from "./TestDatabase/MultiChoice.js";
import SingleChoice from "./TestDatabase/SingleChoice.js";

// console.log(Judgment, MultiChoice, SingleChoice);

function searchAnswer(arr) {
  return new Promise((resolve) => {
    let answer = [];

    for (let i = 0; i < arr.length; i++) {
      switch (arr[i].options.length) {
        case 2:
          const judge = Judgment.find((item) => {
            return (
              item.title == arr[i].title &&
              item.options.toString() === arr[i].options.toString()
            );
          });

          answer.push(judge ? judge.rightAnswer : -1);
          break;
        case 4:
          const single = SingleChoice.find((item) => {
            return (
              item.title == arr[i].title &&
              item.options.toString() === arr[i].options.toString()
            );
          });
          console.log(single);
          // if(single == undefined) answer.push(-1)
          // else
          // answer.push(single.rightAnswer)
          answer.push(single ? single.rightAnswer : -1);
          break;
        case 5:
          const mult = MultiChoice.find((item) => {
            return (
              item.title == arr[i].title &&
              item.options.toString() === arr[i].options.toString()
            );
          });
          answer.push(mult ? mult.rightAnswer : -1);
          break;
        default:
          answer.push(-1);
      }
    }
    resolve(answer);
  });
}
// console.log("data", data);
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // 2. A page requested user data, respond with a copy of `user`
  if (message.origin === "content") {
    console.log(message);
    searchAnswer(message.questions).then((res) => sendResponse(res));
    return true;
  }
});
