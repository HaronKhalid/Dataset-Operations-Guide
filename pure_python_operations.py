"""
Pure Python Dataset Operations (No External Dependencies Required)
==================================================================
Demonstrates how common dataset tasks are performed using standard Python
modules (csv, statistics, operator) without needing third-party libraries.
"""

import csv
from pathlib import Path
from statistics import mean
from collections import defaultdict

DATA_DIR = Path(__file__).resolve().parent
DATASET_PATH = DATA_DIR / "employees.csv"


def load_dataset(file_path):
    """Load CSV into a list of dictionaries with typed fields."""
    records = []
    with open(file_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "id": int(row["id"]),
                "name": row["name"],
                "department": row["department"],
                "role": row["role"],
                "salary": int(row["salary"]),
                "experience_years": int(row["experience_years"]),
                "performance_score": float(row["performance_score"]),
                "city": row["city"],
                "join_date": row["join_date"],
            })
    return records


def print_table(records, columns, title=""):
    """Pretty prints a table in the console."""
    if title:
        print(f"\n--- {title} ---")
    header = " | ".join(f"{col:<20}" for col in columns)
    print(header)
    print("-" * len(header))
    for row in records:
        print(" | ".join(f"{str(row[col]):<20}" for col in columns))


def main():
    print("=" * 70)
    print("  PURE PYTHON DATASET OPERATIONS")
    print("=" * 70)

    employees = load_dataset(DATASET_PATH)
    print(f"\nLoaded {len(employees)} employee records from {DATASET_PATH.name}.\n")

    # 1. SORTING ASCENDING BY SALARY
    sorted_salary_asc = sorted(employees, key=lambda x: x["salary"])
    print_table(
        sorted_salary_asc[:5],
        ["name", "department", "salary"],
        "Top 5 Lowest Salaries (Ascending Order)"
    )

    # 2. SORTING DESCENDING BY SALARY
    sorted_salary_desc = sorted(employees, key=lambda x: x["salary"], reverse=True)
    print_table(
        sorted_salary_desc[:5],
        ["name", "department", "salary"],
        "Top 5 Highest Salaries (Descending Order)"
    )

    # 3. SORTING DESCENDING BY PERFORMANCE SCORE
    sorted_perf_desc = sorted(employees, key=lambda x: x["performance_score"], reverse=True)
    print_table(
        sorted_perf_desc[:5],
        ["name", "role", "performance_score"],
        "Top 5 Performers (Descending Order)"
    )

    # 4. MULTI-KEY SORTING: Department ascending, Salary descending
    sorted_dept_salary = sorted(
        employees,
        key=lambda x: (x["department"], -x["salary"])
    )
    print_table(
        sorted_dept_salary[:8],
        ["department", "name", "salary"],
        "Sorted by Department (Ascending) -> Salary (Descending)"
    )

    # 5. FILTERING
    high_earners = [e for e in employees if e["salary"] >= 90000]
    print_table(
        high_earners,
        ["name", "department", "salary"],
        "Filtered: High Earners (Salary >= 90,000)"
    )

    eng_seniors = [
        e for e in employees 
        if e["department"] == "Engineering" and e["experience_years"] >= 5
    ]
    print_table(
        eng_seniors,
        ["name", "role", "experience_years"],
        "Filtered: Senior Engineers (Experience >= 5 years)"
    )

    # 6. AGGREGATION / GROUPING BY DEPARTMENT
    dept_salaries = defaultdict(list)
    for e in employees:
        dept_salaries[e["department"]].append(e["salary"])

    print("\n--- Department Salary Summary (Pure Python GroupBy) ---")
    print(f"{'Department':<15} | {'Count':<8} | {'Min Salary':<12} | {'Avg Salary':<12} | {'Max Salary':<12}")
    print("-" * 68)
    for dept, sals in sorted(dept_salaries.items()):
        print(f"{dept:<15} | {len(sals):<8} | {min(sals):<12} | {round(mean(sals)):<12} | {max(sals):<12}")

    # 7. EXPORTING RESULTS TO CSV
    # Export descending salary
    out_sorted = DATA_DIR / "sorted_employees_by_salary.csv"
    with open(out_sorted, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=employees[0].keys())
        writer.writeheader()
        writer.writerows(sorted_salary_desc)
    print(f"\n[Exported] {out_sorted.name}")

    # Export department summary
    out_dept = DATA_DIR / "department_summary_report.csv"
    with open(out_dept, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["department", "count", "min_salary", "avg_salary", "max_salary"])
        for dept, sals in sorted(dept_salaries.items()):
            writer.writerow([dept, len(sals), min(sals), round(mean(sals), 2), max(sals)])
    print(f"[Exported] {out_dept.name}")

    # Export enhanced dataset with compensation and seniority tiers
    enhanced_records = []
    for e in employees:
        rec = dict(e)
        score = rec["performance_score"]
        bonus_rate = 0.15 if score >= 4.5 else (0.10 if score >= 4.0 else 0.05)
        bonus_amount = round(rec["salary"] * bonus_rate, 2)
        total_comp = round(rec["salary"] + bonus_amount, 2)
        
        exp = rec["experience_years"]
        if exp <= 2:
            seniority = "Junior (0-2 yrs)"
        elif exp <= 5:
            seniority = "Mid-Level (3-5 yrs)"
        else:
            seniority = "Senior (6+ yrs)"
            
        rec["bonus_rate"] = bonus_rate
        rec["bonus_amount"] = bonus_amount
        rec["total_compensation"] = total_comp
        rec["seniority_level"] = seniority
        enhanced_records.append(rec)

    out_enhanced = DATA_DIR / "employees_with_compensation.csv"
    with open(out_enhanced, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=enhanced_records[0].keys())
        writer.writeheader()
        writer.writerows(enhanced_records)
    print(f"[Exported] {out_enhanced.name}")

    print("\n" + "=" * 70)
    print("  All Pure Python tasks executed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
