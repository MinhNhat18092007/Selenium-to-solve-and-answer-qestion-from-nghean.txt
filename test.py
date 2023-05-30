import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Thông tin đăng nhập vào tài khoản email
sender_email = 'minhnhat18092007113@gmail.com'
sender_password = 'nbaplqrklhrtbpqm'

# Thông tin người nhận email
receiver_email = 'trandinhnhatngocrongk7@gmail.com'

# Tạo đối tượng MIMEMultipart
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'Chia sẻ ảnh'

# Đính kèm file ảnh
image_path = 'D:\\DocumentPy\\ATGTSele\\screenshotcut.png'  # Đường dẫn đến file ảnh trên máy tính của bạn
with open(image_path, 'rb') as file:
    image_data = file.read()

image_mime = MIMEImage(image_data)
image_mime.add_header('Content-Disposition', 'attachment', filename='image.png')
message.attach(image_mime)

# Gửi email
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print('Email đã được gửi thành công!')
except Exception as e:
    print('Đã xảy ra lỗi trong quá trình gửi email:', str(e))
