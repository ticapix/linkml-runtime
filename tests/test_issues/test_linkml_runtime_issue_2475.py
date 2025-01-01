import dataclasses
from dataclasses import dataclass
import json
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper
from linkml_runtime.utils.metamodelcore import XSDDateTime
from linkml_runtime.utils.yamlutils import YAMLRoot, as_rdf
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.curienamespace import CurieNamespace
from rdflib import Graph, Literal, URIRef
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)
import unittest


schema_content = """
id: Literal2JsonLD
name: Literal2JsonLD
prefixes:
  ex: http://example.org/
  linkml: https://w3id.org/linkml/
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  vcard: http://www.w3.org/2006/vcard/ns#
default_prefix: ex
default_range: string
imports:
- linkml:types
classes:
  Person:
    class_uri: vcard:Individual
    slots:
      - comment
      - nickname
slots:
  comment:
    slot_uri: rdfs:comment
  nickname:
    slot_uri: vcard:nickname
"""


#
# below was generated with gen-python using the above schema
#

# Auto generated from Literal2JsonLD.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-01-01T22:37:07
# Schema: Literal2JsonLD
#
# id: Literal2JsonLD
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/


metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
EX = CurieNamespace('ex', 'http://example.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
VCARD = CurieNamespace('vcard', 'http://www.w3.org/2006/vcard/ns#')
DEFAULT_ = EX


# Types

# Class references


@dataclass(repr=False)
class Person(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = VCARD["Individual"]
    class_class_curie: ClassVar[str] = "vcard:Individual"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = EX.Person

    comment: Optional[str] = None
    nickname: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.comment is not None and not isinstance(self.comment, str):
            self.comment = str(self.comment)

        if self.nickname is not None and not isinstance(self.nickname, str):
            self.nickname = str(self.nickname)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass


slots.comment = Slot(uri=RDFS.comment, name="comment", curie=RDFS.curie('comment'),
                     model_uri=EX.comment, domain=None, range=Optional[str])

slots.nickname = Slot(uri=VCARD.nickname, name="nickname", curie=VCARD.curie('nickname'),
                      model_uri=EX.nickname, domain=None, range=Optional[str])

#
# below was generated with gen-jsonld-context using the above schema
#

context = {
    "comments": {
        "description": "Auto generated by LinkML jsonld context generator",
        "generation_date": "2025-01-01T23:08:58",
        "source": "Literal2JsonLD.yaml"
    },
    "@context": {
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "ex": "http://example.org/",
        "linkml": "https://w3id.org/linkml/",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "vcard": "http://www.w3.org/2006/vcard/ns#",
        "@vocab": "http://example.org/",
        "comment": {
            "@id": "rdfs:comment"
        },
        "nickname": {
            "@id": "vcard:nickname"
        },
        "Person": {
            "@id": "vcard:Individual"
        }
    }
}


#
# the tests start here
#


class TestConvertingRDFLibLiteral(unittest.TestCase):
    """
    See https://github.com/linkml/linkml/issues/2475
    """

    def setUp(self) -> None:
        self.schemaview = SchemaView(schema_content)
        self.person = Person(
            nickname=Literal("Bob", lang="en"),
            comment=Literal("Bob is <b>strong</b>", datatype=RDF.HTML))

    def _test_jsonld_has_tags(self, person: dict):
        self.assertIn('@type', person)
        self.assertIn(
            'http://www.w3.org/2006/vcard/ns#Individual', person['@type'])
        self.assertIn('http://www.w3.org/2000/01/rdf-schema#comment', person)
        self.assertIn({'@type': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML',
                      '@value': 'Bob is <b>strong</b>'}, person['http://www.w3.org/2000/01/rdf-schema#comment'])
        self.assertIn('http://www.w3.org/2006/vcard/ns#nickname', person)
        self.assertIn({'@language': 'en', '@value': 'Bob'},
                      person['http://www.w3.org/2006/vcard/ns#nickname'])

    def test_rdflib_dumper_with_schemaview(self):
        g = Graph()
        g += rdflib_dumper.as_rdf_graph(element=self.person,
                                        schemaview=self.schemaview)
        self.assertEqual(len(g), 3)
        jsonld = json.loads(g.serialize(format="json-ld"))
        print(jsonld)
        self.assertEqual(len(jsonld), 1)
        person = jsonld[0]
        self._test_jsonld_has_tags(person)

    def test_rdflib_dumper_with_context(self):
        g = Graph()
        g += as_rdf(self.person, contexts=context)
        self.assertEqual(len(g), 3)
        jsonld = json.loads(g.serialize(format="json-ld"))
        print(jsonld)
        self.assertEqual(len(jsonld), 1)
        person = jsonld[0]
        self._test_jsonld_has_tags(person)


if __name__ == "__main__":
    unittest.main()
