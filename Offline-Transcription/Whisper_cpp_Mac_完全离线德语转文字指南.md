# whisper.cpp：Mac 完全离线转文字与自动区分说话人指南

这份指南把德语或中文录音在自己的 Mac 上转成文字。首次安装软件与下载模型需要联网；模型下载完后，**转换音频、语音识别和说话人区分均可在关闭 Wi-Fi 的情况下完成**。音频不会上传至云端。

适合：自己的德语/中文录音、学习录音、个人口述笔记，以及 3–4 人的对话录音。

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

## 5. 日常离线转写：一条命令完成

下面假设录音文件名为 `Deutschaufnahme.m4a`，并放在 Mac 的“下载”文件夹中。

在终端完整复制并执行下面这一**条命令**：

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/Deutschaufnahme.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -of "$HOME/Downloads/Deutschaufnahme_Text"
```

这条命令会依次完成：

1. 进入 `whisper-local` 工作文件夹；
2. 把 `.m4a` 录音在本机转换为临时 `aufnahme.wav`；
3. 用 12 个 CPU 线程按德语转写；
4. 在“下载”文件夹生成文本结果。

两个 `&&` 表示“前一步成功后才继续下一步”。`-y` 表示自动覆盖上一次生成的临时 WAV 文件。把 `Deutschaufnahme.m4a` 替换为你的真实录音文件名即可。

完成后，在“下载”文件夹得到：

```text
Deutschaufnahme_Text.txt
```

`-t 12` 表示使用 12 个 CPU 线程。对 16 逻辑线程的 Intel i9 Mac，这是推荐设置：能比默认的 4 线程明显更快，同时保留资源给 macOS。若你的 Mac 只有 8 个逻辑线程，可改为 `-t 6`。

### 5.1 已经以默认 4 线程开始时，如何中断并重跑？

在正在转写的终端窗口按一次 `Control + C`（不是 `Command + C`）。这会停止当前任务并回到命令提示符；随后使用上一节带 `-t 12` 的命令重新执行即可。

打开这个 `.txt` 文件即可查看文字。

## 6. 同时生成字幕文件（可选）

若想要带时间轴的字幕，使用下面的一条命令：

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/Deutschaufnahme.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -osrt -ovtt -of "$HOME/Downloads/Deutschaufnahme_Text"
```

会生成：

- `.txt`：纯文字；
- `.srt`：常用视频字幕；
- `.vtt`：网页视频字幕。

## 7. 处理文件名有空格或中文的录音

把完整路径放进英文双引号即可。例如文件名为 `德语 10月4日.m4a`：

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/德语 10月4日.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -of "$HOME/Downloads/转写结果"
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

## 11. 中文转写

