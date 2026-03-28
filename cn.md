> [!WARNING]
> 本仓库将不再接收更新。感谢所有支持它的人。

<br/>
<p align="center">
  <a href="https://github.com/zfcsoftware/puppeteer-real-browser">
    <img src="https://github.com/zfcsoftware/puppeteer-real-browser/assets/123484092/cc8b5fb9-504a-4fd3-97f6-a51990bb4303" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Puppeteer Real Browser</h3>

  <p align="center">
    这个包可以防止 Puppeteer 在像 Cloudflare 这样的服务中被识别为机器人，并允许你毫无问题地通过验证码。它的行为就像一个真正的浏览器。
    <br/>
    <br/>
    如果你只对 Cloudflare WAF 感兴趣，请查看这个仓库：<br/> https://github.com/zfcsoftware/cf-clearance-scraper
  </p>
</p>

<p align="center">
<video src='https://github.com/user-attachments/assets/5dddca09-6941-42e9-9427-5c666632483f'/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/contributors/zfcsoftware/puppeteer-real-browser?color=dark-green" alt="Contributors" />
  <img src="https://img.shields.io/github/forks/zfcsoftware/puppeteer-real-browser?style=social" alt="Forks" />
  <img src="https://img.shields.io/github/stars/zfcsoftware/puppeteer-real-browser?style=social" alt="Stargazers" />
  <img src="https://img.shields.io/github/issues/zfcsoftware/puppeteer-real-browser" alt="Issues" />
  <img src="https://img.shields.io/github/license/zfcsoftware/puppeteer-real-browser" alt="License" />
</p>

## 赞助 (Sponsor)

