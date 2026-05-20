#!/usr/bin/env python3
import math

def get_int(prompt):
    while True:
        try:
            val = int(input(prompt).strip())
            if val < 0:
                print("Please enter a non-negative integer.")
                continue
            return val
        except ValueError:
            print("Invalid input. Enter an integer.")

def main():
    people = get_int("Enter number of people attending: ")
    per_person = get_int("Enter number of hot dogs per person: ")
    total = people * per_person

    HOTDOGS_PER_PACKAGE = 10
    BUNS_PER_PACKAGE = 8

    hd_packages = math.ceil(total / HOTDOGS_PER_PACKAGE) if total > 0 else 0
    bun_packages = math.ceil(total / BUNS_PER_PACKAGE) if total > 0 else 0

    hd_leftover = hd_packages * HOTDOGS_PER_PACKAGE - total
    bun_leftover = bun_packages * BUNS_PER_PACKAGE - total

    print(f"Minimum packages of hot dogs required: {hd_packages}")
    print(f"Minimum packages of hot dog buns required: {bun_packages}")
    print(f"Hot dogs left over: {hd_leftover}")
    print(f"Hot dog buns left over: {bun_leftover}")

if __name__ == "__main__":
    main()
