import ontologyTsv2Json
import json
import sys

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
                if numericInfo.strip() != "-":
                    citedDataEntity["numericInfo"] = numericInfo.strip().split(";")
                self.entities[citedDataIdentifier] = citedDataEntity
                
                # TODO docs are ignored - no entities created for them
                
                for datasetId in datasetIds.strip().split(";"):
                    entityIdentifier = self.toDatasetId(datasetId)
                    self.entities[entityIdentifier] = self.newEntity("", "dataset", [datasetId])
                    linkIdentifier = self.toLinkId(citedDataIdentifier, entityIdentifier)
                    # TODO relation not yet contained in gold standard
                    link = self.newLink(citedDataIdentifier, entityIdentifier)
                    self.links[linkIdentifier] = link
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
        return "citedData_" + reference.strip().replace(".", "").replace("/", "").replace("(", "").replace(")", "").replace(" ", "") + "_".join(numericInfo.split(";")).replace(".", "").replace("/", "").replace("(", "").replace(")", "").replace(" ", "")
        
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
