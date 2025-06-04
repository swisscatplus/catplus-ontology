from rdflib import Graph, Namespace, URIRef
import tempfile

# Define SHACL namespace
SH = Namespace("http://www.w3.org/ns/shacl#")

# Load the input ontology
g = Graph()
g.parse("ontology/catplus_ontology.ttl", format="turtle")

to_replace = []
for s, p, o in g.triples((None, SH.node, None)):
    to_replace.append((s, p, o))

for s, p, o in to_replace:
    g.remove((s, p, o))
    g.add((s, SH.term("notanode"), o))

insert_query = """
PREFIX sh: <http://www.w3.org/ns/shacl#>
INSERT {
  ?parentShape sh:node ?newNodeShape .
  ?newNodeShape a sh:NodeShape .
  ?newNodeShape sh:property ?innerPropertyShape .
  ?innerPropertyShape ?p ?o .
}
WHERE {
  ?parentShape sh:notanode ?anonShape .
  ?anonShape sh:property ?innerPropertyShape .
  ?innerPropertyShape sh:hasValue ?val ;
                      ?p ?o .
  FILTER(isIRI(?val))
  FILTER(isBlank(?anonShape))
  FILTER(isBlank(?innerPropertyShape))
  BIND(IRI(CONCAT(STR(?val), "Shape")) AS ?newNodeShape)
}
"""
g.update(insert_query)

# 3️⃣ DELETE the sh:notanode triples
delete_query = """
PREFIX sh: <http://www.w3.org/ns/shacl#>
DELETE {
  ?s sh:notanode ?something .
}
WHERE {
  ?s sh:notanode ?something .
}
"""
g.update(delete_query)

# 4️⃣ Save the enriched ontology to a tempfile
with tempfile.NamedTemporaryFile(delete=False, suffix=".ttl", mode="w") as tmpfile:
    enriched_file = tmpfile.name
    g.serialize(destination=tmpfile, format="turtle")
    print(enriched_file)  # This will output the path for downstream usage
