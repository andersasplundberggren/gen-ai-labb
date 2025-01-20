import matplotlib.pyplot as plt
import pandas as pd

# Skapa några testdata
data = {
    'År': [2024, 2025, 2026, 2027, 2028],
    'Befolkning': [1724, 1702, 1690, 1680, 1670]
}
df = pd.DataFrame(data)

# Skapa en enkel linjediagram
plt.plot(df['År'], df['Befolkning'])
plt.title('Testdiagram')
plt.xlabel('År')
plt.ylabel('Befolkning')
plt.show()
