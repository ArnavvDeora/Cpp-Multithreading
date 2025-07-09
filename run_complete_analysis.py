#!/usr/bin/env python3
"""
Complete Data Analysis Workflow
===============================

This script runs the complete data preprocessing and analysis pipeline.
Before running, make sure to:
1. Install dependencies: pip install -r requirements.txt
2. Place your parquet file in the directory
3. Update the PARQUET_FILE_PATH variable below
"""

import os
import sys
from data_preprocessing import clean_dataset, analyze_dataset
from analysis_questions import DatasetAnalyzer

# Configuration
PARQUET_FILE_PATH = "your_dataset.parquet"  # Update this with your actual file path

def main():
    """
    Run the complete analysis pipeline
    """
    print("="*80)
    print("CUSTOMER DATASET ANALYSIS PIPELINE")
    print("="*80)
    
    # Check if parquet file exists
    if not os.path.exists(PARQUET_FILE_PATH):
        print(f"ERROR: Parquet file not found at: {PARQUET_FILE_PATH}")
        print("Please update the PARQUET_FILE_PATH variable in this script.")
        return False
    
    try:
        # Step 1: Data Preprocessing
        print("\n🔧 STEP 1: DATA PREPROCESSING")
        print("-" * 50)
        
        cleaned_df = clean_dataset(PARQUET_FILE_PATH)
        
        if cleaned_df is None:
            print("ERROR: Data preprocessing failed")
            return False
        
        # Basic analysis of cleaned data
        analyze_dataset(cleaned_df)
        
        # Save cleaned dataset
        cleaned_output_path = 'cleaned_dataset.parquet'
        cleaned_df.to_parquet(cleaned_output_path, index=False)
        print(f"\n✅ Cleaned dataset saved to: {cleaned_output_path}")
        
        # Step 2: Comprehensive Analysis
        print("\n📊 STEP 2: COMPREHENSIVE ANALYSIS")
        print("-" * 50)
        
        analyzer = DatasetAnalyzer(cleaned_output_path)
        results = analyzer.generate_comprehensive_report()
        
        # Step 3: Generate Visualizations
        print("\n📈 STEP 3: GENERATING VISUALIZATIONS")
        print("-" * 50)
        
        analyzer.create_visualizations(save_plots=True)
        
        # Step 4: Summary Report
        print("\n📋 STEP 4: SUMMARY REPORT")
        print("-" * 50)
        
        generate_summary_report(results, cleaned_df)
        
        print("\n✅ ANALYSIS PIPELINE COMPLETED SUCCESSFULLY!")
        print("\nGenerated Files:")
        print(f"  • cleaned_dataset.parquet - Cleaned dataset")
        print(f"  • cleaned_dataset.csv - CSV version of cleaned dataset")
        print(f"  • dataset_analysis_plots.png - Visualization plots")
        print(f"  • analysis_summary_report.txt - Summary report")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Analysis pipeline failed with error: {str(e)}")
        return False

def generate_summary_report(results, cleaned_df):
    """
    Generate a summary report file
    """
    report_filename = "analysis_summary_report.txt"
    
    with open(report_filename, 'w') as f:
        f.write("CUSTOMER DATASET ANALYSIS SUMMARY REPORT\n")
        f.write("=" * 50 + "\n\n")
        
        # Dataset Overview
        f.write("DATASET OVERVIEW\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Records: {len(cleaned_df):,}\n")
        f.write(f"Total Variables: {len(cleaned_df.columns)}\n")
        f.write(f"Data Quality: Cleaned and validated\n\n")
        
        # Key Findings Summary
        f.write("KEY FINDINGS SUMMARY\n")
        f.write("-" * 20 + "\n")
        
        # Interest Analysis Summary
        if results.get('q1_interests'):
            f.write("• Interest Analysis: Completed\n")
            interest_data = results['q1_interests']
            if interest_data and 'interest_columns' in interest_data:
                f.write(f"  - Found {len(interest_data['interest_columns'])} interest categories\n")
        
        # Spending Analysis Summary
        if results.get('q2_spending'):
            f.write("• Spending Analysis: Completed\n")
            spending_data = results['q2_spending']
            if spending_data:
                total_categories = len(spending_data)
                f.write(f"  - Analyzed {total_categories} spending categories\n")
        
        # Offer Analysis Summary
        if results.get('q3_offers'):
            f.write("• Offer Response Analysis: Completed\n")
            offer_data = results['q3_offers']
            if offer_data:
                f.write(f"  - Analyzed {len(offer_data)} offer types\n")
        
        # Boolean Variables Summary
        if results.get('q4_boolean'):
            f.write("• Boolean Variables Analysis: Completed\n")
            bool_data = results['q4_boolean']
            if bool_data and 'individual_analysis' in bool_data:
                f.write(f"  - Analyzed {len(bool_data['individual_analysis'])} boolean variables\n")
        
        # Segmentation Summary
        if results.get('q5_segmentation'):
            f.write("• Customer Segmentation: Completed\n")
            f.write("  - Created spending-based segments\n")
            f.write("  - Created interest-based segments\n")
        
        # Predictive Analysis Summary
        if results.get('q6_predictive'):
            f.write("• Predictive Analysis: Completed\n")
            f.write("  - Identified key factors for high spending\n")
            f.write("  - Analyzed offer response predictors\n")
        
        f.write("\nRECOMMENDations\n")
        f.write("-" * 15 + "\n")
        f.write("1. Use the cleaned dataset for further analysis\n")
        f.write("2. Review the visualization plots for key insights\n")
        f.write("3. Consider the segmentation results for targeted marketing\n")
        f.write("4. Leverage predictive factors for customer scoring\n")
        f.write("5. Monitor boolean variables for behavior patterns\n")
        
        f.write(f"\nReport generated successfully.\n")
    
    print(f"Summary report saved to: {report_filename}")

if __name__ == "__main__":
    print("Starting Customer Dataset Analysis Pipeline...")
    print("Make sure to update PARQUET_FILE_PATH with your actual file path!")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()  # Wait for user confirmation
        success = main()
        if success:
            print("\n🎉 Analysis completed successfully!")
        else:
            print("\n❌ Analysis failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user.")
        sys.exit(0)