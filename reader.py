import email
from email.policy import default

class MboxReader:
    def __init__(self, filename):
        self.handle = open(filename, 'rb')
        assert self.handle.readline().startswith(b'From ')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.handle.close()

    def __iter__(self):
        return iter(self.__next__())

    def __next__(self):
        lines = []
        while True:
            line = self.handle.readline()
            if line == b'' or line.startswith(b'From '):
                yield email.message_from_bytes(b''.join(lines), policy=default)
                if line == b'':
                    break
                lines = []
                continue
            lines.append(line)


if __name__ == '__main__':

    input_fname = 'input_file_path.mbox'

    output_fname = 'output_file_path.txt'
    unique_to_emails = []
    email_data = MboxReader(input_fname)

    with open(output_fname,'w',encoding="utf-8") as file:
        for message in email_data:
            to_address = message['To']
            print(to_address)
            if to_address and not to_address in unique_to_emails:
                unique_to_emails.append(to_address)
                file.write(to_address + '\n')