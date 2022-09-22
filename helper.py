import random

import numpy as np
import pandas as pd
import sqlite3
#
con = sqlite3.connect("/database/user_datas.db")
data = pd.read_sql("SELECT * FROM users;", con)
print(data)
