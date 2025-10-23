# Kyoto-Style Tatemae (京都風建前)

## Overview

The translator now uses **Kyoto-style communication** - the art of being extremely polite on the surface while subtly conveying your true meaning underneath. Like a Kyoto merchant, it praises while actually criticizing, and says "yes" while meaning "no".

## What is Kyoto-Style Tatemae?

Kyoto has a famous reputation for indirect communication where:
- **Surface meaning**: Polite, humble, praising
- **Hidden meaning**: Criticism, refusal, sarcasm
- **Key principle**: The sarcasm is so subtle that it cannot be used as evidence against you

### Famous Kyoto Phrases

| Surface (What they say) | Hidden Meaning |
|-------------------------|----------------|
| 「お茶漬けでもどうどすか？」<br>("Won't you have some ochazuke?") | Please leave now |
| 「さすがのお考えですね」<br>("What an impressive idea") | That's a terrible idea |
| 「勉強になります」<br>("I learned so much") | This was useless |
| 「ぜひ参考にさせていただきます」<br>("I'll definitely reference this") | I'll never use this |

## How This Translator Implements Kyoto Style

### 1. Preserves Original Context

**Unlike generic translations**, each output maintains specific details from your input:

```bash
Input: "Your code is terrible"
Output: 大変興味深いコードのご提案を拝見いたしました。私どもには大変勉強になる斬新なアプローチでございます。

Input: "Your proposal is inefficient"
Output: 誠に素晴らしいご提案と拝見いたしました。さすがに独創的なお考えで、大変勉強になる内容でございます。

Input: "This design is ugly"
Output: おお、これはまた大変独創的なデザインでございますね。私どものような古い商いをしております者には、なかなか思い至らなかった発想で...
```

Notice how each mentions the specific subject (code, proposal, design).

### 2. Kyoto-Style Sarcasm Patterns

#### Pattern 1: Praise as Criticism
```bash
$ python cli.py -m "Your deadline is unrealistic and shows poor planning" -q
ご提示いただきました納期のご提案、大変意欲的なお考えと感心いたしました。
弊社といたしましても、より良いご提案ができるよう、改めて工程を精査させていただければと存じます。
```
**Surface**: Admiring the ambitious deadline
**Hidden**: The deadline is impossible and we need to revise it

#### Pattern 2: Learning = Useless
```bash
$ python cli.py -m "Your presentation was boring and I learned nothing" -l ultra_polite -q
大変貴重なご発表を拝聴させていただきました。誠に勉強になるお時間をいただき、
心より感謝申し上げます。今後の糧とさせていただきたく、謹んで参考にさせていただきます。
```
**Surface**: So educational and valuable!
**Hidden**: Complete waste of time

#### Pattern 3: "Will Consider" = No
```bash
$ python cli.py -m "I don't want to work with John anymore" -q
ジョンさんには大変お世話になっております。ただ、今後のプロジェクトにつきましては、
より多様なスキルセットをお持ちの方々との協働も検討させていただきたく存じます。
```
**Surface**: Thank you John, we're just considering other options
**Hidden**: I'm done working with John

### 3. Context-Aware Variations

The same intent produces different outputs based on specific context:

**Criticism Examples:**

```bash
# About code
$ python cli.py -m "Your code is terrible" -q
大変興味深いコードのご提案を拝見いたしました。私どもには大変勉強になる斬新なアプローチでございます。
今後の参考にさせていただき、より良い方向へと発展させていただきたく存じます。

# About design
$ python cli.py -m "This design is ugly" -q
おお、これはまた大変独創的なデザインでございますね。私どものような古い商いをしております者には、
なかなか思い至らなかった発想で、大変勉強させていただきました。今後の参考にしっかりとさせていただきたく存じます。

# About proposal
$ python cli.py -m "Your proposal will never work" -q
さすがに独創的なご提案で、大変勉強になります。現実の様々な事情を考慮いたしますと、
実現にはさらなる工夫が必要かもしれませんね。今後の参考とさせていただきます。
```

Each maintains the specific subject while using Kyoto-style indirect praise-as-criticism.

## Politeness Level Variations

The Kyoto style adapts to different formality levels:

### Business (Standard)
Polite but measured praise:
```
誠に素晴らしいご提案と拝見いたしました。
```

