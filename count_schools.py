import csv

# Header and first line of data:
# NCESSCH,LEAID,LEANM05,SCHNAM05,LCITY05,LSTATE05,LATCOD,LONCOD,MLOCALE,ULOCALE,status05
# 010000200277,0100002,ALABAMA YOUTH SERVICES,SEQUOYAH SCHOOL - CHALKVILLE CAMPUS,PINSON,AL,33.674697,-86.627775,3,41,1

def read_data():
    data = []  
    with open ('school_data.csv', encoding='utf8', errors='replace') as csvfile:
        for row in csv.DictReader(csvfile):
            data.append(row)
    return data

def aggregate_by(data, field):
    aggs = dict()
    for r in data:
        agg = r[field]
        if not agg in aggs:
            aggs[agg] = 0
        aggs[agg] += 1
    return aggs

def print_aggs(data, field):
    aggs = aggregate_by(data, field)
    for agg in sorted(aggs):
        print ('%s: %s' % (agg, aggs[agg]))  

def print_counts():
    data = read_data()

    print ('Total Schools: %s' % len(data))

    print ('Schools by State:')
    print_aggs(data, 'LSTATE05')

    print ('Schools by Metro-entric locale:')
    print_aggs(data, 'MLOCALE')

    cities = aggregate_by(data, 'LCITY05')
    topCity = max(cities.keys(), key=(lambda k: cities[k]))
    print ('City with the most schools: %s (%d schools)' % (topCity, cities[topCity]))

    print('Unique cities with at least one school: %d' % len(cities))

if __name__ == "__main__":
    print_counts()
