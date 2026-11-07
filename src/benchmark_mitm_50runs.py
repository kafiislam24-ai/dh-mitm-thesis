

import csv
import statistics
import time
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import dh

def run_mitm_trial(parameters):
    # --- 1. Key Generation Timing (Alice, Bob, and Mallory) ---
    t0_keygen = time.perf_counter_ns()
    
    alice_priv = parameters.generate_private_key()
    alice_pub = alice_priv.public_key()

    bob_priv = parameters.generate_private_key()
    bob_pub = bob_priv.public_key()

    mallory_priv_for_alice = parameters.generate_private_key()
    mallory_pub_for_alice = mallory_priv_for_alice.public_key()

    mallory_priv_for_bob = parameters.generate_private_key()
    mallory_pub_for_bob = mallory_priv_for_bob.public_key()

    t1_keygen = time.perf_counter_ns()

    # --- 2. Key Exchange & Interception Timing ---
    t0_exchange = time.perf_counter_ns()

    alice_secret = alice_priv.exchange(mallory_pub_for_alice)
    mallory_secret_with_alice = mallory_priv_for_alice.exchange(alice_pub)

    bob_secret = bob_priv.exchange(mallory_pub_for_bob)
    mallory_secret_with_bob = mallory_priv_for_bob.exchange(bob_pub)

    t1_exchange = time.perf_counter_ns()

    # Calculate timings in milliseconds (ms)
    keygen_time_ms = (t1_keygen - t0_keygen) / 1_000_000.0
    exchange_time_ms = (t1_exchange - t0_exchange) / 1_000_000.0
    total_time_ms = keygen_time_ms + exchange_time_ms

    # Verification checks
    alice_mallory_match = (alice_secret == mallory_secret_with_alice)
    bob_mallory_match = (bob_secret == mallory_secret_with_bob)
    alice_bob_match = (alice_secret == bob_secret)

    mitm_success = alice_mallory_match and bob_mallory_match and (not alice_bob_match)

    return {
        "keygen_time_ms": keygen_time_ms,
        "exchange_time_ms": exchange_time_ms,
        "total_time_ms": total_time_ms,
        "alice_mallory_match": alice_mallory_match,
        "bob_mallory_match": bob_mallory_match,
        "alice_bob_match": alice_bob_match,
        "mitm_success": mitm_success
    }

def main():
    print("=" * 65)
    print("PHASE 2: MAN-IN-THE-MIDDLE BENCHMARK (5 WARM-UP + 50 MEASURED)")
    print("=" * 65)

    # 1. Generate DH Parameters once (consistent with Phase 1 methodology)
    print("[*] Generating 2048-bit DH domain parameters...")
    parameters = dh.generate_parameters(generator=2, key_size=2048)

    # 2. Phase 2B: 5 Warm-up Runs
    print("[*] Running 5 warm-up iterations (excluded from dataset)...")
    for _ in range(5):
        run_mitm_trial(parameters)

    # 3. Phase 2C: 50 Measured Runs
    print("[*] Executing 50 measured trials...")
    results = []
    for run_id in range(1, 51):
        trial = run_mitm_trial(parameters)
        trial["run_id"] = run_id
        trial["scenario"] = "mitm_attack"
        results.append(trial)

    # 4. Phase 2D: Save to results/mitm.csv
    output_dir = Path("results")
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_file = output_dir / "mitm.csv"

    fieldnames = [
        "run_id", "scenario", "keygen_time_ms", "exchange_time_ms", 
        "total_time_ms", "alice_mallory_match", "bob_mallory_match", 
        "alice_bob_match", "mitm_success"
    ]

    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"[+] Dataset saved successfully: {csv_file.resolve()}")

    # 5. Phase 2E: Statistical Evaluation & Attack Success Rate (ASR)
    keygen_times = [r["keygen_time_ms"] for r in results]
    exchange_times = [r["exchange_time_ms"] for r in results]
    total_times = [r["total_time_ms"] for r in results]
    successes = [r["mitm_success"] for r in results]

    successful_count = sum(successes)
    asr = (successful_count / len(results)) * 100.0

    print("\n" + "=" * 65)
    print("PHASE 2 SUMMARY & BENCHMARK RESULTS")
    print("=" * 65)
    print(f"Total Measured Trials            : {len(results)}")
    print(f"Successful MitM Attacks          : {successful_count}/{len(results)}")
    print(f"Attack Success Rate (ASR)        : {asr:.2f}%")
    print("-" * 65)
    print(f"Mean Key Generation Time         : {statistics.mean(keygen_times):.6f} ms")
    print(f"Mean Exchange/Interception Time  : {statistics.mean(exchange_times):.6f} ms")
    print(f"Mean Total Time                  : {statistics.mean(total_times):.6f} ms")
    print(f"Median Total Time                : {statistics.median(total_times):.6f} ms")
    print(f"Standard Deviation               : {statistics.stdev(total_times):.6f} ms")
    print("=" * 65)

if __name__ == "__main__":
    main()