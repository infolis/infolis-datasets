import json
import sys
import goldstandardTsv2Json
import re

class OntoGoldConverter(goldstandardTsv2Json.GoldConverter):
    
    def linesToJson(self):
        for vals in self.getLine():
            if len(vals) != 5:
                sys.stderr.write("warning, don't know how to process line: '%s'. Ignoring\n" %str(vals))
                continue
                
            fromEntity, toEntity, inverseRelation, doi, annotation = vals
            if annotation == "incorrect":
                continue
              
            toEntityIdentifier = self.toDatasetId(doi)
            datasetIdentifiers = [doi]
            self.entities[toEntityIdentifier] = self.newEntity(toEntity, "dataset", datasetIdentifiers)
                    
            fromEntityIdentifier = self.toCitedDataId(fromEntity, "")
            self.entities[fromEntityIdentifier] = self.newEntity(fromEntity, "citedData")

                    
            linkIdentifier = self.toLinkId(fromEntityIdentifier, toEntityIdentifier)
            link = self.links.get(linkIdentifier, {})
            if not link:
                link = self.newLink(fromEntityIdentifier, toEntityIdentifier, [getInverseRelation(inverseRelation)])
            else:
                relations = link.get("entityRelations")
                relations.append(getInverseRelation(inverseRelation))
                link["entityRelations"] = relations
            self.links[linkIdentifier] = link
            
def getInverseRelation(relation):
    return re.sub("part(s)?", "superset", relation).replace("version_of", "superset_of_version")
    
             
if __name__=="__main__":
    converter = OntoGoldConverter(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(converter.toJson()) 
