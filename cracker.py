#!/usr/bin/env python3
"""
Password Cracker CLI
For educational and authorized security-testing use only.
 
Supports:
  - Dictionary attack against a target hash
  - Brute-force attack (small charset/length, for learning purposes)
  - Multiple hash algorithms (md5, sha1, sha256, sha512)
  - Optional salt
  - Multi-threading for speed
"""
 
import argparse
import hashlib
import itertools
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
 
 
def hash_candidate(candidate: str, algorithm: str, salt: str = "") -> str:
    """Hash a candidate password (optionally salted) with the given algorithm."""
    data = (salt + candidate).encode("utf-8", errors="ignore")
    return hashlib.new(algorithm, data).hexdigest()
 
 
def dictionary_attack(target_hash: str, wordlist_path: str, algorithm: str,
                       salt: str = "", threads: int = 4) -> str | None:
    """Try every word in a wordlist file against the target hash."""
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        words = [line.strip() for line in f if line.strip()]
 
    print(f"[*] Loaded {len(words)} candidate passwords from {wordlist_path}")
 
    found = None
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(hash_candidate, w, algorithm, salt): w for w in words
        }
        for i, future in enumerate(as_completed(futures)):
            word = futures[future]
            if future.result() == target_hash:
                found = word
                break
            if i % 5000 == 0 and i > 0:
                print(f"[*] Tried {i} candidates...")
 
    return found
 
 
def brute_force_attack(target_hash: str, algorithm: str, charset: str,
                        max_length: int, salt: str = "") -> str | None:
    """Try every combination of characters up to max_length."""
    for length in range(1, max_length + 1):
        print(f"[*] Trying length {length}...")
        for combo in itertools.product(charset, repeat=length):
            candidate = "".join(combo)
            if hash_candidate(candidate, algorithm, salt) == target_hash:
                return candidate
    return None
 
 
def main():
    parser = argparse.ArgumentParser(
        description="Educational password cracker (dictionary + brute force)."
    )
    parser.add_argument("--hash", required=True, help="Target hash to crack")
    parser.add_argument(
        "--algo", default="sha256",
        choices=["md5", "sha1", "sha256", "sha512"],
        help="Hash algorithm used to generate the target hash"
    )
    parser.add_argument("--salt", default="", help="Salt prepended to candidates, if any")
    parser.add_argument("--wordlist", help="Path to wordlist file for dictionary attack")
    parser.add_argument(
        "--bruteforce", action="store_true",
        help="Run brute-force attack instead of dictionary attack"
    )
    parser.add_argument(
        "--charset", default="abcdefghijklmnopqrstuvwxyz0123456789",
        help="Character set to use for brute force"
    )
    parser.add_argument(
        "--max-length", type=int, default=4,
        help="Max password length for brute force"
    )
    parser.add_argument("--threads", type=int, default=4, help="Thread count for dictionary attack")
 
    args = parser.parse_args()
 
    if not args.wordlist and not args.bruteforce:
        print("[!] You must specify either --wordlist or --bruteforce")
        sys.exit(1)
 
    start = time.time()
 
    if args.bruteforce:
        result = brute_force_attack(
            args.hash, args.algo, args.charset, args.max_length, args.salt
        )
    else:
        result = dictionary_attack(
            args.hash, args.wordlist, args.algo, args.salt, args.threads
        )
 
    elapsed = time.time() - start
 
    if result:
        print(f"\n[+] Password found: {result}")
    else:
        print("\n[-] Password not found.")
 
    print(f"[*] Time taken: {elapsed:.2f}s")
 
 
if __name__ == "__main__":
    main()
