// Neo4j import script generated from Day19 GraphRAG triples
// Safe to run multiple times because nodes and relationships use MERGE.

CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;

MERGE (s:Entity:Product {name: 'AWS'})
  ON CREATE SET s.type = 'Product'
MERGE (o:Entity:Product {name: 'Azure'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_005', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_005' THEN r.sources ELSE r.sources + ',' + 'doc_005' END;

MERGE (s:Entity:Product {name: 'AWS'})
  ON CREATE SET s.type = 'Product'
MERGE (o:Entity:Product {name: 'Google Cloud'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_005', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_005' THEN r.sources ELSE r.sources + ',' + 'doc_005' END;

MERGE (s:Entity:Company {name: 'Alphabet'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Sundar Pichai'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Alphabet'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Google'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:PARENT_OF]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Amazon'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Alexa'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_005', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_005' THEN r.sources ELSE r.sources + ',' + 'doc_005' END;

MERGE (s:Entity:Company {name: 'Amazon'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Andy Jassy'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_005', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_005' THEN r.sources ELSE r.sources + ',' + 'doc_005' END;

MERGE (s:Entity:Company {name: 'Amazon'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Seattle'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_005', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_005' THEN r.sources ELSE r.sources + ',' + 'doc_005' END;

MERGE (s:Entity:Company {name: 'Amazon'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Anthropic'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:INVESTS_IN]->(o)
  ON CREATE SET r.sources = 'doc_009', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_009' THEN r.sources ELSE r.sources + ',' + 'doc_009' END;

MERGE (s:Entity:Company {name: 'Amazon'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'AWS'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:OPERATES]->(o)
  ON CREATE SET r.sources = 'doc_005', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_005' THEN r.sources ELSE r.sources + ',' + 'doc_005' END;

MERGE (s:Entity:Company {name: 'Anthropic'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'OpenAI'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_009', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_009' THEN r.sources ELSE r.sources + ',' + 'doc_009' END;

MERGE (s:Entity:Company {name: 'Anthropic'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Claude'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_009', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_009' THEN r.sources ELSE r.sources + ',' + 'doc_009' END;

MERGE (s:Entity:Company {name: 'Anthropic'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Daniela Amodei'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_009', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_009' THEN r.sources ELSE r.sources + ',' + 'doc_009' END;

MERGE (s:Entity:Company {name: 'Anthropic'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Dario Amodei'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_009', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_009' THEN r.sources ELSE r.sources + ',' + 'doc_009' END;

MERGE (s:Entity:Company {name: 'Anthropic'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'San Francisco'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_009', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_009' THEN r.sources ELSE r.sources + ',' + 'doc_009' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Google'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'iOS'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'iPhone'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'macOS'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Steve Jobs'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Steve Wozniak'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Year {name: '1976'})
  ON CREATE SET o.type = 'Year'
MERGE (s)-[r:FOUNDED_IN]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Tim Cook'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Apple'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Cupertino'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_007', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_007' THEN r.sources ELSE r.sources + ',' + 'doc_007' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Microsoft'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'OpenAI'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Android'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Gemini'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Google Cloud'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Google Search'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Larry Page'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Sergey Brin'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Year {name: '1998'})
  ON CREATE SET o.type = 'Year'
MERGE (s)-[r:FOUNDED_IN]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Sundar Pichai'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Mountain View'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_003', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_003' THEN r.sources ELSE r.sources + ',' + 'doc_003' END;

MERGE (s:Entity:Company {name: 'Google'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Anthropic'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:INVESTS_IN]->(o)
  ON CREATE SET r.sources = 'doc_009', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_009' THEN r.sources ELSE r.sources + ',' + 'doc_009' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Red Hat'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:ACQUIRED]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Year {name: '2019'})
  ON CREATE SET o.type = 'Year'
MERGE (s)-[r:ACQUIRED_IN]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Red Hat OpenShift'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Watson'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Arvind Krishna'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Armonk'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Sector {name: 'artificial intelligence'})
  ON CREATE SET o.type = 'Sector'
MERGE (s)-[r:OPERATES_IN]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'IBM'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Sector {name: 'hybrid cloud'})
  ON CREATE SET o.type = 'Sector'
MERGE (s)-[r:OPERATES_IN]->(o)
  ON CREATE SET r.sources = 'doc_010', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_010' THEN r.sources ELSE r.sources + ',' + 'doc_010' END;

MERGE (s:Entity:Company {name: 'Meta'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'OpenAI'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_006', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_006' THEN r.sources ELSE r.sources + ',' + 'doc_006' END;

MERGE (s:Entity:Company {name: 'Meta'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Instagram'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_006', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_006' THEN r.sources ELSE r.sources + ',' + 'doc_006' END;

MERGE (s:Entity:Company {name: 'Meta'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Llama'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_006', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_006' THEN r.sources ELSE r.sources + ',' + 'doc_006' END;

MERGE (s:Entity:Company {name: 'Meta'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'WhatsApp'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_006', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_006' THEN r.sources ELSE r.sources + ',' + 'doc_006' END;

MERGE (s:Entity:Company {name: 'Meta'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Mark Zuckerberg'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_006', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_006' THEN r.sources ELSE r.sources + ',' + 'doc_006' END;

MERGE (s:Entity:Company {name: 'Meta'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Mark Zuckerberg'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_006', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_006' THEN r.sources ELSE r.sources + ',' + 'doc_006' END;

MERGE (s:Entity:Company {name: 'Meta'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Menlo Park'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_006', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_006' THEN r.sources ELSE r.sources + ',' + 'doc_006' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Azure'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_002', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_002' THEN r.sources ELSE r.sources + ',' + 'doc_002' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'GitHub Copilot'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_002', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_002' THEN r.sources ELSE r.sources + ',' + 'doc_002' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Satya Nadella'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_002', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_002' THEN r.sources ELSE r.sources + ',' + 'doc_002' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Redmond'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_002', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_002' THEN r.sources ELSE r.sources + ',' + 'doc_002' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'OpenAI'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:INVESTS_IN]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Sector {name: 'artificial intelligence'})
  ON CREATE SET o.type = 'Sector'
MERGE (s)-[r:OPERATES_IN]->(o)
  ON CREATE SET r.sources = 'doc_002', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_002' THEN r.sources ELSE r.sources + ',' + 'doc_002' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Sector {name: 'cloud computing'})
  ON CREATE SET o.type = 'Sector'
MERGE (s)-[r:OPERATES_IN]->(o)
  ON CREATE SET r.sources = 'doc_002', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_002' THEN r.sources ELSE r.sources + ',' + 'doc_002' END;

MERGE (s:Entity:Company {name: 'Microsoft'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'OpenAI'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:PARTNERS_WITH]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'CUDA'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'GPUs'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Jensen Huang'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Jensen Huang'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Santa Clara'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'AWS'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:PARTNERS_WITH]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Azure'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:PARTNERS_WITH]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'Nvidia'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Google Cloud'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:PARTNERS_WITH]->(o)
  ON CREATE SET r.sources = 'doc_004', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_004' THEN r.sources ELSE r.sources + ',' + 'doc_004' END;

MERGE (s:Entity:Company {name: 'OpenAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'ChatGPT'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'OpenAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'GPT models'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'OpenAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Elon Musk'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'OpenAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Greg Brockman'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'OpenAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Sam Altman'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'OpenAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Year {name: '2015'})
  ON CREATE SET o.type = 'Year'
MERGE (s)-[r:FOUNDED_IN]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'OpenAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'San Francisco'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_001', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_001' THEN r.sources ELSE r.sources + ',' + 'doc_001' END;

MERGE (s:Entity:Company {name: 'Tesla'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Elon Musk'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:HAS_CEO]->(o)
  ON CREATE SET r.sources = 'doc_008', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_008' THEN r.sources ELSE r.sources + ',' + 'doc_008' END;

MERGE (s:Entity:Company {name: 'Tesla'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Location {name: 'Austin'})
  ON CREATE SET o.type = 'Location'
MERGE (s)-[r:HEADQUARTERED_IN]->(o)
  ON CREATE SET r.sources = 'doc_008', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_008' THEN r.sources ELSE r.sources + ',' + 'doc_008' END;

MERGE (s:Entity:Company {name: 'xAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Anthropic'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_008', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_008' THEN r.sources ELSE r.sources + ',' + 'doc_008' END;

MERGE (s:Entity:Company {name: 'xAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'Google'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_008', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_008' THEN r.sources ELSE r.sources + ',' + 'doc_008' END;

MERGE (s:Entity:Company {name: 'xAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Company {name: 'OpenAI'})
  ON CREATE SET o.type = 'Company'
MERGE (s)-[r:COMPETES_WITH]->(o)
  ON CREATE SET r.sources = 'doc_008', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_008' THEN r.sources ELSE r.sources + ',' + 'doc_008' END;

MERGE (s:Entity:Company {name: 'xAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Product {name: 'Grok'})
  ON CREATE SET o.type = 'Product'
MERGE (s)-[r:DEVELOPS]->(o)
  ON CREATE SET r.sources = 'doc_008', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_008' THEN r.sources ELSE r.sources + ',' + 'doc_008' END;

MERGE (s:Entity:Company {name: 'xAI'})
  ON CREATE SET s.type = 'Company'
MERGE (o:Entity:Person {name: 'Elon Musk'})
  ON CREATE SET o.type = 'Person'
MERGE (s)-[r:FOUNDED_BY]->(o)
  ON CREATE SET r.sources = 'doc_008', r.confidence = 1.0
  ON MATCH SET r.sources = CASE WHEN r.sources CONTAINS 'doc_008' THEN r.sources ELSE r.sources + ',' + 'doc_008' END;
