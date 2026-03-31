"""
gRPC: protobuf stubs live under ``generated/`` with import paths like ``payment.v1``.

The compiler emits absolute imports from those package roots; we prepend ``generated``
to ``sys.path`` once so those imports resolve without a separate pip package.
"""

from __future__ import annotations

import sys
from pathlib import Path

_gen_root = Path(__file__).resolve().parent / "generated"
if _gen_root.is_dir() and str(_gen_root) not in sys.path:
    sys.path.insert(0, str(_gen_root))
