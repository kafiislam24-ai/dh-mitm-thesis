"""
Phase 3B & 3C: Repeated Benchmark for Authenticated Diffie-Hellman
Execution: 5 Warm-up runs + 50 Measured runs
Outputs: results/authenticated_dh.csv and performance overhead analysis
"""

import csv
import statistics
import time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

# Phase 1 Baseline Mean Time for comparison
PHASE1_BASELINE_MEAN_MS = 9.057158

def run_authenticated_trial(dh_parameters, alice_rsa_priv, alice_rsa_pub, bob_rsa_priv, bob_rsa_pub):
    # --- 1. Ephemeral DH Key Generation ---
    t0_keygen = time.perf_counter_ns()
    alice_dh_priv = dh_parameters.generate_private_key()
    alice_dh_pub = alice_dh_priv.public_key()

    bob_dh_priv = dh_parameters.generate_private_key()
    bob_dh_pub = bob_dh_priv.public_key()
    t1_keygen = time.perf_counter_ns()

    # Public keys serialized to PEM for signature payload
    alice_pub_bytes = alice_dh_pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    bob_pub_bytes = bob_dh_pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # --- 2. Digital Signature Generation (Alice & Bob sign their DH public keys) ---
    t0_sign = time.perf_counter_ns()
    alice_sig = alice_rsa_priv.sign(
        alice_pub_bytes,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    bob_sig = bob_rsa_priv.sign(
        bob_pub_bytes,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    t1_sign = time.perf_counter_ns()

    # --- 3. Digital Signature Verification (Mutual authentication) ---
    t0_verify = time.perf_counter_ns()
    try:
        bob_rsa_pub.verify(
            bob_sig,
            bob_pub_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        alice_verified_bob = True
    except InvalidSignature:
        alice_verified_bob = False

    try:
        alice_rsa_pub.verify(
            alice_sig,
            alice_pub_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        bob_verified_alice = True
    except InvalidSignature:
        bob_verified_alice = False
    t1_verify = time.perf_counter_ns()

    # --- 4. Shared Secret Derivation ---
    t0_exchange = time.perf_counter_ns()
    if alice_verified_bob and bob_verified_alice:
        alice_secret = alice_dh_priv.exchange(bob_dh_pub)
        bob_secret = bob_dh_priv.exchange(alice_dh_pub)
        secrets_match = (alice_secret == bob_secret)
    else:
        secrets_match = False
    t1_exchange = time.perf_counter_ns()

    # --- 5. Active Tampering Resistance Verification (Attack Detection Check) ---
    tampered_bytes = alice_pub_bytes[:-5] + b"XXXXX"
    try:
        alice_rsa_pub.verify(
            alice_sig,
            tampered_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        tamper_detected = False
    except InvalidSignature:
        tamper_detected = True

    # Calculate individual step timings in milliseconds (ms)
    keygen_ms = (t1_keygen - t0_keygen) / 1_000_000.0
    sign_ms = (t1_sign - t0_sign) / 1_000_000.0
    verify_ms = (t1_verify - t0_verify) / 1_000_000.0
    exchange_ms = (t1_exchange - t0_exchange) / 1_000_000.0
    total_authenticated_ms = keygen_ms + sign_ms + verify_ms + exchange_ms

    return {
        "keygen_time_ms": keygen_ms,
        "sign_time_ms": sign_ms,
        "verify_time_ms": verify_ms,
        "exchange_time_ms": exchange_ms,
        "total_time_ms": total_authenticated_ms,
        "signatures_valid": alice_verified_bob and bob_verified_alice,
        "secrets_match": secrets_match,
        "tamper_detected": tamper_detected
    }

def main():
    print("=" * 70)
    print("PHASE 3: AUTHENTICATED DIFFIE-HELLMAN BENCHMARK (50 RUNS)")
    print("=" * 70)

    # Generate domain parameters & long-term identity keys outside the timing loop
    print("[*] Generating 2048-bit DH domain parameters...")
    dh_parameters = dh.generate_parameters(generator=2, key_size=2048)

    print("[*] Provisioning RSA identity keys for Alice and Bob...")
    alice_rsa_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    alice_rsa_pub = alice_rsa_priv.public_key()

    bob_rsa_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    bob_rsa_pub = bob_rsa_priv.public_key()

    # Phase 3B: 5 Warm-up runs
    print("[*] Running 5 warm-up iterations (excluded from final dataset)...")
    for _ in range(5):
        run_authenticated_trial(
            dh_parameters, alice_rsa_priv, alice_rsa_pub, bob_rsa_priv, bob_rsa_pub
        )

    # Phase 3C: 50 Measured runs
    print("[*] Executing 50 measured trials...")
    results = []
    for run_id in range(1, 51):
        trial = run_authenticated_trial(
            dh_parameters, alice_rsa_priv, alice_rsa_pub, bob_rsa_priv, bob_rsa_pub
        )
        trial["run_id"] = run_id
        trial["scenario"] = "authenticated_dh"
        results.append(trial)

    # Phase 3D: Save to results/authenticated_dh.csv
    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_file = output_dir / "authenticated_dh.csv"

    fieldnames = [
        "run_id", "scenario", "keygen_time_ms", "sign_time_ms", "verify_time_ms",
        "exchange_time_ms", "total_time_ms", "signatures_valid", "secrets_match", "tamper_detected"
    ]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"[+] Dataset saved successfully: {csv_file.resolve()}")

    # Phase 3E: Statistical Analysis & Overhead Calculation
    total_times = [r["total_time_ms"] for r in results]
    keygen_times = [r["keygen_time_ms"] for r in results]
    sign_times = [r["sign_time_ms"] for r in results]
    verify_times = [r["verify_time_ms"] for r in results]
    exchange_times = [r["exchange_time_ms"] for r in results]
    
    detection_count = sum(1 for r in results if r["tamper_detected"])
    adr = (detection_count / len(results)) * 100.0

    mean_total = statistics.mean(total_times)
    median_total = statistics.median(total_times)
    std_total = statistics.stdev(total_times)

    # Overhead relative to Phase 1 Baseline
    absolute_overhead_ms = mean_total - PHASE1_BASELINE_MEAN_MS
    percentage_overhead = (absolute_overhead_ms / PHASE1_BASELINE_MEAN_MS) * 100.0

    print("\n" + "=" * 70)
    print("PHASE 3 SUMMARY & PERFORMANCE OVERHEAD RESULTS")
    print("=" * 70)
    print(f"Total Measured Trials               : {len(results)}")
    print(f"Signatures Valid in all runs        : {all(r['signatures_valid'] for r in results)}")
    print(f"Shared Secrets Match in all runs    : {all(r['secrets_match'] for r in results)}")
    print(f"Tamper Detection Rate (ADR)         : {adr:.2f}% ({detection_count}/{len(results)})")
    print("-" * 70)
    print(f"Mean Ephemeral DH KeyGen Time       : {statistics.mean(keygen_times):.6f} ms")
    print(f"Mean RSA Signing Time (Alice + Bob) : {statistics.mean(sign_times):.6f} ms")
    print(f"Mean RSA Verify Time (Alice + Bob)  : {statistics.mean(verify_times):.6f} ms")
    print(f"Mean DH Secret Derivation Time      : {statistics.mean(exchange_times):.6f} ms")
    print("-" * 70)
    print(f"Mean Authenticated DH Total Time    : {mean_total:.6f} ms")
    print(f"Median Authenticated DH Total Time  : {median_total:.6f} ms")
    print(f"Standard Deviation                  : {std_total:.6f} ms")
    print("-" * 70) 
    print("COMPARISON WITH PHASE 1 BASELINE (Standard DH: 9.057158 ms):")
    print(f"Absolute Authentication Overhead    : +{absolute_overhead_ms:.6f} ms")
    print(f"Percentage Performance Overhead     : +{percentage_overhead:.2f}%")
    print("=" * 70)

if __name__ == "__main__":
    main()