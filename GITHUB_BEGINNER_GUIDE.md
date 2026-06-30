# GitHub 新手指南

这份指南面向第一次接触 GitHub 的用户，结合本仓库当前状态：这是一个非常轻量的静态网页项目，核心文件是 `index.html`，可以直接用浏览器打开，也可以部署到 GitHub Pages。

## 1. GitHub 是什么？

GitHub 是一个托管代码和协作开发的平台。你可以把它理解成：

- **代码网盘**：把项目文件保存到云端。
- **版本记录本**：每一次改动都可以保存成一个版本，方便回退和追踪。
- **协作工具**：多人可以通过 Pull Request 一起讨论、审核和合并代码。
- **发布平台**：静态网页可以通过 GitHub Pages 免费发布。

## 2. Git 和 GitHub 的区别

- **Git**：安装在电脑上的版本控制工具，用来记录文件变化。
- **GitHub**：在线平台，用来托管 Git 仓库并支持协作。

常见关系是：你在本地用 Git 管理项目，再把代码推送到 GitHub。

## 3. 最常用的几个概念

### Repository（仓库）

一个项目的完整文件夹，例如本项目就是一个仓库。

### Commit（提交）

一次保存下来的改动记录。好的提交信息应该简短说明“做了什么”。

示例：

```bash
git add index.html
git commit -m "Update wedding video links"
```

### Branch（分支）

分支用于在不影响主线代码的情况下开发新内容。

常见做法：

```bash
git switch -c add-guide
```

### Pull Request（PR）

Pull Request 是把某个分支的改动请求合并到主分支前的讨论和审核页面。它通常包含：

- 改了什么
- 为什么改
- 如何测试
- 需要别人注意的地方

### Merge（合并）

当 PR 审核通过后，把分支里的改动合并进主分支。

## 4. 新手最常用工作流

下面是一套最常见、最安全的操作流程。

### 第一步：查看当前状态

```bash
git status
```

它会告诉你当前有哪些文件被修改、哪些文件还没被 Git 跟踪。

### 第二步：创建新分支

```bash
git switch -c my-first-change
```

建议不要直接在主分支上改动，尤其是多人协作时。

### 第三步：修改文件

比如修改 `index.html` 里的文字、链接或样式。

### 第四步：查看改动

```bash
git diff
```

确认改动符合预期后，再进入下一步。

### 第五步：暂存改动

```bash
git add index.html
```

如果要暂存所有改动，可以用：

```bash
git add .
```

### 第六步：提交改动

```bash
git commit -m "Describe your change"
```

提交信息建议用英文或中文都可以，但要具体。例如：

- `Add GitHub beginner guide`
- `修正婚礼视频链接`
- `Update page title and button text`

### 第七步：推送到 GitHub

```bash
git push origin my-first-change
```

推送后，GitHub 通常会提示你创建 Pull Request。

## 5. 如何用 GitHub Pages 发布静态网页

本项目只有一个 `index.html`，非常适合 GitHub Pages。

大致步骤：

1. 把仓库推送到 GitHub。
2. 打开 GitHub 仓库页面。
3. 进入 **Settings**。
4. 找到 **Pages**。
5. 在 **Build and deployment** 中选择分支，例如 `main`。
6. 保存后等待部署完成。
7. GitHub 会生成一个可以访问的网址。

如果仓库名是 `username.github.io`，它通常会直接成为个人主页。

## 6. 修改本项目时要注意什么

当前项目是一个单文件静态页面：

- 页面结构、样式和链接都在 `index.html` 里。
- 不需要安装依赖。
- 不需要构建步骤。
- 可以直接双击 `index.html` 或用浏览器打开预览。

如果你只是修改文案或链接，通常只需要：

```bash
git status
git diff
git add index.html
git commit -m "Update wedding page copy"
```

## 7. 常见问题

### 我改错了，还没提交怎么办？

查看改动：

```bash
git diff
```

如果确定要丢弃某个文件的本地改动：

```bash
git restore index.html
```

### 我提交错了怎么办？

如果只是提交信息写错，可以用：

```bash
git commit --amend
```

如果已经推送到共享分支，修改历史前要先和协作者确认。

### 我不知道当前在哪个分支怎么办？

```bash
git branch
```

带 `*` 的就是当前分支。

### 我想下载别人 GitHub 上的项目怎么办？

```bash
git clone https://github.com/owner/repository.git
```

把地址替换成对应仓库的 GitHub 地址。

## 8. 推荐养成的习惯

- 每次开始前先运行 `git status`。
- 一次提交只做一类事情。
- 提交信息写清楚，不要只写 `update`。
- 开发新功能时使用新分支。
- 提交前用 `git diff` 自查。
- PR 描述里写清楚“改了什么”和“如何验证”。

## 9. 本项目的建议下一步

如果你想继续完善这个仓库，可以考虑：

- 增加 `README.md`，说明页面用途和预览方式。
- 把 CSS 拆到单独文件，便于维护。
- 增加 GitHub Pages 部署说明。
- 给链接增加更明确的访问说明。
- 添加预览截图，方便别人快速了解页面效果。
