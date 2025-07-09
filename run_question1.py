#!/usr/bin/env python3
"""
Quick Runner for Question 1 Analysis
====================================

This script runs Question 1 analysis on the cleaned dataset.
Make sure you have run the data preprocessing first.
"""

import os
import sys
from question1_amex_analysis import AmexPortalAnalyzer

def main():
    """
    Run Question 1 analysis
    """
    print("="*60)
    print("QUESTION 1: AMEX PORTAL ACTIVE USERS ANALYSIS")
    print("="*60)
    
    # Check if cleaned dataset exists
    dataset_path = 'cleaned_dataset.parquet'
    
    if not os.path.exists(dataset_path):
        print(f"❌ ERROR: Cleaned dataset not found at '{dataset_path}'")
        print("\nPlease run data preprocessing first:")
        print("  python data_preprocessing.py")
        print("  OR")
        print("  python run_complete_analysis.py")
        return False
    
    try:
        # Run the analysis
        analyzer = AmexPortalAnalyzer(dataset_path)
        results = analyzer.solve_question_1()
        
        if results:
            # Save results to file for easy reference
            with open('question1_results.txt', 'w') as f:
                f.write("QUESTION 1 RESULTS\n")
                f.write("==================\n\n")
                f.write(f"Statement 1 (Airline Offers): {results['statement1']}\n")
                f.write(f"Statement 2 (Discount Savings): {results['statement2']}\n")
                f.write(f"Population Count: {results['population']}\n\n")
                f.write(f"Active Users Identified: {results['active_users_count']}\n")
                f.write(f"Analysis Methods Used: {results['methods_used']}\n")
            
            print(f"\n📄 Results saved to: question1_results.txt")
            print("\n✅ Question 1 analysis completed successfully!")
            
            return True
        else:
            print("\n❌ Question 1 analysis failed!")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Question 1 Analysis...")
    success = main()
    
    if not success:
        sys.exit(1)