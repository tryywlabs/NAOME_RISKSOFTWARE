import sys
import pathlib
import io
import pandas as pd
import os

input_folder = "raw"
output_folder = "cleaned"

def clean_csv(source_path, dest_path):
    """Main function for processing risk CSV files."""
    print("Processing risk CSV files...")

    df = pd.read_csv(source_path)

    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    df["equipment_size"] = df["equipment_size"].ffill()

    df.to_csv(dest_path, index=False)

    print("Processing complete. Cleaned file saved to:", dest_path)

for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        source_path = os.path.join(input_folder, filename)
        dest_path = os.path.join(output_folder, filename)
        clean_csv(source_path, dest_path)

print("All files processed.")