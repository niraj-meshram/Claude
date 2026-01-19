#!/usr/bin/env python3
"""
Quick example script to demonstrate the LinkedIn Post Generator.
This runs the system with a sample topic.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.crew_orchestrator import LinkedInPostGenerator
from src.config import get_settings
from src.utils import print_header, print_error, print_success, print_info, console


def main():
    """Run an example post generation."""
    print_header()

    # Example topic
    topic = "Latest trends in AI agents and autonomous systems 2026"

    print_info("🎯 This is an example run of the LinkedIn Post Generator")
    print_info(f"📝 Topic: {topic}\n")

    try:
        # Check configuration
        try:
            settings = get_settings()
            print_success("✅ Configuration loaded")
        except Exception as e:
            print_error(f"❌ Configuration error: {e}")
            print_info("\n📋 Setup instructions:")
            print_info("1. Copy .env.example to .env")
            print_info("2. Add your Anthropic API key to .env")
            print_info("3. Get API key from: https://console.anthropic.com/\n")
            return

        # Generate post
        print_info("🚀 Starting autonomous post generation...\n")
        generator = LinkedInPostGenerator()
        result = generator.generate_post(topic)

        # Show success
        console.print("\n")
        print_success("✨ Example completed successfully!")
        print_info(f"📁 Post saved to: {result['filename']}")
        print_info("\n💡 Try it yourself:")
        print_info('   python main.py generate --topic "Your topic here"')

    except KeyboardInterrupt:
        print_error("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"❌ Error: {e}")
        console.print_exception()
        sys.exit(1)


if __name__ == '__main__':
    main()
