import pandas as pd
import sqlite3
import numpy as np

# ── 1. Load CSV ──────────────────────────────────────────────────────────────
df = pd.read_csv('Findex_Microdata_2025_updateViet Nam.csv')
print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ── 2. Load into SQLite (covers SQL requirement) ─────────────────────────────
conn = sqlite3.connect('findex_vietnam.db')
df.to_sql('findex', conn, if_exists='replace', index=False)
print("Loaded into SQLite: findex_vietnam.db")

# ── 3. Basic adoption rates via SQL ─────────────────────────────────────────
queries = {
    "Overall account ownership (%)": """
        SELECT ROUND(AVG(account) * 100, 1) as pct FROM findex
    """,
    "Digital account ownership (%)": """
        SELECT ROUND(AVG(dig_account) * 100, 1) as pct FROM findex
    """,
    "Any digital payment (%)": """
        SELECT ROUND(AVG(anydigpayment) * 100, 1) as pct FROM findex
    """,
    "Mobile account (%)": """
        SELECT ROUND(AVG(account_mob) * 100, 1) as pct FROM findex
    """,
    "Merchant digital payment (%)": """
        SELECT ROUND(AVG(merchantpay_dig) * 100, 1) as pct FROM findex
    """,
}

print("\n── Adoption rates (SQL) ──────────────────────────────────────────────")
for label, q in queries.items():
    result = pd.read_sql(q, conn).iloc[0, 0]
    print(f"  {label}: {result}%")

# ── 4. Adoption by demographics via SQL ──────────────────────────────────────
print("\n── Digital payment adoption by income quintile (SQL) ─────────────────")
q_inc = """
    SELECT inc_q,
           COUNT(*) as n,
           ROUND(AVG(anydigpayment) * 100, 1) as dig_pay_pct
    FROM findex
    GROUP BY inc_q
    ORDER BY inc_q
"""
print(pd.read_sql(q_inc, conn).to_string(index=False))

print("\n── Digital payment adoption by urban/rural (SQL) ─────────────────────")
q_urb = """
    SELECT urbanicity,
           COUNT(*) as n,
           ROUND(AVG(anydigpayment) * 100, 1) as dig_pay_pct
    FROM findex
    GROUP BY urbanicity
    ORDER BY urbanicity
"""
print(pd.read_sql(q_urb, conn).to_string(index=False))

print("\n── Digital payment adoption by gender (SQL) ──────────────────────────")
q_gen = """
    SELECT female,
           COUNT(*) as n,
           ROUND(AVG(anydigpayment) * 100, 1) as dig_pay_pct
    FROM findex
    GROUP BY female
    ORDER BY female
"""
print(pd.read_sql(q_gen, conn).to_string(index=False))

print("\n── Digital payment adoption by education (SQL) ───────────────────────")
q_edu = """
    SELECT ROUND(educ, 0) as educ_level,
           COUNT(*) as n,
           ROUND(AVG(anydigpayment) * 100, 1) as dig_pay_pct
    FROM findex
    WHERE educ IS NOT NULL
    GROUP BY ROUND(educ, 0)
    ORDER BY educ_level
"""
print(pd.read_sql(q_edu, conn).to_string(index=False))

# ── 5. Age bands ─────────────────────────────────────────────────────────────
print("\n── Digital payment adoption by age band (SQL) ────────────────────────")
q_age = """
    SELECT
        CASE
            WHEN age BETWEEN 15 AND 24 THEN '15-24'
            WHEN age BETWEEN 25 AND 34 THEN '25-34'
            WHEN age BETWEEN 35 AND 44 THEN '35-44'
            WHEN age BETWEEN 45 AND 54 THEN '45-54'
            WHEN age >= 55 THEN '55+'
        END as age_band,
        COUNT(*) as n,
        ROUND(AVG(anydigpayment) * 100, 1) as dig_pay_pct
    FROM findex
    GROUP BY age_band
    ORDER BY age_band
"""
print(pd.read_sql(q_age, conn).to_string(index=False))

# ── 6. Key variable null check ───────────────────────────────────────────────
print("\n── Null counts for key variables ─────────────────────────────────────")
key_vars = ['female', 'age', 'educ', 'inc_q', 'emp_in', 'urbanicity',
            'account', 'account_fin', 'account_mob', 'dig_account',
            'anydigpayment', 'merchantpay_dig', 'internet_use',
            'borrowed', 'saved', 'pay_utilities']
for v in key_vars:
    nulls = df[v].isna().sum()
    print(f"  {v}: {nulls} nulls ({round(nulls/len(df)*100,1)}%)")

conn.close()
print("\n── Done. SQLite db saved as findex_vietnam.db ────────────────────────")
