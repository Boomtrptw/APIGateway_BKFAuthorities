import os
import pathlib
import requests
import shutil
import uuid
import appsetting as appsetting
import base64
import secrets
import string
import smtplib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# All
stringEmpty = ""
pathRoot = str(pathlib.Path(__file__).parent.resolve().parent)
pathRootImgSurvey = "media/survey/"

# Format
formatYmd = f"%Y-%m-%d"  # 0000-00-00

# Fast API
fastAPITitle = "Supply Chain Information Management"
fastAPIVersion = "1.0.0"
fastAPIDescription = "API Gateway for Supply Chain Information Management By PostgreSQL"

# Email Subject
emailSubjectForgotPassword = "Forgot Password"
emailSubjectAccountDetail = "Account Detail"

# Permission
permissionSurvey = "permission-Id-2fc1e1de-284c-429d-8a08-a755003bb854"
permissionBOMManagement = "permission-Id-55c953f3-83e9-4558-811d-f88c420980a4"
permissionManagePartInformation = "permission-Id-63ca0863-33dc-42b1-b260-03f12e7e6912"
permissionManageMaterialComponent = "permission-Id-75ac618f-3562-4d47-bb1e-6a67bf9e4797"
permissionManageModel = "permission-Id-761a15e0-9fab-41c8-bbf2-78bdf92319da"
permissionManageCompany = "permission-Id-79e30e63-fad5-40dd-8f67-9e6529081659"
permissionManageUserManagement = "permission-Id-8b47bfd4-53df-4802-8a8f-77eee8a8638e"
permissionManageOwnProfile = "permission-Id-ba2d6294-a99f-4daa-8419-d12aad55487b"
permissionManagePartnersProfile = "permission-Id-bf814978-f222-40d8-8f47-ed5b4bc15156"
permissionReportInformationSearch = "permission-Id-cfa1967f-85d1-4554-a94a-74865c9caac3"
permissionReportStatusSearch = "permission-Id-fbaf127a-cef6-4129-9c5b-d88b1902551d"


# Icon
iconToyotaBoshokuAsia = f"{appsetting.urlAPI88}SaveAndShowAttachment/Image/SupplyChainInformationManagement/IconToyotaBoshokuAsia.png"


def GetUUID():
    return str(uuid.uuid4())


def Print(value):
    print(f"\n{value}\n")


def StringIsNullOrEmpty(value):
    return [stringEmpty, "None", None].__contains__(value)


def IsNumberZero(value):
    return ["0", "0.0", 0, 0.0, None].__contains__(value)


def ConvertToBool(value: str):
    return str(value).strip().lower() == "true"


