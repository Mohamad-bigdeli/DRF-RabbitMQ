import pandas as pd

def analyze_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        top_transaction = df.loc[df['amount'].idxmax()].copy()
        top_transaction['timestamp'] = top_transaction['timestamp'].isoformat()  

        results = {
            'total_amount': float(df['amount'].sum()),
            'average_amount': float(df['amount'].mean()),
            'category_counts': df['category'].value_counts().to_dict(),
            'category_totals': df.groupby('category')['amount'].sum().to_dict(),
            'monthly_totals': {
                str(k): float(v) for k, v in df.groupby(df['timestamp'].dt.to_period('M'))['amount'].sum().items()
            },
            'top_transaction': top_transaction.to_dict()  
        }

        print("Analysis complete.")
        return results

    except Exception as e:
        print(f"Error analyzing CSV: {e}")
        return None