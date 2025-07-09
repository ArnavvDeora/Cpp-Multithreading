import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class DatasetAnalyzer:
    """
    A comprehensive analyzer for the customer dataset
    """
    
    def __init__(self, cleaned_dataset_path):
        """
        Initialize the analyzer with the cleaned dataset
        """
        self.df = pd.read_parquet(cleaned_dataset_path)
        print(f"Dataset loaded: {self.df.shape[0]} rows, {self.df.shape[1]} columns")
        
    def question_1_customer_interest_analysis(self):
        """
        Analyze customer interest patterns across different categories
        """
        print("\n" + "="*60)
        print("QUESTION 1: CUSTOMER INTEREST ANALYSIS")
        print("="*60)
        
        # Find interest score columns
        interest_columns = [col for col in self.df.columns if 'interest' in col.lower() and 'score' in col.lower()]
        
        if interest_columns:
            print(f"Found {len(interest_columns)} interest categories:")
            
            # Calculate average interest scores
            interest_stats = {}
            for col in interest_columns:
                stats_dict = {
                    'mean': self.df[col].mean(),
                    'median': self.df[col].median(),
                    'std': self.df[col].std(),
                    'high_interest_customers': (self.df[col] > 0.7).sum()
                }
                interest_stats[col] = stats_dict
                print(f"\n{col}:")
                print(f"  Average Score: {stats_dict['mean']:.3f}")
                print(f"  Median Score: {stats_dict['median']:.3f}")
                print(f"  High Interest Customers (>0.7): {stats_dict['high_interest_customers']}")
            
            # Create correlation matrix of interests
            interest_corr = self.df[interest_columns].corr()
            
            return {
                'interest_stats': interest_stats,
                'interest_correlation': interest_corr,
                'interest_columns': interest_columns
            }
        else:
            print("No interest score columns found")
            return None
    
    def question_2_spending_behavior_analysis(self):
        """
        Analyze customer spending patterns
        """
        print("\n" + "="*60)
        print("QUESTION 2: SPENDING BEHAVIOR ANALYSIS")
        print("="*60)
        
        # Find spending columns
        spend_columns = [col for col in self.df.columns if 'spend' in col.lower()]
        
        if spend_columns:
            print(f"Found {len(spend_columns)} spending categories:")
            
            spending_analysis = {}
            for col in spend_columns:
                if self.df[col].dtype in ['int64', 'float64']:
                    analysis = {
                        'total_spending': self.df[col].sum(),
                        'average_spending': self.df[col].mean(),
                        'median_spending': self.df[col].median(),
                        'top_spenders': self.df[col].quantile(0.95),
                        'spending_customers': (self.df[col] > 0).sum(),
                        'zero_spenders': (self.df[col] == 0).sum()
                    }
                    spending_analysis[col] = analysis
                    
                    print(f"\n{col}:")
                    print(f"  Total Spending: ${analysis['total_spending']:,.2f}")
                    print(f"  Average per Customer: ${analysis['average_spending']:,.2f}")
                    print(f"  Customers with Spending: {analysis['spending_customers']}")
                    print(f"  95th Percentile: ${analysis['top_spenders']:,.2f}")
            
            return spending_analysis
        else:
            print("No spending columns found")
            return None
    
    def question_3_offer_response_analysis(self):
        """
        Analyze customer response to different offer categories
        """
        print("\n" + "="*60)
        print("QUESTION 3: OFFER RESPONSE ANALYSIS")
        print("="*60)
        
        # Find offer-related columns
        offer_columns = [col for col in self.df.columns if 'offer' in col.lower()]
        
        offer_analysis = {}
        for col in offer_columns:
            if col in self.df.columns:
                value_counts = self.df[col].value_counts()
                offer_analysis[col] = {
                    'distribution': dict(value_counts),
                    'response_rate': value_counts.get(1, 0) / len(self.df) if 1 in value_counts else 0
                }
                
                print(f"\n{col}:")
                print(f"  Distribution: {dict(value_counts)}")
                if 1 in value_counts and 0 in value_counts:
                    response_rate = value_counts[1] / (value_counts[1] + value_counts[0])
                    print(f"  Response Rate: {response_rate:.2%}")
        
        return offer_analysis
    
    def question_4_boolean_variables_analysis(self):
        """
        Analyze boolean variables (var_44 to var_50)
        """
        print("\n" + "="*60)
        print("QUESTION 4: BOOLEAN VARIABLES ANALYSIS (var_44 to var_50)")
        print("="*60)
        
        bool_columns = [f'var_{i}' for i in range(44, 51)]
        existing_bool_columns = [col for col in bool_columns if col in self.df.columns]
        
        if existing_bool_columns:
            bool_analysis = {}
            for col in existing_bool_columns:
                value_counts = self.df[col].value_counts()
                bool_analysis[col] = {
                    'distribution': dict(value_counts),
                    'positive_rate': value_counts.get(1, 0) / len(self.df),
                    'negative_rate': value_counts.get(0, 0) / len(self.df)
                }
                
                print(f"\n{col}:")
                print(f"  Distribution: {dict(value_counts)}")
                print(f"  Positive Rate (1): {bool_analysis[col]['positive_rate']:.2%}")
                print(f"  Negative Rate (0): {bool_analysis[col]['negative_rate']:.2%}")
            
            # Check correlations between boolean variables
            if len(existing_bool_columns) > 1:
                bool_corr = self.df[existing_bool_columns].corr()
                print(f"\nCorrelations between boolean variables:")
                print(bool_corr)
                
                return {
                    'individual_analysis': bool_analysis,
                    'correlations': bool_corr
                }
            
            return {'individual_analysis': bool_analysis}
        else:
            print("No boolean variables (var_44 to var_50) found")
            return None
    
    def question_5_customer_segmentation(self):
        """
        Perform customer segmentation analysis
        """
        print("\n" + "="*60)
        print("QUESTION 5: CUSTOMER SEGMENTATION ANALYSIS")
        print("="*60)
        
        # Find relevant columns for segmentation
        spend_columns = [col for col in self.df.columns if 'spend' in col.lower()]
        interest_columns = [col for col in self.df.columns if 'interest' in col.lower() and 'score' in col.lower()]
        
        segmentation_results = {}
        
        # Segment by spending level
        if spend_columns:
            total_spending = self.df[spend_columns].sum(axis=1)
            spending_quartiles = pd.qcut(total_spending, q=4, labels=['Low', 'Medium-Low', 'Medium-High', 'High'])
            
            segmentation_results['spending_segments'] = spending_quartiles.value_counts()
            print("Spending-based segmentation:")
            print(segmentation_results['spending_segments'])
            
            # Analyze segments
            for segment in ['Low', 'Medium-Low', 'Medium-High', 'High']:
                segment_data = self.df[spending_quartiles == segment]
                print(f"\n{segment} Spenders ({len(segment_data)} customers):")
                print(f"  Average total spending: ${total_spending[spending_quartiles == segment].mean():,.2f}")
                
                # Check interest patterns in each segment
                if interest_columns:
                    avg_interests = segment_data[interest_columns].mean()
                    print(f"  Top interests: {avg_interests.nlargest(3).to_dict()}")
        
        # Segment by interest diversity
        if interest_columns:
            interest_diversity = self.df[interest_columns].sum(axis=1)
            diversity_quartiles = pd.qcut(interest_diversity, q=4, labels=['Focused', 'Selective', 'Diverse', 'Very Diverse'])
            
            segmentation_results['interest_segments'] = diversity_quartiles.value_counts()
            print("\n\nInterest-based segmentation:")
            print(segmentation_results['interest_segments'])
        
        return segmentation_results
    
    def question_6_predictive_analysis(self):
        """
        Perform predictive analysis to identify key factors
        """
        print("\n" + "="*60)
        print("QUESTION 6: PREDICTIVE ANALYSIS")
        print("="*60)
        
        # Find target variables (could be offer response, high spending, etc.)
        offer_columns = [col for col in self.df.columns if 'offer' in col.lower()]
        spend_columns = [col for col in self.df.columns if 'spend' in col.lower()]
        
        predictive_results = {}
        
        # Analyze what predicts high spending
        if spend_columns:
            total_spending = self.df[spend_columns].sum(axis=1)
            high_spender = (total_spending > total_spending.quantile(0.8)).astype(int)
            
            # Find correlations with high spending
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns
            correlations = {}
            
            for col in numeric_columns:
                if col not in spend_columns:
                    try:
                        corr = self.df[col].corr(high_spender)
                        if not pd.isna(corr):
                            correlations[col] = corr
                    except:
                        continue
            
            # Sort by absolute correlation
            sorted_correlations = dict(sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True))
            
            print("Top factors correlated with high spending:")
            for col, corr in list(sorted_correlations.items())[:10]:
                print(f"  {col}: {corr:.3f}")
            
            predictive_results['high_spending_correlations'] = sorted_correlations
        
        # Analyze what predicts offer response
        if offer_columns:
            for offer_col in offer_columns:
                if self.df[offer_col].dtype in ['int64', 'float64']:
                    print(f"\nFactors predicting {offer_col} response:")
                    
                    numeric_columns = self.df.select_dtypes(include=[np.number]).columns
                    offer_correlations = {}
                    
                    for col in numeric_columns:
                        if col != offer_col:
                            try:
                                corr = self.df[col].corr(self.df[offer_col])
                                if not pd.isna(corr):
                                    offer_correlations[col] = corr
                            except:
                                continue
                    
                    sorted_offer_corr = dict(sorted(offer_correlations.items(), key=lambda x: abs(x[1]), reverse=True))
                    
                    for col, corr in list(sorted_offer_corr.items())[:5]:
                        print(f"  {col}: {corr:.3f}")
                    
                    predictive_results[f'{offer_col}_correlations'] = sorted_offer_corr
        
        return predictive_results
    
    def generate_comprehensive_report(self):
        """
        Generate a comprehensive analysis report answering all questions
        """
        print("\n" + "="*80)
        print("COMPREHENSIVE DATASET ANALYSIS REPORT")
        print("="*80)
        
        results = {}
        
        # Run all analyses
        results['q1_interests'] = self.question_1_customer_interest_analysis()
        results['q2_spending'] = self.question_2_spending_behavior_analysis()
        results['q3_offers'] = self.question_3_offer_response_analysis()
        results['q4_boolean'] = self.question_4_boolean_variables_analysis()
        results['q5_segmentation'] = self.question_5_customer_segmentation()
        results['q6_predictive'] = self.question_6_predictive_analysis()
        
        print("\n" + "="*80)
        print("ANALYSIS COMPLETED")
        print("="*80)
        
        return results
    
    def create_visualizations(self, save_plots=True):
        """
        Create key visualizations for the analysis
        """
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Interest scores distribution
        interest_columns = [col for col in self.df.columns if 'interest' in col.lower() and 'score' in col.lower()]
        if interest_columns:
            interest_means = self.df[interest_columns].mean().sort_values(ascending=False)
            axes[0, 0].bar(range(len(interest_means)), interest_means.values)
            axes[0, 0].set_title('Average Interest Scores by Category')
            axes[0, 0].set_xticks(range(len(interest_means)))
            axes[0, 0].set_xticklabels([col.replace('interest_score_', '') for col in interest_means.index], rotation=45)
        
        # Plot 2: Spending distribution
        spend_columns = [col for col in self.df.columns if 'spend' in col.lower()]
        if spend_columns:
            total_spending = self.df[spend_columns].sum(axis=1)
            axes[0, 1].hist(total_spending, bins=50, edgecolor='black', alpha=0.7)
            axes[0, 1].set_title('Total Spending Distribution')
            axes[0, 1].set_xlabel('Total Spending')
            axes[0, 1].set_ylabel('Number of Customers')
        
        # Plot 3: Boolean variables distribution
        bool_columns = [f'var_{i}' for i in range(44, 51) if f'var_{i}' in self.df.columns]
        if bool_columns:
            bool_means = self.df[bool_columns].mean()
            axes[1, 0].bar(bool_columns, bool_means.values)
            axes[1, 0].set_title('Boolean Variables (var_44-var_50) Positive Rates')
            axes[1, 0].set_ylabel('Positive Rate (1s)')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Plot 4: Correlation heatmap of key variables
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns[:20]  # Top 20 numeric columns
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr()
            im = axes[1, 1].imshow(corr_matrix, cmap='coolwarm', aspect='auto')
            axes[1, 1].set_title('Correlation Heatmap (Key Variables)')
            plt.colorbar(im, ax=axes[1, 1])
        
        plt.tight_layout()
        
        if save_plots:
            plt.savefig('dataset_analysis_plots.png', dpi=300, bbox_inches='tight')
            print("Visualizations saved as 'dataset_analysis_plots.png'")
        
        plt.show()

# Usage example
def main():
    """
    Main function to run the complete analysis
    """
    # Load the cleaned dataset
    analyzer = DatasetAnalyzer('cleaned_dataset.parquet')
    
    # Generate comprehensive report
    results = analyzer.generate_comprehensive_report()
    
    # Create visualizations
    analyzer.create_visualizations()
    
    return analyzer, results

if __name__ == "__main__":
    print("Analysis script created successfully!")
    print("To use this script:")
    print("1. Make sure you have run the data_preprocessing.py script first")
    print("2. Run: python analysis_questions.py")
    print("3. The script will generate a comprehensive analysis report")