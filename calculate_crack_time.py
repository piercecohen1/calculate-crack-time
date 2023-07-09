
import argparse
import sys

def read_wordlist(file_path):
    with open(file_path, 'r', errors='ignore') as f:
        wordlist = f.read().splitlines()
    return wordlist


def calculate_crack_time(charset, hash_rate, max_length, is_wordlist=False):
    if hash_rate == 0:
        return float('inf')
    
    hash_rate = hash_rate * 1e6  # convert from MH/s to H/s

    if is_wordlist:
        total_combinations = len(charset)
    else:
        total_combinations = sum(len(charset)**i for i in range(1, max_length + 1))
    
    time_in_seconds = total_combinations / hash_rate

    days, remainder = divmod(time_in_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return int(days), int(hours), int(minutes), seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate password crack time.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--char-set', help='set of characters to brute force')
    group.add_argument('--wordlist', help='wordlist file to use')
    parser.add_argument('--hash-rate', type=float, required=True, help='hash rate in MH/s')
    parser.add_argument('--max-length', type=int, help='maximum password length')

    args = parser.parse_args()

    if args.char_set and not args.max_length:
        parser.error("--max-length is required when using --char-set")

    if args.wordlist:
        charset = read_wordlist(args.wordlist)
        is_wordlist = True
    else:
        charset = args.char_set
        is_wordlist = False

    result = calculate_crack_time(charset, args.hash_rate, args.max_length, is_wordlist)
    if result == float('inf'):
        print("Time to crack: Infinity (Hash rate is 0)")
    else:
        days, hours, minutes, seconds = result
        print(f"Time to crack: {days} days, {hours} hours, {minutes} minutes, and {seconds:.5f} seconds")
