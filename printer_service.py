import win32print
import win32api
from printer_commands import text_block, build_qr_code, separator, cut_paper, empty_lines

def process_print_commands(commands):
    try:
        printer_name = win32print.GetDefaultPrinter()
        receipt = b""

        for cmd in commands:
            action = cmd.get('action')
            params = cmd.get('params', {})

            if action == 'TITLE':
                receipt += text_block(
                    params.get('text', ''),
                    align=params.get('align', 'center'),
                    bold=True
                )
            elif action == 'TEXT':
                receipt += text_block(
                    params.get('text', ''),
                    align=params.get('align', 'left'),
                    bold=params.get('bold', False)
                )
            elif action == 'SEPARATOR':
                receipt += separator(char=params.get('char', '-'))
            elif action == 'QR_CODE':
                receipt += build_qr_code(
                    params.get('data', ''),
                    size=params.get('size', 'medium')
                )
                receipt += empty_lines(1)
            elif action == 'EMPTY_LINES':
                receipt += empty_lines(params.get('count', 1))
            elif action == 'CUT':
                receipt += cut_paper()
            else:
                pass

        hPrinter = win32print.OpenPrinter(printer_name)
        try:
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("Generic Receipt", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, receipt)
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
        finally:
            win32print.ClosePrinter(hPrinter)

        return True, "Impressão realizada com sucesso."

    except Exception as e:
        return False, f"Erro na impressão: {str(e)}"