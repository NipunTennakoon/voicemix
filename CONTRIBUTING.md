# Contributing to VoiceMix

Thank you for your interest in contributing to VoiceMix! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version, etc.)
- Screenshots if applicable

### Suggesting Enhancements

We welcome suggestions! Please open an issue with:
- A clear description of the enhancement
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, commented code
   - Follow the existing code style
   - Add tests if applicable

3. **Test your changes**
   - Ensure existing tests pass
   - Add new tests for new features
   - Test on your target platform

4. **Commit your changes**
   - Use clear, descriptive commit messages
   - Reference issues when applicable

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Describe your changes clearly
   - Link related issues
   - Request review from maintainers

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NipunTennakoon/voicemix.git
   cd voicemix
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install pytest black  # Development tools
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

4. **Format code**
   ```bash
   black src/ tests/
   ```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and modular
- Comment complex logic

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Test on multiple platforms if possible

## Documentation

- Update README.md if you change functionality
- Update docstrings for modified functions
- Add examples for new features
- Update user guides if applicable

## Project Structure

```
voicemix/
├── src/              # Source code
│   ├── voicemix_app.py      # Main GUI application
│   ├── audio_processor.py   # Audio processing logic
│   └── config.py            # Configuration
├── tests/            # Unit tests
├── docs/             # Documentation
├── resources/        # Images, icons, etc.
└── output/          # Processed files (gitignored)
```

## Areas for Contribution

We especially welcome contributions in:

1. **Audio Processing**
   - Better speaker diarization
   - Neural voice conversion integration
   - Audio quality improvements

2. **User Interface**
   - UI/UX improvements
   - Additional features (batch processing, etc.)
   - Accessibility enhancements

3. **Documentation**
   - Tutorials and guides
   - Code examples
   - Translations

4. **Testing**
   - More comprehensive tests
   - Performance testing
   - Edge case coverage

5. **Platform Support**
   - macOS specific improvements
   - Linux compatibility
   - Mobile support (future)

## Getting Help

- Open an issue for questions
- Check existing issues and documentation
- Reach out to maintainers via GitHub

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Maintain a positive environment

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

Thank you for contributing to VoiceMix! 🎵
