from VersionOne.PDF_Reader.readpdf import PDFReader
import os
from VersionOne.PDF_Reader.constant import Constant
from datetime import datetime
import json

def main():
    try:
        result = {"IsSuccess":False, "json_result": None, "Message":"Json creation failed!"}
        pdfreader = PDFReader()
        basic_and_billing_details = pdfreader.extract_basic_details_pdf()
        if basic_and_billing_details['IsSuccess']:
            output_path = Constant.SAVE_JSON
            output_file = f"pdf_details_{datetime.now().strftime("%Y%m%d%H%M%S")}.json"
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            with open(output_path+"\\"+output_file, 'w') as file:
                json.dump(basic_and_billing_details['Json_Base_Details_billing_details'], file)
            print("New Json file is sucessfully saved with data points......")
            result["IsSuccess"] = True
            result['Message'] = "Json creation successfully executed!"
            result['json_result'] = basic_and_billing_details["Json_Base_Details_billing_details"]
        else:
            result['IsSuccess'] = basic_and_billing_details['IsSuccess']
            result['Message'] = basic_and_billing_details['Message']
    except PermissionError:
        result['IsSuccess'] =  basic_and_billing_details['IsSuccess']
        result["Message"] = basic_and_billing_details["Message"]
        result['json_result'] = basic_and_billing_details["Json_Base_Details_billing_details"]
        print(f"Error occured during json creation {exception.args}")
    except Exception as exception:
        result["Message"] = basic_and_billing_details["Message"]
        result['json_result'] = basic_and_billing_details["Json_Base_Details_billing_details"]
        print(f"Error occured during json creation {exception.args}")
    finally:
        return result

if __name__ == "__main__":
    main()
