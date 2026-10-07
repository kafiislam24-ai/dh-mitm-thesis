import csv
import time
import statistics
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import dh


WARMUP_RUNS = 5
MEASURED_RUNS = 50

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

CSV_FILE = RESULTS_DIR / "standard_dh.csv"



parameters = dh.generate_parameters(
    generator=2,
    key_size=2048
)


def run_standard_dh():
    keygen_start = time.perf_counter_ns()

    alice_private_key = parameters.generate_private_key()
    alice_public_key = alice_private_key.public_key()

    bob_private_key = parameters.generate_private_key()
    bob_public_key = bob_private_key.public_key()

    keygen_end = time.perf_counter_ns()

    exchange_start = time.perf_counter_ns()

    alice_shared_secret = alice_private_key.exchange(
        bob_public_key
    )

    bob_shared_secret = bob_private_key.exchange(
        alice_public_key
    )

    exchange_end = time.perf_counter_ns()

    keygen_time_ms = (
        keygen_end - keygen_start
    ) / 1_000_000

    exchange_time_ms = (
        exchange_end - exchange_start
    ) / 1_000_000

    total_time_ms = (
        keygen_time_ms + exchange_time_ms
    )

    shared_secret_match = (
        alice_shared_secret == bob_shared_secret
    )

    return {
        "keygen_time_ms": keygen_time_ms,
        "exchange_time_ms": exchange_time_ms,
        "total_time_ms": total_time_ms,
        "shared_secret_match": shared_secret_match
    }


print(f"Running {WARMUP_RUNS} warm-up runs...")

for _ in range(WARMUP_RUNS):
    run_standard_dh()



print(f"Running {MEASURED_RUNS} measured runs...")

results = []

for run_id in range(1, MEASURED_RUNS + 1):

    result = run_standard_dh()

    result["run_id"] = run_id
    result["scenario"] = "standard_dh"

    results.append(result)

    print(
        f"Run {run_id:02d}: "
        f"{result['total_time_ms']:.6f} ms | "
        f"Match: {result['shared_secret_match']}"
    )


fieldnames = [
    "run_id",
    "scenario",
    "keygen_time_ms",
    "exchange_time_ms",
    "total_time_ms",
    "shared_secret_match"
]

with open(
    CSV_FILE,
    mode="w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(results)



total_times = [
    r["total_time_ms"]
    for r in results
]

keygen_times = [
    r["keygen_time_ms"]
    for r in results
]

exchange_times = [
    r["exchange_time_ms"]
    for r in results
]


mean_total = statistics.mean(total_times)
median_total = statistics.median(total_times)
stdev_total = statistics.stdev(total_times)

mean_keygen = statistics.mean(keygen_times)
mean_exchange = statistics.mean(exchange_times)


all_matches = all(
    r["shared_secret_match"]
    for r in results
)



print("\n=== Standard DH Summary ===")

print(
    f"Measured runs: {MEASURED_RUNS}"
)

print(
    f"Mean key generation time: "
    f"{mean_keygen:.6f} ms"
)

print(
    f"Mean shared-secret time: "
    f"{mean_exchange:.6f} ms"
)

print(
    f"Mean total time: "
    f"{mean_total:.6f} ms"
)

print(
    f"Median total time: "
    f"{median_total:.6f} ms"
)

print(
    f"Standard deviation: "
    f"{stdev_total:.6f} ms"
)

print(
    f"All shared secrets matched: "
    f"{all_matches}"
)

print(
    f"CSV saved to: {CSV_FILE}"
)