# -*- coding: utf-8 -*-

# Brief analysis of daily COVID data from Italian regions in June 2020.
# Data source: Protezione Civile on GitHub.
# Test functions below. 

#####

# Define 'Region' object

def str2int(x):
    """ Takes a string as input, returns the corresponding integer. 
        If the string cannot be converted into an integer, returns 'nan'. """
    try: 
        return int(x)
    except:
        return 'nan'


class Region(object):
    
    def __init__(self, row):
        self.Date = row[0]                  # when the data was collected
        self.Name = row[3]                  # region name
        self.ICU = str2int(row[7])          # number of patients in ICU
        self.NewCases = str2int(row[12])    # number of new COVID cases
        self.Deaths = str2int(row[14])      # number of deaths
        self.TotalCases = str2int(row[10])  # total positive cases
        self.Tests = str2int(row[16])       # number of tests
        
    def __str__(self):
        return 'Region: {}, Total: {}, Deaths: {}, Tests: {}'.format(
            self.Name, self.TotalCases, self.Deaths, self.Tests)
    
    def __repr__(self):
        return self.__str__()
    
    def __lt__(self, other):
        return float(self.Deaths) / self.TotalCases < float(other.Deaths) / other.TotalCases
    

# Read and analyze data

def Parse(filename):
    """ Takes the name of a file as input, returns a list of 'Region' objects as output. 
        Each object corresponds to one row in the file. """
    
    fh = open(filename, 'r', encoding = 'utf-8')
    fh.readline()
    
    Ls = []
    for l in fh: 
        row = l.replace('\n','').split(',')
        Ls.append(Region(row))
    
    return Ls


def TopRegion(Ls, n=3):
    """ Returns the n regions with the highest death-to-infected ratio """
    
    return sorted(Ls, reverse=True)[:n]


def ParseFiles(names):
    """ Takes as input a list of file names (each file corresponds to a date). 
        Returns a list of all the 'Region' objects corresponding to the rows in each file. """
        
    Rs = []
    for n in names: 
        Rs.extend(Parse(n))
    return Rs


def ComputeAverage(Ls):
    """ Takes as input a list of 'Region' objects and calculates 
        the daily average of new cases for each region. 
        Returns a dictionary with a key for each region and,
        as values, the corresponding daily average of new cases. """
        
    D = {}
    C = {}
    for l in Ls: 
        D[l.Name] = D.get(l.Name, 0) + l.NewCases
        C[l.Name] = C.get(l.Name, 0) + 1 
    
    for name in D: 
        D[name] = round(D[name] / C[name], 2)
    
    return D


# Create visualizations

def AveragePlot(D):
    """ Takes as input a dictionary with a key for each region and, 
        as values, the corresponding daily average of new cases. 
        Creates bar chart of different regions and their corresponding daily average 
        of new cases, sorted from high to low. """
        
    Ds = dict(sorted(D.items(), key = lambda x:x[1], reverse = True))
        
    x = list(Ds.keys())
    y = list(Ds.values())
    
    import matplotlib.pyplot as plt 
    
    plt.bar(x,y, color='steelblue')
    plt.xticks(rotation=90)
    plt.xlabel('Regions')
    plt.ylabel('Daily average of new cases')
    plt.title('Daily average of new cases per region')
    plt.show()
    

def str2date(s):
    """ Takes as input a string 'yyyy-mm-ddThh:mm:ss' and returns 
        a string 'yyyy-mm-dd' """
    year = s[0:4]
    month = s[5:7]
    day = s[8:10]
    return '{}-{}-{}'.format(year, month, day)
    

def TimelinePlot(Ls, region='Lombardia', attr='Deaths'):
    """ Takes as input a list of 'Region' objects and as optional arguments 
        the name of a region and an attribute. 
        Creates a timeline of the given attribute in the indicated region. 
        The default region is Lombardia and the default attribute is Deaths. """
    
    t = [ ( str2date(l.Date), getattr(l, attr) ) for l in Ls if l.Name == region]
    x = [c[0] for c in t]
    y = [c[1] for c in t]

    import matplotlib.pyplot as plt
    
    plt.plot(x,y)
    plt.xticks(rotation=90)
    plt.title('Timeline of {} in {}'.format(attr, region))
    plt.xlabel('Date')
    plt.ylabel(attr)
    plt.show()
    

def TimelineAll(Ls, attr='ICU'):
    """ Takes as input a list of 'Region' objects and as optional argument 
        an attribute. Creates a timeline of the given attribute in each region, 
        for the top 5 regions sorted by daily average of new cases. 
        The default attribute is the number of patients in ICU. """
    
    A = set()
    for l in Ls: 
        A.add(l.Name)
    
    D = {}
    for n in A: 
        D[n] = [ ( str2date(l.Date), getattr(l, attr) ) for l in Ls if l.Name == n ]
    
    Cu = ComputeAverage(Ls)
    Cs = dict( sorted(Cu.items(), key = lambda x: x[1], reverse = True)[:5] )
    
    import matplotlib.pyplot as plt
    
    for k in Cs: 
        x = [c[0] for c in D[k]]
        y = [c[1] for c in D[k]]
        plt.plot(x,y, label='{}'.format(k))
    
    plt.title('Timeline of {} in each region'.format(attr))
    plt.xticks(rotation=90)
    plt.xlabel('Date')
    plt.ylabel(attr)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.show()
    
#-----------------------------------------------
# MAIN function
#-----------------------------------------------
if __name__ == "__main__":

    # Read one file 
    print("===>>> Read one file:")
    Ls = Parse('dpc-covid19-ita-regioni-latest.csv')
    for reg in Ls[:3]:
        print(reg)
    print()
    
    # Identify 'top' regions for deaths-to-infected ratio
    print("===>>> Regions with the highest deaths-to-infected ratio:")
    for p in TopRegion(Ls):
        print(p.Name, round(p.Deaths/p.TotalCases, 2))
    print()
    
    # Read multiple files
    print("===>>> Read multiple files:")
    Fs = ['dpc-covid19-ita-regioni-20200614.csv',
          'dpc-covid19-ita-regioni-20200615.csv',
          'dpc-covid19-ita-regioni-20200616.csv',
          'dpc-covid19-ita-regioni-20200617.csv',
          'dpc-covid19-ita-regioni-20200618.csv',
          'dpc-covid19-ita-regioni-20200619.csv',
          'dpc-covid19-ita-regioni-20200620.csv']
    As = ParseFiles(Fs)
    print(As[:5])
    print()

    # Dictionary of daily averages of new cases
    print("===>>> Daily average of new cases per region:")
    Bs = ComputeAverage(As)
    for k in Bs:
        print('{}: {}'.format(k, Bs[k]))
    print()
    
    # Bar chart of daily averages of new cases
    print("===>>> See bar chart of daily averages of new cases per region")
    AveragePlot(Bs)
    
    # Timeline per region & attribute
    print("===>>> See timeline of given attribute per region")
    TimelinePlot(As, attr='ICU')
    TimelinePlot(As, region='Emilia-Romagna', attr='ICU')
    
    # Timeline of all regions per attribute
    print("===>>> See all timelines of given attribute per region")
    TimelineAll(As)
    TimelineAll(As, attr = 'NewCases')
    
    
    





