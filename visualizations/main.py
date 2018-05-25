import pandas as pd
import matplotlib.pyplot as plt

NOT_USING = 'Nepoužívam'
NOT_INSTALL = 'Neinštaloval/a som'
NOT_CREATE = 'Nevytvoril'

TIMESTAMP = 'timestamp'
AGE = 'age'
GENDER = 'gender'
WOMAN = 'Žena'
MAN = 'Muž'

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
        '5': 'Často nefungujú',
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

# LESS_RED = '#d152ce'
# LESS_BLUE = '#52add1'

RED = '#d31717'
LESS_RED = '#d18052'
YELLOW = '#eddf1c'
LESS_BLUE = '#17d21d'
BLUE = '#1c99ed'
GREY = '#ddedce'

COLOR_MAP = {
    '5': RED,
    '4': LESS_RED,
    '3': YELLOW,
    '2': LESS_BLUE,
    '1': BLUE,
}
COLORS = {}
for question_id, answers in ANSWERS.items():
    col = {}
    for answer_id, answer in answers.items():
        col[answer] = COLOR_MAP[answer_id]
    COLORS[question_id] = col

ANSWERS = {
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


def plot_pie(column, colors=None, answers=None, legend=False):
    def my_autopct(pct):
        return '{p:.2f}%'.format(p=pct)

    plt.axis('off')
    value_counts = column.value_counts()
    if (answers):
        value_counts = value_counts[answers]
    keys = value_counts.keys()
    values = value_counts.values
    explode = [0.03 for i in range(len(values))]

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
        plt.legend(loc=3, labels=keys)


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


data = pd.read_csv('inf-spol-data.csv', delimiter=',', header=0)
old_columns, col_map, new_col_names = get_col_names(data)
data.columns = new_col_names

use_sk = data[data['1'] != NOT_USING]

woman = use_sk[use_sk['gender'] == WOMAN]
men = use_sk[use_sk['gender'] == MAN]
a = '9'

fig = plt.figure(figsize=(11, 6))
fig.suptitle(col_map[a])
ax1 = plt.subplot(121)
plt.title('Ženy')
plot_pie(woman[a], colors=COLORS[a], answers=ANSWERS[a], legend=True)
ax2 = plt.subplot(122)
plt.title('Muži')
plot_pie(men[a], colors=COLORS[a], answers=ANSWERS[a])
plt.show()

# AGE analysis
age_data = use_sk['age']
age_data = use_sk[pd.to_numeric(use_sk['age'], errors='coerce').notnull()]
age_data['age'] = age_data['age'].astype(int)
age_data = age_data[age_data['age'] < 100]

younger = age_data[age_data['age'] < 30]
older = age_data[age_data['age'] >= 30]
print(younger.shape)
print(older.shape)

fig = plt.figure(figsize=(11, 6))
fig.suptitle(col_map['9'])
ax1 = plt.subplot(121)
plt.title('Vek < 30')
plot_pie(younger[a], legend=True)
ax2 = plt.subplot(122)
plt.title('Vek >= 30')
plot_pie(older['9'])
plt.show()

print(use_sk.shape)
