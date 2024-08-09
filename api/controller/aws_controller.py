# from datetime import date, datetime
# from flask_restx import Namespace, Resource
# from flask import request, jsonify, abort
# from api.service.aws_service import aws_service
# from dotenv import load_dotenv
# import os
# import logging
# import boto3
# from botocore.exceptions import ClientError
# from botocore.config import Config
# import zipfile
#
# logger = logging.getLogger(__name__)
#
# load_dotenv()
#
# bucket_api = Namespace(
#     's3 bucket',
#     description='access to aws s3 bucket')
#
# my_config = Config(
#     region_name='eu-north-1',
#     signature_version='s3v4',
#     retries={
#         'max_attempts': 10,
#         # 'mode': 'standard'
#     },
#     s3={'addressing_style': 'path'},
# )
# UPLOAD_FOLDER = "uploads"
# BUCKET = "upload-me-bucket"
# s3 = boto3.client('s3', config=boto3.session.Config(signature_version='s3v4'), region_name='eu-north-1',
#                   aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
#                   aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY_ID'])
#
#
# def upload_file(file_name, bucket):
#     try:
#         object_name = file_name
#         # s3_client = boto3.client('s3')
#         s3.upload_file(file_name, bucket, object_name)
#         print(f"19: {file_name}")
#     except Exception as e:
#         raise e
#
#
# def generate_presigned_url(s3_client, client_method, method_parameters, expires_in):
#     """
#     Generate a presigned Amazon S3 URL that can be used to perform an action.
#
#     :param s3_client: A Boto3 Amazon S3 client.
#     :param client_method: The name of the client method that the URL performs.
#     :param method_parameters: The parameters of the specified client method.
#     :param expires_in: The number of seconds the presigned URL is valid for.
#     :return: The presigned URL.
#     """
#     try:
#         url = s3_client.generate_presigned_url(
#             ClientMethod=client_method, Params=method_parameters, ExpiresIn=expires_in
#         )
#         logger.info("Got presigned URL: %s", url)
#     except ClientError:
#         logger.exception(
#             "Couldn't get a presigned URL for client method '%s'.", client_method
#         )
#         raise
#     return url
#
#
# @bucket_api.route('/getlist', methods=['GET'])
# class GetListController(Resource):
#     def get(self):
#         try:
#             # List objects in the specified folder
#             response = s3.list_objects_v2(Bucket=BUCKET, Prefix='uploads')
#
#             # Extract filenames from the response
#             files = [obj['Key'] for obj in response.get('Contents', [])]
#
#             return jsonify(files)
#         except ClientError as e:
#             print(e)
#             # Handle errors
#             abort(500)
#
#
# @bucket_api.route('/download/<token>', methods=['GET'])
# class DownloadFilesController(Resource):
#     def get(self, token=None):
#         try:
#             print(token)
#             file = aws_service.getFileName(token)
#             print(f"file only : {file}")
#             if file is not None:
#                 # List objects in the specified folder
#                 # print(response)
#                 url = generate_presigned_url(
#                     s3, 'get_object', {"Bucket": BUCKET, "Key": file.file_name}, 10000
#                 )
#                 print(url)
#                 return {'url': url, 'filename': file.file_name}
#                 # Return the file as an attachment
#                 # return send_file(BytesIO(response), as_attachment=True)
#             else:
#                 return {'message': "the url link must have expired or doesn't exist"}
#         except ClientError as e:
#             print(e)
#             bucket_api.abort(404)
#
#
# @bucket_api.route('/uploads/<id>', methods=['POST'])
# class BucketController(Resource):
#     def post(self, id=None):
#         try:
#             files = request.files
#             if len(files) > 0:
#                 print(files)
#                 filename = list(files.keys())[0].split('.')[0]  # Get the first key (filename)
#                 print(filename)
#                 directory = f"{id}"
#                 try:
#                     os.mkdir(directory)
#                     print("Directory '%s' created successfully" % directory)
#                 except OSError as error:
#                     print("Directory '%s' can not be created" % directory)
#                 today = date.today()
#                 time = datetime.now().time()
#                 zip_file_path = f"{id}/{filename}-{today}-{time}.zip"
#                 with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
#                     # Iterate over each key-value pair in the ImmutableMultiDict
#                     for filename, file_storage in files.items():
#                         # Get the contents of the file
#                         file_contents = file_storage.read()
#
#                         # Write the file to the zip file
#                         zip_file.writestr(filename, file_contents)
#                 upload_file(zip_file_path, BUCKET)
#                 link_info = aws_service.CreateLink(id)
#                 token = link_info[1]
#                 aws_service.StoreFile(link_info[0], zip_file_path, id)
#                 print("Zip file saved successfully at:")
#                 # for fname in request.files:
#                 #     print(f"fname type : {type(fname)}")
#                 #     f = request.files.get(fname)
#                 #     print(f"prem: {fname}")
#                 #     print(f"deux: {f.filename}")
#                 #     print(f"trois: {f}")
#                 #     f.save('./uploads/%s' % secure_filename(f.filename))
#                 # upload_file(f"uploads/{f.filename}", BUCKET)
#                 return {'token': token}
#             else:
#                 return 'no files'
#         except Exception as e:
#             raise e
#
#
# @bucket_api.route('/aws_upload/<zip_file>',methods=['POST'])
# class AwsUploadController(Resource):
#     def post(self, zip_file=None):
#         try:
#             if zip_file:
#                 upload_file(zip_file, BUCKET)
#         except Exception as e:
#             raise e