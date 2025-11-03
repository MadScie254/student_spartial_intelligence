# SpatialIQ: AI-Driven Prediction of Students' Spatial Intelligence

## 🎯 Project Overview

**SpatialIQ** is a comprehensive machine learning research project that predicts high school students' **spatial intelligence levels** using behavioral, academic, and demographic features. This project combines rigorous statistical analysis, interpretable machine learning, and interactive visualization to provide actionable insights for educators and researchers.

### Key Contributions:

- **Predictive Models**: Four complementary ML algorithms (Logistic Regression, Random Forest, XGBoost, Neural Networks)
- **Interpretability**: SHAP-based explanation methods revealing feature contributions to predictions
- **Feature Engineering**: Domain-driven engineered features capturing latent educational constructs
- **Interactive Dashboard**: Streamlit app for single and batch predictions with personalized recommendations
- **Reproducible Research**: Modular code structure enabling replication and extension

---

## 📊 Dataset Overview

### Data Source:
**Citation:** DOI: 10.21227/5qxw-bw66

### Dataset Characteristics:
- **Sample Size**: 398 high school students
- **Features**: 40 behavioral, academic, and demographic attributes
- **Target Variable**: Spatial Intelligence (5 ordinal classes: VL, L, M, H, VH)
- **Data Modality**: Multimodal (numeric, categorical, ordinal)

### Feature Categories:

1. **Demographics** (Age, Gender, Class Size, Environment)
2. **Socioeconomic** (Family Size, Parental Occupation/Education, Income)
3. **Academic** (Major, GPA, Study Time, Extra Classes, Teacher Assessment)
4. **Behavioral** (Internet Usage, TV Watching, Pattern Recognition, Geographic Familiarity)
5. **Gaming Preferences** (Action, Adventure, Strategy, Sport, Simulation, Role-playing, Puzzle)
6. **Learning Modes** (Visual vs. Auditory, Map Usage, Diagram Usage, GIS Experience)

---

## 🏗️ Project Architecture

```
student_spatial_intelligence/
├── data/
│   └── Dataset.csv                           # Raw dataset
├── visualizations/                           # Generated plots and charts
├── SpatialIQ_Comprehensive_Analysis.ipynb   # Main analysis notebook
├── data_prep.py                              # Data preprocessing module
├── model_train.py                            # Model training framework
├── app.py                                    # Streamlit interactive dashboard
├── requirements.txt                          # Python dependencies
└── README.md                                 # This file
```

---

## 🔬 Methodological Framework

### Step 1: Exploratory Data Analysis
- Comprehensive statistical profiling of all features
- Distribution analysis and outlier detection
- Missing value assessment and handling
- Correlation and mutual information analysis

### Step 2: Intelligent Data Preprocessing
- **Ordinal Encoding**: For hierarchical categorical features (e.g., education levels)
- **One-Hot Encoding**: For nominal categorical features (e.g., gender, major)
- **Standardization**: StandardScaler normalization for numeric features
- **Feature Engineering**: Domain-driven derived features

### Step 3: Feature Engineering
Created meaningful derived features capturing educational constructs:
- `Study_Efficiency = Study_Time / GPA`
- `Gaming_Engagement = Sum of all gaming preferences`
- `Visual_Learning = Map usage + Diagram usage`
- `Academic_Support = Extra classes + Parental education`
- `Digital_Lifestyle = Internet usage + Gaming engagement`

### Step 4: Dimensionality Reduction
- Principal Component Analysis (PCA) for variance-preserving reduction
- Feature selection based on correlation and mutual information
- Multicollinearity assessment using Variance Inflation Factor (VIF)

### Step 5: Model Training & Evaluation
Trained and compared four complementary models with rigorous cross-validation and comprehensive metrics.

### Step 6: Model Interpretation
- **SHAP Analysis**: TreeExplainer for tree-based models
- **Feature Importance**: Built-in and permutation-based approaches
- **Actionable Insights**: Research narrative with educator recommendations

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook or JupyterLab
- Streamlit (for interactive dashboard)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/student_spatial_intelligence.git
cd student_spatial_intelligence
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Usage

#### Run Jupyter Notebook (Recommended for analysis)
```bash
jupyter notebook SpatialIQ_Comprehensive_Analysis.ipynb
```

#### Run Streamlit Dashboard (For predictions)
```bash
streamlit run app.py
```

---

## ⚠️ Ethical Considerations

### Important Caveats:
1. **Not Deterministic**: Predictions are probabilistic; individual performance may differ
2. **Developmental**: Spatial intelligence is highly trainable; low scores aren't fixed
3. **Non-Discriminatory**: Never use for limiting educational opportunities
4. **Bias Awareness**: Gender differences reflect socialization, not ability
5. **Transparency**: Always explain model limitations to stakeholders

### Key Recommendations:
- Focus on **identifying strengths** for development
- Provide **visual learning resources** and spatial reasoning practice
- Avoid **tracking students** based on predictions
- Ensure **accessibility** of learning opportunities
- Conduct **regular bias audits** for fairness

---

## 📚 References

**Dataset Citation:** DOI: 10.21227/5qxw-bw66

**Key References:**
- Gardner, H. (1983). *Frames of Mind: The Theory of Multiple Intelligences*
- Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system
- Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions

---

## 📄 Citation

If you use this project in your research:

```bibtex
@project{spatialiq2024,
  title={SpatialIQ: AI-Driven Prediction of Students' Spatial Intelligence},
  author={AI Research Developer},
  year={2024},
  url={https://github.com/yourusername/student_spatial_intelligence}
}
```

---

**Last Updated:** November 2024  
**Project Status:** Active Research & Development

