import pandas as pd

try:
    df = pd.read_csv('/app/data/historical_name_decisions.xlsx') # The user said xlsx but previous logs showed it might be read as csv in code? 
    # Wait, the code in scoring.py says:
    # path = DATA_DIR / "historical_name_decisions.xlsx"
    # df = pd.read_csv(path)
    # This implies the file extension is .xlsx but it is actually a CSV file? Or the code is wrong?
    # Let's check the file type first using `file` command or just try to read it.
    print("Read as CSV success")
    print(df.columns)
    print(df.head())
except Exception as e:
    print(f"Read as CSV failed: {e}")
    try:
        df = pd.read_excel('/app/data/historical_name_decisions.xlsx')
        print("Read as Excel success")
        print(df.columns)
        print(df.head())
    except Exception as e2:
        print(f"Read as Excel failed: {e2}")
