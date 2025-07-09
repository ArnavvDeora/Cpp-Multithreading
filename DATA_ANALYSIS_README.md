# Customer Dataset Analysis Project

This project provides comprehensive data preprocessing and analysis tools for your customer dataset. The scripts address the 5 data anomaly types you specified and include analysis templates for answering your 6 research questions.

## 📋 Prerequisites

### Required Dependencies
Install the required packages using:
```bash
pip install -r requirements.txt
```

### Dataset Requirements
- Your dataset should be in Parquet format
- Variables var_44 to var_50 should be boolean (0/1) columns
- The dataset should contain customer interest scores, spending data, and offer response data

## 🔧 Data Preprocessing

The `data_preprocessing.py` script addresses all 5 anomaly types mentioned in your requirements:

### 1. Duplicate Removal
- **Issue**: Duplicate records in the dataset
- **Solution**: Removes duplicate records and keeps only the latest one
- **Method**: Uses `drop_duplicates(keep='last')` to retain the most recent entry

### 2. Datatype Conversions
- **Issue**: Inconsistent data types across columns
- **Solution**: Converts columns to appropriate data types
- **Method**: 
  - Customer IDs → String
  - Numeric variables → Float/Integer
  - Interest scores → Float

### 3. Date Format Mismatch
- **Issue**: Incorrect date formats (e.g., 28/07/2025 instead of MM/DD/YYYY)
- **Solution**: Standardizes all date formats
- **Method**: Handles DD/MM/YYYY, MM/DD/YYYY, and other common formats

### 4. Out-of-Bound Values
- **Issue**: Values outside acceptable ranges
- **Solution**: Filters out invalid records
- **Criteria**:
  - Probability scores: Must be between 0-1
  - Spending amounts: Must be non-negative
  - Interest scores: Must be between 0-1

### 5. Boolean Value Correction
- **Issue**: String values ('True'/'False') instead of binary (1/0)
- **Solution**: Converts categorical strings to binary
- **Method**: 
  - 'True', '1', 'Yes' → 1
  - 'False', '0', 'No' → 0
  - Applies to var_44 through var_50 and other specified columns

## 📊 Analysis Framework

The `analysis_questions.py` script provides a comprehensive analysis framework with 6 main question categories:

### Question 1: Customer Interest Analysis
- Analyzes interest patterns across different categories
- Calculates average, median, and distribution of interest scores
- Identifies high-interest customer segments
- Creates correlation matrix between different interests

### Question 2: Spending Behavior Analysis
- Examines customer spending patterns
- Analyzes total spending, average spending per customer
- Identifies top spenders (95th percentile)
- Compares spending across different categories

### Question 3: Offer Response Analysis
- Studies customer response to different offer types
- Calculates response rates for each offer category
- Analyzes offer effectiveness

### Question 4: Boolean Variables Analysis (var_44 to var_50)
- Examines the distribution of boolean variables
- Calculates positive/negative rates for each variable
- Analyzes correlations between boolean variables

### Question 5: Customer Segmentation
- Segments customers based on spending behavior
- Creates interest-based customer segments
- Analyzes characteristics of each segment

### Question 6: Predictive Analysis
- Identifies factors that predict high spending
- Analyzes what predicts offer response
- Provides correlation analysis for predictive modeling

## 🚀 Usage Instructions

### Step 1: Prepare Your Dataset
1. Place your parquet file in the project directory
2. Update the file path in the scripts

### Step 2: Run Data Preprocessing
```bash
python data_preprocessing.py
```

This will:
- Load your original parquet file
- Apply all 5 data cleaning procedures
- Save the cleaned dataset as `cleaned_dataset.parquet`
- Generate a summary report of the cleaning process

### Step 3: Run Analysis
```bash
python analysis_questions.py
```

This will:
- Load the cleaned dataset
- Execute all 6 analysis questions
- Generate comprehensive insights
- Create visualizations
- Save results and plots

## 📈 Expected Outputs

### From Preprocessing Script:
- `cleaned_dataset.parquet` - Your cleaned dataset
- `cleaned_dataset.csv` - CSV version for easy inspection
- Console output with cleaning statistics

### From Analysis Script:
- Comprehensive analysis report in console
- `dataset_analysis_plots.png` - Key visualizations
- Detailed insights for each of the 6 question categories

## 🔍 Variable Descriptions

Based on your dataset description, key variables include:

**Interest Scores**: 
- Interest scores for various categories (entertainment, hobby, construction, etc.)
- Range: 0-1 (probability scores)

**Spending Variables**:
- Spending amounts in different categories
- Monthly/lifetime spending patterns

**Boolean Variables (var_44 to var_50)**:
- Binary indicators (0/1)
- Various customer characteristics or behaviors

**Offer Variables**:
- Customer response to different offer types
- Click-through rates and conversion metrics

## ⚠️ Important Notes

1. **Data Quality**: The preprocessing script will remove rows with critical data quality issues
2. **Missing Values**: Some missing values are acceptable and handled appropriately
3. **Boolean Conversion**: Ensure var_44 to var_50 are correctly identified as boolean columns
4. **Custom Variables**: You may need to adjust column names based on your specific dataset structure

## 🛠️ Customization

To adapt the scripts for your specific dataset:

1. **Update Column Names**: Modify the column identification patterns in both scripts
2. **Adjust Thresholds**: Change the bounds for out-of-range value detection
3. **Add Custom Analysis**: Extend the analysis functions for your specific research questions
4. **Modify Visualizations**: Customize the plotting functions for your presentation needs

## 📝 Example Workflow

### Complete Analysis Pipeline
```bash
# 1. Run complete preprocessing and analysis
python run_complete_analysis.py
```

### Individual Question Analysis
```bash
# 1. First, run preprocessing if not done already
python data_preprocessing.py

# 2. Run specific question analysis
python run_question1.py  # For Question 1 about Amex Portal users
```

### Programmatic Usage
```python
# 1. Load and clean data
from data_preprocessing import clean_dataset
cleaned_df = clean_dataset('your_dataset.parquet')

# 2. Analyze the cleaned data
from analysis_questions import DatasetAnalyzer
analyzer = DatasetAnalyzer('cleaned_dataset.parquet')
results = analyzer.generate_comprehensive_report()

# 3. Run specific question analysis
from question1_amex_analysis import AmexPortalAnalyzer
q1_analyzer = AmexPortalAnalyzer('cleaned_dataset.parquet')
q1_results = q1_analyzer.solve_question_1()

# 4. Create visualizations
analyzer.create_visualizations()
```

## 🎯 Question 1 Analysis

The project includes a dedicated analysis for **Question 1** about Amex Portal active users:

### Question 1 Requirements:
1. **Statement 1**: Active Users of the Amex Portal are more likely to choose Airline Offers than other offer categories
2. **Statement 2**: Active Users of the Amex Portal are generally able to save more money from Discounts than other users  
3. **Population Count**: Total unique customer IDs who actively use the Amex Portal and have clicked on an Airline Offer

### Running Question 1:
```bash
python run_question1.py
```

### Expected Outputs:
- `question1_results.txt` - Summary of TRUE/FALSE answers and population count
- Detailed console analysis showing methodology and calculations
- Automatic detection of relevant columns in your dataset

### Active User Definition:
- Users who visited the Amex Portal at least once in the past 30 days from any given date
- The script automatically identifies active users using available data columns

## 🤝 Support

If you encounter any issues:
1. Check that your parquet file path is correct
2. Verify all dependencies are installed
3. Ensure your dataset contains the expected column types
4. Review the console output for specific error messages

The scripts are designed to be robust and handle most common data quality issues automatically.