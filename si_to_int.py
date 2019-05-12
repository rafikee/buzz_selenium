def convert_si_to_number(num: str) -> float:
  try:
      return int(float(num)) 
  except ValueError:
      num, unit = num[:-1], num[-1]
      mapper = {"k": 1000, "m": 1000000, "b": 1000000000}
      return int(float(num) * mapper[unit.lower()])
