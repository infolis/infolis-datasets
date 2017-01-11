import ontologyTsv2Json
import json
import sys
import re
import os.path

class GoldConverter(ontologyTsv2Json.OntoConverter):

    def linesToJson(self):
        for vals in self.getLine():
            if len(vals) == 5:
                reference, numericInfo, docs, uncertain, datasetIds = vals
                
                if datasetIds.strip().lower().startswith("<") and datasetIds.strip().lower().endswith(".txt>"):
                    datasetIds = self.loadIdsFromMappingsFile(datasetIds.strip().replace("<", "").replace(">",""))
                
                citedDataIdentifier = self.toCitedDataId(reference, numericInfo)
                citedDataEntity = self.newEntity(reference, "citedData")
                if not numericInfo.strip() == "-":
                    citedDataEntity["numericInfo"] = re.split("\s*;\s*", numericInfo.strip())
                self.entities[citedDataIdentifier] = citedDataEntity
                    
                for datasetId in re.split("\s*;\s*", datasetIds.strip()):
                    if datasetId and not datasetId.strip() == "-":
                        idAndRelations = datasetId.split("@")
                        entityIdentifier = self.toDatasetId(idAndRelations[0])
                        self.entities[entityIdentifier] = self.newEntity("", "dataset", [idAndRelations[0]])
                        linkIdentifier = self.toLinkId(citedDataIdentifier, entityIdentifier)
                        if len(idAndRelations) > 1:
                            link = self.newLink(citedDataIdentifier, entityIdentifier, idAndRelations[1:])
                        else:
                            link = self.newLink(citedDataIdentifier, entityIdentifier)
                        self.links[linkIdentifier] = link
    
                # TODO docs are ignored - no entities created for them
                
            else:
                sys.stderr.write("warning, don't know how to process line: '%s'. Ignoring\n" %str(vals))
                
            
    def loadIdsFromMappingsFile(self, filename):
        mappingDir = "./datasets/goldstandard/mappings/"
        with open(os.path.join(mappingDir, filename), "r") as f:
            content = f.read()
        
        return ";".join(re.findall("10\.\S+", content))
        
            
    def toJson(self):
        obj = { "entity": {}, "entityLink": {} }
        self.linesToJson()
        for entity in self.entities.keys():
            obj.get("entity")[entity] = self.entities.get(entity)
        for link in self.links.keys():
            obj.get("entityLink")[link] = self.links.get(link)

        return json.dumps(obj, sort_keys=True, indent=4, ensure_ascii=False).decode('utf-8').encode('utf8')
            
    def toCitedDataId(self, reference, numericInfo):
        return "citedData_" + re.sub("\W", "", reference.strip() + "_".join(re.split("\s*;\s*", numericInfo.strip())))
        
    def newEntity(self, name, entityType, identifiers=""):
        entity = { "tags": ["infolis-goldstandard"], "reliability": 1.0, "entityType": entityType }
        if identifiers:
            entity["identifiers"] = identifiers
        if name:
            entity["name"] = name
        return entity
        
    def newLink(self, source, target, relations=[]):
        link = { "fromEntity": source, "toEntity": target, "confidence": 1.0, "tags": ["infolis-goldstandard"] }
        if relations:
            link["entityRelations"] = relations
        else:
            link["entityRelations"] = ["unknown"]
        return link 
        

if __name__=="__main__":
    converter = GoldConverter(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(converter.toJson())
