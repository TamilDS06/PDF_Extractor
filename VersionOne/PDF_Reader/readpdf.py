from VersionOne.PDF_Reader.constant import Constant
from VersionOne.PDF_Reader.utils import list_pdf
import sys
import traceback
from pdfminer.high_level import extract_text
import re
import tabula


class PDFReader:


    def __init__(self, pdf_dir):
        try:
            result = {"IsSuccess":False, "List_pdf":None, "Message":"Constructor method failed!"}
            self.pdf_list = list_pdf(pdf_dir)
            if len(self.pdf_list['list_pdf']) == 0:
                print("No pdf files found in specified location!")
                sys.exit()
            result['IsSuccess'] = True
            result['List_pdf'] = self.pdf_list
            result['Message'] = "Constructor method successfully executed!"
        except Exception as exception:
            print(f"Error occurred in contructor! {exception.args}")
            result['Message'] = f"Error occurred in contructor! {traceback.format_exc()}"
        

    def extract_basic_details_pdf(self):
        try:
            result = {"IsSuccess":False, "Json_Base_Details_billing_details":None, "Message":"extract_basic_details_pdf method failed!"}
            basic_billing_details_total = []
            for pdf_file_path in self.pdf_list['list_pdf']:
                current_pdf_basic_details = {}
                text = extract_text(pdf_file=pdf_file_path)

                # Invoice Number
                invoice_number = re.search(r'INVOICE NO: (\d+)', text)
                invoice_number = invoice_number.group(1).strip() if invoice_number else None

                # Date
                date = re.search(r'DATE: (\d{2}/\d{2}/\d{4})', text)
                date = date.group(1).strip() if date else None

                # From Address and PAN NO.
                from_address_match = re.search(r'Address: (.*?)\nGSTIN: (.*?)\nPAN NO. (\d+)', text, re.DOTALL)
                if from_address_match:
                    from_address = from_address_match.group(1).strip()
                    gstin = from_address_match.group(2).strip()
                    pan_number = from_address_match.group(3).strip()
                else:
                    from_address, gstin, pan_number = None, None, None

                # Business Name
                business_name_match = re.search(r'BUSINESS NAME: (.*?),', text)
                business_name = business_name_match.group(1).strip() if business_name_match else None
                # Party's Name, Address, and GSTIN
                party_details = re.search(r"PARTY'S NAME: (.*?)[,\n].*?BUSINESS NAME: (.*?)[,\n].*?Address: (.*?)[,\n].*?GSTIN: (.*?)\n", text)
                if party_details:
                    party_name = party_details.group(1).strip()
                    party_address = party_details.group(3).strip()
                    party_gstin = party_details.group(4).strip()
                else:
                    party_name, party_address, party_gstin = None, None, None
                current_pdf_basic_details['invoice_number'] = invoice_number
                current_pdf_basic_details['date'] = date
                current_pdf_basic_details['from_address'] = [from_address, gstin, pan_number]
                current_pdf_basic_details["party's name"] = business_name
                current_pdf_basic_details['to_address'] = [business_name, party_address, party_gstin]
                tables = tabula.read_pdf(pdf_file_path, pages="all")
                for table in tables:
                    # Handling null values
                    table.dropna(how='all', inplace=True)
                    table.dropna(axis=1, how='all', inplace=True)
                    table = table.fillna('None')
                    product_detail = []
                    # Getting product billing details
                    for Description, Hash, Qty, Rate, Amount in table.itertuples(index=False):
                        product = {}
                        if Description != 'None' and Hash != 'None' and Qty != 'None' and Rate != 'None' and Amount != 'None':
                            product['name'] = Description
                            product["id"] = Hash
                            product['count'] = Qty
                            product["price"] = Rate
                            product['Amount'] = Amount
                            product_detail.append(product)
                        elif Description == 'None' and Hash == 'None' and Qty == 'None':
                            product['total'] = Amount
                            product_detail.append(product)
                        elif Hash == 'None' and Qty == 'None' and Rate == 'None' and Amount == 'None':
                            product["rupees_in_words"] = Description.split(':')[1].strip()
                            product_detail.append(product)
                current_pdf_basic_details["billing_deatils"] = product_detail
                basic_billing_details_total.append(current_pdf_basic_details)

            result['IsSuccess'] = True
            result['Json_Base_Details_billing_details'] = basic_billing_details_total
            result['Message'] = "extract_basic_details_pdf successfully executed!"

        except Exception as exception:
            print(f"Error occurred in extract_basic_details_pdf! {exception.args}")
            result['Message'] = f"Error occurred in extract_basic_details_pdf! {traceback.format_exc()}"
        finally:
            return result
        

    def extract_billing_details_pdf(self):
        try:
            result = {"IsSuccess":False, "Json_Billing_Details":None, "Message":"extract_billing_details_pdf method failed!"}
            billing_details_total = []
            for pdf_file_path in self.pdf_list['list_pdf']:
                current_pdf_billing_details = {}
                pass


        except Exception as exception:
            print(f"Error occurred in extract_billing_details_pdf! {exception.args}")
            result['Message'] = f"Error occurred in extract_billing_details_pdf! {traceback.format_exc()}"
        finally:
            return result
