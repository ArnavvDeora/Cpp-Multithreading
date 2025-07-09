import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def clean_dataset(parquet_file_path):
    """
    Comprehensive data cleaning function that addresses all preprocessing requirements:
    1. Duplicate Removal
    2. Datatype Conversions
    3. Date format corrections
    4. Out-of-bound value handling
    5. Boolean value corrections
    """
    
    print("Loading dataset...")
    df = pd.read_parquet(parquet_file_path)
    print(f"Initial dataset shape: {df.shape}")
    
    # 1. DUPLICATE REMOVAL
    print("\n1. Removing duplicates...")
    initial_rows = len(df)
    # Sort by a timestamp column if available to keep the latest record
    # If no timestamp column, just drop duplicates keeping the last occurrence
    df_cleaned = df.drop_duplicates(keep='last')
    duplicates_removed = initial_rows - len(df_cleaned)
    print(f"Removed {duplicates_removed} duplicate records")
    print(f"Dataset shape after duplicate removal: {df_cleaned.shape}")
    
    # 2. DATATYPE CONVERSIONS
    print("\n2. Converting datatypes...")
    
    # Convert customer_id to string if present
    if 'customer_id' in df_cleaned.columns:
        df_cleaned['customer_id'] = df_cleaned['customer_id'].astype(str)
    
    # Convert numeric columns to appropriate types
    numeric_columns = [col for col in df_cleaned.columns if 'var_' in col and any(x in col for x in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']) and not any(x in col for x in ['44', '45', '46', '47', '48', '49', '50'])]
    for col in numeric_columns:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
    
    # Convert interest score columns to float
    interest_columns = [col for col in df_cleaned.columns if 'interest' in col.lower() or 'score' in col.lower()]
    for col in interest_columns:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
    
    print("Datatype conversions completed")
    
    # 3. DATE FORMAT CORRECTIONS
    print("\n3. Correcting date formats...")
    
    # Find date columns
    date_columns = [col for col in df_cleaned.columns if 'date' in col.lower() or 'time' in col.lower()]
    
    for col in date_columns:
        if col in df_cleaned.columns:
            print(f"Processing date column: {col}")
            # Handle various date formats
            df_cleaned[col] = df_cleaned[col].apply(fix_date_format)
    
    print("Date format corrections completed")
    
    # 4. OUT-OF-BOUND VALUES
    print("\n4. Handling out-of-bound values...")
    
    # Handle probability scores (should be between 0-1)
    probability_columns = [col for col in df_cleaned.columns if 'probability' in col.lower() or 'score' in col.lower()]
    for col in probability_columns:
        if col in df_cleaned.columns:
            initial_count = len(df_cleaned)
            # Remove rows where probability scores are not between 0 and 1
            df_cleaned = df_cleaned[
                (df_cleaned[col].isna()) | 
                ((df_cleaned[col] >= 0) & (df_cleaned[col] <= 1))
            ]
            removed_count = initial_count - len(df_cleaned)
            if removed_count > 0:
                print(f"Removed {removed_count} rows with out-of-bound values in {col}")
    
    # Handle spending columns (should not be negative)
    spend_columns = [col for col in df_cleaned.columns if 'spend' in col.lower() or 'amount' in col.lower()]
    for col in spend_columns:
        if col in df_cleaned.columns:
            initial_count = len(df_cleaned)
            # Remove rows where spending is negative
            df_cleaned = df_cleaned[
                (df_cleaned[col].isna()) | 
                (df_cleaned[col] >= 0)
            ]
            removed_count = initial_count - len(df_cleaned)
            if removed_count > 0:
                print(f"Removed {removed_count} rows with negative values in {col}")
    
    print("Out-of-bound value handling completed")
    
    # 5. BOOLEAN VALUE CORRECTIONS
    print("\n5. Correcting boolean values...")
    
    # Handle var_44 to var_50 (boolean columns)
    bool_columns = [f'var_{i}' for i in range(44, 51)]
    
    for col in bool_columns:
        if col in df_cleaned.columns:
            print(f"Processing boolean column: {col}")
            df_cleaned[col] = df_cleaned[col].apply(convert_to_binary)
    
    # Handle other categorical columns that should be binary
    categorical_binary_columns = ['offer_variable', 'var30']  # Add other columns as needed
    for col in categorical_binary_columns:
        if col in df_cleaned.columns:
            print(f"Processing categorical binary column: {col}")
            df_cleaned[col] = df_cleaned[col].apply(convert_to_binary)
    
    print("Boolean value corrections completed")
    
    # Final cleanup
    print("\n6. Final cleanup...")
    
    # Remove rows with too many missing values (optional)
    # df_cleaned = df_cleaned.dropna(thresh=len(df_cleaned.columns) * 0.5)
    
    print(f"\nFinal dataset shape: {df_cleaned.shape}")
    print("Data cleaning completed successfully!")
    
    return df_cleaned

def fix_date_format(date_value):
    """
    Fix various date format issues
    """
    if pd.isna(date_value):
        return date_value
    
    try:
        date_str = str(date_value)
        
        # Handle DD/MM/YYYY format (like 28/07/2025)
        if '/' in date_str and len(date_str.split('/')) == 3:
            parts = date_str.split('/')
            if len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4:
                # Assume DD/MM/YYYY format
                day, month, year = parts
                if int(day) > 12:  # Day is likely first
                    return pd.to_datetime(f"{year}-{month}-{day}", format='%Y-%m-%d')
                else:
                    # Could be MM/DD/YYYY, try both
                    try:
                        return pd.to_datetime(f"{year}-{parts[0]}-{parts[1]}", format='%Y-%m-%d')
                    except:
                        return pd.to_datetime(f"{year}-{parts[1]}-{parts[0]}", format='%Y-%m-%d')
        
        # Try standard pandas parsing
        return pd.to_datetime(date_value)
    
    except:
        return np.nan

def convert_to_binary(value):
    """
    Convert various boolean representations to binary (0/1)
    """
    if pd.isna(value):
        return value
    
    value_str = str(value).lower().strip()
    
    if value_str in ['true', '1', '1.0', 'yes', 'y']:
        return 1
    elif value_str in ['false', '0', '0.0', 'no', 'n']:
        return 0
    else:
        # Try to convert to numeric
        try:
            numeric_val = float(value_str)
            return 1 if numeric_val > 0 else 0
        except:
            return np.nan

def analyze_dataset(df):
    """
    Provide basic analysis of the cleaned dataset
    """
    print("\n" + "="*50)
    print("DATASET ANALYSIS")
    print("="*50)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Number of columns: {df.shape[1]}")
    print(f"Number of rows: {df.shape[0]}")
    
    print("\nColumn types:")
    print(df.dtypes.value_counts())
    
    print("\nMissing values:")
    missing_counts = df.isnull().sum()
    missing_percentages = (missing_counts / len(df) * 100).round(2)
    missing_info = pd.DataFrame({
        'Missing Count': missing_counts,
        'Missing Percentage': missing_percentages
    })
    missing_info = missing_info[missing_info['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
    print(missing_info.head(10))
    
    # Analyze boolean columns (var_44 to var_50)
    print("\nBoolean columns analysis (var_44 to var_50):")
    bool_columns = [f'var_{i}' for i in range(44, 51)]
    for col in bool_columns:
        if col in df.columns:
            value_counts = df[col].value_counts()
            print(f"{col}: {dict(value_counts)}")
    
    return df

# Example usage function
def main():
    """
    Main function to run the data cleaning pipeline
    """
    # Replace 'your_dataset.parquet' with the actual path to your parquet file
    parquet_file_path = 'your_dataset.parquet'
    
    try:
        # Clean the dataset
        cleaned_df = clean_dataset(parquet_file_path)
        
        # Analyze the cleaned dataset
        analyzed_df = analyze_dataset(cleaned_df)
        
        # Save the cleaned dataset
        output_path = 'cleaned_dataset.parquet'
        cleaned_df.to_parquet(output_path, index=False)
        print(f"\nCleaned dataset saved to: {output_path}")
        
        # Also save as CSV for easier inspection
        csv_output_path = 'cleaned_dataset.csv'
        cleaned_df.to_csv(csv_output_path, index=False)
        print(f"Cleaned dataset also saved as CSV: {csv_output_path}")
        
        return cleaned_df
        
    except Exception as e:
        print(f"Error processing dataset: {str(e)}")
        return None

if __name__ == "__main__":
    # When you have your parquet file, uncomment the line below
    # main()
    print("Data preprocessing script created successfully!")
    print("To use this script:")
    print("1. Place your parquet file in the same directory")
    print("2. Update the 'parquet_file_path' variable in the main() function")
    print("3. Run: python data_preprocessing.py")