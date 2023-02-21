import csv
from dataclasses import dataclass
from typing import Iterable, Tuple

class Startup(dict):

  @staticmethod
  def readByCsvRow(row:Iterable):
    if not (isinstance(row, Iterable) and len(row)>=10): return None
    out = Startup()
    out["permalink"] = row[0]
    out["company_name"] = row[1]
    out["number_employees"] = row[2]
    out["category"] = row[3]
    out["city"] = row[4]
    out["state"] = row[5]
    out["funded_date"] = row[6]
    out["raised_amount"] = row[7]
    out["raised_currency"] = row[8]
    out["round"] = row[9]
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
