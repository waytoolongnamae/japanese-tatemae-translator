#!/usr/bin/env python3
"""
Command-line interface for Japanese Hedging Translator
"""
import argparse
import sys
import os
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from translator import JapaneseTatemaeTranslator
from processing.nodes import initialize_provider, get_provider_info


def print_colored(text, color_code):
    """Print colored text to terminal"""
    print(f"\033[{color_code}m{text}\033[0m")


def print_result(result):
    """Pretty print translation result"""
    print("\n" + "=" * 80)
    print_colored("📝 Translation Result:", "1;36")
    print("=" * 80)
    print_colored(result["tatemae_text"], "1;32")
    print("\n" + "-" * 80)
    print(f"Intent:     {result['intent']}")
    print(f"Confidence: {result.get('confidence', 0):.2%}")
    print(f"Level:      {result['level']}")
    if result.get('detected_language'):
        print(f"Language:   {result['detected_language']}")
    print("=" * 80 + "\n")


def interactive_mode(translator):
    """Run translator in interactive mode"""
    print_colored("\n🇯🇵 Japanese Hedging Translator - Interactive Mode", "1;35")
    print("=" * 80)
    print("Transform direct messages into polite Japanese 建前 expressions")

    # Display model information
    provider_info = get_provider_info()
    print_colored(f"\n🤖 Model: {provider_info['provider']} ({provider_info['model']})", "1;34")

    print("\nCommands:")
    print("  - Type your message (multi-line supported)")
    print("  - Press Esc then Enter (or Meta+Enter) to translate")
    print("  - ':level <business|ultra_polite|casual>' - Change politeness level")
    print("  - ':model' - Show current model information")
    print("  - ':help' - Show this help")
    print("  - ':quit' or ':q' - Exit")
    print("=" * 80 + "\n")

    current_level = "business"
    print(f"Current politeness level: {current_level}")

    # Set up key bindings for multi-line input
    kb = KeyBindings()

    @kb.add('escape', 'enter')  # Meta+Enter (Cmd+Enter on Mac, Alt+Enter on others)
    def _(event):
        """Submit on Cmd+Enter (Mac) or Alt+Enter (others)"""
        event.current_buffer.validate_and_handle()

    while True:
        try:
            # Get user input with multi-line support
            user_input = prompt(
                "\n> ",
                multiline=True,
                key_bindings=kb,
                prompt_continuation="  "
            ).strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith(':'):
                cmd = user_input[1:].lower()

                if cmd in ['quit', 'q', 'exit']:
                    print_colored("\n👋 Goodbye!", "1;33")
                    break

                elif cmd == 'help':
                    print("\nCommands:")
                    print("  Type your message (multi-line supported)")
                    print("  Press Esc then Enter (or Meta+Enter) to translate")
                    print("  :level <business|ultra_polite|casual> - Change politeness level")
                    print("  :model                                 - Show current model information")
                    print("  :help                                  - Show this help")
                    print("  :quit or :q                           - Exit")
                    continue

                elif cmd == 'model':
                    provider_info = get_provider_info()
                    print_colored(f"\n🤖 Current Model:", "1;36")
                    print(f"  Provider: {provider_info['provider']}")
                    print(f"  Model:    {provider_info['model']}")
                    continue

                elif cmd.startswith('level '):
                    level = cmd.split(' ', 1)[1].strip()
                    if level in ['business', 'ultra_polite', 'casual']:
                        current_level = level
                        print_colored(f"✓ Politeness level changed to: {current_level}", "1;32")
                    else:
                        print_colored("✗ Invalid level. Use: business, ultra_polite, or casual", "1;31")
                    continue

                else:
                    print_colored(f"✗ Unknown command: {cmd}", "1;31")
                    continue

            # Translate the message
            print_colored("\n⏳ Translating...", "1;33")
            result = translator.translate(user_input, level=current_level)
            print_result(result)

        except KeyboardInterrupt:
            print_colored("\n\n👋 Goodbye!", "1;33")
            break
        except Exception as e:
            print_colored(f"\n✗ Error: {e}", "1;31")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Japanese Hedging Translator - Transform direct messages into polite 建前 expressions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python cli.py

  # Translate a single message
  python cli.py -m "I'm not interested in this job."

  # With custom politeness level
  python cli.py -m "That's not possible." -l ultra_polite

  # Pipe input
  echo "I disagree with that idea." | python cli.py --stdin

  # Show only the translated text
  python cli.py -m "I can't meet this week." --quiet
        """
    )

    parser.add_argument(
        '-m', '--message',
        type=str,
        help='Message to translate'
    )

    parser.add_argument(
        '-l', '--level',
        type=str,
        choices=['business', 'ultra_polite', 'casual'],
        default='business',
        help='Politeness level (default: business)'
    )

    parser.add_argument(
        '-c', '--context',
        type=str,
        choices=['business', 'personal', 'recruiter'],
        help='Optional context for translation'
    )

    parser.add_argument(
        '--stdin',
        action='store_true',
        help='Read input from stdin'
    )

    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Output only the translated text'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode (default if no message provided)'
    )

    parser.add_argument(
        '--model',
        type=str,
        choices=['deepseek', 'openai'],
        help='LLM provider to use (deepseek or openai)'
    )

    args = parser.parse_args()

    # Initialize provider if model is specified
    if args.model:
        initialize_provider(args.model)

    # Initialize translator
    try:
        translator = JapaneseTatemaeTranslator()
    except Exception as e:
        print_colored(f"✗ Failed to initialize translator: {e}", "1;31")
        sys.exit(1)

    # Interactive mode
    if args.interactive or (not args.message and not args.stdin):
        interactive_mode(translator)
        return

    # Get input message
    if args.stdin:
        message = sys.stdin.read().strip()
    elif args.message:
        message = args.message
    else:
        print_colored("✗ No message provided. Use -m or --stdin", "1;31")
        sys.exit(1)

    if not message:
        print_colored("✗ Empty message", "1;31")
        sys.exit(1)

    # Translate
    try:
        result = translator.translate(
            message,
            level=args.level,
            context=args.context
        )

        if args.quiet:
            print(result["tatemae_text"])
        else:
            print_result(result)

    except Exception as e:
        print_colored(f"✗ Translation error: {e}", "1;31")
        sys.exit(1)


if __name__ == "__main__":
    main()
