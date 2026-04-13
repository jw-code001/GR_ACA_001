# %%
from scraping import get_simple_data
import pandas as pd
import matplotlib.pyplot as plt
# %%
# 한글 깨짐 방지 설정
plt.rcParams['font.family'] = 'Malgun Gothic' # Mac은 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

data = get_simple_data("https://wwdoctor.com/board/review.do?lang=kr&page=2","#main .board_content .list_table  tbody tr td:nth-child(2)")

labels = list(set(data))
values = [data.count(label) for label in labels]

plt.bar(labels, values)
plt.show()

# %%
