import logging

logging.basicConfig(filename='bot.log',
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
log = logging.getLogger('Bot')


class GettingData:

    @staticmethod
    def read_f() -> object:
        with open('data.txt', 'r+') as f:
            last_line = f.readlines()[-1]
        last_line = map(int, last_line.split(','))
        last_line_int = list(last_line)
        return last_line_int

    @staticmethod
    def got_new():
        new = input('Введи 4 числа через пробел (Т1, Т2, Горячая, Холодная): ')
        new = map(int, new.split())
        new_int = list(new)
        return new_int

    @staticmethod
    def get_all_data():
        with open('data.txt', 'r') as f:
            all_data = f.read()
        return all_data

    @staticmethod
    def get_changes_history():
        prev = [0, 0, 0, 0]
        difference_full = ''
        post_string = ''
        with open('data.txt', 'r') as f:
            lines = f.readlines()[1:]
            for line in reversed(lines):
                log.info(line)
                line = map(int, line.split(','))
                line_int = list(line)
                difference = ''
                for n, p in zip(line_int, prev):
                    d = p - n
                    difference = difference + ', ' + str(d)
                prev = line_int
                difference = difference[2:]
                difference_full = difference_full + difference + '\n'
                post_string = difference_full.split("\n", 1)[1]
        return post_string


class Calc:

    def calc(new_data):
        ss = []
        a = False
        old_data = GettingData.read_f()
        # new_data = Getting_data.got_new()

        t1, t2, gor, hol = old_data
        try:
            new_t1, new_t2, new_gor, new_hol = new_data
        except:
            log.info('Введено меньше или больше четырёх значений')
            return 'Введено меньше или больше четырёх значений'

        for o, n in zip(old_data, new_data):
            if n < o:
                log.info('Новые значения меньше предыдущих!')
                a = True
                return 'Новые значения меньше предыдущих'

        if not a:
            sum = ((new_t1 - t1) * 5.92) + ((new_t2 - t2) * 1.74) + \
                  ((new_gor - gor) * 205.15) + ((new_hol - hol) * 42.30)
            s_svet = ((new_t1 - t1) * 5.92) + ((new_t2 - t2) * 1.74)
            s_voda = ((new_gor - gor) * 205.15) + ((new_hol - hol) * 42.30)
            ss = [sum, s_svet, s_voda]

        return ss
