import glob
import os
import traceback
from rest_framework import status
from rest_framework.response import Response

def list_pdf(path):
    try:
        result = {"IsSuccess": False, "list_pdf": None, "Message":"List_pdf method failed"}
        pdf_files = glob.glob(os.path.join(path, '*.pdf'))

        # Display the list of PDF files found
        list_pdf = [pdf_file for pdf_file in pdf_files]
        result['IsSuccess'] = True
        result['list_pdf'] = list_pdf
        result['Message']= "List_pdf method successfully executed"
    except Exception as exception:
        result['Message'] = f"Error occured while listing pdf files! {traceback.format_exc()}"
    finally:
        return result
    
    
def global_response_format(status_value, data, status_code, status_message=None):
	# success Response format
	if status_code == 200:
		status_return=status.HTTP_200_OK
	elif status_code == 400:
		status_return=status.HTTP_400_BAD_REQUEST
	elif status_code == 500:
		status_return=status.HTTP_500_INTERNAL_SERVER_ERROR
	
	return Response(
		{
			'status': status_value,
			'data': data,
			'status_message': status_message,
			'status_code': status_code
		},
		status=status_return
	)