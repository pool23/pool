import pandas as pd
DF = pd.read_excel('thrifyt_car_locations.xlsx')
mainRows =subRows= total_records = DF.to_dict(orient='records')
car_data = dict()
check = 1
while True:
    print(check)
    print(subRows)
    car_data = {'ATL': [], 'ORD': [], 'LAX': [], 'DFW': [], 'JFK': [], 'DEN': [], 'SFO': [], 'LAS': [], 'CLT': [],
                'MIA': [], 'PHX': [], 'IAH': [], 'SEA': [], 'MCO': [], 'EWR': [], 'MSP': [], 'BOS': [], 'DTW': [],
                'PHL': [], 'LGA': [], 'FLL': [], 'BWI': [], 'DCA': [], 'MDW': [], 'SLC': [], 'IAD': [], 'SAN': [],
                'HNL': [], 'TPA': []}

    if len(mainRows) == len(car_data):
        break
    elif check == 3:
        break
    subRows = []
    for r in mainRows:
        if r['Code'] not in car_data:
            subRows.append(r)
    check+= 1

print(len(mainRows))
print(len(car_data))
