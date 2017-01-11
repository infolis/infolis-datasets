import json
import urllib2
import sys

def getJson(filename):
    with open(filename, "r") as f:
        return json.load(f, "utf-8")
        
def getEntities(data):
    return data.get("entity")
    
def getLinks(data):
    return data.get("entityLink")
    
def getDatasetIds(entities):
    datasetIds = []
    for entityId in entities.keys():
        ids = entities.get(entityId).get("identifiers")
        if (ids):
            datasetIds.extend(ids)
    return set(datasetIds)
    
def getMetadata(datasetIds, fields):
    metadataMap = {}
    for datasetId in datasetIds:
        metadata = queryDara(datasetId)
        metadataMap[datasetId] = getDataForFields(metadata, fields)
    return metadataMap
    
def getDataForFields(metadata, fields):
    relevantData = {}
    completeData = metadata.get("response")
    for field in fields.items():
        content = removeEmpty(completeData.get("docs")[0].get(field[0]))
        if content:
            relevantData[field[1]] = content
    return relevantData
    
def removeEmpty(list):
    try:
        return [entry for entry in list if entry != ""]
    except TypeError:
        return []
    
def queryDara(datasetId):
    query = "http://www.da-ra.de/solr/dara/select/?q=doi:" + datasetId + "&wt=json"
    sys.stderr.write(query+"\n")
    return json.load(urllib2.urlopen(query))
    
def addMetadataToEntities(metadataMap, entities):
    for entityId in entities:
        entity = entities.get(entityId)
        if entity.get("identifiers"):
            for datasetId in entity.get("identifiers"):
                metadata = metadataMap.get(datasetId)
                if (metadata):
                    entity.update(metadata)
    return entities
    
def outputEnrichedJson(entities, links):
    enrichedData = {}
    enrichedData["entityLink"] = links
    enrichedData["entity"] = entities
    return json.dumps(enrichedData, sort_keys=True, indent=4, ensure_ascii=False).encode('utf8')

if __name__=="__main__":
    data = getJson(sys.argv[1])
    links = getLinks(data)
    entities = getEntities(data)
    relevantFields = {"geographicCoverage":"spatial_en", "temporalCoverage":"numericInfo", "currentVersion":"versionInfo"}
    enrichedEntities = addMetadataToEntities(getMetadata(getDatasetIds(entities), relevantFields), entities)
    with open(sys.argv[2], "w") as f:
        f.write(outputEnrichedJson(enrichedEntities, links))
    print "wrote " + sys.argv[2]
