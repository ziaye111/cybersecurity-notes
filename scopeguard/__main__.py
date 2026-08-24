"""Allow ``python -m scopeguard`` to behave like the installed command."""

from .cli import main


if __name__ == "__main__":
    raise SystemExit(main())
