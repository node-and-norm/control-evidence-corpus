#!/usr/bin/env python3
"""Historical import/CLI path forwarding to the single installed trace module."""
from cec_agents.tracing import (VERSION, APPROVALS, KNOWN_KIND, CaptureError,
    canonical,sha256_bytes,utc_now,validate_manifest,verify_events,verify_run,
    promotion_gate,record_call,main)
if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (CaptureError,OSError,ValueError) as exc:
        print('CAPTURE GATE BLOCKED:',str(exc))
        raise SystemExit(2)
