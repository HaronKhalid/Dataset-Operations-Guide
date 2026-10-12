"""
Data Science Operations on Dataset
===================================
This script demonstrates essential dataset operations commonly performed in Data Science:
1. Loading & Overview (head, tail, info, describe)
2. Sorting (Ascending, Descending, Multi-column sorting)
3. Filtering & Boolean Indexing
4. Aggregations & Grouping (groupby, mean, count, min, max)
5. Feature Engineering (Derived columns & categories)
6. Statistical Summary & Correlation
7. Exporting Cleaned & Processed Datasets
"""

import sys
from pathlib import Path

# Check if pandas is available
try:
    import pandas as pd
    HAS_PANDAS = True
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
except ImportError:
    HAS_PANDAS = False

DATA_DIR = Path(__file__).resolve().parent
DATASET_PATH = DATA_DIR / "employees.csv"


def print_section(title: str):
    """Helper to print visual section dividers."""
    line = "=" * 80
    print(f"\n{line}")
    print(f"  {title.upper()}")
    print(f"{line}\n")


def print_subsection(title: str):
    """Helper to print sub-section dividers."""
    print(f"\n--- {title} ---")


def main():
    if not HAS_PANDAS:
        print_section("Pandas Not Detected")
        print("Note: 'pandas' is not yet installed in this Python environment.")
        print("To install pandas, run: pip install pandas")
        print("Switching automatically to standard Python implementation (pure_python_operations.py)...\n")
        try:
            import pure_python_operations
            pure_python_operations.main()
        except Exception as e:
            print(f"Error running pure Python operations: {e}")
        return

    # -------------------------------------------------------------
    # 1. LOAD & INSPECT DATASET
    # -------------------------------------------------------------
    print_section("1. Loading & Inspecting Dataset")
    
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset successfully loaded from: {DATASET_PATH.name}")
    print(f"Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
    
    print_subsection("First 5 Rows (head)")
    print(df.head())

    print_subsection("Last 3 Rows (tail)")
    print(df.tail(3))

    print_subsection("Data Types and Non-Null Counts (info)")
    df.info()

    print_subsection("Descriptive Statistics for Numeric Columns (describe)")
    print(df.describe().round(2))

    # -------------------------------------------------------------
    # 2. SORTING OPERATIONS (ASCENDING & DESCENDING)
    # -------------------------------------------------------------
    print_section("2. Sorting Operations")

    # A. Single Column Ascending
    print_subsection("A. Ascending Order: Sorted by Salary (Lowest to Highest)")
    sorted_salary_asc = df.sort_values(by="salary", ascending=True)
    print(sorted_salary_asc[["name", "department", "role", "salary"]])

    # B. Single Column Descending
    print_subsection("B. Descending Order: Sorted by Salary (Highest to Lowest)")
    sorted_salary_desc = df.sort_values(by="salary", ascending=False)
    print(sorted_salary_desc[["name", "department", "role", "salary"]])

    # C. Descending by Performance Score (Top Performers)
    print_subsection("C. Descending Order: Sorted by Performance Score (Top Performers)")
    sorted_perf_desc = df.sort_values(by="performance_score", ascending=False)
    print(sorted_perf_desc[["name", "department", "experience_years", "performance_score"]])

    # D. Multi-Column Sorting
    print_subsection("D. Multi-Column: Department (Ascending) -> Salary (Descending)")
    sorted_multi = df.sort_values(
        by=["department", "salary"], 
        ascending=[True, False]
    )
    print(sorted_multi[["department", "name", "role", "salary"]])

    # -------------------------------------------------------------
    # 3. FILTERING & QUERYING (BOOLEAN INDEXING)
    # -------------------------------------------------------------
    print_section("3. Filtering & Querying")

    # Filter: High Earners (> 80,000)
    print_subsection("Filter 1: Employees with Salary > 80,000")
    high_earners = df[df["salary"] > 80000]
    print(high_earners[["name", "department", "salary"]])

    # Filter: Specific Department
    print_subsection("Filter 2: Engineering Department Only")
    engineering_team = df[df["department"] == "Engineering"]
    print(engineering_team[["name", "role", "experience_years", "salary"]])

    # Multi-condition Filter (AND / OR)
    print_subsection("Filter 3: Experienced Top Performers (Experience >= 5 AND Score >= 4.5)")
    top_veterans = df[(df["experience_years"] >= 5) & (df["performance_score"] >= 4.5)]
    print(top_veterans[["name", "department", "experience_years", "performance_score", "salary"]])

    # Filter with isin()
    print_subsection("Filter 4: Employees based in Lahore or Islamabad")
    north_region = df[df["city"].isin(["Lahore", "Islamabad"])]
    print(north_region[["name", "city", "department"]].head(6))

    # -------------------------------------------------------------
    # 4. GROUPING & AGGREGATIONS (GROUPBY)
    # -------------------------------------------------------------
    print_section("4. Grouping & Aggregations (GroupBy)")

    # Aggregate Salary by Department
    print_subsection("Department Salary Statistics (Mean, Min, Max, Count)")
    dept_stats = df.groupby("department")["salary"].agg(
        Count="count",
        Min="min",
        Average="mean",
        Max="max"
    ).round(2)
    print(dept_stats)

    # City Level Performance
    print_subsection("City-wise Average Performance & Average Experience")
    city_stats = df.groupby("city").agg(
        Employee_Count=("id", "count"),
        Avg_Performance=("performance_score", "mean"),
        Avg_Experience=("experience_years", "mean")
    ).round(2)
    print(city_stats)

    # -------------------------------------------------------------
    # 5. FEATURE ENGINEERING & TRANSFORMATIONS
    # -------------------------------------------------------------
    print_section("5. Feature Engineering (Creating New Columns)")

    # Create a copy to add features
    df_enhanced = df.copy()

    # 1. Performance-based bonus percentage
    # If performance >= 4.5: 15% bonus, >= 4.0: 10% bonus, else 5%
    def calculate_bonus(score):
        if score >= 4.5:
            return 0.15
        elif score >= 4.0:
            return 0.10
        else:
            return 0.05

    df_enhanced["bonus_rate"] = df_enhanced["performance_score"].apply(calculate_bonus)
    df_enhanced["bonus_amount"] = (df_enhanced["salary"] * df_enhanced["bonus_rate"]).round(2)
    df_enhanced["total_compensation"] = (df_enhanced["salary"] + df_enhanced["bonus_amount"]).round(2)

    # 2. Experience Tiers using pd.cut
    df_enhanced["seniority_level"] = pd.cut(
        df_enhanced["experience_years"],
        bins=[-1, 2, 5, 20],
        labels=["Junior (0-2 yrs)", "Mid-Level (3-5 yrs)", "Senior (6+ yrs)"]
    )

    print_subsection("Enhanced Dataset with Bonus, Compensation & Seniority Tiers")
    print(df_enhanced[["name", "role", "salary", "bonus_amount", "total_compensation", "seniority_level"]].head(8))

    # -------------------------------------------------------------
    # 6. STATISTICAL INSIGHTS & DISTRIBUTIONS
    # -------------------------------------------------------------
    print_section("6. Statistical Insights & Frequency Analysis")

    print_subsection("Department Distribution (Count)")
    print(df["department"].value_counts())

    print_subsection("City Distribution (Count)")
    print(df["city"].value_counts())

    print_subsection("Correlation between Experience and Salary")
    corr = df[["experience_years", "salary", "performance_score"]].corr().round(3)
    print(corr)

    # -------------------------------------------------------------
    # 7. EXPORTING PROCESSED OUTPUTS
    # -------------------------------------------------------------
    print_section("7. Exporting Processed Data")

    # Export sorted employees by salary
    out_sorted = DATA_DIR / "sorted_employees_by_salary.csv"
    sorted_salary_desc.to_csv(out_sorted, index=False)
    print(f"Exported: {out_sorted.name}")

    # Export department summary report
    out_summary = DATA_DIR / "department_summary_report.csv"
    dept_stats.to_csv(out_summary)
    print(f"Exported: {out_summary.name}")

    # Export enhanced dataset with compensation and seniority
    out_enhanced = DATA_DIR / "employees_with_compensation.csv"
    df_enhanced.to_csv(out_enhanced, index=False)
    print(f"Exported: {out_enhanced.name}")

    print_section("All Data Science Tasks Completed Successfully!")


if __name__ == "__main__":
    main()
