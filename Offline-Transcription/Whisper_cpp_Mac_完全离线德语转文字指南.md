# whisper.cpp：Mac 完全离线德语录音转文字指南

这份指南把德语录音在自己的 Mac 上转成文字。首次安装软件与下载模型需要联网；模型下载完后，**转换音频和语音识别均可在关闭 Wi-Fi 的情况下完成**。音频不会上传至云端。

适合：自己的德语录音、学习录音、个人口述笔记。

> `whisper.cpp` 是开源的命令行工具。它没有 MacWhisper 那样的图形界面，但本地处理的流程更可控。

## 1. 需要准备什么

- 一台 Mac（Apple Silicon 的 M 系列芯片速度尤其好；Intel Mac 也能使用）。
- 要转写的录音，例如 iPhone“语音备忘录”导出的 `.m4a` 文件。
- 初次设置时的网络连接。
- 约 2–4 GB 可用硬盘空间（程序、模型和临时 WAV 文件）。

## 2. 哪一步后可以关闭 Wi-Fi？

只有以下两件事必须联网：

1. 安装 `whisper.cpp` 和 `ffmpeg`；
2. 下载语音模型文件。

当下面这个模型下载命令**完全执行完毕并回到终端提示符**后，就可以关闭 Wi-Fi：

```bash
curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin -o models/ggml-large-v3-turbo.bin
```

之后的所有转写命令完全离线。为了自己确认，可关闭 Wi-Fi 后再执行第 5 节的命令；它不应要求登录、API Key 或联网。

## 3. 第一次安装

### 3.1 打开终端

在 Mac 按 `Command + Space`，输入 **Terminal**（终端），按回车。

### 3.2 检查 Homebrew

在终端输入：

```bash
brew --version
```

如果显示版本号，说明已经有 Homebrew，直接进入下一节。

