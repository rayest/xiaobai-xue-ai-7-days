# Qdrant 教程中文整理

> 本章整理自本地 Interactive Tutorials，页面版本为 v1.15.4。示例使用 Qdrant REST API；不同版本的 `/search`、`/query` 等接口可能有差异，生产使用前请对照部署版本文档。

## 1. 快速开始：创建、写入、搜索

创建一个 4 维、点积度量的集合：

```http
PUT /collections/star_charts
Content-Type: application/json

{"vectors":{"size":4,"distance":"Dot"}}
```

写入向量和业务元数据（payload）：

```http
PUT /collections/star_charts/points
Content-Type: application/json

{"points":[
  {"id":1,"vector":[0.05,0.61,0.76,0.74],"payload":{"colony":"Mars"}},
  {"id":2,"vector":[0.19,0.81,0.75,0.11],"payload":{"colony":"Jupiter"}},
  {"id":3,"vector":[0.36,0.55,0.47,0.94],"payload":{"colony":"Venus"}},
  {"id":4,"vector":[0.18,0.01,0.85,0.80],"payload":{"colony":"Moon"}},
  {"id":5,"vector":[0.24,0.18,0.22,0.44],"payload":{"colony":"Pluto"}}
]}
```

查询最相近的 3 个点，并返回 payload：

```http
POST /collections/star_charts/points/search
Content-Type: application/json

{"vector":[0.2,0.1,0.9,0.7],"limit":3,"with_payload":true}
```

## 2. 从快照导入数据

教程使用远程快照恢复 `midjourney` 集合，然后通过 count 接口验证数量：

```http
PUT /collections/midjourney/snapshots/recover
{"location":"http://snapshots.qdrant.io/midlib.snapshot"}

POST /collections/midjourney/points/count
```

示例预期约有 5,417 个点。企业环境不要直接信任外部快照：先校验来源、哈希、版本和权限，并在隔离环境恢复后再切换流量。

## 3. 基础过滤与字段索引

教程强调：高频过滤字段应建立 payload index，否则可能退化为全量扫描。典型索引如下：

```http
PUT /collections/terraforming/index
{"field_name":"life","field_schema":"bool"}

PUT /collections/terraforming/index
{"field_name":"color","field_schema":"keyword"}

PUT /collections/terraforming/index
{"field_name":"humidity","field_schema":{"type":"integer","range":true}}
```

过滤语义：`must` 表示同时满足，`should` 表示满足一个或多个，`must_not` 表示排除，`range` 表示范围条件。

```http
POST /collections/terraforming/points/scroll
{"filter":{"must":[{"key":"color","match":{"value":"black"}}]},"limit":3,"with_payload":true}
```

注意：过滤字段必须来自可信的服务端上下文。多租户系统不能允许客户端自行传入任意 `tenant_id` 后就当作权限校验。

## 4. 嵌套过滤

当数组中的多个条件必须命中同一个数组元素时，使用 nested filter。例如只找“喜欢吃肉”的恐龙：

```http
POST /collections/dinosaurs/points/scroll
{"filter":{"must":[{"nested":{"key":"diet","filter":{"must":[
  {"key":"food","match":{"value":"meat"}},
  {"key":"likes","match":{"value":true}}
]}}}]}}
```

数组字段可建立 `diet[].food`、`diet[].likes` 等索引。`has_id` 作为独立条件放在 nested 外层。

## 5. 全文过滤

未建立文本索引时，`match.text` 更接近子串/短语匹配；建立 text index 后可按 token 匹配，支持大小写归一化等配置：

```http
PUT /collections/star_charts/index
{"field_name":"description","field_schema":{"type":"text","tokenizer":"word","lowercase":true}}

POST /collections/star_charts/points/scroll
{"filter":{"must":[{"key":"description","match":{"text":"cave colonies"}}]},"with_payload":true}
```

全文过滤与语义检索不是一回事。关键词必须命中时用全文/稀疏路径，意思相近但措辞不同用稠密向量路径。

## 6. 稀疏、多向量与混合检索

稀疏向量只提交非零位置：

```http
PUT /collections/sparse_charts
{"sparse_vectors":{"keywords":{}}}

PUT /collections/sparse_charts/points
{"points":[{"id":1,"vector":{"keywords":{"indices":[1,42],"values":[0.22,0.8]}}}]}

POST /collections/sparse_charts/points/query
{"query":{"indices":[1,42],"values":[0.22,0.8]},"using":"keywords"}
```

多向量集合可通过 `multivector_config.comparator=max_sim` 配置 ColBERT 风格 MaxSim；一个点的向量字段变成“多个 4 维向量组成的数组”。这会增加存储和计算量，应通过真实数据评测收益。

混合检索先用两路 `prefetch`，再使用 RRF 融合：

```http
POST /collections/terraforming_plans/points/query
{"prefetch":[
  {"query":{"indices":[1,42],"values":[0.22,0.8]},"using":"keywords","limit":20},
  {"query":[0.01,0.45,0.67,0.89],"using":"","limit":20}
],"query":{"fusion":"rrf"},"limit":10,"with_payload":true}
```

## 7. 多租户与分组查询

共享集合时，为 `group_id` 建立 tenant index，并在每一次查询中加入服务端生成的租户过滤：

```http
PUT /collections/central_library/index
{"field_name":"group_id","field_schema":{"type":"keyword","is_tenant":true}}

POST /collections/central_library/points/query
{"query":[0.2,0.1,0.9,0.7],"filter":{"must":[
  {"key":"group_id","match":{"value":"user_1"}}
]},"limit":2,"with_payload":true}
```

还可以用 `query/groups` 按 `station` 等字段分组返回。企业级隔离还需要 API 鉴权、应用层授权、审计、密钥轮换和越权测试；payload filter 只是检索层的一道防线。

## 8. 对初学者的练习顺序

先完成“创建集合 → 写入 5 个点 → 查询 Top-3”，再分别加上 keyword、range、nested、text index。最后使用一个真实的 FAQ 数据集比较：纯稠密、纯关键词、混合 RRF 三种方式的 Recall@K、MRR、延迟和成本。
