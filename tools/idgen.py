#!/usr/bin/env python3
import os
import time
import base64
from datetime import datetime, timezone

# Crockford Base32 alphabet (no I,L,O,U)
ALPH = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

def crockford32(b: bytes) -> str:
  # Encode bytes into Crockford Base32 without padding.
  n = int.from_bytes(b, "big")
  out = []
  # 128 bits -> up to 26 chars; we’ll do fixed width for stability.
  for _ in range(26):
    out.append(ALPH[n & 31])
    n >>= 5
  return "".join(reversed(out))

def now_iso_utc() -> str:
  return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def ulid() -> str:
  # 48 bits time (ms) + 80 bits randomness
  ms = int(time.time() * 1000)
  time_bytes = ms.to_bytes(6, "big")
  rand_bytes = os.urandom(10)
  return crockford32(time_bytes + rand_bytes)

if __name__ == "__main__":
  print(f"now={now_iso_utc()}")
  print(f"ulid={ulid()}")
