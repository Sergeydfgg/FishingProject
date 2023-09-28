import smtplib
import json
import argparse
import email
import pandas as pd
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr


def take_addresses_from_base(path_to_base: str, addresses_limit: int) -> tuple:
    addresses_table = pd.read_csv(path_to_base, sep=',')
    return tuple(addresses_table['email'][:addresses_limit])


def prepare_email_settings(path_to_settings: str) -> dict:
    with open(path_to_settings, 'r', encoding='utf-8') as settings_file:
        settings = json.load(settings_file)
    return settings


def prepare_email_text(email_settings: dict, msg: MIMEMultipart) -> None:
    with open(email_settings['text'], 'r', encoding='utf-8') as text_file:
        text = text_file.read()
    text_parts = text.split('/')
    body = MIMEText(text_parts[0], _subtype='plain', _charset='utf-8')
    link_text = MIMEText(u'Google <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">форма</a> для заполнения',
                         'html')
    footer = MIMEText(text_parts[1], _subtype='plain', _charset='utf-8')
    msg.attach(body)
    msg.attach(link_text)
    msg.attach(footer)


def prepare_email(email_settings: dict, emails_tuple: tuple) -> None:
    username = email_settings['login']
    password = email_settings['password']
    start_send_emails(username, password, emails_tuple, email_settings)


def send_email(username: str, password: str, receivers: tuple, email_settings: dict) -> None:
    client = smtplib.SMTP_SSL('smtpdm.aliyun.com', 465)
    client.connect("smtp.mail.ru", 465)
    client.login(username, password)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = Header(email_settings['header'])
    msg['From'] = formataddr((email_settings['author'], username))
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()
    msg['To'] = ",".join(receivers)
    prepare_email_text(email_settings, msg)
    print(receivers)
    client.sendmail(username, receivers, msg.as_string())
    client.quit()


def start_send_emails(username: str, password: str, receivers: tuple, email_settings: dict) -> None:
    try:
        threads = list()
        for i in range(0, len(receivers), 50):
            th = threading.Thread(target=send_email, args=(username, password, receivers[i:i+50], email_settings))
            threads.append(th)
            th.start()
        for th in threads:
            th.join()
        print('Подарочки успешно разосланы!')
    except smtplib.SMTPConnectError as e:
        print('Письмо не дошло, ошибка соединения', e.smtp_code, e.smtp_error)
    except smtplib.SMTPAuthenticationError as e:
        print('Письмо не дошло, ошибка входа:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPSenderRefused as e:
        print('Письмо не дошло, ошбка отправителя:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPRecipientsRefused as e:
        print('Письмо не дошло, ошбика получателя')
    except smtplib.SMTPDataError as e:
        print('Письмо не дошло, ошибка содержимого:', e.smtp_code, e.smtp_error)
    except smtplib.SMTPException as e:
        print('Письмо не дошло, ', str(e))
    except Exception as e:
        print('Ошибка при отправке, ', str(e))


if __name__ == '__main__':
    pars = argparse.ArgumentParser()
    pars.add_argument("path_to_addresses", type=str, help="Путь до базы писем")
    pars.add_argument("addresses_len", type=int, help="Сколько адресов взять")
    pars.add_argument("path_to_email_settings", type=str, help="Путь до настроек письма")
    args = pars.parse_args()

    try:
        prepare_email(prepare_email_settings(args.path_to_email_settings),
                      take_addresses_from_base(args.path_to_addresses, args.addresses_len))
    except FileNotFoundError:
        print('Ошибка при вводе данных')
        