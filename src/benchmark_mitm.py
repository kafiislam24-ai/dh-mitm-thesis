from cryptography.hazmat.primitives.asymmetric import dh
import time
import csv
from pathlib import Path


def run_mitm_experiment():

    parameters = dh.generate_parameters(
        generator=2,
        key_size=2048
    )


    # Alice
    alice_private_key = parameters.generate_private_key()
    alice_public_key = alice_private_key.public_key()


    # Bob
    bob_private_key = parameters.generate_private_key()
    bob_public_key = bob_private_key.public_key()


    # Mallory
    mallory_private_key_1 = parameters.generate_private_key()
    mallory_public_key_1 = mallory_private_key_1.public_key()


    mallory_private_key_2 = parameters.generate_private_key()
    mallory_public_key_2 = mallory_private_key_2.public_key()



    # Alice-Mallory secret
    alice_secret = alice_private_key.exchange(
        mallory_public_key_1
    )

    mallory_secret_alice = mallory_private_key_1.exchange(
        alice_public_key
    )


    # Bob-Mallory secret
    bob_secret = bob_private_key.exchange(
        mallory_public_key_2
    )

    mallory_secret_bob = mallory_private_key_2.exchange(
        bob_public_key
    )


    alice_mallory_match = (
        alice_secret == mallory_secret_alice
    )

    mallory_bob_match = (
        bob_secret == mallory_secret_bob
    )


    attack_success = (
        alice_mallory_match
        and
        mallory_bob_match
    )


    return attack_success



# ----------------------------
# Benchmark Configuration
# ----------------------------

warmup_runs = 5
measured_runs = 50


results = []


print("Starting warm-up runs...")


# Warm-up
for i in range(warmup_runs):
    run_mitm_experiment()


print("Warm-up completed.")
print("Starting measured runs...")


# Measurement
for run_id in range(1, measured_runs + 1):

    start_time = time.perf_counter_ns()


    success = run_mitm_experiment()


    end_time = time.perf_counter_ns()


    total_time_ms = (
        end_time - start_time
    ) / 1_000_000


    results.append([
        run_id,
        "MITM",
        success,
        total_time_ms
    ])


print("Measurement completed.")



# ----------------------------
# Save CSV
# ----------------------------

results_folder = Path("results")
results_folder.mkdir(exist_ok=True)


csv_file = results_folder / "mitm.csv"


with open(csv_file, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "run_id",
        "scenario",
        "attack_success",
        "total_time_ms"
    ])

    writer.writerows(results)



print("\nMITM Benchmark Completed")
print("-----------------------------")

print("Measured Runs:", measured_runs)

print("Attack Success Count:",
      sum(row[2] for row in results))

print("CSV Saved:")
print(csv_file)