# Dataset & Operations Guide

Welcome to the **Data Science** project folder. This project contains a dataset and a Python script showcasing fundamental data analysis operations using **Pandas**.

---

## Project Structure

```
data-science/
├── employees.csv                       # The primary dataset
├── data_analysis.py                   # Python script performing all data tasks
├── sorted_employees_by_salary.csv     # (Generated) Employees sorted by salary desc
├── department_summary_report.csv       # (Generated) Department-level statistics
├── employees_with_compensation.csv     # (Generated) Enhanced dataset with bonus & seniority
└── README.md                          # Documentation and guide
```

---

## Dataset Overview (`employees.csv`)

A structured sample dataset representing 15 professionals across various departments and cities.

| Column | Type | Description |
|---|---|---|
| `id` | Integer | Unique identifier for each employee |
| `name` | String | Full name of the employee |
| `department` | String | Department (Engineering, Sales, Marketing, HR, Finance) |
| `role` | String | Job title / position |
| `salary` | Integer | Annual salary (USD / PKR) |
| `experience_years` | Integer | Years of professional experience |
| `performance_score`| Float | Annual review rating (out of 5.0) |
| `city` | String | Office location (Lahore, Karachi, Islamabad, Rawalpindi) |
| `join_date` | Date | Date when employee joined |

---

## Data Science Tasks Performed

### 1. Data Loading & Inspection
- **`pd.read_csv()`**: Loading tabular data into a DataFrame.
- **`df.head()` & `df.tail()`**: Previewing top and bottom records.
- **`df.shape` & `df.info()`**: Checking dimensions, column types, and null values.
- **`df.describe()`**: Generating descriptive statistical summaries (mean, std, min, percentiles, max).

### 2. Sorting Operations
- **Ascending Order (`ascending=True`)**:
  ```python
  df.sort_values(by="salary", ascending=True)
  ```
  Arranges salaries from lowest to highest.
- **Descending Order (`ascending=False`)**:
  ```python
  df.sort_values(by="salary", ascending=False)
  ```
  Arranges salaries from highest to lowest.
- **Multi-Column Sorting**:
  ```python
  df.sort_values(by=["department", "salary"], ascending=[True, False])
  ```
  Groups by department alphabetically, then ranks salaries highest to lowest within each department.

### 3. Filtering & Querying (Boolean Indexing)
- **Threshold filtering**: Identifying high earners (`salary > 80,000`).
- **Category filtering**: Filtering by specific teams (`department == 'Engineering'`).
- **Compound filtering**: Finding senior high-performers (`(experience >= 5) & (performance >= 4.5)`).
- **Membership filtering**: Filtering multiple locations using `.isin(['Lahore', 'Islamabad'])`.

### 4. Grouping & Aggregations (`groupby`)
- Grouping records by department and calculating `count`, `min`, `mean`, and `max` salaries.
- Grouping by city to compare average performance ratings and experience levels.

### 5. Feature Engineering (New Columns)
- **Bonus Calculation**: Dynamic bonus rates based on performance ratings.
- **Total Compensation**: `salary + bonus_amount`.
- **Seniority Binning (`pd.cut`)**: Categorizing into `Junior (0-2 yrs)`, `Mid-Level (3-5 yrs)`, and `Senior (6+ yrs)`.

### 6. Statistical Insights & Correlation
- Frequency distribution (`value_counts()`) for categorical variables.
- Correlation matrix (`.corr()`) measuring the linear relationship between experience and salary.

### 7. Exporting Outputs
- Saving processed slices and aggregated tables to CSV using `.to_csv(..., index=False)`.

---

## How to Run

1. Open PowerShell or Terminal in this folder:
   ```powershell
   cd "data-science"
   ```

2. Run the analysis script:
   ```powershell
   python data_analysis.py
   ```
