# Password Cracker (Educational)

A command-line tool that demonstrates dictionary and brute-force password
cracking techniques against hashed passwords. Built as a learning project
to understand hashing, wordlists, and search-space complexity.

> **⚠️ Disclaimer:** This tool is for educational purposes and authorized
> security testing only. Do not use it against systems, accounts, or hashes
> you do not own or do not have explicit written permission to test.
> Unauthorized access to computer systems is illegal in most jurisdictions.

## Features

- Dictionary attack using a wordlist file
- Brute-force attack over a configurable character set and max length
- Supports MD5, SHA-1, SHA-256, SHA-512
- Optional salt support
- Multi-threaded dictionary attack for speed

## Installation

```bash
git clone https://github.com/yourusername/password-cracker.git
cd password-cracker
```

No external dependencies are required — it only uses the Python standard
library (`hashlib`, `itertools`, `concurrent.futures`, `argparse`).

Requires Python 3.10+.

## Usage

### Dictionary attack

```bash
python cracker.py --hash <target_hash> --algo sha256 --wordlist wordlists/sample_wordlist.txt
```

### Brute-force attack

```bash
python cracker.py --hash <target_hash> --algo sha256 --bruteforce --charset abcdefghijklmnopqrstuvwxyz0123456789 --max-length 4
```

### With a salt

```bash
python cracker.py --hash <target_hash> --algo sha256 --salt mysalt --wordlist wordlists/sample_wordlist.txt
```

## Example

Generate a test hash:

```bash
python3 -c "import hashlib; print(hashlib.sha256('admin'.encode()).hexdigest())"
```

Crack it:

```bash
python cracker.py --hash <paste_hash_here> --algo sha256 --wordlist wordlists/sample_wordlist.txt
```

Expected output:

```
[*] Loaded 15 candidate passwords from wordlists/sample_wordlist.txt
[+] Password found: admin
[*] Time taken: 0.01s
```

## Running tests

```bash
python -m pytest tests/
```

## Roadmap / ideas for extension

- [ ] Support bcrypt / scrypt / argon2 (slow hashes)
- [ ] Rule-based mutation (e.g., leetspeak, appending numbers)
- [ ] Progress bar with `tqdm`
- [ ] GPU acceleration comparison against hashcat

## License

MIT — see [LICENSE](LICENSE).
