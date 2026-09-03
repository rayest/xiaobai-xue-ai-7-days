# Codex Web Analyzer

一个通过本地 Codex CLI 分析网页的 Chrome 侧边栏扩展 MVP。

## 工作原理

```text
Chrome Side Panel → 127.0.0.1 Bridge → codex exec → SSE → Side Panel
```

插件只负责读取当前标签页中用户可见的正文或选中文本；本地 Bridge 负责启动 Codex CLI。网页内容会作为待分析资料传入，不能覆盖分析指令。

## 启动 Bridge

需要 Node.js 18+，并且 `codex` 已完成登录：

```bash
cd codex-web-analyzer/bridge
CODEX_BRIDGE_TOKEN="请替换为随机长字符串" node server.mjs
```

如果系统 PATH 中找不到 `codex`，Bridge 会自动尝试 macOS ChatGPT 应用内置路径。也可以显式指定 Codex 路径：

```bash
CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex" \
CODEX_BRIDGE_TOKEN="请替换为随机长字符串" \
node server.mjs
```

启动后将 Token 填入扩展侧边栏的“Bridge Token”设置。Bridge 只监听 `127.0.0.1:43127`。

## 安装扩展

1. 打开 Chrome 的 `chrome://extensions`。
2. 开启“开发者模式”。
3. 点击“加载已解压的扩展程序”。
4. 选择本目录下的 `extension/`。
5. 打开任意文章，点击扩展图标，进入侧边栏。

Chrome 内置页、扩展商店页和部分受保护页面不能被内容脚本读取；遇到这种页面可复制选中文本，或改用 Codex 内置浏览器。

## 测试

```bash
cd codex-web-analyzer/bridge
npm test
```

`npm test` 只测试 Bridge 的健康检查、鉴权、参数校验和清洗逻辑，不会调用模型。

实际联调：

```bash
CODEX_BRIDGE_TOKEN=test-token node server.mjs
curl http://127.0.0.1:43127/health
curl -N -X POST http://127.0.0.1:43127/analyze \
  -H 'Content-Type: application/json' \
  -H 'X-Bridge-Token: test-token' \
  -d '{"title":"测试文章","url":"https://example.com","content":"这是一段测试内容。","instruction":"请用一句话总结"}'
```

## 安全边界

- 默认使用 `--sandbox read-only`，本项目不会给网页分析任务写文件或执行高风险命令。
- 不使用 `--dangerously-bypass-approvals-and-sandbox`。
- Bridge 只绑定回环地址，分析接口需要 Token。
- 正文限制为 120,000 字符，扩展侧过滤密码、Token 等敏感字段。
- 生产使用前应增加操作系统级 Native Messaging、签名扩展、审计和企业权限管理。
