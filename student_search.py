#!/usr/bin/env python3
"""Student lookup program using a dictionary keyed by student ID."""

from __future__ import annotations

import csv
import os
import sys


def load_students(filename: str) -> dict[str, list[str]]:
    students: dict[str, list[str]] = {}
    if not os.path.isfile(filename):
        raise FileNotFoundError(f"File not found: {filename}")

    with open(filename, encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for row_number, row in enumerate(reader, start=1):
            if not row:
                continue
            if len(row) != 5:
                print(f"Skipping invalid line {row_number}: wrong number of fields")
                continue
            student_id, last_name, first_name, major, gpa = [field.strip() for field in row]
            if not student_id:
                print(f"Skipping invalid line {row_number}: missing student ID")
                continue
            students[student_id] = [last_name, first_name, major, gpa]
    return students


def print_student(student_id: str, fields: list[str]) -> None:
    last_name, first_name, major, gpa = fields
    print(f"{student_id},{last_name},{first_name},{major},{gpa}")


def search_by_last_name(students: dict[str, list[str]], last_name: str) -> None:
    last_name = last_name.strip().lower()
    found = False
    for student_id, fields in students.items():
        if fields[0].lower() == last_name:
            print_student(student_id, fields)
            found = True
    if not found:
        print("No students found with that last name.")


def search_by_major(students: dict[str, list[str]], major: str) -> None:
    major = major.strip().lower()
    found = False
    for student_id, fields in students.items():
        if fields[2].lower() == major:
            print_student(student_id, fields)
            found = True
    if not found:
        print("No students found with that major.")


def prompt_menu_choice() -> str:
    print("Choose an option:")
    print("1) Search by Last Name")
    print("2) Search by Major")
    print("3) Quit")
    return input("Enter selection: ").strip()


def main() -> int:
    filename = input("Enter the student file name (e.g. students.txt): ").strip() or "students.txt"
    try:
        students = load_students(filename)
    except FileNotFoundError as exc:
        print(exc)
        return 1

    if not students:
        print("No student data loaded.")
        return 1

    while True:
        choice = prompt_menu_choice()
        if choice == "1":
            last_name = input("Enter last name to search for: ").strip()
            search_by_last_name(students, last_name)
        elif choice == "2":
            major = input("Enter major to search for: ").strip()
            search_by_major(students, major)
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
