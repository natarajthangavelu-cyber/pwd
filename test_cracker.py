import hashlib
import os
import sys
 
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
 
from cracker import hash_candidate, dictionary_attack
 
 
def test_hash_candidate_sha256():
    expected = hashlib.sha256("password".encode()).hexdigest()
    assert hash_candidate("password", "sha256") == expected
 
 
def test_hash_candidate_with_salt():
    expected = hashlib.sha256(("saltpassword").encode()).hexdigest()
    assert hash_candidate("password", "sha256", salt="salt") == expected
 
 
def test_dictionary_attack_finds_known_password():
    target = hashlib.sha256("admin".encode()).hexdigest()
    wordlist_path = os.path.join(
        os.path.dirname(__file__), "..", "wordlists", "sample_wordlist.txt"
    )
    result = dictionary_attack(target, wordlist_path, "sha256")
    assert result == "admin"
 
 
def test_dictionary_attack_no_match():
    target = "0" * 64  # invalid hash, should never match
    wordlist_path = os.path.join(
        os.path.dirname(__file__), "..", "wordlists", "sample_wordlist.txt"
    )
    result = dictionary_attack(target, wordlist_path, "sha256")
    assert result is None
 
 
if __name__ == "__main__":
    test_hash_candidate_sha256()
    test_hash_candidate_with_salt()
    test_dictionary_attack_finds_known_password()
    test_dictionary_attack_no_match()
    print("All tests passed.")
