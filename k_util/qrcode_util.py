import qrcode


def make_qrcode(content, file_path):
    q = qrcode.main.QRCode()
    q.add_data(content)
    q.make()
    m = q.make_image()
    m.save(file_path)

