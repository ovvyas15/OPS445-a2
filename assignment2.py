import argparse
import os
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Analyze system memory usage.")
    parser.add_argument("program", nargs="?", help="Name of the program to analyze.")
    parser.add_argument("-H", "--human", action="store_true", help="Display human-readable output.")
    parser.add_argument("-l", "--length", type=int, default=50, help="Specify graph length.")
    return parser.parse_args()

def get_memory_info():
    meminfo = {}
    with open("/proc/meminfo", "r") as f:
        for line in f:
            key, value = line.split(":")
            meminfo[key.strip()] = value.strip()
    return meminfo

def analyze_program_memory(program_name):
    try:
        pid = os.popen(f"pidof {program_name}").read().strip()
        if not pid:
            print(f"Error: Program '{program_name}' is not running.")
            sys.exit(1)
        with open(f"/proc/{pid}/status", "r") as f:
            for line in f:
                if "VmRSS" in line:
                    return line.split(":")[1].strip()
    except FileNotFoundError:
        print(f"Error: PID or program '{program_name}' not found.")
        sys.exit(1)

def main():
    args = parse_args()
    meminfo = get_memory_info()
    
    if args.program:
        memory_usage = analyze_program_memory(args.program)
        print(f"Memory usage of '{args.program}': {memory_usage}")
    else:
        print("System Memory Information:")
        for key, value in meminfo.items():
            if args.human:
                print(f"{key}: {value}")
            else:
                print(f"{key}: {value.replace(' kB', '')}")

if __name__ == "__main__":
    main()
