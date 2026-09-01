# AI 每小时情报脚本

`ai_hourly_intelligence.py` 是定时任务的可复用脚本版本。它负责抓取和初步归类，不替代人工核验，也不自动断言热度等于质量。

## 覆盖来源

- 官方 RSS：OpenAI、Anthropic、Google AI、Microsoft AI、Hugging Face Blog
- 研究：arXiv cs.AI
- 产品/开源：Hugging Face Models、Spaces、Datasets，GitHub 新建 AI 项目
- 产品社区：Product Hunt（需要 `PRODUCT_HUNT_TOKEN`）
- 开发者社区：Hacker News、Reddit r/artificial

## 运行

脚本只使用 Python 标准库：

```bash
python3 scripts/ai_hourly_intelligence.py --output reports/ai-intelligence.md
```

Product Hunt API Token 是可选的：

```bash
PRODUCT_HUNT_TOKEN='[REDACTED]' python3 scripts/ai_hourly_intelligence.py
```

不要把 Token 写进仓库、命令历史或报告。脚本默认生成最近 24 小时的抓取报告；`--hours` 目前用于报告标注，具体 RSS/API 的时间过滤仍应在人工复核阶段完成。

## 每小时运行示例

macOS/Linux 可以使用 cron：

```cron
0 * * * * cd /path/to/xiaobai-xue-ai-7-days && /usr/bin/python3 scripts/ai_hourly_intelligence.py --output reports/ai-intelligence.md >> /tmp/ai-intelligence.log 2>&1
```

如果要提交每小时生成的报告，建议另写一个经过人工审阅的发布流程，不要让脚本自动把未经核验的热度判断推送到公共仓库。

## 数据边界

- 平台点赞、投票、评论、Star、下载量只是公开热度信号。
- 公司客户案例和 ROI 通常是公司自述，不等于独立审计结果。
- RSS/API 可能有延迟、限流、删除和地区差异。
- X、部分 Product Hunt 数据及私有社区内容不能保证通过公开接口获取。
- 生成报告后仍应核对原文、发布时间、重复新闻、引用关系和事实强度。
