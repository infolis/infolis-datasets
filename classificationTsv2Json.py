import json
import sys
import ontologyTsv2Json
import codecs

class ClassifiConverter(ontologyTsv2Json.OntoConverter):
    
    def linesToJson(self):
        for vals in self.getLine():
            if len(vals) != 5:
                sys.stderr.write("warning, don't know how to process line: '%s'. Ignoring\n" %str(vals))
                continue
                
            toEntity, fromEntity, relation, doi, annotation = vals
            if annotation == "incorrect":
                continue
              
            entityIdentifier = self.toDatasetId(doi)
            datasetIdentifiers = [doi]
            self.entities[entityIdentifier] = self.newEntity(fromEntity, datasetIdentifiers)
                    
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
            
            
if __name__=="__main__":
    converter = ClassifiConverter(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        f.write(converter.toJson()) 
