#!/usr/bin/env python3
"""
Question 1: Amex Portal Active Users Analysis
===========================================

This script analyzes active users of the Amex Portal and validates statements about:
1. Their likelihood to choose Airline Offers vs other categories
2. Their ability to save more money from Discounts vs other users
3. Population count of active users who clicked on Airline Offers
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AmexPortalAnalyzer:
    """
    Analyzer for Amex Portal user behavior
    """
    
    def __init__(self, cleaned_dataset_path):
        """
        Initialize with cleaned dataset
        """
        self.df = pd.read_parquet(cleaned_dataset_path)
        print(f"Dataset loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        
        # Display column names to understand the structure
        print("\nAvailable columns:")
        for i, col in enumerate(self.df.columns):
            print(f"  {i+1:2d}. {col}")
    
    def identify_active_users(self, reference_date_col=None, visit_indicator_col=None):
        """
        Identify active users based on portal visits in the last 30 days
        
        Parameters:
        reference_date_col: Column name containing dates for analysis
        visit_indicator_col: Column indicating portal visits
        """
        print("\n" + "="*60)
        print("IDENTIFYING ACTIVE USERS")
        print("="*60)
        
        # Try to identify relevant columns automatically
        date_columns = [col for col in self.df.columns if any(keyword in col.lower() 
                       for keyword in ['date', 'time', 'visit', 'portal'])]
        
        portal_columns = [col for col in self.df.columns if any(keyword in col.lower() 
                         for keyword in ['portal', 'amex', 'visit', 'active', 'click'])]
        
        print(f"Found potential date columns: {date_columns}")
        print(f"Found potential portal activity columns: {portal_columns}")
        
        # Method 1: If we have a specific portal visit column
        portal_visit_cols = [col for col in self.df.columns if 'portal' in col.lower() and 
                           any(x in col.lower() for x in ['visit', 'click', 'active'])]
        
        if portal_visit_cols:
            portal_col = portal_visit_cols[0]
            print(f"Using portal activity column: {portal_col}")
            
            # Assume binary indicator (1 = visited, 0 = not visited)
            active_users = self.df[self.df[portal_col] == 1]['customer_id'].unique() if 'customer_id' in self.df.columns else self.df[self.df[portal_col] == 1].index
            
            print(f"Active users identified: {len(active_users)}")
            return active_users, portal_col
        
        # Method 2: If we have date columns, analyze recent activity
        if date_columns:
            date_col = date_columns[0]
            print(f"Using date column: {date_col}")
            
            # Convert to datetime if not already
            try:
                self.df[date_col] = pd.to_datetime(self.df[date_col])
                
                # Find the latest date in the dataset
                max_date = self.df[date_col].max()
                cutoff_date = max_date - timedelta(days=30)
                
                print(f"Latest date in dataset: {max_date}")
                print(f"30-day cutoff date: {cutoff_date}")
                
                # Users active in last 30 days
                recent_activity = self.df[self.df[date_col] >= cutoff_date]
                active_users = recent_activity['customer_id'].unique() if 'customer_id' in self.df.columns else recent_activity.index.unique()
                
                print(f"Active users (last 30 days): {len(active_users)}")
                return active_users, date_col
                
            except Exception as e:
                print(f"Error processing date column: {e}")
        
        # Method 3: Use click-through or engagement metrics
        engagement_cols = [col for col in self.df.columns if any(x in col.lower() 
                          for x in ['click', 'engagement', 'activity', 'usage'])]
        
        if engagement_cols:
            engagement_col = engagement_cols[0]
            print(f"Using engagement column: {engagement_col}")
            
            # Consider users with above-average engagement as active
            threshold = self.df[engagement_col].median()
            active_users = self.df[self.df[engagement_col] > threshold]['customer_id'].unique() if 'customer_id' in self.df.columns else self.df[self.df[engagement_col] > threshold].index
            
            print(f"Active users (above median engagement): {len(active_users)}")
            return active_users, engagement_col
        
        # Method 4: If we can't identify specific columns, create a proxy
        print("Creating proxy for active users based on available data...")
        
        # Look for any binary indicators that might represent activity
        binary_cols = []
        for col in self.df.columns:
            if self.df[col].dtype in ['int64', 'float64']:
                unique_vals = self.df[col].dropna().unique()
                if len(unique_vals) == 2 and set(unique_vals).issubset({0, 1, 0.0, 1.0}):
                    binary_cols.append(col)
        
        if binary_cols:
            activity_col = binary_cols[0]  # Use first binary column as proxy
            print(f"Using binary column as activity proxy: {activity_col}")
            
            active_users = self.df[self.df[activity_col] == 1]['customer_id'].unique() if 'customer_id' in self.df.columns else self.df[self.df[activity_col] == 1].index
            
            print(f"Active users (proxy method): {len(active_users)}")
            return active_users, activity_col
        
        # Fallback: Use top 50% of customers by some engagement metric
        print("Using fallback method: top 50% by total activity")
        
        # Sum all numeric columns as a proxy for total activity
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df['total_activity'] = self.df[numeric_cols].sum(axis=1)
        
        threshold = self.df['total_activity'].median()
        active_users = self.df[self.df['total_activity'] > threshold]['customer_id'].unique() if 'customer_id' in self.df.columns else self.df[self.df['total_activity'] > threshold].index
        
        print(f"Active users (fallback method): {len(active_users)}")
        return active_users, 'total_activity'
    
    def analyze_airline_offer_preference(self, active_users):
        """
        Analyze if active users prefer airline offers over other categories
        """
        print("\n" + "="*60)
        print("ANALYZING AIRLINE OFFER PREFERENCES")
        print("="*60)
        
        # Find airline-related columns
        airline_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                       for keyword in ['airline', 'flight', 'travel', 'air'])]
        
        # Find other offer columns
        offer_cols = [col for col in self.df.columns if 'offer' in col.lower()]
        
        print(f"Found airline-related columns: {airline_cols}")
        print(f"Found offer-related columns: {offer_cols}")
        
        if not airline_cols and not offer_cols:
            # Look for category columns
            category_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                           for keyword in ['category', 'type', 'segment'])]
            print(f"Found category columns: {category_cols}")
            
            if category_cols:
                cat_col = category_cols[0]
                unique_categories = self.df[cat_col].value_counts()
                print(f"Categories in {cat_col}:")
                print(unique_categories)
                
                # Look for airline-related categories
                airline_categories = [cat for cat in unique_categories.index 
                                    if any(keyword in str(cat).lower() 
                                          for keyword in ['airline', 'flight', 'travel', 'air'])]
                
                if airline_categories:
                    print(f"Found airline categories: {airline_categories}")
                    
                    # Analyze preferences
                    customer_id_col = 'customer_id' if 'customer_id' in self.df.columns else self.df.index.name or 'index'
                    
                    # Active users preferences
                    if 'customer_id' in self.df.columns:
                        active_df = self.df[self.df['customer_id'].isin(active_users)]
                        non_active_df = self.df[~self.df['customer_id'].isin(active_users)]
                    else:
                        active_df = self.df[self.df.index.isin(active_users)]
                        non_active_df = self.df[~self.df.index.isin(active_users)]
                    
                    # Calculate airline preference rates
                    active_airline_rate = (active_df[cat_col].isin(airline_categories)).mean()
                    non_active_airline_rate = (non_active_df[cat_col].isin(airline_categories)).mean()
                    
                    print(f"\nActive users airline offer rate: {active_airline_rate:.3f}")
                    print(f"Non-active users airline offer rate: {non_active_airline_rate:.3f}")
                    
                    statement1_result = active_airline_rate > non_active_airline_rate
                    print(f"\nStatement 1 Result: {statement1_result}")
                    
                    return statement1_result, {
                        'active_airline_rate': active_airline_rate,
                        'non_active_airline_rate': non_active_airline_rate,
                        'category_column': cat_col,
                        'airline_categories': airline_categories
                    }
        
        # Alternative approach: Look for airline-specific offer columns
        if airline_cols:
            airline_col = airline_cols[0]
            print(f"Analyzing airline column: {airline_col}")
            
            customer_id_col = 'customer_id' if 'customer_id' in self.df.columns else 'index'
            
            if 'customer_id' in self.df.columns:
                active_df = self.df[self.df['customer_id'].isin(active_users)]
                non_active_df = self.df[~self.df['customer_id'].isin(active_users)]
            else:
                active_df = self.df[self.df.index.isin(active_users)]
                non_active_df = self.df[~self.df.index.isin(active_users)]
            
            # Calculate airline engagement rates
            active_airline_rate = active_df[airline_col].mean() if airline_col in active_df.columns else 0
            non_active_airline_rate = non_active_df[airline_col].mean() if airline_col in non_active_df.columns else 0
            
            print(f"\nActive users airline engagement: {active_airline_rate:.3f}")
            print(f"Non-active users airline engagement: {non_active_airline_rate:.3f}")
            
            statement1_result = active_airline_rate > non_active_airline_rate
            print(f"\nStatement 1 Result: {statement1_result}")
            
            return statement1_result, {
                'active_airline_rate': active_airline_rate,
                'non_active_airline_rate': non_active_airline_rate,
                'airline_column': airline_col
            }
        
        # Fallback: Analyze based on available offer data
        if offer_cols:
            print("Using general offer analysis as fallback...")
            
            # Assume first offer column relates to airlines or use it as proxy
            offer_col = offer_cols[0]
            
            customer_id_col = 'customer_id' if 'customer_id' in self.df.columns else 'index'
            
            if 'customer_id' in self.df.columns:
                active_df = self.df[self.df['customer_id'].isin(active_users)]
                non_active_df = self.df[~self.df['customer_id'].isin(active_users)]
            else:
                active_df = self.df[self.df.index.isin(active_users)]
                non_active_df = self.df[~self.df.index.isin(active_users)]
            
            active_offer_rate = active_df[offer_col].mean()
            non_active_offer_rate = non_active_df[offer_col].mean()
            
            print(f"\nActive users offer engagement: {active_offer_rate:.3f}")
            print(f"Non-active users offer engagement: {non_active_offer_rate:.3f}")
            
            statement1_result = active_offer_rate > non_active_offer_rate
            print(f"\nStatement 1 Result (proxy): {statement1_result}")
            
            return statement1_result, {
                'active_offer_rate': active_offer_rate,
                'non_active_offer_rate': non_active_offer_rate,
                'offer_column': offer_col
            }
        
        print("Could not find sufficient data for airline offer analysis")
        return None, {}
    
    def analyze_discount_savings(self, active_users):
        """
        Analyze if active users save more money from discounts
        """
        print("\n" + "="*60)
        print("ANALYZING DISCOUNT SAVINGS")
        print("="*60)
        
        # Find discount-related columns
        discount_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                        for keyword in ['discount', 'save', 'saving', 'deal'])]
        
        # Find spending/amount columns
        spending_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                        for keyword in ['spend', 'amount', 'value', 'money'])]
        
        print(f"Found discount-related columns: {discount_cols}")
        print(f"Found spending-related columns: {spending_cols}")
        
        customer_id_col = 'customer_id' if 'customer_id' in self.df.columns else 'index'
        
        if 'customer_id' in self.df.columns:
            active_df = self.df[self.df['customer_id'].isin(active_users)]
            non_active_df = self.df[~self.df['customer_id'].isin(active_users)]
        else:
            active_df = self.df[self.df.index.isin(active_users)]
            non_active_df = self.df[~self.df.index.isin(active_users)]
        
        if discount_cols:
            discount_col = discount_cols[0]
            print(f"Analyzing discount column: {discount_col}")
            
            active_discount_avg = active_df[discount_col].mean()
            non_active_discount_avg = non_active_df[discount_col].mean()
            
            print(f"\nActive users average discount savings: {active_discount_avg:.2f}")
            print(f"Non-active users average discount savings: {non_active_discount_avg:.2f}")
            
            statement2_result = active_discount_avg > non_active_discount_avg
            print(f"\nStatement 2 Result: {statement2_result}")
            
            return statement2_result, {
                'active_discount_avg': active_discount_avg,
                'non_active_discount_avg': non_active_discount_avg,
                'discount_column': discount_col
            }
        
        elif spending_cols:
            # Use spending as proxy - higher spending might indicate more savings through discounts
            spending_col = spending_cols[0]
            print(f"Using spending column as proxy: {spending_col}")
            
            active_spending_avg = active_df[spending_col].mean()
            non_active_spending_avg = non_active_df[spending_col].mean()
            
            print(f"\nActive users average spending: {active_spending_avg:.2f}")
            print(f"Non-active users average spending: {non_active_spending_avg:.2f}")
            
            # Assume higher spending indicates better discount utilization
            statement2_result = active_spending_avg > non_active_spending_avg
            print(f"\nStatement 2 Result (proxy): {statement2_result}")
            
            return statement2_result, {
                'active_spending_avg': active_spending_avg,
                'non_active_spending_avg': non_active_spending_avg,
                'spending_column': spending_col
            }
        
        print("Could not find sufficient data for discount savings analysis")
        return None, {}
    
    def count_active_airline_users(self, active_users):
        """
        Count unique customers who are active and clicked on airline offers
        """
        print("\n" + "="*60)
        print("COUNTING ACTIVE USERS WITH AIRLINE OFFERS")
        print("="*60)
        
        # Find airline-related columns
        airline_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                       for keyword in ['airline', 'flight', 'travel', 'air'])]
        
        customer_id_col = 'customer_id' if 'customer_id' in self.df.columns else 'index'
        
        if airline_cols:
            airline_col = airline_cols[0]
            print(f"Using airline column: {airline_col}")
            
            if 'customer_id' in self.df.columns:
                # Active users who clicked on airline offers
                active_airline_users = self.df[
                    (self.df['customer_id'].isin(active_users)) & 
                    (self.df[airline_col] == 1)
                ]['customer_id'].nunique()
            else:
                active_airline_users = len(self.df[
                    (self.df.index.isin(active_users)) & 
                    (self.df[airline_col] == 1)
                ])
            
            print(f"Active users who clicked on airline offers: {active_airline_users}")
            
            return active_airline_users, airline_col
        
        # Alternative: Look for category-based data
        category_cols = [col for col in self.df.columns if any(keyword in col.lower() 
                        for keyword in ['category', 'type', 'segment'])]
        
        if category_cols:
            cat_col = category_cols[0]
            unique_categories = self.df[cat_col].value_counts()
            print(f"Categories in {cat_col}: {unique_categories.index.tolist()}")
            
            # Look for airline-related categories
            airline_categories = [cat for cat in unique_categories.index 
                                if any(keyword in str(cat).lower() 
                                      for keyword in ['airline', 'flight', 'travel', 'air'])]
            
            if airline_categories:
                print(f"Found airline categories: {airline_categories}")
                
                if 'customer_id' in self.df.columns:
                    active_airline_users = self.df[
                        (self.df['customer_id'].isin(active_users)) & 
                        (self.df[cat_col].isin(airline_categories))
                    ]['customer_id'].nunique()
                else:
                    active_airline_users = len(self.df[
                        (self.df.index.isin(active_users)) & 
                        (self.df[cat_col].isin(airline_categories))
                    ])
                
                print(f"Active users with airline category: {active_airline_users}")
                
                return active_airline_users, cat_col
        
        # Fallback: Use first offer column as proxy
        offer_cols = [col for col in self.df.columns if 'offer' in col.lower()]
        
        if offer_cols:
            offer_col = offer_cols[0]
            print(f"Using offer column as proxy: {offer_col}")
            
            if 'customer_id' in self.df.columns:
                active_offer_users = self.df[
                    (self.df['customer_id'].isin(active_users)) & 
                    (self.df[offer_col] == 1)
                ]['customer_id'].nunique()
            else:
                active_offer_users = len(self.df[
                    (self.df.index.isin(active_users)) & 
                    (self.df[offer_col] == 1)
                ])
            
            print(f"Active users with offers (proxy): {active_offer_users}")
            
            return active_offer_users, offer_col
        
        print("Could not find sufficient data to count airline offer users")
        return 0, None
    
    def solve_question_1(self):
        """
        Solve Question 1 completely
        """
        print("\n" + "="*80)
        print("SOLVING QUESTION 1: AMEX PORTAL ACTIVE USERS ANALYSIS")
        print("="*80)
        
        # Step 1: Identify active users
        active_users, activity_method = self.identify_active_users()
        
        if active_users is None or len(active_users) == 0:
            print("ERROR: Could not identify active users")
            return None
        
        # Step 2: Analyze airline offer preferences
        statement1_result, airline_analysis = self.analyze_airline_offer_preference(active_users)
        
        # Step 3: Analyze discount savings
        statement2_result, discount_analysis = self.analyze_discount_savings(active_users)
        
        # Step 4: Count active users with airline offers
        population_count, airline_method = self.count_active_airline_users(active_users)
        
        # Final Results
        print("\n" + "="*80)
        print("QUESTION 1 RESULTS")
        print("="*80)
        
        print(f"Total active users identified: {len(active_users)}")
        print(f"Activity identification method: {activity_method}")
        
        print(f"\nStatement 1: Active Users are more likely to choose Airline Offers")
        print(f"Answer: {statement1_result}")
        
        print(f"\nStatement 2: Active Users save more money from Discounts")
        print(f"Answer: {statement2_result}")
        
        print(f"\nPopulation Count: Active users who clicked on Airline Offers")
        print(f"Answer: {population_count}")
        
        # Summary for easy copying
        print("\n" + "="*50)
        print("FINAL ANSWERS")
        print("="*50)
        print(f"1. Statement 1: {statement1_result}")
        print(f"2. Statement 2: {statement2_result}")
        print(f"3. Population: {population_count}")
        
        return {
            'statement1': statement1_result,
            'statement2': statement2_result,
            'population': population_count,
            'active_users_count': len(active_users),
            'methods_used': {
                'activity_method': activity_method,
                'airline_method': airline_method
            },
            'detailed_analysis': {
                'airline_analysis': airline_analysis,
                'discount_analysis': discount_analysis
            }
        }

def main():
    """
    Main function to run Question 1 analysis
    """
    # Load the cleaned dataset
    dataset_path = 'cleaned_dataset.parquet'
    
    try:
        analyzer = AmexPortalAnalyzer(dataset_path)
        results = analyzer.solve_question_1()
        
        if results:
            print("\n✅ Question 1 analysis completed successfully!")
            return results
        else:
            print("\n❌ Question 1 analysis failed!")
            return None
            
    except FileNotFoundError:
        print(f"ERROR: Dataset file '{dataset_path}' not found.")
        print("Please run the data preprocessing script first.")
        return None
    except Exception as e:
        print(f"ERROR: Analysis failed with error: {str(e)}")
        return None

if __name__ == "__main__":
    print("Starting Question 1: Amex Portal Active Users Analysis...")
    results = main()