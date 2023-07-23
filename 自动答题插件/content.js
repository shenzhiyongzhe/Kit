chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.isSearching === "true") {
    const questions_container = document.querySelectorAll(
      ".question-main-content"
    );

    // 收集页面题目
    let primative_questions = [];
    let process_questions = [];
    for (let i = 2; i < questions_container.length; i++) {
      let title = questions_container[i].childNodes[0].innerText;
      let options_container =
        questions_container[i].childNodes[1].childNodes[0].childNodes[0]
          .childNodes;
      primative_questions.push({ title, options: options_container });
      let options = [];
      for (let i = 0; i < options_container.length; i++) {
        options.push(options_container[i].innerText);
      }

      process_questions.push({ title, options });
    }
    console.log(process_questions, "原生", primative_questions);

    //向后台提交题目并返回正确答案
    chrome.runtime.sendMessage(
      {
        origin: "content",
        questions: process_questions,
      },
      (res) => {
        console.log("the right answer is", res);
        // 点击正确的答案;
        for (let i = 0; i < res.length; i++) {
          // console.log(questions[i].options);
          if (typeof res[i] === "number" && res[i] >= 0)
            primative_questions[i].options[res[i]].childNodes[0].click();
          else if (res[i] == -1) console.log(res[i]);
          else {
            for (let j = 0; j < res[i].length; j++) {
              primative_questions[i].options[res[i][j]].childNodes[0].click();
            }
          }
        }

        //提交
        // const question_commit = document.querySelector("button");
        // console.log(questions_container, questions, question_commit);
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
