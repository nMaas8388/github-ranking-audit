# Contributing

Thanks for your interest.

## How to contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-change`
3. Test your changes: `python ranking_audit.py torvalds/linux --json`
4. Commit with a clear message
5. Push and open a pull request

## Reporting bugs

Open an issue with:
- The command you ran
- Expected vs actual output
- Python version

## Adding new scoring signals

Each signal follows the same pattern: a `score_` function that returns 0-100. Add your function, give it a weight in the `weights` dict, and it's automatically included in the audit.
