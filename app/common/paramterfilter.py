import re
import magic
_phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
_email_pat = re.compile('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$')


class ParameterFilter(object):

    _file_magic = None

    @staticmethod
    def check_phone(phone: str) -> bool:
        """
        check the phone is valid or not
        :param phone: phone number
        :return: boolean
        """
        try:
            return re.search(_phone_pat, phone)
        except ...:
            return False

    @staticmethod
    def check_email_address(email: str) -> bool:
        """
        check the email address is valid or not
        :param email: email address
        :return: boolean
        """
        if email == '' or email.startswith('@') or email.endswith('@') or not email.find('@'):
            return False
        try:
            return re.search(_email_pat, email)
        except ...:
            return False

    @staticmethod
    def check_username_keyword(username: str, keyword: set) -> bool:
        """
        check username containes keyword, user name not allowed
        :param keyword: keyword list
        :param username: username
        :return: bool
        """
        if any([item in username for item in keyword]):
            return True
        return False

    @staticmethod
    def check_upload_data_not_allowed(upload_data: bytes, not_allowed_set: set) -> bool:
        """
        check upload data filetype is not threat
        :param upload_data: upload file data
        :param not_allowed_set: file mimetype not allowed
        :return:
        """
        global _file_magic
        if _file_magic is None:
            _file_magic = magic.Magic()
        try:
            file_type = _file_magic.from_buffer(upload_data)
            if file_type in not_allowed_set:
                return True
            return False
        except magic.MagicException:
            return False



if __name__ == '__main__':
    username = 'xhou'
    a = {'xh', 'x1'}
    print(ParameterFilter.check_username_keyword(username, a))
