chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.isSearching === "true") {
    const questions_container = document.querySelectorAll(
      ".question-main-content"
    );

    // 收集页面题目
    let questions = [];
    for (let i = 2; i < questions_container.length; i++) {
      questions.push({
        title: questions_container[i].childNodes[0].innerText,

        options:
          questions_container[i].childNodes[1].childNodes[0].childNodes[0]
            .childNodes,
      });
    }
    console.log(questions);

    //向后台提交题目
    chrome.runtime.sendMessage(
      {
        origin: "content",
        questions,
      },
      (res) => {
        // 点击正确的答案;
        for (let i = 0; i < res.length; i++) {
          // console.log(questions[i].options);
          if (i.length === 1)
            questions[i].options[res[i][0]].childNodes[0].click();
          else {
            for (const j of res[i]) {
              questions[i].options[res[i][j]].childNodes[0].click();
            }
          }
        }

        //提交
        // const question_commit = document.querySelector("button");
        // console.log(questions_container, questions, question_commit);
        console.log("the right answer is", res);
        //收到答题消息，返回 “收到” 消息
        sendResponse({ finish: "已经回答完毕" });
      }
    );

    // console.log(
    //   sender.tab
    //     ? "from a content script:" + sender.tab.url
    //     : "from the extension"
    // );
    // console.log(request, sender);
    // const questions = questions_container.map((question) => ({
    //   title:
    //     question.childNodes[1].childNodes[0].childNodes[0].childNodes[0]
    //       .childNodes[0].textContent,
    //   options:
    //     question.childNodes[1].childNodes[1].childNodes[0].childNodes[0]
    //       .childNodes,
    // }));

    // const questions = questions_container.map((i) => i.childNodes[1]); ????????
    // const group = questions_container[0].childNodes[2].innerText;
    // const t_name = questions_container[1].childNodes[2].innerText;
  }
});
