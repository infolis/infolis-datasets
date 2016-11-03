import ontologyTsv2Json
import json
import sys
import re

class GoldConverter(ontologyTsv2Json.OntoConverter):

    def linesToJson(self):
        for vals in self.getLine():
            if len(vals) == 5:
                reference, numericInfo, docs, uncertain, datasetIds = vals
                
                # TODO enhance goldstandard to contain links for "kandidaten: ..." entries
                # for now, ignore them
                if datasetIds.strip().lower().startswith("kandidaten"):
                    continue
                
                citedDataIdentifier = self.toCitedDataId(reference, numericInfo)
                citedDataEntity = self.newEntity(reference, "citedData")
                if not numericInfo.strip() == "-":
                    citedDataEntity["numericInfo"] = re.split("\s*;\s*", numericInfo.strip())
                self.entities[citedDataIdentifier] = citedDataEntity
                    
                for datasetId in re.split("\s*;\s*", datasetIds.strip()):
                    if datasetId and not datasetId.strip() == "-":
                        entityIdentifier = self.toDatasetId(datasetId)
                        self.entities[entityIdentifier] = self.newEntity("", "dataset", [datasetId])
                        linkIdentifier = self.toLinkId(citedDataIdentifier, entityIdentifier)
                        # TODO relation not yet contained in gold standard
                        link = self.newLink(citedDataIdentifier, entityIdentifier)
                        self.links[linkIdentifier] = link
    
                # TODO docs are ignored - no entities created for them
                
            else:
                sys.stderr.write("warning, don't know how to process line: '%s'. Ignoring\n" %str(vals))
                
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
        return link 
        

if __name__=="__main__":
    converter = GoldConverter(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(converter.toJson())
