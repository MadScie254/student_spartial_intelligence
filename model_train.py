"""
Model Training Module for SpatialIQ Prediction System

This module implements training and evaluation of multiple machine learning models
for predicting students' spatial intelligence levels. It provides a unified interface
for model selection, hyperparameter tuning, and cross-validation.

Author: AI Research Developer
Purpose: Scalable model training and comparison framework
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import warnings

warnings.filterwarnings('ignore')


class ModelTrainer:
    """
    Comprehensive model training and evaluation framework.
    
    This class manages the lifecycle of multiple ML models including:
    - Model initialization with optimized hyperparameters
    - Training with cross-validation
    - Evaluation with comprehensive metrics
    - Feature importance extraction
    """
    
    def __init__(self, X_train: pd.DataFrame, X_test: pd.DataFrame, 
                 y_train: np.ndarray, y_test: np.ndarray, random_state: int = 42):
        """
        Initialize the ModelTrainer.
        
        Args:
            X_train: Training features
            X_test: Testing features
            y_train: Training target
            y_test: Testing target
            random_state: Random seed for reproducibility
        """
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.random_state = random_state
        
        self.models = {}
        self.predictions = {}
        self.probabilities = {}
        self.cv_scores = {}
        self.test_scores = {}
        
        # Initialize cross-validation strategy
        self.cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    
    def train_logistic_regression(self) -> 'LogisticRegression':
        """
        Train Logistic Regression baseline model.
        
        Returns:
            Trained LogisticRegression model
        """
        print("\n" + "=" * 80)
        print("TRAINING: LOGISTIC REGRESSION (BASELINE)")
        print("=" * 80)
        
        model = LogisticRegression(
            max_iter=1000,
            random_state=self.random_state,
            multi_class='multinomial',
            solver='lbfgs',
            class_weight='balanced'
        )
        
        # Cross-validation
        cv_scores = cross_validate(
            model, self.X_train, self.y_train,
            cv=self.cv,
            scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'],
            return_train_score=True
        )
        
        self.cv_scores['Logistic_Regression'] = cv_scores
        
        print(f"\nCross-Validation Results:")
        print(f"  Accuracy:  {cv_scores['test_accuracy'].mean():.4f} (+/- {cv_scores['test_accuracy'].std():.4f})")
        print(f"  Precision: {cv_scores['test_precision_macro'].mean():.4f} (+/- {cv_scores['test_precision_macro'].std():.4f})")
        print(f"  Recall:    {cv_scores['test_recall_macro'].mean():.4f} (+/- {cv_scores['test_recall_macro'].std():.4f})")
        print(f"  F1-Score:  {cv_scores['test_f1_macro'].mean():.4f} (+/- {cv_scores['test_f1_macro'].std():.4f})")
        
        # Train on full training set
        model.fit(self.X_train, self.y_train)
        
        # Evaluate on test set
        self._evaluate_model(model, 'Logistic_Regression')
        
        self.models['Logistic_Regression'] = model
        return model
    
    def train_random_forest(self) -> 'RandomForestClassifier':
        """
        Train Random Forest Classifier with optimized hyperparameters.
        
        Returns:
            Trained RandomForestClassifier model
        """
        print("\n" + "=" * 80)
        print("TRAINING: RANDOM FOREST CLASSIFIER")
        print("=" * 80)
        
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=self.random_state,
            n_jobs=-1,
            class_weight='balanced'
        )
        
        # Cross-validation
        cv_scores = cross_validate(
            model, self.X_train, self.y_train,
            cv=self.cv,
            scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'],
            return_train_score=True
        )
        
        self.cv_scores['Random_Forest'] = cv_scores
        
        print(f"\nCross-Validation Results:")
        print(f"  Accuracy:  {cv_scores['test_accuracy'].mean():.4f} (+/- {cv_scores['test_accuracy'].std():.4f})")
        print(f"  Precision: {cv_scores['test_precision_macro'].mean():.4f} (+/- {cv_scores['test_precision_macro'].std():.4f})")
        print(f"  Recall:    {cv_scores['test_recall_macro'].mean():.4f} (+/- {cv_scores['test_recall_macro'].std():.4f})")
        print(f"  F1-Score:  {cv_scores['test_f1_macro'].mean():.4f} (+/- {cv_scores['test_f1_macro'].std():.4f})")
        
        # Train on full training set
        model.fit(self.X_train, self.y_train)
        
        # Evaluate on test set
        self._evaluate_model(model, 'Random_Forest')
        
        self.models['Random_Forest'] = model
        return model
    
    def train_xgboost(self) -> 'XGBClassifier':
        """
        Train XGBoost Classifier with optimized hyperparameters.
        
        Returns:
            Trained XGBClassifier model
        """
        print("\n" + "=" * 80)
        print("TRAINING: XGBOOST CLASSIFIER")
        print("=" * 80)
        
        model = XGBClassifier(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=self.random_state,
            n_jobs=-1,
            eval_metric='mlogloss'
        )
        
        # Cross-validation
        cv_scores = cross_validate(
            model, self.X_train, self.y_train,
            cv=self.cv,
            scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'],
            return_train_score=True
        )
        
        self.cv_scores['XGBoost'] = cv_scores
        
        print(f"\nCross-Validation Results:")
        print(f"  Accuracy:  {cv_scores['test_accuracy'].mean():.4f} (+/- {cv_scores['test_accuracy'].std():.4f})")
        print(f"  Precision: {cv_scores['test_precision_macro'].mean():.4f} (+/- {cv_scores['test_precision_macro'].std():.4f})")
        print(f"  Recall:    {cv_scores['test_recall_macro'].mean():.4f} (+/- {cv_scores['test_recall_macro'].std():.4f})")
        print(f"  F1-Score:  {cv_scores['test_f1_macro'].mean():.4f} (+/- {cv_scores['test_f1_macro'].std():.4f})")
        
        # Train on full training set
        model.fit(self.X_train, self.y_train)
        
        # Evaluate on test set
        self._evaluate_model(model, 'XGBoost')
        
        self.models['XGBoost'] = model
        return model
    
    def train_neural_network(self) -> 'MLPClassifier':
        """
        Train Neural Network (MLPClassifier) with optimized architecture.
        
        Returns:
            Trained MLPClassifier model
        """
        print("\n" + "=" * 80)
        print("TRAINING: NEURAL NETWORK (MLP CLASSIFIER)")
        print("=" * 80)
        
        model = MLPClassifier(
            hidden_layer_sizes=(256, 128, 64),
            activation='relu',
            solver='adam',
            max_iter=500,
            random_state=self.random_state,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20,
            alpha=0.0001,
            learning_rate='adaptive'
        )
        
        # Cross-validation
        cv_scores = cross_validate(
            model, self.X_train, self.y_train,
            cv=self.cv,
            scoring=['accuracy', 'precision_macro', 'recall_macro', 'f1_macro'],
            return_train_score=True
        )
        
        self.cv_scores['Neural_Network'] = cv_scores
        
        print(f"\nCross-Validation Results:")
        print(f"  Accuracy:  {cv_scores['test_accuracy'].mean():.4f} (+/- {cv_scores['test_accuracy'].std():.4f})")
        print(f"  Precision: {cv_scores['test_precision_macro'].mean():.4f} (+/- {cv_scores['test_precision_macro'].std():.4f})")
        print(f"  Recall:    {cv_scores['test_recall_macro'].mean():.4f} (+/- {cv_scores['test_recall_macro'].std():.4f})")
        print(f"  F1-Score:  {cv_scores['test_f1_macro'].mean():.4f} (+/- {cv_scores['test_f1_macro'].std():.4f})")
        
        # Train on full training set
        model.fit(self.X_train, self.y_train)
        
        # Evaluate on test set
        self._evaluate_model(model, 'Neural_Network')
        
        self.models['Neural_Network'] = model
        return model
    
    def _evaluate_model(self, model, model_name: str):
        """
        Evaluate model on test set and store results.
        
        Args:
            model: Trained model
            model_name: Name of the model for tracking
        """
        predictions = model.predict(self.X_test)
        probabilities = model.predict_proba(self.X_test)
        
        self.predictions[model_name] = predictions
        self.probabilities[model_name] = probabilities
        
        # Calculate metrics
        accuracy = accuracy_score(self.y_test, predictions)
        precision = precision_score(self.y_test, predictions, average='macro', zero_division=0)
        recall = recall_score(self.y_test, predictions, average='macro', zero_division=0)
        f1 = f1_score(self.y_test, predictions, average='macro', zero_division=0)
        
        self.test_scores[model_name] = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1_Score': f1
        }
        
        print(f"\nTest Set Results:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
    
    def train_all_models(self) -> Dict:
        """
        Train all models in the ensemble.
        
        Returns:
            Dictionary of trained models
        """
        print("\n" + "=" * 80)
        print("TRAINING COMPLETE ENSEMBLE OF MODELS")
        print("=" * 80)
        
        self.train_logistic_regression()
        self.train_random_forest()
        self.train_xgboost()
        self.train_neural_network()
        
        print("\n" + "=" * 80)
        print("✓ ALL MODELS SUCCESSFULLY TRAINED")
        print("=" * 80)
        
        return self.models
    
    def get_best_model(self, metric: str = 'F1_Score') -> Tuple[str, object]:
        """
        Get the best performing model based on specified metric.
        
        Args:
            metric (str): Metric to use for comparison ('Accuracy', 'Precision', 'Recall', 'F1_Score')
            
        Returns:
            Tuple of (model_name, model_object)
        """
        scores_df = pd.DataFrame(self.test_scores).transpose()
        best_model_name = scores_df[metric].idxmax()
        best_model = self.models[best_model_name]
        
        print(f"\n✓ Best model: {best_model_name} (F1-Score: {scores_df.loc[best_model_name, metric]:.4f})")
        return best_model_name, best_model
    
    def get_evaluation_summary(self) -> pd.DataFrame:
        """
        Get summary of all model evaluations.
        
        Returns:
            DataFrame with evaluation metrics for all models
        """
        return pd.DataFrame(self.test_scores).transpose()


def train_models(X_train: pd.DataFrame, X_test: pd.DataFrame,
                y_train: np.ndarray, y_test: np.ndarray) -> ModelTrainer:
    """
    Convenience function to train all models.
    
    Args:
        X_train: Training features
        X_test: Testing features
        y_train: Training target
        y_test: Testing target
        
    Returns:
        Trained ModelTrainer instance
    """
    trainer = ModelTrainer(X_train, X_test, y_train, y_test)
    trainer.train_all_models()
    return trainer


if __name__ == "__main__":
    # Example usage (requires data preprocessing first)
    print("Model Training Module")
    print("Import and use with preprocessed data:")
    print("  from model_train import train_models")
    print("  trainer = train_models(X_train, X_test, y_train, y_test)")