def CheckFileUrlExists(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")
        return False


async def GetFileName(filePath: str):
    fileName = os.path.basename(filePath)
    return fileName


async def GetAttachmentPath(fileLocation: str):
    if appsetting.host == "0.0.0.0":
        return f"{appsetting.protocol}{appsetting.hostForAccessFile}/{str(appsetting.siteName)}/{("/".join(fileLocation.split("/")[1:]))}"
    else:
        return f"{appsetting.protocol}{appsetting.host}{str(appsetting.portForAccessFile)}/{str(appsetting.siteName)}/{("/".join(fileLocation.split("/")[1:]))}"


async def GetFileExtension(fileName: str):
    filename, file_extension = os.path.splitext(fileName)
    return file_extension.lower()


async def GetFolderAndFilePath(fileLocation: str, partFolderSource: str, partFolderDestination: str):
    pathFile = fileLocation.replace(pathRoot, stringEmpty)
    return pathFile.replace(partFolderSource, partFolderDestination)


async def GetPictureForSearchInformationDetail(picture: str):
    attachmentPath = stringEmpty
    if not StringIsNullOrEmpty(picture):
        attachmentPath = f"{appsetting.urlSCIM}{pathRootImgSurvey}{picture}"
    return attachmentPath


async def DeleteFile(url: str):
    if os.path.exists(url):
        try:
            os.remove(url)
            print(f"File {url} has been deleted successfully.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    else:
        print(f"File {url} does not exist.")


async def MoveFile(fileLocation: str, partFolderSource: str, partFolderDestination: str):
    pathFile = fileLocation.replace(pathRoot, stringEmpty)
    pathFolder = pathRoot + os.path.dirname(pathFile).replace(partFolderSource, partFolderDestination)
    os.makedirs(pathFolder, exist_ok=True)
    shutil.move(fileLocation, pathFolder)


def Encrypt(value):
    iv = os.urandom(appsetting.aesIV)
    cipher = AES.new(base64.b64decode(appsetting.aesSecretKey), AES.MODE_CBC, iv)
    encryptedBytes = cipher.encrypt(pad(value.encode(), AES.block_size))
    encryptedData = base64.b64encode(iv + encryptedBytes).decode("utf-8")
    return encryptedData


def Decrypt(value):
    encryptedBytes = base64.b64decode(value)
    iv = encryptedBytes[: appsetting.aesIV]
    cipher = AES.new(base64.b64decode(appsetting.aesSecretKey), AES.MODE_CBC, iv)
    decryptedMessage = unpad(cipher.decrypt(encryptedBytes[appsetting.aesIV :]), AES.block_size)
    return decryptedMessage.decode("utf-8")


def GeneratePassword(length=12):
    characters = string.ascii_letters + string.digits
    # characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(characters) for _ in range(length))
    return password


def EmailBodyForgotPassword(value):
    body = f"""
        <div style="margin: 0 auto; width: 550px; padding: 30px 20px; background: #f9f9f9; border-radius: 5px; color: #000000 !important">
            <div style="overflow: hidden; margin: 0 0 50px">
                <img alt="Toyota Boshoku Asia" src="{iconToyotaBoshokuAsia}" width="49" style="float: left;">
                <p style="float: left; margin: 5px 0 0 10px; font-family: 'Sarabun', sans-serif; font-size: 18px; font-weight: 500;">
                    Toyota Boshoku Asia
                </p>
            </div>
            <p style="margin: 0 0 20px; font-family: 'Sarabun', sans-serif; font-size: 24px; font-weight: 600;">Reset Password</p>
            <p style="margin: 0; font-family: 'Sarabun', sans-serif; font-size: 16px; line-height: 25px;">
                We have received a request to reset your password. Please confirm the reset to choose a new password. Otherwise, you can ignore this email.
            </p>
            <a href="{appsetting.urlSCIM}change-password?v={Encrypt(value)}" style="display: block;margin: 50px auto;width: 150px;height:40px;color:#ffffff;font-size:14px;line-height:40px;text-align:center;text-decoration:none;background-color:#00a2cf;border-radius:20px;">Reset Password</a>
            <p style="margin: 0; padding-top: 20px; font-family: 'Sarabun', sans-serif; font-size: 14px; line-height: 26px; border-top: 1px solid #595e65; text-align: center;">Address : 801 ถ. กาญจนาภิเษก แขวงประเวศ เขตประเวศ กรุงเทพมหานคร 10250<br>Tel : 02 329 5000</p>
        </div>
        """
    return body


def EmailBodyNewAccount(value, email, password):
    body = f"""
        <div style="margin: 0 auto; width: 550px; padding: 30px 20px; background: #f9f9f9; border-radius: 5px; color: #000000 !important">
            <div style="overflow: hidden; margin: 0 0 50px">
                <img alt="Toyota Boshoku Asia" src="{iconToyotaBoshokuAsia}" width="49" style="float: left;">
                <p style="float: left; margin: 5px 0 0 10px; font-family: 'Sarabun', sans-serif; font-size: 18px; font-weight: 500;">
                    Toyota Boshoku Asia
                </p>
            </div>
            <p style="margin: 0 0 20px; font-family: 'Sarabun', sans-serif; font-size: 24px; font-weight: 600;">Account Detail</p>
            <p style="margin: 0; font-family: 'Sarabun', sans-serif; font-size: 16px; line-height: 25px;">
                Please change your password after the first login
            </p>
            <p style="font-family: 'Sarabun', sans-serif; font-size: 24px;"><font style="font-weight: 600;">User ID  :<font/> {email}</p>
            <p style="font-family: 'Sarabun', sans-serif; font-size: 24px;"><font style="font-weight: 600;">Password  :<font/> {password}</p>
            <a href="{appsetting.urlSCIM}change-password?v={Encrypt(value)}" style="display: block;margin: 50px auto;width: 150px;height:40px;color:#ffffff;font-size:14px;line-height:40px;text-align:center;text-decoration:none;background-color:#00a2cf;border-radius:20px;">Change Password</a>
            <p style="margin: 0; padding-top: 20px; font-family: 'Sarabun', sans-serif; font-size: 14px; line-height: 26px; border-top: 1px solid #595e65; text-align: center;">Address : 801 ถ. กาญจนาภิเษก แขวงประเวศ เขตประเวศ กรุงเทพมหานคร 10250<br>Tel : 02 329 5000</p>
        </div>
        """
    return body


def SendEmail(email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = f"{appsetting.smtpSenderName}<{appsetting.smtpSender}>"
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))
    server = smtplib.SMTP(appsetting.smtpServer, appsetting.smtpPort)
    server.starttls()
    server.login(appsetting.smtpSender, appsetting.smtpPassword)
    server.sendmail(appsetting.smtpSender, email, msg.as_string())
    server.quit()


def NumberFormat(number):
    return stringEmpty if StringIsNullOrEmpty(number) else f"{number:,}"


def GetSearchHasForSearchInformationDetail(item, partNumber, partName, supplierName, address, process, backUp,material):
    searchHas = False
    if not StringIsNullOrEmpty(partNumber) and not StringIsNullOrEmpty(item.PartNumber):
        if not searchHas:
            searchHas = item.PartNumber.lower().__contains__(partNumber.lower())
    if not StringIsNullOrEmpty(partName) and not StringIsNullOrEmpty(item.PartName):
        if not searchHas:
            searchHas = item.PartName.lower().__contains__(partName.lower())
    if not StringIsNullOrEmpty(supplierName) and not StringIsNullOrEmpty(item.SupplierName):
        if not searchHas:
            searchHas = item.SupplierName.lower().__contains__(supplierName.lower())
    if not StringIsNullOrEmpty(address) and not StringIsNullOrEmpty(item.Address):
        if not searchHas:
            searchHas = item.Address.lower().__contains__(address.lower())
    if not StringIsNullOrEmpty(process) and not StringIsNullOrEmpty(item.IndustrialMethod):
        if not searchHas:
            searchHas = item.IndustrialMethod.lower().__contains__(process.lower())
    if not StringIsNullOrEmpty(backUp) and not StringIsNullOrEmpty(item.Backup):
        if not searchHas:
            searchHas = item.Backup.lower().__contains__(backUp.lower())
    if not StringIsNullOrEmpty(material) and not StringIsNullOrEmpty(item.Material):
        if not searchHas:
            searchHas = item.Material.lower().__contains__(material.lower())
    return searchHas
