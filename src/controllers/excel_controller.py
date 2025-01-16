import pandas as pd
from typing import List, Dict

class ExcelController:
    @staticmethod
    def read_contacts(file_path: str) -> List[Dict[str, str]]:
        try:
            df = pd.read_excel(file_path)
            required_columns = ['Name', 'Phone']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Excel file must contain 'Name' and 'Phone' columns")
            
            contacts = []
            for _, row in df.iterrows():
                phone = str(row['Phone']).strip()
                if phone.startswith('0'):
                    phone = '62' + phone[1:]
                elif not phone.startswith('62'):
                    phone = '62' + phone
                    
                contacts.append({
                    'name': str(row['Name']).strip(),
                    'phone': phone
                })
            
            return contacts
            
        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")