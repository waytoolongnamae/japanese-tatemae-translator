# Changelog

## v2.0.0 - Kyoto-Style Update (2025-10-22)

### 🎌 Major Features

#### Kyoto-Style Tatemae (京都風建前)
- **Subtle Sarcasm**: Praise on the surface, criticism underneath
- **Context Preservation**: Each translation maintains specific details from input
- **Varied Outputs**: No more generic "one translation for many" responses
- **Cultural Authenticity**: Based on real Kyoto merchant communication patterns

#### Key Improvements
1. **Context-Aware Translation**
   - Mentions specific subjects (code, design, proposals, people)
   - Preserves original meaning while applying indirectness
   - Different inputs produce unique outputs

2. **Hidden Meanings**
   - "勉強になります" (educational) = useless/wrong
   - "参考にさせていただきます" (will reference) = won't use
   - "さすがですね" (impressive) = terrible
   - "検討させていただきます" (will consider) = not happening

3. **Plausible Deniability**
   - Sarcasm is subtle and cannot be used as evidence
   - Surface meaning is always polite and professional
   - True intent hidden beneath layers of courtesy

### 📝 Examples

**Before (Generic)**:
```
Input: "Your code is terrible"
Output: もう少し検討の余地があるかもしれません。

Input: "Your design is ugly"
Output: もう少し検討の余地があるかもしれません。
```
❌ Same generic response

**After (Context-Aware Kyoto-Style)**:
```
Input: "Your code is terrible"
Output: 誠に興味深いコードのご提案を拝見いたしました。
        大変勉強になるご発想で、さすがお考えがお深いと感服いたしております。

Input: "Your design is ugly"
Output: 誠に素敵なデザインでございますね。大変ユニークなご発想と拝見いたしました。
        私どもの狭い了見では、このような独創的なお考えに至るのは難しく...
```
✅ Each unique, context-specific, with hidden sarcasm

### 🔧 Technical Changes

#### Prompt Engineering
- Completely rewritten system prompt
- Japanese instructions for better LLM understanding
- Explicit Kyoto-style communication principles
- Temperature increased to 0.7 for more variety

#### Processing Pipeline
```
Input → Intent Detection → Template → Kyoto-Style Refinement → Output
                                              ↓
                                    - Preserve context
                                    - Add subtle sarcasm
                                    - Ensure grammar
                                    - Vary expression
```

### 📚 New Documentation

- **[KYOTO_STYLE.md](KYOTO_STYLE.md)**: Comprehensive guide to Kyoto-style communication
- **[IMPROVEMENTS.md](IMPROVEMENTS.md)**: Grammar improvement details
- Updated **[README.md](README.md)** with Kyoto-style examples
- Updated **[USAGE.md](USAGE.md)** with context-aware examples

### 🧪 Testing

All tests pass with new Kyoto-style translations:
```bash
python test_translator.py
# ALL TESTS PASSED! ✓
```

### 💡 Usage

No changes to CLI interface - improvements are automatic:

```bash
# Each produces unique, context-aware output
python cli.py -m "Your code is terrible"
python cli.py -m "Your design is ugly"
python cli.py -m "Your deadline is unrealistic"
```

---

## v1.0.0 - Initial Release

### Features
- Basic intent detection
- Template-based generation
- Three politeness levels
- Grammar refinement
- CLI interface
- Interactive mode
- Python API

### Components
- LangGraph workflow
- DeepSeek API integration
- Keyword-based fallback
- Command-line tool

---

## Comparison: v1.0 vs v2.0

| Aspect | v1.0 | v2.0 |
|--------|------|------|
| **Context** | Generic responses | Specific, context-aware |
| **Variety** | Repetitive | Unique for each input |
| **Style** | Simple polite | Kyoto-style subtle sarcasm |
| **Sarcasm** | None | Hidden beneath politeness |
| **Detail** | Lost specifics | Preserves all details |
| **Temperature** | 0.3 (consistent) | 0.7 (varied) |

## Migration Notes

### From v1.0 to v2.0

**No breaking changes** - all existing code continues to work.

The improvements are in the quality of translations:
- More context-aware
- More varied outputs
- Subtle Kyoto-style sarcasm
- Better preservation of original meaning

Simply update the code and enjoy better translations!

```bash
git pull origin main
# That's it - no code changes needed
```

## Future Roadmap

### Planned Features
- [ ] Language auto-translation (EN/ZH → JA)
- [ ] Fine-tuned intent classification
- [ ] Relationship context (上司/同僚/部下)
- [ ] Industry-specific templates
- [ ] LangGraph Studio visualization
- [ ] Web interface
- [ ] API service

### Under Consideration
- [ ] Reverse translation (建前 → 本音)
- [ ] Sarcasm intensity control
- [ ] Regional style variations (関西弁 etc.)
- [ ] Historical formality levels (古語 etc.)
- [ ] Audio output (TTS integration)

---

**Full documentation**: [README.md](README.md) | [KYOTO_STYLE.md](KYOTO_STYLE.md) | [USAGE.md](USAGE.md)