### Ultra Polite (Formal)
Over-the-top praise (more obvious sarcasm to those who know):
```
大変貴重なご発表を拝聴させていただきました。
誠に勉強になるお時間をいただき、心より感謝申し上げます。
```

### Casual (Relaxed)
Still polite but more natural:
```
もう少しブラッシュアップの余地がありそうですね。
```

## Key Features of Kyoto-Style Translation

### ✅ What It Does:

1. **Preserves Specific Context**: Mentions code, proposals, meetings, people by name
2. **Subtle Sarcasm**: Praises while criticizing underneath
3. **Plausible Deniability**: Cannot be used as evidence of rudeness
4. **Context-Aware**: Different inputs = different outputs
5. **Culturally Authentic**: Based on real Kyoto communication patterns

### ❌ What It Avoids:

1. **Generic Responses**: Each translation is unique to the input
2. **Obvious Sarcasm**: The irony is always subtle
3. **Direct Refusal**: Never says "no" directly
4. **Repetitive Phrases**: Varied expressions for similar intents

## Examples by Category

### 1. Criticism

```bash
# Terrible code
$ python cli.py -m "Your code is full of bugs and poorly written" -q
誠に興味深いコードのご提案をいただき、大変勉強になります。
今後の参考とさせていただきたく、じっくりと拝見させていただきました。
```
*Translation: Your code is so "interesting" (bad) that it was "educational" (to see what not to do)*

### 2. Refusal

```bash
# Don't want to attend
$ python cli.py -m "I'm not attending because the venue is too far" -q
会場の場所につきましては、さすがに遠方でいらっしゃいますね。
せっかくのお誘いではございますが、このたびは参加を見合わせていただきたく存じます。
```
*Translation: The venue choice was "bold" (terrible), so I'll "refrain" (not coming)*

### 3. Disagreement

```bash
# Won't work
$ python cli.py -m "Your proposal will never work in the real world" -q
さすがに独創的なご提案で、大変勉強になります。
現実の様々な事情を考慮いたしますと、実現にはさらなる工夫が必要かもしれませんね。
```
*Translation: So "original" (impractical) that it "needs more work" (won't happen)*

### 4. Annoyance

```bash
# Stop emailing me
$ python cli.py -m "Stop bothering me with these emails" -q
ご連絡いただき誠にありがとうございます。メールの内容は大変興味深く拝見いたしました。
今後の業務の効率化を考えますと、より適切なタイミングで改めてご連絡差し上げる方がよろしいかと存じます。
```
*Translation: Thanks for the emails (that I don't want), let's be "efficient" (stop)*

## Pro Tips

### 1. More Specific Input = Better Output

**Generic:**
```bash
$ python cli.py -m "I don't like it" -q
# Less context preserved
```

**Specific:**
```bash
$ python cli.py -m "I don't like your color scheme in this UI design" -q
# Mentions color scheme and UI specifically
```

### 2. Use Context Flag for Better Results

```bash
python cli.py -m "Your proposal is terrible" -c business
# Adds business context for more appropriate response
```

### 3. Level Choice Affects Sarcasm Intensity

- **Business**: Balanced, professional Kyoto style
- **Ultra Polite**: More exaggerated praise (stronger hidden sarcasm)
- **Casual**: More direct but still polite

## The Art of Reading Between the Lines

In Kyoto-style communication, these are red flags:

| Phrase | Hidden Meaning |
|--------|----------------|
| 参考にさせていただきます | We won't use it |
| 勉強になります | Useless/wrong |
| 検討させていただきます | Not happening |
| さすがですね | That's terrible |
| 独創的ですね | Impractical/weird |
| 意欲的ですね | Unrealistic |

## Cultural Note

This style is based on real Kyoto merchant culture, where maintaining harmony (和) is paramount. Direct confrontation damages relationships, so criticism is wrapped in compliments. The recipient should understand the hidden meaning, but the speaker maintains plausible deniability.

## Testing

Try these examples to see the variety:

```bash
# Different criticisms
python cli.py -m "Your code is terrible"
python cli.py -m "Your design is ugly"
python cli.py -m "Your presentation was boring"

# Same input, different levels
python cli.py -m "This won't work" -l business
python cli.py -m "This won't work" -l ultra_polite
python cli.py -m "This won't work" -l casual
```

Each will produce unique, context-aware Kyoto-style responses!
