# makes a throwaway model so the Part 11 API has something to load
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(42)
n = 500

# fake students
df = pd.DataFrame({
    "hours_studied": rng.uniform(0, 20, n),
    "attendance":    rng.uniform(0, 100, n),
})

# invent a rule: more hours and more attendance means more likely to pass
score = df["hours_studied"] * 0.4 + df["attendance"] * 0.05
passed = (score + rng.normal(0, 1, n) > 5).astype(int)

model = LogisticRegression()
model.fit(df, passed)

Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/model.joblib")

print("saved to models/model.joblib")
print("pass rate in the fake data:", round(passed.mean(), 2))

example = pd.DataFrame([{"hours_studied": 10, "attendance": 80}])
print("10 hours, 80% attendance ->", model.predict_proba(example)[0, 1].round(3))