[![ScrapeDo](data/sdo.gif)](https://scrape.do/?utm_source=github&utm_medium=repo_prb)

## 安装 (Installation)

如果你使用的是 Linux 操作系统，必须安装 xvfb 才能使库正常工作。

```bash
npm i puppeteer-real-browser
```

如果你正在使用 linux:

```bash
sudo apt-get install xvfb
```

## 引入 (Include)

### CommonJS

```js
const { connect } = require("puppeteer-real-browser");

const start = async () => {
  const { page, browser } = await connect();
};
```

### Module

```js
import { connect } from "puppeteer-real-browser";

const { page, browser } = await connect();
```

## 用法 (Usage)

```js
const { connect } = require("puppeteer-real-browser");

async function test() {
  const { browser, page } = await connect({
    headless: false,

    args: [],

    customConfig: {},

    turnstile: true,

    connectOption: {},

    disableXvfb: false,
    ignoreAllFlags: false,
    // proxy:{
    //     host:'<proxy-host>',
    //     port:'<proxy-port>',
    //     username:'<proxy-username>',
    //     password:'<proxy-password>'
    // }
  });
  await page.goto("<url>");
}

test();
```

**headless**: 默认值为 false。也可以发送诸如“new”、true、“shell”等值，但在使用 false 时工作最稳定。

**args:** 如果你在启动 Chromium 时想要添加额外的标志 (flag)，可以通过这个字符串数组发送。
支持的标志: https://github.com/GoogleChrome/chrome-launcher/blob/main/docs/chrome-flags-for-tools.md

**customConfig:** https://github.com/GoogleChrome/chrome-launcher 浏览器通过此库进行初始化。你通过这个对象发送的内容会作为直接的初始化参数添加。你应该使用本仓库中的初始化值。你应该在这里设置 userDataDir 选项，如果你想指定自定义的 chrome 路径，你应该通过 chromePath 值进行设置。

**turnstile:** 如果设置为 true，Cloudflare Turnstile 验证码会自动被点击。

**connectOption:** 你在连接通过 puppeteer.connect 创建的 chromium 时发送的变量会被添加进去。

**disableXvfb:** 在 Linux 中，当 headless 为 false 时，会创建一个虚拟屏幕并在那里运行浏览器。如果你想看到浏览器，可以将此值设置为 true。

**ignoreAllFlags:** 如果为 true，所有的初始化参数都会被覆盖。这包括首次加载时出现的“让我们开始”页面。

## 如何安装 Puppeteer-extra 插件？

某些插件，例如 puppeteer-extra-plugin-anonymize-ua，可能会导致你被检测到。你可以使用库的测试文件中的插件安装测试，看看它是否会导致你被检测。

以下是安装插件的示例。你可以按照这个示例以相同的方式安装其他插件。

```bash
npm i puppeteer-extra-plugin-click-and-wait
```

```js
const test = require("node:test");
const assert = require("node:assert");
const { connect } = require("puppeteer-real-browser");

test("Puppeteer Extra Plugin", async () => {
  const { page, browser } = await connect({
    args: ["--start-maximized"],
    turnstile: true,
    headless: false,
    // disableXvfb: true,
    customConfig: {},
    connectOption: {
      defaultViewport: null,
    },
    plugins: [require("puppeteer-extra-plugin-click-and-wait")()],
  });
  await page.goto("https://google.com", { waitUntil: "domcontentloaded" });
  await page.clickAndWaitForNavigation("body");
  await browser.close();
});
```

## Docker

你可以使用主目录中的 Dockerfile 文件来将此库与 docker 一起使用。它已经在 Ubuntu 服务器操作系统的 docker 上进行了测试。

要运行测试，你可以按照以下步骤操作：

```bash
git clone https://github.com/zfcsoftware/puppeteer-real-browser
```

```bash
cd puppeteer-real-browser
```

```bash
docker build -t puppeteer-real-browser-project .
```

```bash
docker run puppeteer-real-browser-project
```

## 支持我们

这个库是完全开源的，并且在不断更新中。请为这个仓库点星 (star) 以支持这个项目。点星和支持项目将确保它收到更新。如果你想进一步支持，可以考虑赞助我 (https://github.com/sponsors/zfcsoftware)

## 常见问题与解答 (Q&A)

### 我无法访问 Window 对象中的函数，我该怎么办？

这个问题很可能是由于使用的 rebrowser 关闭了运行时 (runtime) 引起的。
https://github.com/zfcsoftware/puppeteer-real-browser/tree/access-window
我为此创建了一个分支。你可以通过 puppeteer-intercept-and-modify-requests 将 javascript 添加到页面源代码中来访问所需的值，正如 success.js 中所做的那样。如果你了解 Chrome 插件，你也可以使用它。

### page.setViewport 方法不起作用，我该怎么办？

与测试模块中的初始化参数一样，你可以在 connectOption 中设置 defaultViewport。如果你设置为 null，它将占据与浏览器宽度一样的空间。

### 库有任何已知的检测问题吗？

使用了经过 rebrowser 修补的 puppeteer-core。在 headless false 模式下用测试文件中具挑战性的站点进行了测试，并以优异的成绩通过了。唯一已知的问题是鼠标 screenX 与鼠标位置不匹配。这已在库中进行了修补。

库中包含了 ghost-cursor。（https://github.com/zfcsoftware/puppeteer-real-browser/blob/2a5fba37a85c15625fb3c8d1f7cf8dcb109b9492/lib/cjs/module/pageController.js#L54）你可以使用 ghost-cursor 与 page.realCursor。 建议使用 page.realClick 而不是 page.click。

### 是什么让这个库与众不同？

这个库让你以最自然的状态启动和使用 Chrome。它尝试以最小的修补获得最佳结果。感谢 @nwebson，他解决了由此产生的 Runtime.enable 问题。如果使用 rebrowser 解决了你的问题，我不建议使用 real browser。

Real browser 并没有让你完全控制启动过程。它使用 Chrome launcher 启动 Chrome 并通过 rebrowser 连接到它。

### 为什么我无法通过 Recaptcha v3？

https://stackoverflow.com/questions/52546045/how-to-pass-recaptcha-v3

请参阅上面链接中的答案。当没有 Google 会话时，无论你的浏览器多好，recaptcha 都会将你识别为机器人。这是一个普遍的问题。

## 许可证 (License)

在 MIT 许可证下分发。更多信息请参见 [LICENSE](https://github.com/zfcsoftware/puppeteer-real-browser/blob/main/LICENSE.md)。

## 鸣谢 (Thank You)

**对当前版本的贡献**

- **rebrowser™** - [rebrowser™](https://github.com/rebrowser) - _为 Runtime 创建了一个补丁包，这个包留下了很多痕迹。由于不使用 Runtime，大多数问题都得到了解决。过去使用并导致许多问题的 TargetFilter，切换到了此补丁。Puppeteer-core 库已被修补并添加到此仓库中。多亏了 rebrowser，许多优秀的机器人检测系统没有被抓到。请给 rebrowser 仓库点赞。谢谢。（https://github.com/rebrowser/rebrowser-patches）_

- **Skill Issue™** - [TheFalloutOf76](https://github.com/TheFalloutOf76) - _他意识到无法准确模拟鼠标移动并为此创建了一个解决方案。他的解决方案用于此库。（https://github.com/TheFalloutOf76/CDP-bug-MouseEvent-.screenX-.screenY-patcher）_

## 免责声明 (Disclaimer of Liability)

对于使用此软件不承担任何责任。此软件仅供教育和参考之用。用户应自行承担使用此软件的风险。开发者不对因使用本软件而可能导致的任何损害负责。

此软件并非旨在绕过 Cloudflare Captcha 或任何其他安全措施。不得将其用于恶意目的。恶意使用可能导致法律后果。

本软件未获得官方认可或保证。用户可以访问 GitHub 页面报告错误或为软件做贡献，但无权提出任何索赔或请求服务修复。

使用本软件即表示您同意本免责声明。
