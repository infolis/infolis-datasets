import json
import sys

class OntoConverter:
    
    def __init__(self, tsv):
        self.tsv = tsv
        self.entities = {}
        self.links = {}

    def getLine(self):
        with open(self.tsv, "r") as f:
            lines = f.readlines()
        for i in range(len(lines)):
            if i > 0:
                yield lines[i].strip().split("\t")
            else:
                sys.stderr.write("Ignoring line '%s', assuming it contains the definitions of the fields\n" %lines[i])
   
    def linesToJson(self):
        for vals in self.getLine():
            if len(vals) == 5:
                toEntity, name, relation, evidence, doi = vals
                entityIdentifier = self.toDatasetId(doi)
                datasetIdentifiers = [doi]
                self.entities[entityIdentifier] = self.newEntity(name, datasetIdentifiers)
                    
                toEntityIdentifier = self.toDatasetId(toEntity)
                self.entities[toEntityIdentifier] = self.newEntity(toEntity)
                    
                linkIdentifier = self.toLinkId(entityIdentifier, toEntityIdentifier)
                link = self.links.get(linkIdentifier, {})
                if not link:
                    link = self.newLink(entityIdentifier, toEntityIdentifier, relation)
                else:
                    relations = link.get("entityRelations")
                    relations.append(relation)
                    link["entityRelations"] = relations
                self.links[linkIdentifier] = link
                    
            elif len(vals) == 3:
                toEntity, fromEntity, relation = vals
                toEntityIdentifier = self.toDatasetId(toEntity)
                fromEntityIdentifier = self.toDatasetId(fromEntity)
                linkIdentifier = self.toLinkId(fromEntityIdentifier, toEntityIdentifier)
                self.links[linkIdentifier] = self.newLink(fromEntityIdentifier, toEntityIdentifier, relation)
            else:
                sys.stderr.write("warning, don't know how to process line: '%s'. Ignoring\n" %str(vals))
                
    def toJson(self):
        obj = { "entity": {}, "entityLink": {} }
        self.linesToJson()
        for entity in self.entities.keys():
            obj.get("entity")[entity] = self.entities.get(entity)
        for link in self.links.keys():
            obj.get("entityLink")[link] = self.links.get(link)

        return json.dumps(obj, sort_keys=True, indent=4)
            
            
    def toDatasetId(self, string):
        return "dataset_" + string.replace(".", "").replace("/", "").replace("(", "").replace(")", "").replace(" ", "")
        
    def toLinkId(self, fromEntityIdentifier, toEntityIdentifier):
        return "entityLink_" + fromEntityIdentifier + "_" + toEntityIdentifier
        
    def newEntity(self, name, identifiers=""):
        entity = { "name": name, "tags": ["infolis-ontology"], "reliability": 1.0, "entityType": "dataset" }
        if identifiers:
            entity["identifiers"] = identifiers
        return entity
        
    def newLink(self, source, target, relation):
        return { "fromEntity": source, "toEntity": target, "entityRelations": [relation], "confidence": 1.0, "tags": ["infolis-ontology"] }
        

if __name__=="__main__":
    converter = OntoConverter(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(converter.toJson())
