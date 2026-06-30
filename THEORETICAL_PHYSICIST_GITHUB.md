# 理论物理学者的 GitHub 使用建议

这份文档给理论物理学者准备，用来规划 GitHub 账号、用户名、个人主页和仓库用途。

## 1. 用户名建议

GitHub 用户名需要适合被引用、搜索和写进论文/简历/项目链接。建议满足：

- 简短、稳定、容易读。
- 尽量不用随机数字串。
- 避免太长，避免难输入的拼写。
- 尽量使用小写字母、数字和连字符 `-`。
- 能体现你的研究气质，但不要过度玩梗。

你提到“亏格 1 的黎曼面”。数学上它通常可以和以下英文表达关联：

- `genus-one-riemann-surface`
- `genus-one-surface`
- `genus1-riemann`
- `riemann-torus`
- `complex-torus`
- `elliptic-curve`
- `elliptic-torus`
- `torus-geometry`

其中我最推荐：

1. `riemann-torus`：短、清楚、有数学味，也容易记。
2. `genus1-riemann`：更贴近“亏格 1 的黎曼面”，但略技术化。
3. `complex-torus`：数学上很自然，简洁专业。
4. `elliptic-curve`：辨识度高，但可能更容易被占用，也可能让人以为你主要做数论/代数几何。

如果这些已经被占用，可以考虑加研究方向或姓名缩写，例如：

- `riemann-torus-phys`
- `genus1-phys`
- `complex-torus-qft`
- `elliptic-qft`
- `torus-cft`

## 2. 修改 GitHub 用户名的注意事项

改 GitHub 用户名之前，建议先想清楚，因为它会影响你的个人链接、仓库链接和别人对你的引用。

修改后通常需要检查：

- 个人主页链接，例如 `https://github.com/旧用户名`。
- 本地仓库的 remote 地址。
- 论文、简历、个人网站、ORCID、Google Scholar、arXiv 个人页里的链接。
- README、项目文档、徽章、GitHub Pages 链接。
- 个人 Profile README 仓库名是否仍然等于新用户名。

本地仓库 remote 地址可以这样查看：

```bash
git remote -v
```

如果用户名改了，远程地址可能需要更新：

```bash
git remote set-url origin https://github.com/NEW_USERNAME/REPOSITORY.git
```

## 3. 理论物理学者的 GitHub 可以用来做什么

### 3.1 放可复现实验和计算

即使理论工作不以软件工程为主，GitHub 也非常适合保存：

- Mathematica / Wolfram Language notebook
- Python / Julia / SageMath 脚本
- 数值验证代码
- 符号计算代码
- 图像生成脚本
- 论文附录中的计算细节

目标是让别人能复现你的推导、图和数值结果。

### 3.2 管理论文相关材料

可以为每篇论文建一个仓库，内容包括：

- `README.md`：论文题目、摘要、arXiv 链接、引用方式。
- `notebooks/`：计算 notebook。
- `scripts/`：生成图表或数据的脚本。
- `figures/`：论文图像源文件。
- `data/`：小规模可公开数据。
- `environment.yml` 或 `requirements.txt`：复现环境。

### 3.3 建个人学术主页

可以用 GitHub Pages 发布：

- 个人简介
- 研究方向
- 论文列表
- 代码和 notebook 列表
- 课程材料
- 学术笔记
- 联系方式

### 3.4 写公开学习笔记

理论物理很适合用 GitHub 维护长期笔记，例如：

- 量子场论笔记
- 共形场论笔记
- 广义相对论笔记
- 规范场论笔记
- 弦论或几何分析笔记
- 拓扑、黎曼面、模空间相关笔记

如果用 Markdown、LaTeX 或 Jupyter Book，后续可以发布成网页。

### 3.5 展示代码能力和研究品味

一个好的学术 GitHub 不一定要有大量 star，但最好让访问者快速看懂：

- 你研究什么。
- 哪些项目和论文相关。
- 哪些结果可以复现。
- 如何引用你的代码。
- 如何联系你。

## 4. 推荐的账号设置

如果你能登录 GitHub，建议手动检查以下设置：

### Profile

- Name：可以用真实姓名，或者学术场合常用姓名。
- Bio：一句话说明研究方向。
- Location：可选。
- Website：个人主页、Google Scholar、ORCID 或机构主页。
- Social accounts：可加入 ORCID、个人网站等。

Bio 示例：

```text
Theoretical physicist. QFT, geometry, and mathematical structures in physics.
```

如果你的方向更偏几何/场论，可以写：

```text
Theoretical physicist working on QFT, geometry, Riemann surfaces, and related mathematical structures.
```

### Emails

- 添加常用邮箱和学术邮箱。
- 如果重视隐私，开启 GitHub 提供的 noreply 邮箱。
- 确保 Git 提交使用的邮箱和 GitHub 账号关联，否则贡献图可能不显示。

### Security

- 开启 two-factor authentication（2FA）。
- 使用 passkey 或 authenticator app。
- 保存恢复码。

### Repositories

- 重要项目写清楚 README。
- 给论文相关仓库添加 license。
- 如果希望别人引用，添加 `CITATION.cff`。
- 给成熟项目添加 topic，例如 `theoretical-physics`、`qft`、`mathematica`、`julia`、`riemann-surfaces`。

## 5. 推荐的 Profile README 结构

你可以创建一个和用户名同名的公开仓库，并在里面放 `README.md`。例如用户名是 `riemann-torus`，仓库名也应是 `riemann-torus`。

建议结构：

```markdown
# Hi, I'm YOUR_NAME

I am a theoretical physicist interested in quantum field theory, geometry, and mathematical structures in physics.

## Research interests

- Quantum field theory
- Geometry and topology in physics
- Riemann surfaces and moduli
- Mathematical physics

## Selected repositories

- `paper-title-code`: code and notebooks for reproducing figures/results in PAPER_TITLE.
- `qft-notes`: personal notes on quantum field theory.

## Links

- Website: ...
- ORCID: ...
- Google Scholar: ...
- arXiv: ...
```

## 6. 我能帮你继续做什么

我不能直接修改你的 GitHub 账号用户名，除非你提供合适的 GitHub 授权方式或在浏览器里自己操作。但我可以继续帮你：

- 判断候选用户名是否符合规则。
- 帮你写 Profile README。
- 帮你把这个仓库整理成适合 GitHub Pages 的项目。
- 帮你创建论文复现仓库模板。
- 帮你写 `README.md`、`LICENSE`、`CITATION.cff`。
- 帮你设计个人学术主页结构。
