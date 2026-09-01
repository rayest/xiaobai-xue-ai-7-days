# AI 每小时情报脚本

`ai_hourly_intelligence.py` 使用 Python 标准库抓取公开情报，供每小时定时任务调用。它不把点赞、投票、评论、Star 或下载量直接当成用户规模、产品质量或商业成功。

## 覆盖来源

- 官方：OpenAI、Anthropic Newsroom、Anthropic API Release Notes、Claude Code Docs、Google AI、Microsoft AI、Hugging Face Blog
- Claude Code：`anthropics/claude-code` GitHub Releases
- 研究：arXiv cs.AI
- 产品/开源：Hugging Face Models、Spaces、Datasets，GitHub 新建 AI 项目
- 产品社区：Product Hunt（需要 `PRODUCT_HUNT_TOKEN`）
- 开发者社区：Hacker News、Reddit r/artificial

## 运行

```bash
python3 scripts/ai_hourly_intelligence.py --output reports/ai-intelligence.md
```

Product Hunt API Token 是可选的，不要把 Token 写进仓库、命令历史或报告：

```bash
PRODUCT_HUNT_TOKEN='your-token' python3 scripts/ai_hourly_intelligence.py
```

脚本默认标注最近 24 小时窗口；各 RSS/API 的时间过滤仍应在人工复核阶段完成。

## 每小时运行示例

```cron
0 * * * * cd /path/to/xiaobai-xue-ai-7-days && /usr/bin/python3 scripts/ai_hourly_intelligence.py --output reports/ai-intelligence.md >> /tmp/ai-intelligence.log 2>&1
```

建议人工审阅后再提交每小时生成的报告，不要把未经核验的热度判断自动推送到公共仓库。

## 数据边界

- Anthropic、Claude Code 及其他公司官方内容属于公司自述，需要和社区反馈及独立结果交叉验证。
- RSS/API 可能有延迟、限流、删除和地区差异。
- X、部分 Product Hunt 数据及私有社区内容不能保证通过公开接口获取。
