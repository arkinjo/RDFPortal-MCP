from pyrudof import Rudof, RudofConfig
rudof = Rudof(RudofConfig())

rudof.read_shex_str("""
prefix : <http://example.org/>
prefix xsd:    <http://www.w3.org/2001/XMLSchema#>

:Person {
 :name xsd:string
}
""")

rudof.read_data_str("""
prefix : <http://example.org/>

:ok :name "alice" .
:ko :name 1 .
""")

rudof.read_shapemap_str(":ok@:Person, :ko@:Person")

result = rudof.validate_shex()
print(result.show())