你已经下载的 `large-v3-turbo` 同样支持中文，不需要另下载 Whisper 模型。把转写命令中的 `-l de` 改为 `-l zh` 即可：

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/中文录音.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l zh -otxt -oj -of "$HOME/Downloads/中文转写结果"
```

这会生成 `中文转写结果.txt` 和 `中文转写结果.json`。后一个 JSON 含有每段话的时间戳，是自动合并说话人标签所必需的。

## 12. 自动区分说话人：准备工作（只需一次）

Whisper 负责“说了什么”，另一个开源本地模型 `pyannote Community-1` 负责“谁在什么时候说话”。它输出的是 `SPEAKER_00`、`SPEAKER_01` 等声音标签，而不会知道真实姓名。

> 对三四人中文对话：若你确认恰好有 3 人或 4 人，固定人数通常更稳定；若人数不确定，就让程序自动估计。

### 12.1 保持 Wi-Fi 开启，安装本地运行环境

在终端运行：

```bash
brew install python@3.11 git-lfs
python3.11 -m venv "$HOME/whisper-local/diarization-env"
source "$HOME/whisper-local/diarization-env/bin/activate"
python -m pip install --upgrade pip
pip install pyannote.audio
git lfs install
```

这些命令只是在 Mac 上安装 Python 与本地模型运行程序。安装可能需要数分钟；Intel i9 + 64 GB 内存足够使用。

### 12.2 一次性下载说话人模型

1. 打开 <https://huggingface.co>，免费注册或登录；
2. 打开 <https://huggingface.co/pyannote/speaker-diarization-community-1>；
3. 接受该模型的使用条款；
4. 在 Hugging Face 的 Token 页面创建一个只读（read）访问令牌；
5. 回到终端并执行：

```bash
cd "$HOME/whisper-local"
git clone https://hf.co/pyannote/speaker-diarization-community-1 pyannote-speaker-diarization-community-1
```

终端询问账号时输入 Hugging Face 用户名；询问密码时粘贴刚创建的访问令牌。输入密码时屏幕不显示字符是正常的。

模型下载结束、终端重新出现提示符后，语音转写和分人都能离线运行。建议随后关闭 Wi-Fi。

### 12.3 保存合并脚本

将本指南配套的 `speaker_labeled_transcript.py` 保存到：

```text
/Users/macw/whisper-local/speaker_labeled_transcript.py
```

在 Finder 中，`~` 等于你的个人文件夹 `/Users/macw`。保存后在终端检查：

```bash
ls "$HOME/whisper-local/speaker_labeled_transcript.py"
```

只要显示该路径，脚本就准备好了。

#### 更新脚本（仅在提示本地模型路径错误时需要）

如果第 13.2 步报错 `HFValidationError`，并把本地路径误认为 Hugging Face 仓库名，请暂时打开 Wi-Fi，然后执行以下命令覆盖为修正版脚本：

```bash
curl -L "https://raw.githubusercontent.com/XiaguGHW/python-script-notiz/main/Offline-Transcription/speaker_labeled_transcript.py" -o "$HOME/whisper-local/speaker_labeled_transcript.py"
```

命令执行完后，重新运行原来的第 13.2 步即可；无需重新下载说话人模型，也无需修改第 13.2 步命令。

## 13. 每次处理中文或德语多人录音

### 13.1 第一步：用 Whisper 转写，并导出带时间戳的 JSON

中文录音（整行复制到终端执行）：

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/中文多人录音.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l zh -otxt -oj -of "$HOME/Downloads/中文多人录音_Whisper"
```

这是一条完整命令：它会先转换音频，再转写中文，并生成文字和带时间戳的 JSON。你只需按需要改下面两处：

- **原始录音名**：把 `中文多人录音.m4a` 改为“下载”文件夹中你的实际录音文件名；保留 `.m4a`（或按实际格式改为 `.mp3`、`.wav` 等）。
- **输出文件名前缀**：把 `中文多人录音_Whisper` 改为你希望的结果名，例如 `会议10月8日_Whisper`。程序会自动生成同名的 `.txt` 和 `.json` 文件。

例如，录音文件叫 `项目会议.m4a`，希望结果叫 `项目会议_Whisper`，就把命令中的两个中文位置分别替换为这两个名称。文件名含中文或空格无需额外处理，因为路径已放在英文双引号中。

