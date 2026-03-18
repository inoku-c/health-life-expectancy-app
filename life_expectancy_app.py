life_expectancy_app.py"""
life_expectancy_app.py
======================

This script demonstrates a simple approach to estimate an individual's
"healthy life expectancy" based on common health and lifestyle factors.
It is **not** a medical device and should not be used to make decisions in
healthcare or insurance domains.  The model is trained on a synthetic
dataset created for demonstration purposes only.

The features used include:

  - `age` (years): chronological age of the individual.
  - `gender` (0 for male, 1 for female): sex assigned at birth.
  - `bmi` (kg/m²): body mass index.
  - `smoking` (0/1): whether the person currently smokes.
  - `alcohol` (0/1): whether the person consumes alcohol frequently.
  - `physical_activity` (0/1): whether the person meets recommended physical activity
    levels (≥150 minutes of moderate or ≥75 minutes of vigorous activity per week).
  - `diet` (0/1): whether the person follows a healthy diet (rich in fruits,
    vegetables, whole grains and lean proteins, and low in refined sugars and
    saturated fat).
  - `blood_pressure` (mmHg): systolic blood pressure.
  - `cholesterol` (mg/dL): total cholesterol concentration.
  - `chronic_condition` (0/1): whether the person has a major chronic
    condition (e.g., diabetes, heart disease, hypertension, asthma).

The synthetic dataset is generated using reasonable rules of thumb drawn from
epidemiological literature: poor lifestyle factors and chronic conditions
reduce expected lifespan, while healthy behaviours and optimal biometrics
extend it.  The base life expectancy is set around 90 years for illustrative
purposes.

The trained model is a random forest regressor from scikit‑learn.  Once
trained, the script exposes a `predict_life_expectancy` function that takes
a dictionary of feature values and returns the estimated life expectancy.

Because this example relies on randomly simulated data, the resulting
predictions should be viewed purely as an educational tool.  In a real
application you would train the model on a large, validated cohort dataset
containing actual clinical and lifestyle information, following rigorous
ethical guidelines for data handling, model validation and bias mitigation.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib


def generate_synthetic_dataset(n_samples: int = 5000, random_state: int = 42) -> pd.DataFrame:
    """Generate a synthetic dataset for life expectancy prediction.

    Parameters
    ----------
    n_samples : int
        Number of synthetic individuals to simulate.
    random_state : int
        Seed for reproducibility.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing feature columns and the target (life_expectancy).
    """
    rng = np.random.default_rng(random_state)

    # Continuous variables
    ages = rng.integers(20, 81, size=n_samples)  # Age between 20 and 80
    gender = rng.integers(0, 2, size=n_samples)  # 0 = male, 1 = female
    bmi = rng.uniform(18.0, 40.0, size=n_samples)  # BMI 18–40
    blood_pressure = rng.uniform(90.0, 180.0, size=n_samples)  # Systolic blood pressure
    cholesterol = rng.uniform(150.0, 300.0, size=n_samples)  # Total cholesterol

    # Binary variables (0 or 1)
    smoking = rng.integers(0, 2, size=n_samples)
    alcohol = rng.integers(0, 2, size=n_samples)
    physical_activity = rng.integers(0, 2, size=n_samples)
    diet = rng.integers(0, 2, size=n_samples)
    chronic_condition = rng.integers(0, 2, size=n_samples)

    # Calculate baseline remaining years
    base_expectancy = 90.0  # baseline life expectancy (years)
    remaining_years = (
        base_expectancy
        - ages
        # BMI penalty: distance from BMI=21; penalise overweight/underweight
        - np.abs(bmi - 21.0) * 0.5
        # Smoking penalty
        - smoking * 5.0
        # Alcohol penalty
        - alcohol * 3.0
        # Physical activity: +2 if active, -2 if not
        + (physical_activity * 2.0) - ((1 - physical_activity) * 2.0)
        # Diet: +2 if healthy, -2 if unhealthy
        + (diet * 2.0) - ((1 - diet) * 2.0)
        # Blood pressure penalty relative to optimal 120 mmHg
        - (blood_pressure - 120.0) * 0.05
        # Cholesterol penalty relative to optimal 200 mg/dL
        - (cholesterol - 200.0) * 0.03
        # Chronic condition penalty
        - chronic_condition * 5.0
    )

    # Ensure remaining years are at least 5 years
    remaining_years = np.maximum(remaining_years, 5.0)
    life_expectancy = ages + remaining_years

    data = {
        "age": ages,
        "gender": gender,
        "bmi": bmi,
        "smoking": smoking,
        "alcohol": alcohol,
        "physical_activity": physical_activity,
        "diet": diet,
        "blood_pressure": blood_pressure,
        "cholesterol": cholesterol,
        "chronic_condition": chronic_condition,
        "life_expectancy": life_expectancy,
    }
    df = pd.DataFrame(data)
    return df


def train_model(df: pd.DataFrame) -> RandomForestRegressor:
    """Train a random forest regressor on the synthetic dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing features and target.

    Returns
    -------
    model : RandomForestRegressor
        Trained model.
    """
    features = [
        "age",
        "gender",
        "bmi",
        "smoking",
        "alcohol",
        "physical_activity",
        "diet",
        "blood_pressure",
        "cholesterol",
        "chronic_condition",
    ]
    X = df[features]
    y = df["life_expectancy"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"Training complete. Mean Absolute Error on holdout: {mae:.2f} years")
    return model


def predict_life_expectancy(model: RandomForestRegressor, user_features: dict) -> float:
    """Estimate life expectancy given user input features.

    Parameters
    ----------
    model : RandomForestRegressor
        Trained random forest model.
    user_features : dict
        Dictionary mapping feature names to values. Required keys: age, gender,
        bmi, smoking, alcohol, physical_activity, diet, blood_pressure,
        cholesterol, chronic_condition.

    Returns
    -------
    float
        Predicted life expectancy in years.
    """
    feature_order = [
        "age",
        "gender",
        "bmi",
        "smoking",
        "alcohol",
        "physical_activity",
        "diet",
        "blood_pressure",
        "cholesterol",
        "chronic_condition",
    ]
    X_new = np.array([[user_features[k] for k in feature_order]])
    prediction = model.predict(X_new)[0]
    return float(prediction)


def main():
    """Entry point for running the training and demonstrating a prediction."""
    df = generate_synthetic_dataset()
    model = train_model(df)
    # Save the model
    joblib.dump(model, "life_expectancy_model.pkl")
    print("Model saved to life_expectancy_model.pkl")

    # Demonstration using a hypothetical user
    user = {
        "age": 45,
        "gender": 0,  # male
        "bmi": 28.0,
        "smoking": 1,
        "alcohol": 0,
        "physical_activity": 1,
        "diet": 0,
        "blood_pressure": 130.0,
        "cholesterol": 220.0,
        "chronic_condition": 0,
    }
    estimated_le = predict_life_expectancy(model, user)
    print(f"Estimated life expectancy for sample user: {estimated_le:.1f} years")


if __name__ == "__main__":
    main()
