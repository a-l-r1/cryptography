from aes import *
from tkinter import *
from tkinter import filedialog, messagebox, simpledialog


class App(object):
    _str_title = 'AES 加解密程序'
    _str_encrypt = '加密'
    _str_decrypt = '解密'
    _str_open_plaintext_file = '打开明文文件'
    _str_open_ciphertext_file = '打开密文文件'
    _str_save_plaintext_file = '保存明文文件'
    _str_save_ciphertext_file = '保存密文文件'
    _str_error = '错误'
    _str_info = '信息'
    _str_user_cancelled = '用户已取消'
    _str_ask_key = '请输入密钥'
    _str_key_format = '密钥为 32 位十六进制数，字母大小写不限'
    _str_key_format_error = '密钥格式错误'
    _str_encrypt_completed = '加密完成'
    _str_decrypt_completed = '解密完成'

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        master.title(self._str_title)

        self.encrypt = Button(
            frame, text=self._str_encrypt, command=self.button_encrypt
        )
        self.encrypt.pack(side=LEFT)

        self.decrypt = Button(
            frame, text=self._str_decrypt, command=self.button_decrypt
        )
        self.decrypt.pack(side=LEFT)

    @staticmethod
    def show_open_dialog(title: str) -> str:
        s = filedialog.askopenfilename(title=title)
        return s

    @staticmethod
    def show_save_dialog(title: str) -> str:
        s = filedialog.asksaveasfilename(title=title)
        return s

    @classmethod
    def show_error_messagebox(cls, contents: str) -> None:
        messagebox.showerror(cls._str_error, contents)

    @classmethod
    def show_info_messagebox(cls, contents: str) -> None:
        messagebox.showinfo(cls._str_info, contents)

    @staticmethod
    def _check_key(k: bytes) -> None:
        # TODO: key length != 128 bit
        if len(k) != 16:
            raise ValueError(__name__ + ": invalid bytes length")

    def button_encrypt(self) -> None:
        open_filename = self.show_open_dialog(self._str_open_plaintext_file)

        if len(open_filename) == 0:
            self.show_info_messagebox(self._str_user_cancelled)
            return

        save_filename = self.show_save_dialog(self._str_save_ciphertext_file)

        if len(save_filename) == 0:
            self.show_info_messagebox(self._str_user_cancelled)
            return

        k_str = simpledialog.askstring(self._str_ask_key, self._str_key_format)

        try:
            k = bytes.fromhex(k_str)
        except ValueError:
            self.show_error_messagebox(self._str_key_format_error)
            return

        try:
            self._check_key(k)
        except ValueError:
            self.show_error_messagebox(self._str_key_format_error)
            return

        try:
            encrypt_file(open_filename, save_filename, k)
        except OSError as e:
            self.show_error_messagebox(e.strerror)
            return

        self.show_info_messagebox(self._str_encrypt_completed)

    def button_decrypt(self) -> None:
        open_filename = self.show_open_dialog(self._str_open_ciphertext_file)

        if len(open_filename) == 0:
            self.show_info_messagebox(self._str_user_cancelled)
            return

        save_filename = self.show_save_dialog(self._str_save_plaintext_file)

        if len(save_filename) == 0:
            self.show_info_messagebox(self._str_user_cancelled)
            return

        k_str = simpledialog.askstring(self._str_ask_key, self._str_key_format)

        try:
            k = bytes.fromhex(k_str)
        except ValueError:
            self.show_error_messagebox(self._str_key_format_error)
            return

        try:
            self._check_key(k)
        except ValueError:
            self.show_error_messagebox(self._str_key_format_error)
            return

        try:
            decrypt_file(save_filename, open_filename, k)
        except OSError as e:
            self.show_error_messagebox(e.strerror)
            return

        self.show_info_messagebox(self._str_decrypt_completed)


def main() -> None:
    root = Tk()
    App(root)
    root.mainloop()

    try:
        root.destroy()
    except TclError:
        # 一般是用户手动点击关闭，这样程序手动调用 destroy 方法时会出错，因此这种情况不用处理
        pass


if __name__ == '__main__':
    main()
