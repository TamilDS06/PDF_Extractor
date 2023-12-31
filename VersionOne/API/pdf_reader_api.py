from rest_framework.views import APIView
from VersionOne.PDF_Reader.main import main
from VersionOne.PDF_Reader.utils import global_response_format


class ExtractPdf(APIView):
    def get(self, request):
        result = main()
        if result['IsSuccess']:
            return global_response_format(result['IsSuccess'], result["json_result"], 200, result['Message'])
        else:
            return global_response_format(result['IsSuccess'], result["json_result"], 200, result['Message'])
        
        