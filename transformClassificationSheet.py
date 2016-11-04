import sys
import re

def transform(source):
    annotations = []
    n = 0
    with open(source, "r") as f:
        for line in f.readlines():
            if n == 0:
                sys.stderr.write("Ignoring line '%s', assuming it contains the definitions of the fields\n" %line)
                n = 1
                continue
                
            fields = re.split("\t+", line.strip())
            study, dataset, relation, doi, annotation = ("", "", "", "", "")
            if len(fields) == 5:
                study, dataset, relation, doi, annotation = fields
            elif len(fields) == 4:
                study, dataset, relation, doi = fields
                annotation = "correct"
            else:
                sys.stderr.write("warning: cannot process line %s; ignoring." %line)
                continue
            
            if study == "Eurobarometer" and dataset.startswith("Flash"):
                annotations.append([study, dataset, relation, doi, "incorrect"])
            else:
                annotations.append([study, dataset, relation, doi, annotation])
    return annotations
                
def toDictionary(annotations):
    d = {}
    for annotation in annotations:
        vals = d.get(annotation[1] + "@" + annotation[3], [])
        vals.append(annotation)
        d[annotation[1] + "@" + annotation[3]] = vals
    return d
    
def addRelations(dictionary):
    for key in dictionary.keys():
        name = key.split("@")[0]
        if name.startswith("Candidate Countries Eurobarometer") or name.startswith("Applicant Countries Eurobarometer"):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "parts_of_spatial"
            dictionary[key].append(newAnno)
        elif re.match("Eurobarometer.*?((OVR)|(LAN))", name):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "part_of_supplement"
            dictionary[key].append(newAnno)
        elif re.match("(Candidate Countries )?Eurobarometer.*?:.*", name):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "part_of"
            dictionary[key].append(newAnno)
        elif re.match("Central and Eastern Eurobarometer.*?\(.*\)", name):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "part_of"
            dictionary[key].append(newAnno)
        elif name.startswith("German Social Survey (ALLBUS)") or name.startswith("German Election Study"):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "part_of_translation"
            dictionary[key].append(newAnno)
        elif name.startswith("Politbarometer (Kumulierter Datensatz, inkl. Kurzbarometer)"):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "part_of_supplement"
            dictionary[key].append(newAnno)
        elif name.startswith("Wahlstudie (Politbarometer)"):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "version_of"
            dictionary[key].append(newAnno)
        elif re.match("International Social Survey Programme:.*", name):
            newAnno = dictionary.get(key)[0][:]
            newAnno[2] = "part_of"
            dictionary[key].append(newAnno)
    return dictionary
    
def removeIncorrectPartOfs(dictionary):
    for key in dictionary.keys():
        parts_of, part_of, parts_of_spatial, part_of_spatial, parts_of_temporal, part_of_temporal = ([], [], [], [], [], [])
        
        for entry in dictionary.get(key):
            if entry[2] == "parts_of":
                parts_of = entry
            if entry[2] == "part_of":
                part_of = entry
            if entry[2] == "parts_of_spatial":
                parts_of_spatial = entry
            if entry[2] == "part_of_spatial":
                part_of_spatial = entry
            if entry[2] == "parts_of_temporal":
                parts_of_temporal = entry
            if entry[2] == "part_of_temporal":
                part_of_temporal = entry
           
        if parts_of and part_of:
            part_of[4] = "incorrect"
        if parts_of_spatial and part_of_spatial:
            part_of_spatial[4] = "incorrect"
        if parts_of_temporal and part_of_temporal:
            part_of_temporal[4] = "incorrect"
            
    return dictionary
    
def flattenDictionary(dictionary):
    l = []
    for entry in dictionary.values():
        try:
            l.append("\t".join(entry))
        except TypeError:
            for item in entry:
                l.append("\t".join(item))
    return l
            
if __name__=="__main__":
    with open(sys.argv[2], "w") as f:
        f.write("\n")
        for entry in flattenDictionary(removeIncorrectPartOfs(addRelations(toDictionary(transform(sys.argv[1]))))):
            f.write((entry + "\n").decode('utf-8').encode('utf-8'))
