"""
Data Preprocessing Module for SpatialIQ Prediction System

This module handles all data loading, validation, encoding, and transformation operations.
It provides a clean, reusable pipeline for preparing raw dataset for machine learning.

Author: AI Research Developer
Purpose: Support reproducible data preprocessing for spatial intelligence prediction
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, List
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder, OneHotEncoder
from sklearn.impute import SimpleImputer
import warnings

warnings.filterwarnings('ignore')


class DataPreprocessor:
    """
    Comprehensive data preprocessing pipeline for spatial intelligence prediction.
    
    This class orchestrates the entire data preparation workflow including:
    - Loading and validating raw data
    - Identifying and handling missing values
    - Intelligent encoding of categorical variables
    - Standardization of numeric features
    - Feature engineering from domain knowledge
    """
    
    def __init__(self, data_path: str):
        """
        Initialize the DataPreprocessor.
        
        Args:
            data_path (str): Path to the CSV dataset file
        """
        self.data_path = Path(data_path)
        self.df = None
        self.X = None
        self.y = None
        self.target_col = None
        self.numeric_features = []
        self.categorical_features = []
        self.scaler = None
        self.le_target = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load dataset from CSV file with validation checks.
        
        Returns:
            pd.DataFrame: Loaded dataset
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            ValueError: If dataset is empty or invalid
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
        
        self.df = pd.read_csv(self.data_path)
        
        if self.df.empty:
            raise ValueError("Dataset is empty")
        
        print(f"✓ Data loaded: {self.df.shape[0]} rows × {self.df.shape[1]} columns")
        return self.df
    
    def identify_target(self) -> str:
        """
        Identify the target variable (typically the last column).
        
        Returns:
            str: Name of the target column
        """
        self.target_col = self.df.columns[-1]
        print(f"✓ Target variable identified: {self.target_col}")
        return self.target_col
    
    def separate_features_target(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Separate features and target variable.
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Features and target series
        """
        self.X = self.df.drop(columns=[self.target_col])
        self.y = self.df[self.target_col]
        
        print(f"✓ Features: {self.X.shape[1]}")
        print(f"✓ Target classes: {self.y.nunique()} ({sorted(self.y.unique())})")
        return self.X, self.y
    
    def classify_features(self) -> Dict[str, List[str]]:
        """
        Classify features by data type (numeric vs categorical).
        
        Returns:
            Dict: Dictionary with 'numeric' and 'categorical' feature lists
        """
        self.numeric_features = self.X.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_features = self.X.select_dtypes(include=['object']).columns.tolist()
        
        print(f"\n✓ Numeric features: {len(self.numeric_features)}")
        print(f"✓ Categorical features: {len(self.categorical_features)}")
        
        return {
            'numeric': self.numeric_features,
            'categorical': self.categorical_features
        }
    
    def handle_missing_values(self, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values through imputation.
        
        Args:
            strategy (str): Imputation strategy ('mean', 'median', 'mode', 'drop')
            
        Returns:
            pd.DataFrame: Dataset with missing values handled
        """
        initial_missing = self.X.isnull().sum().sum()
        
        if initial_missing == 0:
            print("✓ No missing values detected")
            return self.X
        
        if strategy == 'drop':
            self.X = self.X.dropna()
            print(f"✓ Removed {initial_missing} rows with missing values")
        else:
            imputer = SimpleImputer(strategy=strategy)
            self.X[self.numeric_features] = imputer.fit_transform(self.X[self.numeric_features])
            print(f"✓ Imputed {initial_missing} missing values using {strategy}")
        
        return self.X
    
    def encode_target(self) -> np.ndarray:
        """
        Encode target variable using ordinal encoding to preserve class order.
        
        Returns:
            np.ndarray: Encoded target values
        """
        self.le_target = LabelEncoder()
        self.y = pd.Series(self.le_target.fit_transform(self.y), index=self.y.index)
        
        print(f"✓ Target encoded: {dict(zip(self.le_target.classes_, range(len(self.le_target.classes_))))}")
        return self.y
    
    def encode_categorical_features(self, method: str = 'onehot') -> pd.DataFrame:
        """
        Encode categorical features using specified method.
        
        Args:
            method (str): Encoding method ('onehot' or 'ordinal')
            
        Returns:
            pd.DataFrame: Dataset with encoded categorical features
        """
        if method == 'onehot':
            X_encoded = pd.get_dummies(self.X, columns=self.categorical_features, 
                                       drop_first=False, dtype=int)
            print(f"✓ One-Hot Encoding applied to {len(self.categorical_features)} features")
        else:
            encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
            X_categorical = self.X[self.categorical_features].copy()
            X_encoded = self.X.copy()
            X_encoded[self.categorical_features] = encoder.fit_transform(X_categorical)
            print(f"✓ Ordinal Encoding applied to {len(self.categorical_features)} features")
        
        return X_encoded
    
    def standardize_numeric_features(self, X_encoded: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize numeric features using StandardScaler.
        
        Args:
            X_encoded (pd.DataFrame): Dataset with encoded categorical features
            
        Returns:
            pd.DataFrame: Dataset with standardized numeric features
        """
        numeric_cols = X_encoded.select_dtypes(include=[np.number]).columns.tolist()
        
        self.scaler = StandardScaler()
        X_scaled = X_encoded.copy()
        X_scaled[numeric_cols] = self.scaler.fit_transform(X_encoded[numeric_cols].fillna(0))
        
        print(f"✓ Standardized {len(numeric_cols)} numeric features (mean=0, std=1)")
        return X_scaled
    
    def create_engineered_features(self, X_processed: pd.DataFrame) -> pd.DataFrame:
        """
        Create domain-driven engineered features from existing variables.
        
        Args:
            X_processed (pd.DataFrame): Processed feature set
            
        Returns:
            pd.DataFrame: Dataset with additional engineered features
        """
        X_engineered = X_processed.copy()
        
        # Identify columns for feature engineering
        study_cols = [col for col in self.X.columns if 'study' in col.lower()]
        gpa_cols = [col for col in self.X.columns if 'gpa' in col.lower()]
        game_cols = [col for col in self.X.columns if col.startswith('G-')]
        visual_cols = [col for col in self.X.columns if any(x in col.lower() for x in ['map', 'diagram'])]
        internet_cols = [col for col in self.X.columns if 'internet' in col.lower()]
        
        # Create engineered features
        if study_cols and gpa_cols:
            X_engineered['Study_Efficiency'] = self.X[study_cols[0]] / (self.X[gpa_cols[0]] + 1e-6)
            
        if game_cols:
            X_engineered['Gaming_Engagement'] = self.X[game_cols].sum(axis=1)
            
        if visual_cols:
            X_engineered['Visual_Learning'] = self.X[visual_cols].sum(axis=1)
            
        if internet_cols:
            X_engineered['Internet_Usage'] = self.X[internet_cols[0]]
        
        print(f"✓ Created {len([col for col in X_engineered.columns if col not in X_processed.columns])} engineered features")
        return X_engineered
    
    def get_processed_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Execute the complete preprocessing pipeline and return processed data.
        
        Returns:
            Tuple[pd.DataFrame, pd.Series]: Processed features and encoded target
        """
        print("\n" + "=" * 80)
        print("EXECUTING COMPLETE PREPROCESSING PIPELINE")
        print("=" * 80 + "\n")
        
        # Step 1: Load and validate
        self.load_data()
        self.identify_target()
        self.separate_features_target()
        
        # Step 2: Classify and inspect
        self.classify_features()
        self.handle_missing_values()
        
        # Step 3: Encoding
        self.encode_target()
        X_encoded = self.encode_categorical_features()
        
        # Step 4: Standardization
        X_scaled = self.standardize_numeric_features(X_encoded)
        
        # Step 5: Feature Engineering
        X_final = self.create_engineered_features(X_scaled)
        
        print("\n" + "=" * 80)
        print(f"✓ PREPROCESSING COMPLETE")
        print(f"  Final feature set: {X_final.shape[1]} features")
        print(f"  Sample size: {X_final.shape[0]} students")
        print("=" * 80 + "\n")
        
        return X_final, self.y


def prepare_data(data_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Convenience function to prepare data in one call.
    
    Args:
        data_path (str): Path to CSV dataset
        
    Returns:
        Tuple[pd.DataFrame, pd.Series]: Processed features and target
    """
    preprocessor = DataPreprocessor(data_path)
    X, y = preprocessor.get_processed_data()
    return X, y


if __name__ == "__main__":
    # Example usage
    X, y = prepare_data("data/Dataset.csv")
    print(f"\nFinal dataset shape: {X.shape}")
    print(f"Target variable shape: {y.shape}")
    print(f"\nFirst few rows of processed features:")
    print(X.head())
