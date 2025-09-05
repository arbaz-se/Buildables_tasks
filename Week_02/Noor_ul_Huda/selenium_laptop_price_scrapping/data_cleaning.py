import pandas as pd
import re


def clean_laptop_data(csv_file_path: str, usd_to_pkr_rate: float = 278.5) -> pd.DataFrame:
    """
    Clean and process laptop data from Amazon scraping

    Parameters:
    csv_file_path: Path to the CSV file
    usd_to_pkr_rate: Current USD to PKR exchange rate

    Returns:
    pd.DataFrame: Cleaned and processed dataframe
    """

    # Load the data
    df = pd.read_csv(csv_file_path)

    # Assume the columns are named 'description' and 'price' - adjust as needed
    # You may need to change these column names based on your actual CSV
    if 'description' not in df.columns:
        # If different column name, find the text column (usually the longest text)
        text_col = df.select_dtypes(include=['object']).columns[0]
        df.rename(columns={text_col: 'description'}, inplace=True)

    if 'price' not in df.columns:
        # Find price column (usually contains $ or numbers)
        price_cols = [col for col in df.columns if 'price' in col.lower() or '$' in str(df[col].iloc[0])]
        if price_cols:
            df.rename(columns={price_cols[0]: 'price'}, inplace=True)

    # Create a copy for processing
    df_clean = df.copy()

    # Extract Company/Brand
    def extract_company(description):
        companies = ['HP', 'Dell', 'Lenovo', 'Asus', 'ASUS', 'Acer', 'MSI', 'Apple', 'MacBook',
                     'Samsung', 'LG', 'Huawei', 'Microsoft', 'Surface', 'Razer', 'Alienware',
                     'ThinkPad', 'IdeaPad', 'Pavilion', 'Inspiron', 'Latitude', 'XPS',
                     'VivoBook', 'ZenBook', 'ROG', 'TUF', 'Predator', 'Aspire', 'Swift',
                     'Nitro', 'ConceptD', 'Chromebook', 'Spectre', 'Envy', 'EliteBook']

        description_upper = description.upper()
        for company in companies:
            if company.upper() in description_upper:
                # Map some specific models to parent companies
                if company.upper() in ['MACBOOK']:
                    return 'Apple'
                elif company.upper() in ['THINKPAD', 'IDEAPAD']:
                    return 'Lenovo'
                elif company.upper() in ['PAVILION', 'SPECTRE', 'ENVY', 'ELITEBOOK']:
                    return 'HP'
                elif company.upper() in ['INSPIRON', 'LATITUDE', 'XPS', 'ALIENWARE']:
                    return 'Dell'
                elif company.upper() in ['VIVOBOOK', 'ZENBOOK', 'ROG', 'TUF']:
                    return 'ASUS'
                elif company.upper() in ['PREDATOR', 'ASPIRE', 'SWIFT', 'NITRO', 'CONCEPTD']:
                    return 'Acer'
                elif company.upper() in ['SURFACE']:
                    return 'Microsoft'
                else:
                    return company
        return 'Unknown'

    # Extract RAM
    def extract_ram(description):
        # Look for patterns like "8GB", "16GB", "32GB", "4GB"
        ram_pattern = r'(\d+)\s*GB\s*(?:RAM|DDR|Memory|LPDDR)'
        matches = re.findall(ram_pattern, description, re.IGNORECASE)
        if matches:
            # Return the highest RAM found
            return max([int(match) for match in matches])

        # Alternative pattern for RAM
        ram_pattern2 = r'(\d+)\s*GB\s*DDR'
        matches2 = re.findall(ram_pattern2, description, re.IGNORECASE)
        if matches2:
            return max([int(match) for match in matches2])

        return None

    # Extract Storage
    def extract_storage(description):
        # Look for SSD storage
        ssd_pattern = r'(\d+)\s*(?:GB|TB)\s*(?:SSD|Storage|NVME|M\.2)'
        ssd_matches = re.findall(ssd_pattern, description, re.IGNORECASE)

        # Look for HDD storage
        hdd_pattern = r'(\d+)\s*(?:GB|TB)\s*(?:HDD|Hard\s*Drive)'
        hdd_matches = re.findall(hdd_pattern, description, re.IGNORECASE)

        # Look for general storage pattern
        storage_pattern = r'(\d+)\s*(?:GB|TB)(?:\s+Storage|\s+SSD|\s+HDD|(?=\s))'
        storage_matches = re.findall(storage_pattern, description, re.IGNORECASE)

        all_storage = []

        # Process SSD matches
        for match in ssd_matches:
            if 'TB' in description[description.find(match):description.find(match) + 10]:
                all_storage.append(int(match) * 1024)  # Convert TB to GB
            else:
                all_storage.append(int(match))

        # Process general storage matches
        for match in storage_matches:
            if 'TB' in description[description.find(match):description.find(match) + 10]:
                all_storage.append(int(match) * 1024)  # Convert TB to GB
            else:
                all_storage.append(int(match))

        if all_storage:
            return max(all_storage)  # Return highest storage
        return None

    # Extract Processor/Core information
    def extract_processor(description):
        processors = {
            'Intel': ['Intel', 'i3', 'i5', 'i7', 'i9', 'Core', 'Pentium', 'Celeron', 'Xeon'],
            'AMD': ['AMD', 'Ryzen', 'Athlon', 'A4', 'A6', 'A8', 'A10', 'A12', 'FX'],
            'Apple': ['M1', 'M2', 'M3', 'Apple Silicon'],
            'ARM': ['ARM', 'Snapdragon'],
            'Other': ['Quad-core', 'Dual-core', 'Octa-core', '4-Core', '6-Core', '8-Core']
        }

        description_upper = description.upper()
        for brand, keywords in processors.items():
            for keyword in keywords:
                if keyword.upper() in description_upper:
                    # Extract specific processor model if possible
                    if brand == 'Intel':
                        intel_models = re.findall(r'(i[3579]-?\w*|Pentium\s+\w*|Celeron\s+\w*)', description,
                                                  re.IGNORECASE)
                        if intel_models:
                            return f"Intel {intel_models[0]}"
                        return 'Intel'
                    elif brand == 'AMD':
                        amd_models = re.findall(r'(Ryzen\s+\w*|Athlon\s+\w*)', description, re.IGNORECASE)
                        if amd_models:
                            return f"AMD {amd_models[0]}"
                        return 'AMD'
                    elif brand == 'Apple':
                        apple_models = re.findall(r'(M[123]\s*\w*)', description, re.IGNORECASE)
                        if apple_models:
                            return f"Apple {apple_models[0]}"
                        return 'Apple'
                    else:
                        return brand
        return 'Unknown'

    # Extract Screen Size
    def extract_screen_size(description):
        # Look for patterns like 14", 15.6", 13.3"
        screen_pattern = r'(\d+(?:\.\d+)?)\s*(?:inch|"|\')\s*(?:LED|LCD|Display|Screen)?'
        matches = re.findall(screen_pattern, description, re.IGNORECASE)
        if matches:
            return float(matches[0])
        return None

    # Clean price and convert to numeric
    def clean_price(price_str):
        if pd.isna(price_str):
            return None

        # Remove currency symbols and extract numbers
        price_clean = re.sub(r'[^\d.]', '', str(price_str))
        try:
            return float(price_clean)
        except:
            return None

    # Apply feature extraction
    print("Extracting features...")
    df_clean['Company'] = df_clean['description'].apply(extract_company)
    df_clean['RAM_GB'] = df_clean['description'].apply(extract_ram)
    df_clean['Storage_GB'] = df_clean['description'].apply(extract_storage)
    df_clean['Processor'] = df_clean['description'].apply(extract_processor)
    df_clean['Screen_Size'] = df_clean['description'].apply(extract_screen_size)

    # Clean and process price
    df_clean['Price_USD_Clean'] = df_clean['price'].apply(clean_price)

    # Convert to PKR
    df_clean['Price_PKR'] = df_clean['Price_USD_Clean'] * usd_to_pkr_rate

    # Create high price indicator (above 50,000 PKR)
    df_clean['Price_Above_50K_PKR'] = df_clean['Price_PKR'] > 50000
    df_clean['Price_Above_50K_PKR'] = df_clean['Price_Above_50K_PKR'].map({True: 'Yes', False: 'No'})

    # Create additional useful features
    # Storage Type
    def extract_storage_type(description):
        if 'SSD' in description.upper():
            return 'SSD'
        elif 'HDD' in description.upper():
            return 'HDD'
        elif 'NVME' in description.upper():
            return 'NVMe SSD'
        elif 'EMMC' in description.upper():
            return 'eMMC'
        else:
            return 'Unknown'

    df_clean['Storage_Type'] = df_clean['description'].apply(extract_storage_type)

    # Price categories
    def categorize_price_pkr(price):
        if pd.isna(price):
            return 'Unknown'
        elif price < 30000:
            return 'Budget (<30K)'
        elif price < 50000:
            return 'Mid-Range (30K-50K)'
        elif price < 100000:
            return 'Premium (50K-100K)'
        else:
            return 'High-End (>100K)'

    df_clean['Price_Category'] = df_clean['Price_PKR'].apply(categorize_price_pkr)

    # RAM categories
    def categorize_ram(ram):
        if pd.isna(ram):
            return 'Unknown'
        elif ram <= 4:
            return 'Low (≤4GB)'
        elif ram <= 8:
            return 'Medium (5-8GB)'
        elif ram <= 16:
            return 'High (9-16GB)'
        else:
            return 'Very High (>16GB)'

    df_clean['RAM_Category'] = df_clean['RAM_GB'].apply(categorize_ram)

    # Storage categories
    def categorize_storage(storage):
        if pd.isna(storage):
            return 'Unknown'
        elif storage < 256:
            return 'Low (<256GB)'
        elif storage <= 512:
            return 'Medium (256-512GB)'
        elif storage <= 1024:
            return 'High (513GB-1TB)'
        else:
            return 'Very High (>1TB)'

    df_clean['Storage_Category'] = df_clean['Storage_GB'].apply(categorize_storage)

    # Reorder columns for better readability
    column_order = [
        'description', 'Company', 'Processor', 'RAM_GB', 'RAM_Category',
        'Storage_GB', 'Storage_Type', 'Storage_Category', 'Screen_Size',
        'price', 'Price_USD_Clean', 'Price_PKR', 'Price_Above_50K_PKR', 'Price_Category'
    ]

    # Only include columns that exist
    existing_columns = [col for col in column_order if col in df_clean.columns]
    df_final = df_clean[existing_columns]

    # Print summary statistics
    print("\n=== DATA CLEANING SUMMARY ===")
    print(f"Total records: {len(df_final)}")
    print(f"\nCompany distribution:")
    print(df_final['Company'].value_counts())
    print(f"\nRAM distribution:")
    print(df_final['RAM_GB'].value_counts().sort_index())
    print(f"\nPrice above 50K PKR:")
    print(df_final['Price_Above_50K_PKR'].value_counts())
    print(f"\nMissing values per column:")
    print(df_final.isnull().sum())

    return df_final


