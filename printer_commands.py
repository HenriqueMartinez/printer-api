ESC = b'\x1b'
GS = b'\x1d'
LINE_FEED = b'\n'
PAPER_CUT = GS + b'V\x00'

ALIGN_LEFT = ESC + b'a\x00'
ALIGN_CENTER = ESC + b'a\x01'
ALIGN_RIGHT = ESC + b'a\x02'

BOLD_ON = ESC + b'E\x01'
BOLD_OFF = ESC + b'E\x00'

QR_MODEL = b'\x1D\x28\x6B\x04\x00\x31\x41\x32\x00'
QR_CORRECTION = b'\x1D\x28\x6B\x03\x00\x31\x45\x30'
QR_PRINT = b'\x1D\x28\x6B\x03\x00\x31\x51\x30'

QR_SIZES = {
    'small': b'\x1D\x28\x6B\x03\x00\x31\x43\x02',
    'medium': b'\x1D\x28\x6B\x03\x00\x31\x43\x03',
    'large': b'\x1D\x28\x6B\x03\x00\x31\x43\x04',
    'xlarge': b'\x1D\x28\x6B\x03\x00\x31\x43\x05',
}

def text_block(text, align='left', bold=False):
    align_cmd = {
        'left': ALIGN_LEFT,
        'center': ALIGN_CENTER,
        'right': ALIGN_RIGHT
    }.get(align, ALIGN_LEFT)
    
    return (
        (BOLD_ON if bold else b'') +
        align_cmd +
        text.encode('cp860') +
        (BOLD_OFF if bold else b'') +
        LINE_FEED
    )

def build_qr_code(qr_data, size='medium'):
    size_cmd = QR_SIZES.get(size, QR_SIZES['medium'])
    qr_bytes = qr_data.encode('utf-8')
    qr_len = len(qr_bytes) + 3
    pL = qr_len % 256
    pH = qr_len // 256
    return (
        QR_MODEL +
        size_cmd +
        QR_CORRECTION +
        b'\x1D\x28\x6B' + bytes([pL, pH]) + b'\x31\x50\x30' + qr_bytes +
        QR_PRINT
    )

def separator(char='-', align='center'):
    return text_block(char * 42, align)

def cut_paper():
    return PAPER_CUT

def empty_lines(count=1):
    return LINE_FEED * count