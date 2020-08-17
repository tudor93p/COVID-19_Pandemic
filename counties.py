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

def printable(s): 
  return "".join(list(filter(lambda x:  x in set(string.printable),  s)))

def names_nonASCII(root):

  good_names = list(set(geopandas.read_file(root+"geodata.gpkg")['NAME_1']))

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

  def __init__(self, country_code, country_nameASCII = None, country_name = None, PopFactor = 1):


    self.country_code = country_code


    if country_nameASCII is not None:
      self.country_nameASCII = country_nameASCII

    else:
      self.country_nameASCII = country_code
         
      if country_name is not None and country_name==printable(country_name):
        self.country_nameASCII = country_name


    if country_name is not None:
      self.country_name = country_name
    else:
      self.country_name = self.country_nameASCII


    self.root = country_code + "_data/"

    self.list_codes = list(codes(self.root))

    self.code_to_name = names_nonASCII(self.root)

    self.code_to_nameASCII = names_ASCII(self.root)

    self.name_to_code = dict()

    for ctn in [self.code_to_name,self.code_to_nameASCII]:

      self.name_to_code.update({v: k for (k, v) in ctn.items()})

    self.code_to_pop = {k: v/PopFactor for (k, v) in populations(self.root).items()}

    self.country_pop = sum(self.code_to_pop.values())

    self.code_to_capcoord = capitalcoord(self.root)

    self.country = geopandas.read_file(self.root+"geodata.gpkg")

    self.code_to_geoindices = {c:  self.country["NAME_1"] == self.code_to_name[c] for c in self.list_codes}

    self.code_to_geoindicesC = {c:  self.country["NAME_1"] != self.code_to_name[c] for c in self.list_codes}
				# 'C' at the end stands for complementary set

    self.code_to_geocenters = {c: np.mean([list(item.centroid.coords) for item in self.country[v]["geometry"]], axis=(0, 1)) for (c, v) in self.code_to_geoindices.items()}



  def get_CountryName(self,ASCII=False):

    return self.country_nameASCII if ASCII else self.country_name


  def dict_CountryCodeToName(self, ASCII=False):

    name = self.country_nameASCII if ASCII else self.country_name

    return {self.country_code: self.get_CountryName(ASCII=ASCII)}



  def dict_CountryNameToCode(self):

    out = {self.get_CountryName(ASCII=False):self.country_code}
 
    out.update({self.get_CountryName(ASCII=True):self.country_code})

    return out

  
  
  def get_CodeList(self, include_country=False): 

    return [self.country_code]*include_country + self.list_codes 

  def dict_CodeToName(self, include_country=False, ASCII=False): 

    only_counties = self.code_to_nameASCII if ASCII else self.code_to_name

    if not include_country:
      return only_counties

    return {**only_counties, **dict_CountryCodeToName(ASCII=ASCII)}


  def dict_NameToCode(self, include_country=False): 

    if not include_country:
      return self.name_to_code

    return {**self.name_to_code, **self.dict_CountryNameToCode()}


  def dict_CodeToPop(self, include_country=False): 

    if include_country: 
      return {**self.code_to_pop, **{self.country_code: self.country_pop}}

    return self.code_to_pop


  def CountyNames(self,  include_country=False, ASCII=False): 

    only_counties = sorted(list(self.dict_CodeToName(ASCII=ASCII).values()))

    if not include_country:
      return only_counties

    add = list(self.dict_CountryCodeToName(ASCII=ASCII).values())

    return add + only_counties


  def get_Name(self, code=None, ASCII=False): 

    if code is not None: 
      return self.dict_CodeToName(include_country=True, ASCII=ASCII)[code]

  def get_Code(self, name=None): 

    if name is not None: 
      return self.dict_NameToCode(include_country=True)[name]

  def get_Pop(self, code=None, name=None): 

    D = self.dict_CodeToPop(include_country=True)

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

  print(names_ASCII("RO_data/"))


  geo = Counties("RO")

  print(geo.get_geoCountryBox())
