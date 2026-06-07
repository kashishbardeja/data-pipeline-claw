import pandas as pd
from datetime import datetime, timezone

def check_freshness(file_path: str) -> dict:
    """Checks if the data contains recent records (within 24 hours)."""
    try:
        df = pd.read_csv(file_path)
        if 'timestamp' not in df.columns or df.empty:
            return {"status": "FAIL", "message": "Missing timestamp column or empty file."}
        
        # Parse timestamps safely
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        latest_record = df['timestamp'].max()
        
        # Calculate age in hours (Simulated current date: June 7, 2026)
        current_time = datetime(2026, 6, 7, tzinfo=timezone.utc)
        if latest_record.tzinfo is None:
            latest_record = latest_record.replace(tzinfo=timezone.utc)
            
        age_hours = (current_time - latest_record).total_seconds() / 3600
        
        if age_hours > 24:
            return {"status": "FAIL", "message": f"Data is stale. Latest record is {age_hours:.1f} hours old (Max 24h)."}
        
        return {"status": "SUCCESS", "message": f"Data freshness verified. Latest record is {age_hours:.1f} hours old."}
    except Exception as e:
        return {"status": "FAIL", "message": f"Freshness check crashed: {str(e)}"}

def validate_schema(file_path: str) -> dict:
    """Validates structural integrity, critical nulls, and data types."""
    try:
        df = pd.read_csv(file_path)
        required_columns = ['transaction_id', 'customer_id', 'amount', 'status', 'timestamp']
        
        # 1. Check missing columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            return {"status": "FAIL", "message": f"Schema Drift Detected: Missing columns {missing_cols}"}
        
        # 2. Check critical null values
        null_txn = df['transaction_id'].isnull().sum()
        null_cust = df['customer_id'].isnull().sum()
        if null_txn > 0 or null_cust > 0:
            return {"status": "FAIL", "message": f"Data Quality Violation: Found {null_txn} missing transaction_ids and {null_cust} missing customer_ids."}
            
        # 3. Check data type anomalies (amount must be numeric)
        # errors='coerce' turns text like 'ERROR_VAL' or 'NULL' into NaN values
        numeric_amounts = pd.to_numeric(df['amount'], errors='coerce')
        type_faults = numeric_amounts.isnull().sum() - df['amount'].isnull().sum()
        if type_faults > 0:
            return {"status": "FAIL", "message": f"Type Mismatch: Found {type_faults} non-numeric values in the 'amount' column."}
            
        return {"status": "SUCCESS", "message": "Schema structure and data quality constraints verified successfully."}
    except Exception as e:
        return {"status": "FAIL", "message": f"Schema validation crashed: {str(e)}"}

def send_terminal_alert(claw_name: str, current_state: str, log_summary: str):
    """Simulates a highly structured operational alert (e.g., Slack Webhook payload)."""
    border = "=" * 60
    print(f"\n{border}")
    print(f"🚨🚨 [AGENTIC ESCALATION SYSTEM] Triggered by {claw_name} 🚨🚨")
    print(f"Current Agent State: {current_state}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(border)
    print(log_summary.strip())
    print(f"{border}\n")