# 🇯🇵 Japanese Hedging Translator - Quick Start

Transform direct messages into polite Japanese 建前 expressions

## Installation (One-time)

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your DeepSeek API key
```

## Basic Usage

### 1️⃣ Interactive Mode (Easiest!)

```bash
python cli.py
```

Then just type your messages:
```
> I'm not interested in this job.
> I disagree with that idea.
> :q  # to quit
```

### 2️⃣ Single Translation

```bash
python cli.py -m "Your direct message here"
```

### 3️⃣ With Politeness Level

```bash
# Standard business (default)
python cli.py -m "I can't do this"

# Very formal/polite
python cli.py -m "I can't do this" -l ultra_polite

# Casual but polite
python cli.py -m "I can't do this" -l casual
```

### 4️⃣ Quiet Mode (Just Translation)

```bash
python cli.py -m "Your message" -q
```

### 5️⃣ With Pipes

```bash
echo "I'm not interested" | python cli.py --stdin -q
```

## Examples

### Declining a Job
```bash
$ python cli.py -m "I'm not interested in this job." -q
貴重な情報をありがとうございます。魅力的なご提案ですが、今回は今後の参考とさせていただきます。
```

### Giving Criticism
```bash
$ python cli.py -m "Your proposal is inefficient." -q
精査について、改善の余地があるかもしれないと感じました。
```

### Declining a Meeting
```bash
$ python cli.py -m "I can't meet this week." -l ultra_polite -q
誠に恐縮ですが、現在社内調整中でして、別の機会にご相談できればと存じます。
```

### Disagreeing
```bash
$ python cli.py -m "I disagree with that idea." -q
ご意見ごもっともですが、もう少し慎重に考えたいと思っております。
```

## Quick Tips

✅ Use **interactive mode** for multiple translations
✅ Use **business level** (default) for most situations
✅ Use **ultra_polite** for senior management or important clients
✅ Use **-q flag** when you just want the translation
✅ Pipe with other commands for automation

## Politeness Levels

| Level | Use For |
|-------|---------|
| `business` | Colleagues, regular business (default) |
| `ultra_polite` | Senior management, formal situations |
| `casual` | Internal team, casual professional |

## Interactive Commands

| Command | Description |
|---------|-------------|
| `<message>` | Translate the message |
| `:level business` | Change to business level |
| `:level ultra_polite` | Change to ultra polite |
| `:level casual` | Change to casual |
| `:help` | Show help |
| `:quit` or `:q` | Exit |

## Python API

```python
from translator import JapaneseTatemaeTranslator

translator = JapaneseTatemaeTranslator()
result = translator.translate("Your message", level="business")
print(result["tatemae_text"])
```

## More Help

- Full documentation: [README.md](README.md)
- Detailed usage examples: [USAGE.md](USAGE.md)
- CLI help: `python cli.py --help`

---

**Pro tip:** Add an alias to your shell:
```bash
alias tatemae='python /path/to/winwin/cli.py'
```

Then just use: `tatemae -m "Your message"`
