# 实践项目

统一存放通过自然语言编程完成的独立应用、网页游戏和交互工具。后续类似项目均在本目录新增子目录。

## 项目索引

| 项目 | 类型 | 技术 | 简介 |
| --- | --- | --- | --- |
| [ORBIT · 星环穿越](orbit-game/README.md) | 3D 网页游戏 | Three.js、Vite、Web Audio | 星际飞行、加速、外星战机交战和母舰 Boss |

## 目录约定

```text
projects/
├── README.md
├── orbit-game/
│   ├── README.md
│   ├── package.json
│   ├── package-lock.json
│   ├── src/
│   ├── public/
│   └── design/
└── <下一个项目>/
```

- 每个项目使用独立的英文短横线目录名，保持自己的依赖、资源和构建配置。
- README 说明项目用途、安装启动方式、操作方法和测试命令。
- 提交源码、必要素材及依赖锁文件；依赖目录、构建产物、缓存和密钥不入库。
- 新增项目时同步更新本页索引。

## 启动星环穿越

在仓库根目录执行：

```sh
cd projects/orbit-game
npm ci
npm run dev
```

打开终端输出的本地地址。验证命令为 `npm test` 和 `npm run build`。
