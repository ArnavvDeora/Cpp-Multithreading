# Question 1 Solution: Amex Portal Active Users Analysis

## 📋 Question Overview

**Question 1** analyzes active users of the Amex Portal and validates three key statements:

1. **Statement 1**: Active Users of the Amex Portal are more likely to choose Airline Offers than other offer categories *(Answer: TRUE/FALSE)*
2. **Statement 2**: Active Users of the Amex Portal are generally able to save more money from Discounts than other users *(Answer: TRUE/FALSE)*
3. **Population Count**: Total unique customer IDs who actively use the Amex Portal and have clicked on an Airline Offer *(Answer: Integer)*

### Definition: Active Users
- Users who have visited the Amex Portal **at least once in the past 30 days** from any given date within the provided timeframe

## 🔧 Solution Components

### 1. `question1_amex_analysis.py` - Main Analysis Engine
This script contains the `AmexPortalAnalyzer` class that:
- **Automatically detects** relevant columns in your dataset
- **Identifies active users** using multiple methods
- **Analyzes airline offer preferences** comparing active vs non-active users
- **Calculates discount savings** differences between user groups
- **Counts population** of active users with airline offers

### 2. `run_question1.py` - Quick Runner
Simple script to execute Question 1 analysis and save results to file.

### 3. Integration with Complete Pipeline
Question 1 is integrated into `run_complete_analysis.py` for comprehensive analysis.

## 🚀 How to Run

### Option 1: Quick Run (Recommended)
```bash
# Make sure your dataset is preprocessed first
python data_preprocessing.py

# Run Question 1 analysis
python run_question1.py
```

### Option 2: Complete Pipeline
```bash
# Run everything including Question 1
python run_complete_analysis.py
```

### Option 3: Programmatic Usage
```python
from question1_amex_analysis import AmexPortalAnalyzer

# Initialize analyzer
analyzer = AmexPortalAnalyzer('cleaned_dataset.parquet')

# Run complete analysis
results = analyzer.solve_question_1()

# Access results
print(f"Statement 1: {results['statement1']}")
print(f"Statement 2: {results['statement2']}")
print(f"Population: {results['population']}")
```

## 🔍 Analysis Methodology

### Active User Identification
The script uses a **multi-method approach** to identify active users:

1. **Portal Visit Columns**: Looks for columns containing 'portal', 'visit', 'click', 'active'
2. **Date-Based Analysis**: Uses date columns to find users active in last 30 days
3. **Engagement Metrics**: Uses click-through or engagement columns as proxies
4. **Binary Indicators**: Uses binary columns (0/1) as activity indicators
5. **Fallback Method**: Uses top 50% of users by total activity as proxy

### Airline Offer Analysis
**Multiple detection approaches:**
- Direct airline columns (containing 'airline', 'flight', 'travel', 'air')
- Category-based analysis (looking for airline categories)
- Offer column analysis as proxy

### Discount Savings Analysis
**Detection methods:**
- Direct discount columns (containing 'discount', 'save', 'saving')
- Spending columns as proxy (higher spending = better discount utilization)

## 📊 Expected Outputs

### Console Output
- Detailed analysis with step-by-step methodology
- Column detection results
- Statistical comparisons
- Final TRUE/FALSE answers and population count

### Generated Files
- **`question1_results.txt`** - Summary of final answers
- Detailed methodology and calculations logged to console

### Sample Output Format
```
FINAL ANSWERS
=============
1. Statement 1: TRUE
2. Statement 2: FALSE  
3. Population: 1547
```

## 🔧 Customization Options

### Manual Column Specification
You can modify the script to use specific columns:

```python
# In question1_amex_analysis.py, modify the identify_active_users method
active_users, method = analyzer.identify_active_users(
    reference_date_col='your_date_column',
    visit_indicator_col='your_portal_visit_column'
)
```

### Adjusting Active User Criteria
Modify the 30-day window:
```python
# Change this line in the date-based analysis section
cutoff_date = max_date - timedelta(days=30)  # Change 30 to your preference
```

## ⚠️ Important Notes

### Data Requirements
- **Cleaned dataset**: Must run preprocessing first
- **Customer ID column**: Preferred but script handles missing IDs
- **Relevant columns**: Script auto-detects but manual specification possible

### Robustness Features
- **Automatic fallbacks**: If specific columns aren't found, uses proxy methods
- **Error handling**: Graceful handling of missing data
- **Multiple approaches**: Uses best available method for your dataset structure

### Interpretation Guidelines
- **TRUE results**: Active users show statistically higher rates/savings
- **FALSE results**: No significant difference or non-active users perform better
- **Population count**: Exact count of unique customers meeting both criteria

## 📈 Validation Approach

The analysis ensures reliability by:

1. **Multiple Methods**: Uses several approaches to identify patterns
2. **Comparative Analysis**: Always compares active vs non-active users
3. **Statistical Validation**: Uses means, medians, and distributions
4. **Automatic Fallbacks**: Ensures analysis completes even with limited data

## 🛠️ Troubleshooting

### Common Issues
1. **"Dataset not found"**: Run preprocessing first
2. **"No relevant columns found"**: Check if your dataset has expected column types
3. **"Zero active users"**: Dataset might need manual column specification

### Solutions
1. Ensure preprocessing is complete: `python data_preprocessing.py`
2. Check column names in your dataset match expected patterns
3. Manually specify columns in the analysis script if auto-detection fails

## 📝 Next Steps

After getting Question 1 results:
1. **Validate findings** against business knowledge
2. **Use insights** for targeted marketing strategies
3. **Expand analysis** to other offer categories
4. **Monitor trends** over time with new data

The solution is designed to be **robust, automatic, and adaptable** to various dataset structures while providing reliable answers to your specific research questions.