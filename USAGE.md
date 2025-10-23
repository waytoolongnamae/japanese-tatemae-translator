# Japanese Hedging Translator - Usage Guide

## Quick Reference

### Command Line Usage

```bash
# 1. Interactive mode (easiest for multiple translations)
python cli.py

# 2. Single translation
python cli.py -m "Your message here"

# 3. With politeness level
python cli.py -m "Your message" -l ultra_polite

# 4. Quiet mode (just the translation)
python cli.py -m "Your message" -q

# 5. From stdin/pipe
echo "Your message" | python cli.py --stdin

# 6. Using wrapper script
./tatemae -m "Your message"
```

## Common Use Cases

### 1. Declining a Job Offer (Recruiter)

**Direct:** "I'm not interested in this job."

```bash
python cli.py -m "I'm not interested in this job."
```

**Output:** 貴重な情報をありがとうございます。魅力的なご提案ですが、今回は今後の参考とさせていただきます。

---

### 2. Giving Feedback on Work

**Direct:** "Your proposal is inefficient."

```bash
python cli.py -m "Your proposal is inefficient."
```

**Output:** 精査について、改善の余地があるかもしれないと感じました。

---

### 3. Declining a Meeting

**Direct:** "I can't meet this week."

```bash
python cli.py -m "I can't meet this week." -l ultra_polite
```

**Output:** 誠に恐縮ですが、現在社内調整中でして、別の機会にご相談できればと存じます。

---

### 4. Disagreeing with an Idea

**Direct:** "I disagree with that idea."

```bash
python cli.py -m "I disagree with that idea."
```

**Output:** ご意見ごもっともですが、もう少し慎重に考えたいと思っております。

---

### 5. Saying No to a Request

**Direct:** "That's not possible."

```bash
python cli.py -m "That's not possible." -l ultra_polite
```

**Output:** 誠に恐縮ですが、現在はスケジュールの都合上、今回はお断りさせていただきます。

---

## Politeness Levels Explained

### business (default)
Standard business Japanese. Use for:
- Colleagues at similar level
- Regular business correspondence
- Professional but not overly formal contexts

### ultra_polite
Very formal, heavy honorific usage. Use for:
- Senior management
- Important clients
- Formal business proposals
- First-time communications

### casual
Light polite form. Use for:
- Internal team communications
- Casual professional settings
- People you work closely with

## Interactive Mode Tips

Start interactive mode:
```bash
python cli.py
```

**Commands in interactive mode:**
- Just type your message and press Enter
- `:level business` - Switch to business level
- `:level ultra_polite` - Switch to ultra polite
- `:level casual` - Switch to casual
- `:help` - Show help
- `:quit` or `:q` - Exit

**Example session:**
```
> I'm not interested
⏳ Translating...
[Shows translation]

> :level ultra_polite
✓ Politeness level changed to: ultra_polite

> That won't work
⏳ Translating...
[Shows more polite translation]

> :q
👋 Goodbye!
```

## Integration Examples

### In a Shell Script

```bash
#!/bin/bash
# Translate all messages in a file

while IFS= read -r line; do
    echo "Original: $line"
    echo "Tatemae:  $(python cli.py -m "$line" -q)"
    echo "---"
done < messages.txt
```

### With Git Commit Messages

```bash
# Create a polite version of your commit message
COMMIT_MSG="This code is poorly written"
POLITE_MSG=$(python cli.py -m "$COMMIT_MSG" -q)
git commit -m "$POLITE_MSG"
```

### Email Response Helper

```bash
# Save your direct response to a file
echo "I don't think this will work" > direct_message.txt

# Get polite version
cat direct_message.txt | python cli.py --stdin -l ultra_polite -q > polite_message.txt

# Use polite_message.txt in your email
```

## Python API Usage

For programmatic usage:

```python
from translator import JapaneseTatemaeTranslator

# Initialize once
translator = JapaneseTatemaeTranslator()

# Translate multiple messages
messages = [
    "I'm not interested",
    "That's inefficient",
    "I can't make it"
]

for msg in messages:
    result = translator.translate(msg, level="business")
    print(f"Original: {msg}")
    print(f"Tatemae:  {result['tatemae_text']}")
    print(f"Intent:   {result['intent']}")
    print()
```

## Troubleshooting

### "No API key" warning
- Make sure you created `.env` file
- Check that `DEEPSEEK_API_KEY_CHAT` is set correctly
- The tool will fall back to keyword-based detection

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Permission denied on `./tatemae`
```bash
chmod +x tatemae
```

## Tips for Best Results

1. **Be specific**: Clear, direct messages work best
2. **Context matters**: Use `-c` flag when relevant
3. **Choose level carefully**: Match formality to situation
4. **Review output**: AI-generated, so review before using
5. **Use interactive mode**: Great for multiple translations

## Need Help?

```bash
python cli.py --help
```

Or check the main [README.md](README.md) for full documentation.
