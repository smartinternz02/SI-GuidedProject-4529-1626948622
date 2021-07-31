import datetime
import ibm_boto3
from ibm_botocore.client import Config, ClientError
from ibmcloudant.cloudant_v1 import CloudantV1
from ibmcloudant import CouchDbSessionAuthenticator
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

# Constants for IBM COS values
COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud" 
COS_API_KEY_ID = "IGbcgg9b_h2tMQ0AViAvulQWyj_s6YZ-S8jA1TzhnWKy"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/0442c0d0ae004a13a9d51bddd30f7054:656ea592-b88d-4acc-a2b4-a9b64c38d531::" 
# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

authenticator = BasicAuthenticator('apikey-v2-2ms0p6wxyzft3spsof0u2dslfgntpzzupu7pcwp9rwl','72aaf50add88e1e54ad53b3f53418cea')
service = CloudantV1(authenticator=authenticator)
service.set_service_url('https://apikey-v2-2ms0p6wxyzft3spsof0u2dslfgntpzzupu7pcwp9rwl:72aaf50add88e1e54ad53b3f53418cea@2b65707c-b34f-474b-99bc-9be10d93ff37-bluemix.cloudantnosqldb.appdomain.cloud')

bucket = "ptojectbuck"
def multi_part_upload(bucket_name, item_name, file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        # set 5 MB chunks
        part_size = 1024 * 1024 * 5

        # set threadhold to 15 MB
        file_threshold = 1024 * 1024 * 15

        # set the transfer threshold and chunk size
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        # the upload_fileobj method will automatically execute a multi-part upload
        # in 5 MB chunks for all files over 15 MB
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))
picname='download (4)' #datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
multi_part_upload('projectbuck', picname+'.jpg', picname+'.jpg')
json_document={"link":COS_ENDPOINT+'/'+bucket+'/'+picname+'.jpg'}
response = service.post_document(db='ped', document=json_document).get_result()
        
  
