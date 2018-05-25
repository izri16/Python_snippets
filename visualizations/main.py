import os
import pandas as pd
import matplotlib.pyplot as plt

GRAPHS_DIR = 'graphs'
FIGSIZE = (11, 6)

NOT_USING = 'Nepoužívam'
NOT_VISIT = 'Nenavštevujem'
NONE_SERVICE = 'Žiadne'
TIMESTAMP = 'timestamp'
AGE = 'age'
GENDER = 'gender'
WOMAN = 'Žena'
MAN = 'Muž'

RED = '#d31717'
BROWN = '#d18052'
YELLOW = '#efd425'
GREEN = '#17d21d'
BLUE = '#1c99ed'
GREY = '#ddedce'

ANSWERS = {
    '1': {
        '1': 'Prehľadné',
        '2': 'Celkom prehľadné',
        '4': 'Málo prehľadné',
        '5': 'Neprehľadné',
    },
    '2': {
        '1': 'Prehľadné',
        '2': 'Celkom prehľadné',
        '4': 'Málo prehľadné',
        '5': 'Neprehľadné',
    },
    '3': {
        '1': 'Veľmi užitočná služba dobre sa s ňou pracuje',
        '3': 'Bežná služba, ničím výnimočné ale pracuje sa s ňou dobre',
        '5': 'Ťažko sa mi s ňou pracuje',
    },
    '4': {
        '1': 'Jednoduchá inštalácia a prehľadné návody',
        '2': 'Jednoduchá inštalácia, avšak neprehľadné návody',
        '4': 'Zložitá inštalácia, avšak prehľadné návody',
        '5': 'Zložitá inštalácia a neprehľadné návody',
    },
    '5': {
        '1': 'Nenáročný',
        '3': 'Stredne náročný',
        '5': 'Náročný',
    },
    '8': {
        '1': 'Vždy fungujú',
        '3': 'Často fungujú',
        '5': 'Často ne fungujú',
    },
    '9': {
        '1': 'Veľmi pozitívne',
        '2': 'Pozitívne',
        '3': 'Neutrálne',
        '4': 'Negatívne',
        '5': 'Veľmi negatívne',
    },
    '10': {
        '1': 'Áno',
        '5': 'Nie',
    },
}

COLOR_MAP = {
    '5': RED,
    '4': BROWN,
    '3': YELLOW,
    '2': GREEN,
    '1': BLUE,
}
COLORS = {}
for question_id, answers in ANSWERS.items():
    col = {}
    for answer_id, answer in answers.items():
        col[answer] = COLOR_MAP[answer_id]
    COLORS[question_id] = col

ANSWERS_ORDER = {
    '1': ['Prehľadné', 'Celkom prehľadné', 'Málo prehľadné', 'Neprehľadné'],
    '2': ['Prehľadné', 'Celkom prehľadné', 'Málo prehľadné', 'Neprehľadné'],
    '3': ['Veľmi užitočná služba dobre sa s ňou pracuje',
          'Bežná služba, ničím výnimočné ale pracuje sa s ňou dobre',
          'Ťažko sa mi s ňou pracuje'],
    '4': ['Jednoduchá inštalácia a prehľadné návody',
          'Jednoduchá inštalácia, avšak neprehľadné návody',
          'Zložitá inštalácia, avšak prehľadné návody',
          'Zložitá inštalácia a neprehľadné návody'],
    '5': ['Nenáročný', 'Stredne náročný', 'Náročný'],
    '8': ['Vždy fungujú', 'Často fungujú', 'Často ne fungujú'],
    '9': ['Veľmi pozitívne', 'Pozitívne', 'Neutrálne', 'Negatívne',
          'Veľmi negatívne'],
    '10': ['Áno', 'Nie']
}


def make_autopct(values):
    def my_autopct(pct):
        return '{p:.2f}%'.format(p=pct)
    return my_autopct


