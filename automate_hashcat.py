import subprocess
import argparse
import os

def run_hashcat(hash_file, hash_type, wordlist, attack_mode, output_file, additional_params):
    # Construct the Hashcat command
    cmd = [
        "hashcat",
        "-m", str(hash_type),
        "-a", str(attack_mode),
        "-o", output_file,
        hash_file,
        wordlist
    ] + additional_params

    print(f"Running command: {' '.join(cmd)}")

    # Execute the Hashcat command
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Monitor the process output
    for line in iter(process.stdout.readline, b''):
        print(line.decode('utf-8').strip())

    # Wait for the process to complete
    process.wait()

    if process.returncode == 0:
        print(f"Hashcat completed successfully. Results saved in {output_file}")
    else:
        print(f"Hashcat failed with return code {process.returncode}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Hashcat to maximize efficiency of password cracking.")
    parser.add_argument("hash_file", help="Path to the file containing hashes.")
    parser.add_argument("hash_type", type=int, help="Hash type (e.g., 0 for MD5, 100 for SHA1).")
    parser.add_argument("wordlist", help="Path to the wordlist file.")
    parser.add_argument("attack_mode", type=int, help="Attack mode (e.g., 0 for dictionary attack).")
    parser.add_argument("output_file", help="Path to the output file to save cracked passwords.")
    parser.add_argument("--additional", nargs='*', default=[], help="Additional parameters for Hashcat.")

    args = parser.parse_args()

    if not os.path.exists(args.hash_file):
        print(f"Error: Hash file '{args.hash_file}' not found.")
        exit(1)

    if not os.path.exists(args.wordlist):
        print(f"Error: Wordlist '{args.wordlist}' not found.")
        exit(1)

    run_hashcat(args.hash_file, args.hash_type, args.wordlist, args.attack_mode, args.output_file, args.additional)
