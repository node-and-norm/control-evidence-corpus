#!/usr/bin/env python3
"""Compatibility command: validate the existing prototype; never regenerate evidence.
The original builder remains at baseline commit ab5140f9 for historical reproduction.
"""
from check_catholic_agent_package import main
if __name__=='__main__':
    raise SystemExit(main())
