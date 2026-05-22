import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

# ── 1. Load data ─────────────────────────────────────────────────────────────
conn = sqlite3.connect('findex_vietnam.db')
df = pd.read_sql('SELECT * FROM findex', conn)
conn.close()

# ── 2. Prepare variables ──────────────────────────────────────────────────────
df = df.dropna(subset=['educ', 'anydigpayment'])

# Binary outcome: any digital payment
y = df['anydigpayment'].astype(int)

# Features
X = pd.DataFrame({
    'age':        df['age'],
    'age_sq':     df['age'] ** 2,           # non-linear age effect
    'female':     (df['female'] == 1).astype(int),
    'educ':       df['educ'],
    'inc_q':      df['inc_q'],
    'rural':      (df['urbanicity'] == 1).astype(int),
    'employed':   df['emp_in'],
    'internet':   df['internet_use'],
    'saved':      df['saved'],
    'borrowed':   df['borrowed'],
    'pay_util':   df['pay_utilities'],
})

print("── Sample size ───────────────────────────────────────────────────────")
print(f"  n = {len(y)}, adopters = {y.sum()} ({round(y.mean()*100,1)}%)")

# ── 3. Logistic regression (statsmodels — for coefficients + p-values) ────────
X_const = sm.add_constant(X)
logit_model = sm.Logit(y, X_const.astype(float))
result = logit_model.fit(disp=0)

print("\n── Logistic regression results ───────────────────────────────────────")
summary = pd.DataFrame({
    'coef':    result.params,
    'odds_ratio': np.exp(result.params),
    'p_value': result.pvalues
}).round(4)
summary['significant'] = summary['p_value'] < 0.05
print(summary.to_string())
print(f"\nPseudo R-squared: {round(result.prsquared, 4)}")
print(f"Log-likelihood: {round(result.llf, 2)}")

# ── 4. Marginal effects (more interpretable than coefficients) ────────────────
print("\n── Average marginal effects ──────────────────────────────────────────")
marginal = result.get_margeff()
me_df = pd.DataFrame({
    'marginal_effect': marginal.margeff,
    'p_value': marginal.pvalues
}, index=X.columns).round(4)
me_df['significant'] = me_df['p_value'] < 0.05
me_df = me_df.sort_values('marginal_effect', ascending=False)
print(me_df.to_string())

# ── 5. Sklearn logistic regression for ROC-AUC ───────────────────────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.25, random_state=42)

lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_auc = roc_auc_score(y_test, lr.predict_proba(X_test)[:, 1])
print(f"\n── Logistic regression AUC: {round(lr_auc, 4)} ─────────────────────")

# ── 6. Decision tree (ML layer) ───────────────────────────────────────────────
dt = DecisionTreeClassifier(max_depth=4, min_samples_leaf=20, random_state=42)
dt.fit(X_train, y_train)
dt_auc = roc_auc_score(y_test, dt.predict_proba(X_test)[:, 1])
print(f"── Decision tree AUC:       {round(dt_auc, 4)} ─────────────────────")

print("\n── Decision tree feature importance ──────────────────────────────────")
fi = pd.DataFrame({
    'feature': X.columns,
    'importance': dt.feature_importances_
}).sort_values('importance', ascending=False).round(4)
print(fi.to_string(index=False))

# ── 7. Segment profiling: who are the next-wave adopters? ────────────────────
print("\n── Segment: account holders who do NOT yet use digital payments ──────")
gap = df[(df['account'] == 1) & (df['anydigpayment'] == 0)]
print(f"  Size: {len(gap)} respondents ({round(len(gap)/len(df)*100,1)}% of sample)")
print(f"  Avg age:         {round(gap['age'].mean(), 1)}")
print(f"  % rural:         {round((gap['urbanicity']==1).mean()*100, 1)}%")
print(f"  % female:        {round((gap['female']==1).mean()*100, 1)}%")
print(f"  Avg income quintile: {round(gap['inc_q'].mean(), 2)}")
print(f"  Avg education:   {round(gap['educ'].mean(), 2)}")
print(f"  % internet user: {round(gap['internet_use'].mean()*100, 1)}%")
print(f"  % saved (formal):{round(gap['saved'].mean()*100, 1)}%")

print("\n── Segment: full digital adopters (account + digital payment) ─────────")
adopters = df[(df['account'] == 1) & (df['anydigpayment'] == 1)]
print(f"  Size: {len(adopters)} respondents ({round(len(adopters)/len(df)*100,1)}% of sample)")
print(f"  Avg age:         {round(adopters['age'].mean(), 1)}")
print(f"  % rural:         {round((adopters['urbanicity']==1).mean()*100, 1)}%")
print(f"  % female:        {round((adopters['female']==1).mean()*100, 1)}%")
print(f"  Avg income quintile: {round(adopters['inc_q'].mean(), 2)}")
print(f"  Avg education:   {round(adopters['educ'].mean(), 2)}")
print(f"  % internet user: {round(adopters['internet_use'].mean()*100, 1)}%")
print(f"  % saved (formal):{round(adopters['saved'].mean()*100, 1)}%")

print("\n── Done ──────────────────────────────────────────────────────────────")
