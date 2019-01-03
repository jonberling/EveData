#!/usr/bin/env python3

import csv

TRITANIUM = 34
PYERITE   = 35
MEXALLON  = 36
ISOGEN    = 37
NOCXIUM   = 38
ZYDRINE   = 39
MEGACYTE  = 40
MORPHITE  = 11399

MINERALS_USED_IN_T1_PRODUCTION = [TRITANIUM, PYERITE, MEXALLON, ISOGEN, NOCXIUM, ZYDRINE, MEGACYTE]

def main():

  typeToName, typeToVolume, typeToPackedVolume, typeToMaterialsRequred = buildMaps()
  t1Types = getT1Types(typeToMaterialsRequred)

  print('Name,TypeId,Packaged Volume,Tritanium,Pyerite,Mexallon,Isogen,Nocxium,Zydrine,Megacyte')
  for typeId in t1Types:

    if typeId not in typeToName: continue

    output = [
      typeToName[typeId],
      typeId,
      typeToPackedVolume[typeId],
      typeToMaterialsRequred[typeId].setdefault(TRITANIUM, 0),
      typeToMaterialsRequred[typeId].setdefault(PYERITE, 0),
      typeToMaterialsRequred[typeId].setdefault(MEXALLON, 0),
      typeToMaterialsRequred[typeId].setdefault(ISOGEN, 0),
      typeToMaterialsRequred[typeId].setdefault(NOCXIUM, 0),
      typeToMaterialsRequred[typeId].setdefault(ZYDRINE, 0),
      typeToMaterialsRequred[typeId].setdefault(MEGACYTE, 0)
    ]

    print(','.join(map(str, output)))

def buildMaps():
  blueprintToMaterialsRequred = parseIndustryActivityMaterials()
  blueprintToProduct, blueprintToProductCount = parseIndustryActivityProducts()
  typeToName, typeToVolume = parseTypes()
  typeToPackedVolume = parseVolumes()

  typeToMaterialsRequred = buildMapTypeToMaterialsRequred(blueprintToProduct, blueprintToMaterialsRequred)
  typeToPackedVolume = buildCompletePackedVolume(typeToPackedVolume, typeToVolume)

  return typeToName, typeToVolume, typeToPackedVolume, typeToMaterialsRequred

def buildMapTypeToMaterialsRequred(blueprintToProduct, blueprintToMaterialsRequred):
  typeToMaterialsRequred = {}

  for blueprint, typeId in blueprintToProduct.items():
    if blueprint in blueprintToMaterialsRequred:
      typeToMaterialsRequred[typeId] = blueprintToMaterialsRequred[blueprint]

  return typeToMaterialsRequred

def buildCompletePackedVolume(typeToPackedVolume, typeToVolume):
  completeTypeToPackedVolume = typeToPackedVolume
  for typeId, volume in typeToVolume.items():
    if typeId not in typeToPackedVolume:
      completeTypeToPackedVolume[typeId] = volume

  return completeTypeToPackedVolume

def getT1Types(typeToMaterialsRequired):
  t1Types = []
  for typeId, mineralsRequred in typeToMaterialsRequired.items():
    t1 = True
    for mineral, amount in mineralsRequred.items():
      if mineral not in MINERALS_USED_IN_T1_PRODUCTION:
        t1 = False
        break
    if t1:
      t1Types.append(typeId)

  return t1Types

def parseVolumes():
  volumes = {}

  with open('static_db/invVolumes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    parsed_header = False
    for row in csv_reader:
      if not parsed_header:
        parsed_header = True
        continue

      typeId = int(row[0])
      volume = float(row[1])

      volumes[typeId] = volume

  return volumes

def parseTypes():
  names = {}
  volumes = {}

  with open('static_db/invTypes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    parsed_header = False
    for row in csv_reader:
      if not parsed_header:
        parsed_header = True
        continue

      typeId = int(row[0])
      name = row[2]
      volume = float(row[5])

      names[typeId] = name
      volumes[typeId] = volume

  return names, volumes

def parseIndustryActivityProducts():
  products = {}
  counts = {}

  with open('static_db/industryActivityProducts.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    parsed_header = False
    for row in csv_reader:
      if not parsed_header:
        parsed_header = True
        continue

      blueprintId = int(row[0])
      activity = int(row[1])
      productId = int(row[2])
      productCount = int(row[3])

      if activity == 1:
        products[blueprintId] = productId
        counts[blueprintId] = productCount

  return products, counts

def parseIndustryActivityMaterials():

  materials = {}

  with open('static_db/industryActivityMaterials.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    parsed_header = False
    for row in csv_reader:
      if not parsed_header:
        parsed_header = True
        continue

      blueprintId = int(row[0])
      activity = int(row[1])
      materialId = int(row[2])
      materialCount = int(row[3])

      if activity == 1:
        if blueprintId not in materials: materials[blueprintId] = {}
        materials[blueprintId][materialId] = materialCount

  return materials

if __name__ == "__main__":
  main()

