#!/bin/bash
dataset="repwiki"
mkdir -p "$dataset/meta"

echoerr () {
    >&2 echo -e "\e[33;1mDEBUG\e[0m: $*"
}

grep-doi () {
    url="$1"
    curl -Ls "$url" \
        | grep -o 'http://dx.doi.org/[^"]*' \
        | sed 's,http://dx.doi.org/,,'
}

while read -r tsvline;do

    study=$(echo "$tsvline"|cut -d$'\t' -f1)
    wikititle=$(echo "$tsvline"|cut -d$'\t' -f2)
    url="http://replication.uni-goettingen.de/wiki/index.php/${wikititle// /_}"
    doi=$(grep-doi "$url"|head -n1)
    echoerr "'$doi' doi of '$wikititle'"
    journal_year=$(echo "$wikititle"|grep -o '([0-9A-Z: ]*)$'|sed 's/[()]//g')
    title=${wikititle:0:$(( ${#wikititle} - 3 - ${#journal_year} ))}
    journal=${journal_year%% *}
    year=${journal_year##* }
    > "$dataset/meta/${wikititle}.xml" echo "
<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>
<record>
<header>
    <identifier>doi:$doi</identifier>
</header>
<metadata>
<oai_dc:dc
    xmlns:dc=\"http://purl.org/dc/elements/1.1/\"
    xmlns:oai_dc=\"http://www.openarchives.org/OAI/2.0/oai_dc/\"
    xmlns:dcterms=\"http://purl.org/dc/terms/\"
    xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
    xsi:schemaLocation=\"http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd\" >
    <dc:title>$title</dc:title>
    <dc:date>$year</dc:date>
    <dc:citesStudy>$study</dc:citesStudy>
    <dcterms:bibliographicCitation>$journal</dcterms:bibliographicCitation>
    <dc:language>en</dc:language>
    <dc:identifier>http://doi.org/$doi</dc:identifier>
    <dc:creator>TODO 1</dc:creator>
    <dc:creator>TODO 2</dc:creator>
    <dc:subject>TODO 1</dc:subject>
    <dc:subject>TODO 2</dc:subject>
    <dc:subject>TODO 3</dc:subject>
</oai_dc:dc>
</metadata>
</record>
"

    # >&2 echo "DOI == '$doi'"
    # url=$(curl -sI "http://doi.org/$doi"|grep 'Location:'|sed 's,\x0d,,g'|grep -o 'http.*')
    # # >&2 echo "URL == '$url'"
    # # curl -vI "http://www-test.bib.uni-mannheim.de/infolis/zotero/?format=coins&url=$url"
done
