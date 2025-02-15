import matplotlib.pyplot as plt
import pandas as pd

a = pd.read_json('/Users/pascal/Documents/AccessBuildingClimate/DataReview/example/rasp4log.txt', lines=True)
a['date'] = pd.to_datetime(a.time)
a = a.set_index(a["date"]).sort_index()
a

a.plot('date','temperature')
plt.show()