如果显示 `command not found`，请访问 [Homebrew 官网](https://brew.sh/)，复制官网显示的安装命令到终端执行。安装过程会要求输入 Mac 登录密码；输入时屏幕不会显示字符，这是正常的。

### 3.3 安装转写程序与音频转换工具

在终端运行：

```bash
brew install whisper-cpp ffmpeg
```

- `whisper-cpp`：本地语音识别程序。
- `ffmpeg`：把 iPhone 常见的 `.m4a` 录音转换成通用 WAV 格式。

安装完成后，可检查：

```bash
whisper-cli --help
ffmpeg -version
```

只要看到帮助信息或版本信息，就表示安装成功。

## 4. 下载模型（完成后即可断网）

先建立专门文件夹：

```bash
mkdir -p ~/whisper-local/models
cd ~/whisper-local
```

然后下载推荐模型：

```bash
curl -L https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin -o models/ggml-large-v3-turbo.bin
```

下载完成后，检查文件是否存在：

```bash
ls -lh ~/whisper-local/models/ggml-large-v3-turbo.bin
```

若能看到文件大小，模型已准备好。**从此刻起可关闭 Wi-Fi。**

### 模型怎么选？

| 模型 | 建议用途 | 取舍 |
| --- | --- | --- |
| `large-v3-turbo` | 默认推荐，德语对话、学习录音 | 准确、速度较好，下载较大 |
| `medium` | Mac 较旧或录音很多 | 更省资源，准确度略低 |
| `small` | 只需要快速粗略稿 | 快，但错字会更多 |

不要下载带 `.en` 的模型，例如 `base.en`，因为它们专为英语优化，不适合德语。

## 5. 日常离线转写：最可靠流程

下面假设录音文件名为 `Deutschaufnahme.m4a`，并放在 Mac 的“下载”文件夹中。

### 5.1 进入工作目录

```bash
cd ~/whisper-local
```

### 5.2 把录音转为 WAV

```bash
ffmpeg -i ~/Downloads/Deutschaufnahme.m4a -ar 16000 -ac 1 aufnahme.wav
```

这一步只在本机把音频转换为单声道、16 kHz 的 WAV。它不会上传文件。

### 5.3 按德语转写，并生成文本

```bash
whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -of ~/Downloads/Deutschaufnahme_Text
```

完成后，在“下载”文件夹得到：

```text
Deutschaufnahme_Text.txt
```

`-t 12` 表示使用 12 个 CPU 线程。对 16 逻辑线程的 Intel i9 Mac，这是推荐设置：能比默认的 4 线程明显更快，同时保留资源给 macOS。若你的 Mac 只有 8 个逻辑线程，可改为 `-t 6`。

### 5.4 已经以默认 4 线程开始时，如何中断并重跑？

在正在转写的终端窗口按一次 `Control + C`（不是 `Command + C`）。这会停止当前任务并回到命令提示符；随后使用上一节带 `-t 12` 的命令重新执行即可。

打开这个 `.txt` 文件即可查看文字。

## 6. 同时生成字幕文件（可选）

若想要带时间轴的字幕，使用：

```bash
whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -osrt -ovtt -of ~/Downloads/Deutschaufnahme_Text
```

会生成：

- `.txt`：纯文字；
- `.srt`：常用视频字幕；
- `.vtt`：网页视频字幕。

## 7. 处理文件名有空格或中文的录音

把完整路径放进英文双引号即可。例如文件名为 `德语 10月4日.m4a`：

```bash
ffmpeg -i "$HOME/Downloads/德语 10月4日.m4a" -ar 16000 -ac 1 aufnahme.wav
```

转写命令不变。

## 8. 从 iPhone 导入录音

最简单的是在 iPhone 的“语音备忘录”中选择录音：

1. 点击 `…`；
2. 选择“共享”；
3. 选择 **AirDrop**；
4. 发到 Mac；
5. 保存到“下载”文件夹，再按第 5 节操作。

也可以通过 iCloud 同步到 Mac 的“语音备忘录”，然后把录音拖到“下载”文件夹。

## 9. 常见问题

### `brew: command not found`

尚未安装 Homebrew。按第 3.2 节安装后，关闭并重新打开终端，再执行命令。

### `whisper-cli: command not found`

重新执行：

```bash
brew install whisper-cpp
```

若刚刚安装过，请关闭并重新打开终端后再试。

### 找不到录音文件

在 Finder 中找到录音文件，然后直接拖到终端窗口。终端会自动填入完整路径；复制该路径并放到命令中即可。

### 德语识别结果不理想

- 保持 `-l de`，避免自动误判语言；
- 尽量使用原始录音，不要先用即时通信软件反复压缩；
- 说话人与麦克风距离近一些，减少环境声；
- 专业术语、人名、数字和口音仍应人工校对；
- 两个人重叠说话时，任何自动转写都会变差。

### 转写很慢

这是正常的，取决于录音长度和 Mac 性能。确认命令中已加入 `-t 12`（或适合你电脑的线程数）；还可让 Mac 接通电源、不要同时运行大型程序，必要时改用更小模型。

## 10. 隐私检查清单

- 只使用 `whisper-cli` 本地命令；
- 不需要 OpenAI API Key，也不要配置任何云端转写服务；
- 模型下载完后关闭 Wi-Fi，照样可以转写；
- 不要把录音拖到在线“AI transcription”网页；
- 重要文件转写后，若不再需要，可删除 `aufnahme.wav` 这个临时文件。

删除临时 WAV 的命令：

```bash
rm ~/whisper-local/aufnahme.wav
```

这只会删除转换产生的临时音频，不会删除原始 `.m4a` 录音和 `.txt` 文本。

## 11. 最短操作备忘

以后每次只需要：

```bash
cd ~/whisper-local
ffmpeg -i "$HOME/Downloads/你的录音.m4a" -ar 16000 -ac 1 aufnahme.wav
whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -of "$HOME/Downloads/转写结果"
```

## 官方项目

- [whisper.cpp 官方 GitHub 项目](https://github.com/ggml-org/whisper.cpp)
- [Homebrew 的 whisper.cpp 软件包页面](https://formulae.brew.sh/formula/whisper.cpp)