# Example usage:
if __name__ == "__main__":
    # Replace 'your_laptop_data.csv' with your actual file path
    csv_file_path = 'laptop_data.csv'

    # You can adjust the USD to PKR rate as needed
    current_usd_to_pkr = 278.5  # Update this with current exchange rate

    try:
        # Clean the data
        cleaned_df = clean_laptop_data(csv_file_path, current_usd_to_pkr)

        # Save the cleaned data
        output_file = 'cleaned_laptop_data.csv'
        cleaned_df.to_csv(output_file, index=False)
        print(f"\nCleaned data saved to: {output_file}")

        # Display first few rows
        print("\n=== SAMPLE OF CLEANED DATA ===")
        print(cleaned_df.head())

    except FileNotFoundError:
        print(f"Error: File '{csv_file_path}' not found. Please check the file path.")
    except Exception as e:
        print(f"Error processing data: {str(e)}")


# Additional utility functions for further analysis
def analyze_laptop_data(df):
    """Perform additional analysis on the cleaned data"""

    print("\n=== DETAILED ANALYSIS ===")

    # Price analysis
    print("Price Statistics (PKR):")
    print(df['Price_PKR'].describe())

    # Company vs Average Price
    print("\nAverage Price by Company (PKR):")
    company_price = df.groupby('Company')['Price_PKR'].mean().sort_values(ascending=False)
    print(company_price)

    # RAM vs Price correlation
    print("\nAverage Price by RAM (PKR):")
    ram_price = df.groupby('RAM_GB')['Price_PKR'].mean().sort_values(ascending=False)
    print(ram_price)

    # Storage vs Price
    print("\nAverage Price by Storage Type (PKR):")
    storage_price = df.groupby('Storage_Type')['Price_PKR'].mean().sort_values(ascending=False)
    print(storage_price)

    return df


# Function to handle missing values and outliers
def handle_missing_values_and_outliers(df):
    """Handle missing values and detect outliers"""

    print("\n=== HANDLING MISSING VALUES AND OUTLIERS ===")

    # Fill missing RAM with median by company
    df['RAM_GB'] = df.groupby('Company')['RAM_GB'].transform(
        lambda x: x.fillna(x.median())
    )

    # Fill remaining missing RAM with overall median
    df['RAM_GB'].fillna(df['RAM_GB'].median(), inplace=True)

    # Similar approach for Storage
    df['Storage_GB'] = df.groupby('Company')['Storage_GB'].transform(
        lambda x: x.fillna(x.median())
    )
    df['Storage_GB'].fillna(df['Storage_GB'].median(), inplace=True)

    # Detect price outliers using IQR method
    Q1 = df['Price_PKR'].quantile(0.25)
    Q3 = df['Price_PKR'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df['Price_PKR'] < lower_bound) | (df['Price_PKR'] > upper_bound)]
    print(f"Number of price outliers detected: {len(outliers)}")

    # Flag outliers
    df['Price_Outlier'] = (df['Price_PKR'] < lower_bound) | (df['Price_PKR'] > upper_bound)

    return df