def plot_pie(column, colors=None, answers=None, legend=False, loc=3,
             is_outside=False, dont_explode=False):
    def my_autopct(pct):
        return '{p:.2f}%'.format(p=pct)

    plt.axis('off')
    value_counts = column.value_counts()
    if (answers):
        value_counts = value_counts[answers]
    keys = value_counts.keys()
    values = value_counts.values
    explode = [0.03 for i in range(len(values))] if not dont_explode else None

    custom_colors = [] if colors else None
    if (colors):
        for k in keys:
            custom_colors.append(colors[k])

    _, _, texts = plt.pie(values, shadow=True, explode=explode,
                          colors=custom_colors,
                          labeldistance=0.6, autopct=make_autopct(values))

    for t in texts:
        t.set_horizontalalignment('center')
        t.set_color('white')

    if (legend):
        if (is_outside):
            plt.legend(bbox_to_anchor=(1.0, 0.7), loc=loc, labels=keys)
        else:
            plt.legend(loc=loc, labels=keys)


def create_pie_plots(data1, data2, title1, title2, out, skip):
    for task in range(1, 11):
        if (task in skip):
            continue
        t = str(task)
        colors = COLORS[t] if t in COLORS else None
        answers = ANSWERS_ORDER[t] if t in ANSWERS_ORDER else None
        fig = plt.figure(figsize=FIGSIZE)
        fig.suptitle(col_map[t])
        plt.subplot(121)
        plt.title(title1)
        plot_pie(data1[t], colors=colors, answers=answers, legend=True)
        plt.subplot(122)
        plt.title(title2)
        plot_pie(data2[t], colors=colors, answers=answers)
        plt.savefig('{}/{}_{}.png'.format(GRAPHS_DIR, out, task))
        plt.close()


def get_col_names(data):
    old_columns = data.columns
    col_map = {}
    new_col_names = [TIMESTAMP, AGE, GENDER]
    for index, c in enumerate(data.columns[len(new_col_names):]):
        splitted = c.split()
        new_col_name = splitted[0][:-1]
        col_map[new_col_name] = ' '.join(splitted[1:])
        new_col_names.append(new_col_name)
    return (old_columns, col_map, new_col_names)


def plot_services(services):
    splitted_services = []
    min_freq = 5
    for col in services:
        splitted_services += filter(
            lambda x: x != NONE_SERVICE,
            map(str.strip, col.split(',')))

    merged = pd.Series(splitted_services).value_counts()
    merged = merged[merged > min_freq]
    to_plot_services = []
    for i, m in merged.items():
        to_plot_services += ([i] * m)

    plt.figure(figsize=FIGSIZE)
    plt.title('Najpoužívanejšie služby')
    plt.subplots_adjust(right=0.5)
    plot_pie(pd.Series(to_plot_services), legend=True, loc=2, is_outside=True,
             dont_explode=True)
    plt.savefig('{}/services.png'.format(GRAPHS_DIR))
    plt.close()


if __name__ == '__main__':
    if (not os.path.exists(GRAPHS_DIR)):
        os.makedirs(GRAPHS_DIR)

    data = pd.read_csv('inf-spol-data.csv', delimiter=',', header=0)
    old_columns, col_map, new_col_names = get_col_names(data)
    data.columns = new_col_names

    # filter out those that dont really use it
    use_sk = data[data['6'] != NOT_VISIT]

    # GENDER analysis
    woman = use_sk[use_sk['gender'] == WOMAN]
    men = use_sk[use_sk['gender'] == MAN]
    create_pie_plots(woman, men, 'Ženy', 'Muži', 'gender', [7])

    # AGE analysis
    age_data = use_sk['age']
    age_data = use_sk[pd.to_numeric(use_sk['age'], errors='coerce').notnull()]
    age_data = age_data.assign(age=lambda d: d['age'].astype(int))
    age_data = age_data[age_data['age'] < 100]

    younger = age_data[age_data['age'] < 30]
    older = age_data[age_data['age'] >= 30]
    create_pie_plots(younger, older, 'Vek < 30', 'Vek >= 30', 'age', [7])

    # Services
    plot_services(use_sk['7'])

    # Stats
    print('Use slovensko.sk: {}'.format(use_sk.shape[0]))
    print('\nUse slovensko.sk (woman): {}'.format(woman.shape[0]))
    print('Use slovensko.sk (men): {}'.format(men.shape[0]))
    print('\nUse slovensko.sk (age < 30): {}'.format(younger.shape[0]))
    print('Use slovensko.sk (age > 30): {}'.format(older.shape[0]))
    print('\nNote that invalid ages were filtered out.')
