import numpy as np
import geopandas
import string


def codes(root):
  """List of county codes."""
  with open(root+"CountyCodes_ASCII.txt", "r") as f:
    return [line.split(" ")[0] for line in f.readlines()]

def names_ASCII(root):
  """ {county_code :  county_ASCIIname} and non-ASCII. """
  def code(line): 
    return line.split(" ")[0]

  def name(line): 
    return line.split(" ")[-1].strip("\n")

  with open(root+"CountyCodes_ASCII.txt", "r") as f: 

    return {code(line): name(line) for line in f.readlines()}

def names_nonASCII(root):

  def printable(s): 
    return "".join(list(filter(lambda x:  x in set(string.printable),  s)))

  good_names = list(set(geopandas.read_file(root+"gadm36_ROU.gpkg")['NAME_1']))

  good_names_print = [set(printable(n)) for n in good_names]


  def code(line): 
    return line.split(" ")[0]

  def name(line): 

    N = printable(line.split(" ")[-1].strip("\n"))

    L = np.array([len(n.intersection(N)) for n in good_names_print])

    I = np.where(L == np.max(L))[0]

    if len(I) == 1: 
      return good_names[I[0]]

    L = np.abs(len(N) - np.array([len(good_names_print[i]) for i in I]))

    I = I[np.where(L==np.min(L))[0]]

    if len(I) == 1: 
      return good_names[I[0]]

    return "ERROR: "+" ".join([good_names[i] for i in I])

  with open(root+"CountyCodes.txt", "r", encoding="latin-1") as f: 
    return {code(line): name(line) for line in f.readlines()}


def populations(root):
  """ {county_code :  county_population} """
  namecode = {v: k for (k, v) in names_ASCII(root).items()}

  def code(line): 
    return namecode[line.split("\t")[1]]

  def pop(line): 
    return int(line.split("\t")[-1].strip("\n").replace(".", ""))

  with open(root+"CountyPopulations_rawASCII.txt", "r") as f:
    return {code(line): pop(line) for line in f.readlines()}


def capitalcoord(root):
  """{county_code :  county_capital_coord} ."""

  def code(line): 

    return line.strip("\n").split(" ")[0]

  def coord(line): 

    return np.array(line.strip("\n").split(" ")[1: 3][: : -1], dtype=float)

  with open(root+"CountyCapitalCoordinates.txt", "r") as f: 

    return {code(line): coord(line) for line in f.readlines()}


def allinfo(root): #country=False):
  """{county_code :  all info} """
  name_A = names_ASCII(root)

  name = names_nonASCII(root)

  pop = populations(root)

  coord = capitalcoord(root)


  return {code: {
		"Name_ASCII": name_A[code], 
		"Name": name[code], 
		"Population": pop[code], 
		"CapitalCoord": coord[code], 
		}
					for code in codes(root)}


class Counties:
  """class with all info and convenient methods. """

  def __init__(self, PopFactor=1,  root="Ro_data/"):

    self.root = root

    self.list_codes = list(codes(self.root))

    self.code_to_name = names_nonASCII(self.root)

    self.name_to_code = {v: k for (k, v) in self.code_to_name.items()}

    self.code_to_pop = {k: v/PopFactor for (k, v) in populations(self.root).items()}

    self.code_to_capcoord = capitalcoord(self.root)

    self.country = geopandas.read_file(root+"gadm36_ROU.gpkg")

    self.code_to_geoindices = {c:  self.country["NAME_1"] == self.code_to_name[c] for c in self.list_codes}
    self.code_to_geoindicesC = {c:  self.country["NAME_1"] != self.code_to_name[c] for c in self.list_codes}
    self.code_to_geocenters = {c: np.mean([list(item.centroid.coords) for item in self.country[v]["geometry"]], axis=(0, 1)) for (c, v) in self.code_to_geoindices.items()}

  def get_CodeList(self, RO=False): 

    return ["RO"]*RO + self.list_codes 

  def dict_CodeToName(self, RO=False): 

    if RO: 
      return {**self.code_to_name, **{"RO": "România"}}

    return self.code_to_name

  def dict_NameToCode(self, RO=False): 

    if RO: 
      return {**self.name_to_code, **{"România": "RO"}}

    return self.name_to_code

  def dict_CodeToPop(self, RO=False): 

    if RO: 
      return {**self.code_to_pop, **{"RO": sum(self.code_to_pop.values())}}


    return self.code_to_pop

  def CountyNames(self,  RO=False): 

    return ["România"]*RO + sorted(list(self.dict_CodeToName().values()))

  def get_Name(self, code=None): 

    if code is not None: 
      return self.dict_CodeToName(RO=True)[code]

  def get_Code(self, name=None): 

    if name is not None: 
      return self.dict_NameToCode(RO=True)[name]

  def get_Pop(self, code=None, name=None): 

    D = self.dict_CodeToPop(RO=True)

    if code is not None: 
      return D[code]

    if name is not None: 
      return D[self.get_Code(name=name)]

  def get_geoIndex(self, code=None, name=None, complement=False): 

    D = self.code_to_geoindicesC if complement else self.code_to_geoindices

    if code is not None: 
      return D[code]

    if name is not None: 
      return D[self.get_Code(name=name)]

  def get_geoCenter(self, code=None, name=None): 

    if code is not None: 
      return self.code_to_geocenters[code]

    if name is not None: 
      return self.code_to_geocenters[self.get_Code(name=name)]

  def get_geoCapCoord(self, code=None, name=None): 

    if code is not None: 
      return self.code_to_capcoord[code]

    if name is not None: 
      return self.code_to_capcoord[self.get_Code(name=name)]

  def get_geoCapCoord_All(self): 

    return np.array(list(self.code_to_capcoord.values()))

  def set_geoColumn(self, column, value, code=None, name=None): 

    row = self.get_geoIndex(code=code, name=name)

    self.country.loc[row, column] = value

  def plot(self, **kwargs): 

    return self.country.plot(**kwargs)

  def get_geoColumn(self, column, name=None, code=None, **kwargs): 

    if name is None and code is None: 
      return self.country[column]

    row = self.get_geoIndex(code=code, name=name, **kwargs)

    return self.country[row][column]

  def get_geoCountryBox(self): 

    bounds = self.country.bounds

    xlim = [np.min(bounds.minx), np.max(bounds.maxx)]
    ylim = [np.min(bounds.miny), np.max(bounds.maxy)]
  
    return xlim, ylim 


if __name__ == '__main__': 
  """Test."""

  geo = Counties()

  print(geo.get_geoCountryBox())