德语录音只需把 `-l zh` 改为 `-l de`：

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/德语多人录音.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -oj -of "$HOME/Downloads/德语多人录音_Whisper"
```

德语命令中同样只改“原始录音名”和“输出文件名前缀”；不要改 `-l de`.

### 13.2 第二步：本地自动区分说话人，并与文字合并

以下例子假设录音中**恰好 4 人**：

```bash
source "$HOME/whisper-local/diarization-env/bin/activate" && PYANNOTE_METRICS_ENABLED=0 HF_HUB_OFFLINE=1 python "$HOME/whisper-local/speaker_labeled_transcript.py" --audio "$HOME/whisper-local/aufnahme.wav" --whisper-json "$HOME/Downloads/中文多人录音_Whisper.json" --pipeline "$HOME/whisper-local/pyannote-speaker-diarization-community-1" --speakers 4 --output "$HOME/Downloads/中文多人录音_按说话人.txt"
```

- `--speakers 4`：录音确定恰好四人时保留；三人就改为 `--speakers 3`。
- 若人数不确定：删除整段 `--speakers 4`，让模型自行估计。
- `HF_HUB_OFFLINE=1`：禁止 Hugging Face 访问网络；`PYANNOTE_METRICS_ENABLED=0`：关闭可选的匿名使用统计。

输出文件在“下载”文件夹，例如：

```text
[00:00:03] SPEAKER_00: 大家好，我们现在开始。
[00:00:08] SPEAKER_02: 我先说一下……
[00:00:16] SPEAKER_00: 好的。
```

先听每个编号最早的一句话，再把文本里的 `SPEAKER_00`、`SPEAKER_01` 等替换为真实姓名即可。

### 13.3 可直接复制的完整示例

以下假设两个原始录音都在“下载”文件夹中：德语录音名为 `test_de.m4a`，中文录音名为 `test_zh.m4a`。每一种语言都先执行“转写”，等它完成后，再执行对应的“区分说话人”。以下例子设定为**恰好 4 位说话人**；如为 3 人，把 `--speakers 4` 改为 `--speakers 3`。

#### 德语：`test_de.m4a`

**1. 转写并生成 JSON：**

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/test_de.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -oj -of "$HOME/Downloads/test_de_Whisper"
```

**2. 区分说话人并合并文字：**

```bash
source "$HOME/whisper-local/diarization-env/bin/activate" && PYANNOTE_METRICS_ENABLED=0 HF_HUB_OFFLINE=1 python "$HOME/whisper-local/speaker_labeled_transcript.py" --audio "$HOME/whisper-local/aufnahme.wav" --whisper-json "$HOME/Downloads/test_de_Whisper.json" --pipeline "$HOME/whisper-local/pyannote-speaker-diarization-community-1" --speakers 4 --output "$HOME/Downloads/test_de_按说话人.txt"
```

最后会得到：`test_de_Whisper.txt`、`test_de_Whisper.json` 和 `test_de_按说话人.txt`。

#### 中文：`test_zh.m4a`

**1. 转写并生成 JSON：**

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/test_zh.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l zh -otxt -oj -of "$HOME/Downloads/test_zh_Whisper"
```

**2. 区分说话人并合并文字：**

```bash
source "$HOME/whisper-local/diarization-env/bin/activate" && PYANNOTE_METRICS_ENABLED=0 HF_HUB_OFFLINE=1 python "$HOME/whisper-local/speaker_labeled_transcript.py" --audio "$HOME/whisper-local/aufnahme.wav" --whisper-json "$HOME/Downloads/test_zh_Whisper.json" --pipeline "$HOME/whisper-local/pyannote-speaker-diarization-community-1" --speakers 4 --output "$HOME/Downloads/test_zh_按说话人.txt"
```

最后会得到：`test_zh_Whisper.txt`、`test_zh_Whisper.json` 和 `test_zh_按说话人.txt`。

## 14. 结果质量与限制

- 录音清晰、每个人轮流发言时，三四人通常可以较好分开。
- 多人同时抢话、远距离收音、餐厅噪声或有人说话很少时，可能误分、合并两个人或多分出一个人。
- 两个人声音很像、电话扬声器回声很重时，结果也会变差。
- 这项功能不认识“身份”，只把同一种声音归为同一个编号；请人工听开头进行命名确认。
- 建议保留原始 `.m4a`，并将最终文本快速抽听校对。

## 15. 最短操作备忘

以后每次只需要：

```bash
cd "$HOME/whisper-local" && ffmpeg -y -i "$HOME/Downloads/你的录音.m4a" -ar 16000 -ac 1 aufnahme.wav && whisper-cli -t 12 -m models/ggml-large-v3-turbo.bin -f aufnahme.wav -l de -otxt -of "$HOME/Downloads/转写结果"
```

## 官方项目

- [whisper.cpp 官方 GitHub 项目](https://github.com/ggml-org/whisper.cpp)
- [Homebrew 的 whisper.cpp 软件包页面](https://formulae.brew.sh/formula/whisper.cpp)
