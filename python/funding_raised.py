import csv
from dataclasses import dataclass
from typing import Iterable, Tuple

class Startup(dict):
  ATTR_LIST = [
    "permalink", 
    "company_name",
    "number_employees",
    "category",
    "city",
    "state",
    "funded_date",
    "raised_amount",
    "raised_currency",
    "round"
    ]

  def __init__(self) -> None:
    self.permalink, self.companyName, self.employeeCount, self.category, self.city, self.state, self.foundedDate, self.raisedAmount, self.raisedCurrency, self.round= ["affe"]*10
    self._superInit()
  
  def _superInit(self):
    super().__init__([
      ("permalink", self.permalink),
      ("company_name", self.companyName),
      ("number_employees", self.employeeCount),
      ("category", self.category),
      ("city", self.city),
      ("state", self.state),
      ("funded_date", self.foundedDate),
      ("raised_amount", self.raisedAmount),
      ("raised_currency", self.raisedCurrency),
      ("round", self.round)
    ])

  @staticmethod
  def readByCsvRow(row:Iterable):
    if not (isinstance(row, Iterable) and len(row)>=10):
      return None
    out = Startup()
    out.permalink = row[0]
    out.companyName = row[1]
    out.employeeCount = row[2]
    out.category = row[3]
    out.city = row[4]
    out.state = row[5]
    out.foundedDate = row[6]
    out.raisedAmount = row[7]
    out.raisedCurrency = row[8]
    out.round = row[9]
    out._superInit()
    return out


class FundingRaised:
  def readCsv(func):
    def _readCsv(*args, **kwargs):
      with open("../startup_funding.csv", "rt") as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='"')
        # skip header
        next(data)
        startupList:Iterable[Startup] = []
        for row in data:
          ele = Startup.readByCsvRow(row)
          if ele is not None:
            startupList.append(ele)
      result = func(*args, **kwargs, startupList=startupList)
      return result
    return _readCsv

  @staticmethod
  @readCsv
  def where(options = {}, startupList:Iterable[Startup] = []):
    options:Iterable[Tuple[str,str]] = list(options.items())
    result:Iterable[Startup] = []
    for row in startupList:
      rowItems = row.items()
      if all(option in rowItems for option in options):
        result.append(row)
    return result

  @staticmethod
  @readCsv
  def find_by(options, startupList:Iterable[Startup]=[]):
    options:Iterable[Tuple[str,str]] = list(options.items())
    for row in startupList:
      rowItems = row.items()
      if all(option in rowItems for option in options):
        return row
    raise RecordNotFound

class RecordNotFound(Exception):
  pass
