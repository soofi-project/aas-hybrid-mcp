

Fachbereich 2 – Technik, Informatik und Wirtschaft
## Studiengang Informatik
Erschließung unstrukturierter Daten in
Verwaltungsschalen zur
agentenbasierten Informationsabfrage
## Bachelorarbeit
vorgelegt am 31.01.2026
von Remmet, Joshua
durchgeführt am Deutschen Forschungszentrum
für Künstliche Intelligenz (DFKI)
Betreuer (TH):Prof. Dr. rer. nat. Michael Schmidt
Betreuer (extern):    Mike Reichardt, DFKI Kaiserslautern
Angenommen als Bachelorarbeit
Bingen, den 31.01.2026Prof. Dr. rer. nat. Michael Schmidt

## Ehrenwörtliche Erklärung
Hiermit versichere ich, die vorliegende Arbeit ohne Hilfe Dritter und nur mit den an-
gegebenen Quellen und Hilfsmitteln angefertigt zu haben. Alle Stellen, die aus den
Quellen entnommen wurden, sind als solche kenntlich gemacht worden. Diese Ar-
beit hat in gleicher oder ähnlicher Form noch keiner Prüfungsbehörde vorgelegen.
Bingen, den 31.01.2026
## Joshua Remmet

Erklärung zu Eigentum und
## Urheberrecht
Hiermit erkläre ich mein Einverständnis, dass die Technische Hochschule Bingen
die vorliegende Abschlussarbeit den Studierenden und interessierten Dritten zur
Einsichtnahme zur Verfügung stellt und unter Nennung meines Namens (Urheber)
veröffentlichen darf.
Bingen, den 31.01.2026
## Joshua Remmet

## Abkürzungsverzeichnis
AAS  Asset Administration Shell.
ANN  Approximate Nearest Neighbor.
BM25  Best Matching 25.
HNSW  Hierarchical Navigable Small World.
IDTA  Industrial Digital Twin Association.
KG  Knowledge Graph.
KG-RAG  Knowledge Graph Retrieval-Augmented Generation.
KI  Künstliche Intelligenz.
LLM  Large Language Model.
LPG  Labeled Property Graph.
MCP  Model Context Protocol.
NLP  Natural Language Processing.
RAG  Retrieval-Augmented Generation.
RQL  Resource Query Language.
VDB  Vektordatenbank.
Vector-RAG  Vector Retrieval-Augmented Generation.
i

## Abbildungsverzeichnis
2.1   Darstellung einer AAS im AASX Explorer [1] .  .  .  .  .  .  .  .  .  .  .  .  .  .4
2.2   Darstellung des BaSyx-Web-UI .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .5
2.3   Darstellung eines Apache Kafka Systems  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .6
2.4   Darstellung von AAS in Neo4j    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .7
4.1   Systemarchitektur des AAS-Kafka-Neo4j-Connectors [2]  .  .  .  .  .  .  .   15
4.2   SME_UPDATED Event in Kafka   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   17
5.1   Zielarchitektur  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   21
5.2   Ablauf der Service-Pipeline  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   25
6.1   Systemarchitektur mit ausgewählten Komponenten  .  .  .  .  .  .  .  .  .  .   33
6.2   Flowchart eines Agentflows mit den Integrierten MCPs  .  .  .  .  .  .  .  .   35
A.1   Frage zu der maximalen Nutzlast .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   43
A.2   Frage zu der Nutzersteuerung   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   43
A.3   Frage zu den Laserscannern  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   44
A.4   Frage zu der maximalen Geschwindigkeit   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   44
A.5   Frage zu der Ladedauer .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   44
A.6   Frage zu den 3D-Kameras   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   45
A.7   Frage zu dem Einsatzbereich .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   45
A.8   Frage zu der Navigationskarte   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   45
A.9   Frage zu der maximalen Steigung   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   46
A.10 Frage zu der Sicherheitszone .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   46
A.11 Erster Neo4j MCP Aufruf   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   47
A.12 Zweiter Neo4j MCP Aufruf   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   48
A.13 Weaviate MCP Aufruf  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   49
ii

## Tabellenverzeichnis
4.1   Komponenten der Systemarchitektur zur Ereignisverarbeitung  .  .  .  .   16
4.2   Definition der Felder in einem Event   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   17
4.3   Analyse   der   architektonischen   Erweiterungsaspekte   und   deren
technische Voraussetzung   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   18
5.1   Merkmale der Split-Worker-Architektur .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   23
6.1   Vergleichsmatrix über Neo4J CE und Weaviate  .  .  .  .  .  .  .  .  .  .  .  .   30
7.1   Soll-Ist-Vergleich der Antwortkorrektheit  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   38
iii

## Inhaltsverzeichnis
## Abkürzungsverzeichnisi
## Abbildungsverzeichnisii
## Tabellenverzeichnisiii
## 1   Einleitung1
## 2   Grundlagen3
2.1   Asset Administration Shell   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .3
2.2   BaSyx   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .4
2.3   Apache Kafka  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .6
2.4   Neo4j .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .7
2.5   Embeddings  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .8
2.6   Vektordatenbanken   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .8
2.7   Chatbots  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .9
3   Stand der Wissenschaft10
3.1   Informationsabfrage aus strukturierten Daten der AAS   .  .  .  .  .  .  .  .   10
3.2   Informationsaufbereitung  aus  unstrukturierten  Daten  für  digitale
Zwillinge  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   11
3.3   Agentenbasierte Informationsanfrage aus heterogenen Daten  .  .  .  .   12
4   Analyse der bestehenden Architektur14
4.1   Architektur des AAS-Kafka-Neo4j Connectors  .  .  .  .  .  .  .  .  .  .  .  .  .   14
4.2   Event-Struktur  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   16
4.3   Analyse der Erweiterbarkeit .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   18
## 5   Konzept20
5.1   Anforderungen an die Systemarchitektur .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   20
5.2   Systemarchitektur  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   21
5.2.1    Funktionale Schichten und Komponenten   .  .  .  .  .  .  .  .  .  .  .   21
5.2.2    Strategische Abwägung der Worker-Anordnung  .  .  .  .  .  .  .  .   22
5.3   Datenmodell für Vektordatenbanken  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   23
5.3.1    Metadaten-Mapping und Kontext-Isolierung  .  .  .  .  .  .  .  .  .  .   23
5.3.2    Relationale Verknüpfung im KG-RAG    .  .  .  .  .  .  .  .  .  .  .  .  .   24
5.4   Erzeugung der Embeddings   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   24
iv

## Inhaltsverzeichnis
5.4.1    Die Service-Pipeline .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   24
5.4.2    Methodik der Ähnlichkeitsmessung .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   25
5.5   Synchronisationslogik  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   26
5.5.1    Idempotenz durch deterministische Identifikatoren   .  .  .  .  .  .   26
5.5.2    CUD-Mapping der AAS-Ereignisse  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   26
5.5.3    Agentische Orchestrierung mittels Model Context Protocol  .  .   27
## 6   Implementierung29
6.1   Komponentenauswahl .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   29
6.1.1    Auswahl der Vektordatenbank    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   29
6.1.2    Textextraktion mit Docling  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   31
6.1.3    Auswahl des Embedding-Modells .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   32
6.2   Erweiterung des Kafka-Connectors    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   32
6.2.1    Service-Architektur   .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   32
6.2.2    Implementierung der Idempotenz .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   33
6.3   Aufbau der Docker-Container  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   33
6.3.1    Container-Dienste  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   34
6.3.2    Konfiguration .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   34
6.4   Integration in Chatbot  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   34
6.4.1    Agentische Architektur mittels MCP   .  .  .  .  .  .  .  .  .  .  .  .  .  .   34
6.4.2    Hybrid-RAG Reasoning Loop  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   35
7   Evaluation der Funktionalität37
7.1   Methodische Erläuterung der Testfälle  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   37
7.2   Tabellarische Ergebnisauswertung  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   38
7.3   Analyse des agentenbasierten Abfrageprozesses .  .  .  .  .  .  .  .  .  .  .   39
8   Fazit und Ausblick40
8.1   Zusammenfassung der Arbeit .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   40
8.2   Ausblick auf zukünftige Entwicklungen  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .   41
## Anhang43
## Literaturverzeichnis50
## Digitaler Anhang54
v

## 1  Einleitung
Moderne Industrie-4.0-Umgebungen basieren auf dem Konzept der Digitalen Zwil-
linge [3]. Dieses sieht eine umfassende digitale Vernetzung physischer Komponen-
ten vor. Dabei verschmelzen die Informationstechnik und die Produktion mitein-
ander. In diesen Umgebungen liegen große Mengen an Daten in unstrukturierter
Form vor. Diese Daten spielen eine zentrale Rolle für die Bedienung der Syste-
me. Besonders technische Dokumentationen und Datenblätter sind hier wichtig,
da sie essenzielle Informationen über Anlagen und Komponenten enthalten. In ei-
ner intelligenten Fabrik dienen diese unstrukturierten Texte als Wissensbasis. Sie
helfen dabei, Ausfallzeiten zu minimieren. Zudem unterstützen sie die dezentrale
## Entscheidungsfindung.
Trotz dieser zentralen Bedeutung zeigt sich in der aktuellen Praxis eine deutliche
technologische Lücke. Während strukturierte Daten innerhalb der Asset Adminis-
tration  Shell  (AAS)  bereits  effizient  verwaltet  werden,  bleiben  die  darin  referen-
zierten unstrukturierten Dokumente für automatisierte Systeme weitgehend uner-
schlossen. Der Informationen dieser Dokumente bleibt oft unberücksichtigt, was
dazu führt, dass Anwender relevante technische Informationen nicht über digita-
le Schnittstellen abrufen können, sondern diese weiterhin manuell suchen müs-
sen. Ein typisches Szenario stellt hierbei die Wartung dar: Erblickt ein Mitarbeiter
beispielsweise einen rot leuchtenden mobilen Roboter des Typs MiR100, muss er
zunächst das entsprechende Nutzerhandbuch händisch heraussuchen und die Do-
kumentation nach der Bedeutung des Fehlercodes durchsuchen. Diese Form der
Informationsbeschaffung mindert die Effizienz der dezentralen Entscheidungsfin-
dung erheblich und schränkt die Nutzbarkeit der AAS ein.
Das Ziel der vorliegenden Bachelorarbeit besteht daher darin, ein technisches
Konzept  zu  entwickeln,  welches  die  automatisierte  Erschließung  von  unstruktu-
rierten  Dokumenten  innerhalb  der  AAS  ermöglicht,  um  Anwendern  über  einen
Chatbot schnelle und präzise Antworten auf komplexe Fragen zu liefern. Hierbei
werden die Inhalte mittels moderner Embedding-Modelle verarbeitet und in einer
VDB gespeichert, wobei eine konsistente Verknüpfung zwischen dem strukturier-
ten Knowledge Graph (KG) und den semantischen Vektordaten gewahrt bleibt. Die
Untersuchung zeigt auf, wie diese Integration technisch realisiert werden muss,
um die Daten im Sinne eines hybriden Retrieval-Ansatzes für den Chatbot nutz-
bar zu machen. Zur praktischen Umsetzung dieses Konzepts wird der bestehende
AAS-Kafka-Neo4j-Connector als technologische Basis herangezogen und entspre-
chend erweitert.
## 1

## 1  Einleitung
Die  Arbeit  analysiert  hierzu  die  bestehende  Infrastruktur,  entwirft  eine  Zielar-
chitektur und setzt diese im Rahmen eines Prototyp-Ansatzes praktisch um. Zur
Realisierung  dient  die  Entwicklung  eines  „Proof-of-Concepts“,  der  eine  automa-
tisierte Service-Pipeline implementiert. Dabei werden geeignete Frameworks für
die  strukturierte  Textextraktion,  eine  VDB  evaluiert  und  integriert.  Abschließend
validiert eine systematische Evaluation anhand eines realitätsnahen Szenarios mit
dem mobilen Roboter MiR100 die Funktionalität des Gesamtsystems, wobei die
Antwortkorrektheit des entwickelten Chatbots mittels definierter Testfälle überprüft
wird.
Der  Aufbau  der  Arbeit  gliedert  sich  in  acht  Kapitel,  die  den  Prozess  von  der
theoretischen Basis bis zur praktischen Auswertung abbilden. In Kapitel 2 „Grund-
lagen“ die wesentlichen technologischen Bausteine erläutert, wozu neben der AAS
und  BaSyx  auch  Apache  Kafka,  die  Graphdatenbank  Neo4j  sowie  die  Konzep-
te von Embeddings und VDBs gehören. Kapitel 3 „Stand der Wissenschaft“ bie-
tet einen Überblick über aktuelle Forschungsansätze zur Informationsabfrage aus
strukturierten AAS-Daten sowie Methoden zur Aufbereitung unstrukturierter Da-
ten für digitale Zwillinge. In Kapitel 4 „Analyse der bestehenden Architektur“ wird
das Fundament des bestehenden Connectors sowie dessen Event-Struktur detail-
liert untersucht, um die Anforderungen für die Erweiterung zu definieren. Kapitel
5 „Konzept“ widmet sich dem Entwurf des hybriden Systems, wobei insbesondere
die strategische Abwägung der Worker-Anordnung und die Synchronisationslogik
im Fokus stehen. Die technische Umsetzung des Prototyps wird in Kapitel 6 „Imple-
mentierung“ beschrieben, was die Komponentenauswahl, die Service-Architektur
und die Integration in den agentenbasierten Chatbot umfasst. In Kapitel 7 „Evalua-
tion der Funktionalität“ wird die Funktionalität des Systems anhand von Testfälle
methodisch geprüft und tabellarisch ausgewertet. Abschließend erfolgt in Kapitel 8
„Fazit und Ausblick“ eine Zusammenfassung der Ergebnisse sowie eine Diskussion
potenzieller zukünftiger Entwicklungen.
## 2

## 2  Grundlagen
Die Realisierung industrieller Digitalisierungsvorhaben erfordert eine präzise Ab-
stimmung  zwischen  standardisierten  Informationsmodellen  und  der  darunterlie-
genden technologischen Infrastruktur. Um das spätere Konzept auf einer einheit-
lichen Basis aufzubauen, werden im Folgenden die theoretischen Rahmenbedin-
gungen definiert. Dies schafft die notwendige Grundlage, um das Zusammenwir-
ken von digitaler Repräsentation, Datenfluss und moderner Informationsverarbei-
tung im Kontext der vorliegenden Arbeit einzuordnen.
## 2.1  Asset Administration Shell
Die AAS ist ein standardisiertes Format der Industrial Digital Twin Association (ID-
TA), um eine digitale Repräsentation einer Komponente im Kontext von Industrie-
4.0 zu ermöglichen [4].
Dabei beschreibt der digitale Zwilling das übergeordnete Konzept der virtuellen
Abbildung eines Assets, während die AAS die konkrete technologische Implemen-
tierung darstellt, welche die Interoperabilität und den Datenaustausch erst ermög-
licht.  Sie  dient  dazu,  Informationen  eines  Assets  strukturiert  darzustellen.  Dazu
gehören Eigenschaften, Statusmeldung, Messdaten und Fähigkeiten. Die Struktur
einer AAS basiert dabei auf einem technologieunabhängigen Meta-Modell, wel-
ches die logische Organisation der Information festlegt und durch Serialisierungs-
zuordnungen wie XML oder JSON die herstellerübergreifende Interoperabilität si-
cherstellt. [5] Für den dateibasierten Austausch dient das standardisierte AASX-
Paketformat, welcher die Serialisierungen zusammen mit zugehörigen Dokumen-
ten in einer transportablen Datei bündelt [6].
Die Gliederung der AAS wird in Abbildung 2.1 deutlich. An oberster Stelle steht
die AAS als digitaler Repräsentant, die alle zugehörigen Informationen bündelt.
Darunter ist das Submodell Identification angeordnet, welches Merkmale des As-
sets im digitalen Raum speichert. Der Inhalt der AAS ist durch Submodellvorlagen
beschrieben, wodurch eine konsistente und wiederverwendbare Datenstruktur ge-
währleistet wird. [7]
In Abbildung 2.1 wird dies durch das Submodell Identification verdeutlicht, wel-
ches spezifische Merkmale wie den Herstellernamen, die Produktbezeichnung und
die Software-Revision in Form von Properties bündelt. Ergänzend dazu definiert
das Submodell „Handover Documentation“ [8] einen standardisierten Rahmen für
die Bereitstellung technischer Dokumente. Es legt die notwendigen Strukturen fest,
## 3

## 2  Grundlagen
um Dokumentationen wie Betriebsanleitungen oder Zertifikate maschinenlesbar in
die AAS zu integrieren und somit für automatisierte Prozesse zugänglich zu ma-
chen. [8] Die Informationen einer AAS werden während des gesamten Lebens-
zyklus eines Assets aktualisiert, wodurch Anwendungen jederzeit auf konsistente
und aktuelle Daten zugreifen können, was die Effizienz, Nachverfolgbarkeit und
Integration von Industrie-4.0-Systemen erheblich verbessert [4].
Abbildung 2.1: Darstellung einer AAS im AASX Explorer [1]
2.2  BaSyx
BaSyx ist eine Open-Source-Plattform, die als Middleware fungiert und die Digita-
lisierung von Produktionsumgebung unterstützt. Im Zentrum von BaSyx steht die
Implementierung der AAS. Die Plattform stellt Komponenten und SDKs zur Verfü-
gung, welche die Entwicklung und Einsatz erleichtern. [9] Abbildung 2.2 zeigt die
Web-Benutzeroberfläche von BaSyx, in der die geladenen AAS zentral verwaltet
werden.
Ein wesentlicher Aspekt von BaSyx ist die Digitalisierung von Produktionspro-
zessen. Dies ermöglicht es, Produktionsdaten und Funktionalität der Maschine in
AAS zu speichern. In Abbildung 2.2 der Weboberfläche wird diese Struktur deut-
lich. Links werden alle aktuell verfügbaren AAS aufgelistet, was ein Management
## 4

## 2  Grundlagen
mehrerer Assets ermöglicht. In der mittleren Spalte wird die Struktur der ausge-
wählten AAS mit ihren Submodellen und Elementen aufgezeigt. Wählt der Nutzer
ein spezifisches Element aus, werden in der rechten Spalte die detaillierten In-
halte und Informationen, wie zum Beispiel hinterlegte Dokumente oder technische
Parameter, angezeigt. BaSyx bietet Registry, Repository, Dashboards, Visualisie-
rungsmöglichkeiten und außerdem Komponenten, um reale Geräte mit ihrem di-
gitalen Zwilling zu verbinden. Durch diese Funktionalitäten entsteht ein virtuelles
Modell, was die Analyse und Automatisierung unterstützt. [10] Anwendungsnahe
Werkzeuge  ermöglichen  eine  Echtzeit-Datenanalyse  und  die  Überwachung  von
## Datenströmen [11].
MiR100-0
ѓ઴દǙ
## Identification
## ͝
## ݰ
## Submodel
## Ǚ
AssetType
## Ȯ
## Property
## Ǚ
ManufacturerN...
## Ȯ
## Property
## Ǚ
ManufacturerId
## Ȯ
## Property
## Ǚ
ManufacturerPr...
## Ȯ
## Property
## Ǚ
ManufacturerPr...
## Ȯ
## Property
## Ǚ
ManufacturerPr...
## Ȯ
## Property
## Ǚ
ProductNumber
## Ȯ
## Property
## Ǚ
ManufacturerPr...
## Ȯ
## Property
## Ǚ
ClassificationS...
## Ȯ
## Property
## Ǚ
## Manufacturing...
## Ȯ
## Property
## Ǚ
DeviceRevision
## Ȯ
## Property
## Ǚ
SoftwareRevisi...
## Ȯ
## Property
## Ǚ
HardwareRevisi...
## Ȯ
## Property
## Ǚ
## URL
## Ȯ
## Property
## Ǚ
SupplierName
## Ȯ
## Property
## Ǚ
TypClass
## Ȯ
## Property
## Ǚ
ClassificationS...
## Ȯ
## Property
## Ǚ
InstanceId
## Ȯ
## Property
## Ǚ
TypeThumbnail
## Ȯ
## File
## Ǚ
## Documentation
## Ȯ
## File
## Ǚ
## ELEMENT DETAILS
## ෎
## VISUALIZATION
## ட
## Documentation
## File
ID short:
## Documentation
## Path:
Mime Type: ...DOWNLOAD FILE
aHR0cDovL2Fhcy5kZm
## Ւ
## Ϣ
## UPLOAD FILE
Last sync:2026-01-27 14:26:16
j
## ஹ஺
## 2026-01-27 14:26:15
ѓ
## 2 Shells
Search for AAS...
## Ǚ
MiR100-0
http://aas.dfki.de/ids/aas/evaluation/m...
## Ǚ
mir100_type_aas
http://aas.dfki.de/ids/aas/mir100_type
## Ǚ
j
http://aas.dfki.de/ids/asset/mir100
## Instance
Global Asset ID:
http://aas.dfki.de/ids/asset/mir100_0
MiR100-0
## AAS
Identification (ID):
http://aas.dfki.de/ids/aas/evaluation/mir100_10000...
ID short:
mir100_0_aas
DisplayName:
MiR100-0en
## Administrative Information
l·
## Close Sidebar
## Ľ
2026 — Eclipse BaSyx™ ©
## ڡ
AAS Editor
l·
## AUTO SYNC:OFF
l·
ғᙱ
Abbildung 2.2: Darstellung des BaSyx-Web-UI
## 5

## 2  Grundlagen
## 2.3  Apache Kafka
## Apache Kafka
## Producer
## Producer
## Topic
## Partition
## Partition
## Partition
## Partition
## Consumer
## Consumer
## Consumer
## Topic
## Partition
## Partition
## Partition
## Partition
Abbildung 2.3: Darstellung eines Apache Kafka Systems
Apache  Kafka  ist  ein  verteiltes  Publish-Subscribe-Messaging-System  zur  Verar-
beitung von Ereignisdaten [12]. Kafka ist auf hohen Datendurchsatz und Skalier-
barkeit ausgelegt [13]. Die grundlegende Architektur und das Zusammenspiel der
Komponenten innerhalb eines Apache Kafka Brokers sind in Abbildung 2.3 illus-
triert. Daten werden in Topics organisiert und intern in Partitionen aufgeteilt. Ei-
ne  Nachricht  ist  die  kleinste  Dateneinheit,  die  in  einem  Topic  gespeichert  wird.
Nachrichten werden von Erzeugern (Producer) in Topics geschrieben, welche von
Verbrauchern (Consumer) sequentiell gelesen werden. Sie bestehen aus einem
Schlüssel (Key), einem Wert (Value), der die eigentliche Nutzlast enthält und ei-
nem Zeitstempel. [14]
Nachrichten können durch die Partitionierung auf mehrere Vermittler (Broker)
verteilt und parallel bearbeitet werden, was eine horizontale Skalierung ermöglicht.
Replikationen zwischen Brokern stellen eine hohe Ausfallsicherheit her [15]. Durch
diese  Eigenschaften  eignet  sich  Kafka  ideal  für  Ereignis-Streaming  und  Daten-
Pipelines,  bei  denen  Daten  aus  verschiedenen  Quellen  erfasst  werden  können
und  an  mehrere  Consumer  weitergeleitet  werden.  Über  Kafka  Connect  Plugins
lassen  sich  externe  Systeme  wie  Datenbanken  integrieren.  Durch  das  robuste
Replikations- und Partitionierungsmodell stellt Kafka eine zuverlässige Plattform
für Streaming-Anwendungen im großen Maßstab dar. [16]
## 6

## 2  Grundlagen
## 2.4  Neo4j
Instance:neo4j://localhost:7687Database:neo4jUser:-
Go back to old Browser
## $
## $
neo4j$
## :welcome
## GUIDE
Learn what's new in this
preview
Take a quick tour of this preview to
learn about the latest features to
help you be productive.
## DATASET
Try Neo4j with the Movie
## Graph
Dive into a fully-built graph
example to kickstart your Neo4j
journey. Discover key query
patterns through a fun, familiar
world of actors and films.
Share your feedback
Help us improve the new Browser!
Let us know what's working well
and what could be better.
Send feedback
## :connect
Connected to neo4j://localhost:7687
Database information
## Nodes (281)
## Relationships (377)
Property keys
Last update: 13:38:47
*AnnotatedRelationshipEl...Asset
AssetAdministrationShellBasicEventElement
BlobCapabilityDataElementEntity
EventElementFileIdentifiable
MultiLanguagePropertyOperationProperty
RangeReferableReferenceElement
RelationshipElementSemanticConcept
SubmodelSubmodelElement
SubmodelElementCollec...
SubmodelElementList
assetKindassetTypeididShort
idShortPathnameregistrationTimesmId
sourceUrltypevalue
## *HAS_ASSETHAS_ELEMENT
## HAS_REFERENCEHAS_SEMANTIC
## HAS_SUBMODEL
neo4j$MATCH p=()-[]->() RETURN p LIMIT 25;
Started streaming 25 records after 121 ms and completed after 173 ms.
GraphTableRAW
Abbildung 2.4: Darstellung von AAS in Neo4j
Neo4j ist eine Graphdatenbank, die das Property-Graph-Modell nutzt. Daten wer-
den als Knoten (Entitäten) und Kanten (Beziehungen) gespeichert, wobei Knoten
beliebig viele Key-Value-Paare tragen können. Die Struktur ist flexibel erweiterbar,
da jeder Knoten oder Kante eigene Labels und Properties besitzen kann. [17]
Verfügen die Knoten und Kanten eines solchen Graphen über typisierte Labels,
spricht man von einem Labeled Property Graph (LPG). In Abbildung 2.4 wird diese
Semantik durch die Beschriftung der Kanten deutlich. Die Beziehungen sind expli-
zit als „HAS_ELEMENT“ oder „HAS_SEMANTIC“ definiert, was die Art der Verbin-
dung zwischen den Objekten direkt im Datenmodell festlegt. Neo4j erlaubt außer-
dem, dass tabellarisch organisierte Datenbestände direkt als Graphen abgebildet
werden können. Dadurch ist die semantische Lücke zwischen der konzeptionellen
Modellierung und der Speicherung in der Graphdatenbank minimal. [18]
Während eine solche Überführung konzeptionell systemunabhängig möglich ist,
## 7

## 2  Grundlagen
bietet Neo4j hierfür spezialisierte, teils automatisierte Migrationswerkzeuge an. Um
Abfragen an die Datenbank zu stellen, wird die Abfragesprache Cypher verwendet,
die speziell für Abfragen auf Pfade und Subgraphen entwickelt wurde. Das graph-
orientierte Modell bietet insbesondere bei Daten mit vielen oder rekursiven Bezie-
hungen signifikante Vorteile: Da keine aufwändigen JOIN-Operationen notwendig
sind, erfolgt die Traversierung von Kanten selbst in tiefen Hierarchien effizient. [19]
## 2.5  Embeddings
Embeddings sind Vektordarstellungen von beispielsweise einem Text oder einem
Bild. Diese überführen semantische oder inhaltliche Informationen in einen kontinu-
ierlichen Vektorraum. Diese Repräsentationen werden von Embedding-Modellen
erzeugt, indem Eingabedaten so transformiert werden, dass die einzelnen Dimen-
sionen des Vektors spezifische Merkmale der Bedeutung kodieren. [20]
Moderne Modelle erzeugen dabei kontextuelle Embeddings, welche die Bedeu-
tung eines Wortes in Abhängigkeit von seinem jeweiligen Satzkontext abbilden. Die
Anordnung in diesem Vektorraum ermöglicht es, den Grad der Verwandtschaft zwi-
schen  verschiedenen  Eingaben  durch  Ähnlichkeitsmessungen  zu  quantifizieren.
Während semantisch ähnliche Eingaben zu nahe beieinander liegenden Vektoren
führen, resultieren inhaltliche Unterschiede in entsprechend größeren Distanzen.
Diese Eigenschaft bildet die Grundlage für moderne KI-Anwendungen, da sie das
effiziente Auffinden relevanter Textpassagen auf Basis ihrer Bedeutung statt reiner
Keyword-Übereinstimmungen ermöglicht. [21]
## 2.6  Vektordatenbanken
Eine Vektordatenbank (VDB) ist ein Datenbanksystem, speziell zum Speichern von
Datenobjekten zusammen mit ihren Vektorembeddings. Ein solches Datenobjekt
kann zum Beispiel ein Text oder ein Bild sein. Eine solche Datenbank ermöglicht
es, basierend auf diesen Vektoren ähnliche Objekte schneller in großen Datenmen-
gen zu finden. Die Ähnlichkeit wird dabei nicht über exakte Zeichenfolgen definiert,
sondern über die mathematische Distanz im Vektorraum und spezielle Indexstruk-
turen. Die Datenbank indiziert das Dokument zusammen mit den Embeddings in
einer spezialisierten Architektur. Im Gegensatz zu herkömmlichen Datenbanken,
die Daten meist in Zeilen und Spalten organisieren, verwalten VDBs diese hochdi-
mensionalen Vektoren. Bei einer Suchabfrage wird der Suchbegriff zunächst durch
dasselbe Embedding-Modell in einen Vektor umgewandelt. Um die Effizienz bei der
Verarbeitung großer Datenmengen sicherzustellen, nutzen VDBs Algorithmen für
## 8

## 2  Grundlagen
die die Suche wie den Approximate Nearest Neighbor (ANN). Diese begrenzen
die Suche gezielt auf eine relevante Teilmenge des Vektorraums und identifizieren
über die mathematische Distanz diejenigen Dokumentvektoren mit der größten se-
mantischen Übereinstimmung. Dies ermöglicht eine massive Beschleunigung bei
minimalem Präzisionsverlust.
Durch diese Fähigkeit zur schnellen Ähnlichkeitssuche bilden VDBs das techno-
logische Rückgrat für Retrieval-Augmented Generation (RAG) [21]. Hierbei fungiert
die Datenbank als Wissensarchiv, das einem LLM gezielt relevante Informationen
aus unstrukturierten Datenquellen zuliefert. [21] Die hier beschriebene Möglichkeit
nach semantischen Vergleichen zu suchen, erfordert zuverlässige und skalierba-
re VDB-Systeme und bildet die Grundlage für moderne Anwendungen wie LLM
basierte Chatbots [22].
## 2.7  Chatbots
Chatbots sind Computerprogramme, die menschliche Konversationen simulieren
und  Anfragen  in  natürlicher  Sprache  beantworten.  Nicht  alle  Chatbots  basieren
auf KI-Modellen. Allerdings nutzen moderne Chatbots zunehmend KI-Techniken,
wie Natural Language Processing (NLP) um Nutzeranfragen zu verstehen und au-
tomatisiert zu antworten. [23]
Diese  Chatbots  basieren  auf  komplexen  KI-Modellen  und  generativer  KI.  Sie
können LLMs verwenden, um verschiedenste Aufgaben zu erfüllen. Ein Chatbot-
System besteht in der Regel aus Komponenten zur Texteingabe, NLP-Analyse und
einer Antwortgenerierung. Sie verfügen ebenfalls über Mechanismen, um aus Nut-
zerinteraktionen zu lernen und mit steigender Datenbasis ihre Antworten zu ver-
bessern. [24]
## 9

3  Stand der Wissenschaft
Die Nutzbarmachung der AAS als zentrale Informationsquelle erfordert Verfahren,
die über die reine Bereitstellung von Datenmodellen hinausgehen. In der wissen-
schaftlichen Diskussion steht zunehmend die Frage im Vordergrund, wie die se-
mantische Tiefe strukturierter Metamodelle mit der Flexibilität unstrukturierter Do-
kumentationsdaten technisch sinnvoll verknüpft werden kann. Die Betrachtung ak-
tueller  Forschungsansätze  verdeutlicht  hierbei  die  Notwendigkeit,  automatisierte
Mechanismen  für  den  Informationsabruf  zu  entwickeln,  die  den  manuellen  Auf-
wand bei der Informationsabfragen reduzieren. Diese Analyse liefert den notwen-
digen Kontext, um bestehende Grenzen bei der Abfrage heterogener Datenquel-
len zu identifizieren und die technologische Reife heutiger Abfrage-Architekturen
sowie agentenbasierter Systeme zu bewerten. Damit bildet der wissenschaftliche
Überblick den Referenzpunkt für die Einordnung der in dieser Arbeit entwickelten
## Lösungsansätze.
3.1  Informationsabfrage aus strukturierten Daten
der AAS
Die AAS stellt strukturierte Informationen über Assets bereit und bildet damit ei-
ne zentrale Grundlage für Anwendungen im Kontext von Industrie 4.0. Die IDTA-
Spezifikation definiert die Struktur der AAS einschließlich Metamodelle, Submo-
delle und Properties sowie die Serialisierungsformate JSON oder XML, in denen
die Daten bereitgestellt werden. [25]
Ein  Ansatz  zur  Abfrage  von  strukturierten  AAS-Daten  bietet  der  AAS-Kafka-
Neo4j-Connector. Dieser überführt die Daten in einen Property-Graph und spei-
chert diesen in einer Graphdatenbank. Dabei werden Hierarchien und Referen-
zen explizit als Knoten und Kanten modelliert. Die Informationsabfrage selbst er-
folgt durch einen KI-Agenten, der als „Proof-of-Concept“ implementiert wurde und
auf die Graphdatenbank zugreift. Dieser Agent nutzt das Model Context Protocol
(MCP) [26], um Benutzereingaben in Cypher-Abfragen zu übersetzen und die Da-
ten damit abzurufen. Durch die Synchronisation über Apache Kafka bleiben die
Daten innerhalb der Graphdatenbank stets aktuell, wodurch der Agent auf Ände-
rungen in den AAS-Daten unmittelbar zugreifen kann. Dieses Vorgehen bietet eine
Schnittstelle, wodurch Anwender Informationen aus AAS abgerufen können, oh-
ne die oft aufwendige und unübersichtliche Navigation durch die hierarchischen
Dokumentstrukturen der AAS. [2]
## 10

3  Stand der Wissenschaft
Ein anderer Ansatz ist die standardisierte AAS Query Language. Diese Sprache
zielt primär darauf ab, den Bandbreitenbedarf und den Verarbeitungsaufwand bei
der Kommunikation zwischen Client und Server zu minimieren, indem nur relevan-
te Objekte übertragen werden. Sie bietet eine protokollunabhängige Grammatik,
die auf der „Resource Query Language (RQL)“ [27] basiert und einen konsisten-
ten Datenzugriff über verschiedene Technologie-Mappings hinweg gewährleistet.
Durch die Nutzung spezifischer Feldidentifikatoren wie $aas, $sm oder $sme kön-
nen  hierarchische  Strukturen  der  AAS  gezielt  gefiltert  werden,  wobei  komplexe
Kriterien mittels logischer Operatoren und regulärer Ausdrücke definiert werden
können. Die Sprache adressiert insbesondere identifizierbare Elemente wie AAS
oder Submodelle und erlaubt sowohl punktuelle Abfragen innerhalb einer Instanz
als auch explorative Suchen in großen Repositories. Damit stellt dieser standar-
disierte Mechanismus eine performante Alternative dar, um Informationen effizi-
ent abzurufen, ohne die vollständige Dokumentenstruktur manuell traversieren zu
müssen. [27]
3.2  Informationsaufbereitung aus unstrukturierten
Daten für digitale Zwillinge
Die effiziente Nutzung von Digitalen Zwillingen im operativen Kontext erfordert die
Aufbereitung unstrukturierter Daten, die während des gesamten Lebenszyklus ei-
nes Assets anfallen [28]. Die Informationsaufbereitung stützt sich hierbei auf die
Architektur der RAG, die als technisches Framework Wissensquellen für LLM er-
schließt. Dabei fungiert RAG als entscheidende Schnittstelle, die es ermöglicht,
domänenspezifisches Wissen aus einer externen Datenbank abzurufen und dem
Modell als Kontext zur Verfügung zu stellen, ohne dass ein erneutes Training der
Modellparameter erforderlich ist. [29]
Der Prozess der Datenaufbereitung folgt einer mehrstufigen Pipeline, beginnend
mit der Datensammlung und der Vorverarbeitung. Ziel der Vorverarbeitung ist es,
Rohdaten  aus  verschiedenen  Formaten  in  ein  konsistentes  Format  zu  bringen,
Metadaten zu extrahieren und irrelevante Informationen zu filtern. Anschließend
erfolgt  die  Segmentierung  (Chunking),  bei  der  Dokumente  in  kleinere  Einheiten
zerlegt werden. [30] Die Herausforderung im Kontext von Digitalen Zwillingen sind
die heterogenen Datenformate sowie deren chronologische Abhängigkeit [28].
Aufgrund dieser Struktur ist meist eine Feinabstimmung von neuronalen Netzen
für jeden Zwilling notwendig. Dabei werden die Gewichte eines vortrainierten Mo-
dells basierend auf einem kleineren und spezifischen Datensatz aktualisiert. Da-
durch lassen sich generische Modelle für Digitale Zwillinge begrenzt skalieren. [31]
## 11

3  Stand der Wissenschaft
Hier setzt die RAG-Architektur an, indem sie die notwendige Spezialisierung durch
ein  gezielten  Informationsabruf,  realisiert.  [29]  Nach  der  Segmentierung  erfolgt
die Vektorisierung (Embedding). Hierbei wandelt ein Embedding-Modell die Text-
Segmente in eine numerische Vektorrepräsentation um, die die semantische Be-
deutung erfasst. Diese Vektoren sind grundlegend für die Effizienz und Genauigkeit
anschließender  Ähnlichkeitssuchen.  Die  Auswahl  eines  geeigneten  Embedding-
Modells und dessen Token-Grenze sind dabei wichtige Faktoren um die Balance
zwischen Berechnungsaufwand und semantischer Tiefe zu halten. [30]
3.3  Agentenbasierte Informationsanfrage aus
heterogenen Daten
Intelligente  Agenten  in  komplexen  Systemen  benötigen  die  Fähigkeit,  präzise
und  nachvollziehbare  Antworten  auf  heterogenen  Datenquellen  zu  generieren,
die  sowohl  strukturiert  als  auch  unstrukturiert  sein  können.  Reine  Retrieval-
Architekturen, die sich entweder auf VDB oder auf KGs stützen, sind auf ihre je-
weilige Funktion optimiert. Einzeln betrachtet sind sie für duale Anforderung al-
lerdings unzureichend. Vector Retrieval-Augmented Generation (Vector-RAG) ver-
wendet klassisch VDBs, um semantische Ähnlichkeiten zwischen der Anfrage und
den Textfragmenten zu messen. Dieser Ansatz eignet sich für breite Informations-
beschaffung aus unstrukturierten Datenquellen und bietet hohe Flexibilität. KGs
stellen Entitäten und Beziehungen dar. Sie sind optimiert für relationale Anfragen
und das Verständnis komplexer Abhängigkeiten, aber weniger flexibel bei seman-
tischen Suchanfragen. [32]
Die hybride Architektur (HybridRAG) wurde entwickelt, um diese Einschränkun-
gen zu überwinden. Sie kombiniert beide Ansätze und ermöglicht eine duale Ab-
frage [32]. Hierbei findet zum einen eine strukturelle Suche auf dem KG statt, zum
anderen findet eine semantische Suche in der Vektor-Komponente statt [33]. Ein
passend konfiguriertes HybridRAG liefert im Vergleich zu Vector-RAG und Know-
ledge Graph Retrieval-Augmented Generation (KG-RAG), sowohl in Genauigkeit
des Abrufs als auch in der Qualität, nützlichere Ergebnisse [32]. Die Effektivität
hängt bei HybridRAG weniger von der Feinabstimmung des Modells ab, sondern
von der Qualität der Dateninfrastruktur. Dies meint die Fähigkeit der Architektur,
Entitäten über verschiedene Quellen hinweg eindeutig zu identifizieren, semanti-
sche Vektoren konsistent mit den relationalen Graph-Strukturen zu synchronisieren
und eine hohe Integrität der zugrunde liegenden Beziehungsstrukturen zu gewähr-
leisten. [33]
Die Integration von KGs ermöglicht ein sogenanntes Multi-Hop-Reasoning [34].
## 12

3  Stand der Wissenschaft
Dabei beantworten Agenten komplexe Fragen, indem sie Informationen verknüp-
fen, die über mehrere Knoten und Beziehungen verteilt sind. Zudem wird die Ant-
wort des Modells durch den präzisen und strukturierten Kontext geerdet, was Hal-
luzinationen reduziert. HybridRAG bietet eine inhärente Erklärbarkeit und Nach-
vollziehbarkeit,  da  KGs  Beziehungen  speichern.  Dadurch  kann  der  abgerufene
Kontext offengelegt und die Antwort auf überprüfbare Fakten zurückgeführt wer-
den. [33]
## 13

4  Analyse der bestehenden
## Architektur
Aufbauend  auf  der  theoretischen  Einordnung  hybrider  RAG-Architekturen  rückt
nun die bestehende Infrastruktur zur Integration von AAS-Daten in einen KG in
den Fokus. Die folgende Untersuchung orientiert sich an dem von Sonnenberg et
al. [2] entwickelten Ansatz für ereignisgesteuerte KGs in AAS-Umgebungen. Ziel
ist es, die technologische Basis zu validieren und deren Potenzial für eine hybride
Erweiterung um unstrukturierte Datenquellen zu bestimmen.
Den  Ausgangspunkt  bildet  die  funktionale  Architektur  des  Connectors,  wobei
die Rolle von Apache Kafka als skalierbares Nachrichtenrückgrat. Ergänzend dazu
betrachtet die Untersuchung der Event-Struktur das informationstechnische Binde-
glied, welches Zustandsänderungen am Digitalen Zwilling in verarbeitbare Nach-
richten übersetzt. Dies verdeutlicht, wie das System hierarchische AAS-Strukturen
synchronisiert  und  über  die  Abfragesprache  Cypher  für  komplexe  Analysen  zu-
gänglich macht.
Die abschließende Evaluierung der Erweiterbarkeit bereitet den Übergang zur
Zielarchitektur vor. Hierbei steht die Frage im Mittelpunkt, inwieweit das modulare
Design und die Integration des Model Context Protocol (MCP) die strukturelle Tie-
fe von Neo4j mit der semantischen Flexibilität einer VDB vereinen können. Diese
Analyse bildet das Fundament, um die rein strukturbasierte Datenhaltung zu ei-
nem hybriden Assistenzsystem weiterzuentwickeln, welches auch unstrukturierte
Dokumenteninhalte effizient erschließt.
4.1  Architektur des AAS-Kafka-Neo4j Connectors
Die  Architektur  des  betrachteten  Systems  ist  als  entkoppelte,  ereignisgesteuer-
te  Pipeline  konzipiert,  welche  die  Integration  von  AAS-Inhalten  in  eine  Neo4j-
Graphdatenbank automatisiert. Wie in Abbildung 4.1 ersichtlich, folgt das System
einem modularen Aufbau, der den linearen Datenfluss von der Entstehung eines
Ereignisses in der BaSyx-Umgebung bis zur Speicherung im KG orchestriert. Aus-
gangspunkt bilden die AAS- und Submodell-Repositories, die um ereignisemitie-
rende  Fähigkeiten  erweitert  wurden.  Jede  Zustandsänderung,  wie  zum  Beispiel
die Erstellung einer neuen AAS oder die Aktualisierung eines Wertes, triggert ein
spezifische CUD-Event (Create, Update, Delete). [2]
Ein zentrales Element der Architektur ist Apache Kafka, das als fehlertolerantes
## 14

4  Analyse der bestehenden Architektur
und skalierbares Nachrichtenrückgrat fungiert.
CUD Events
BaSyx AAS
Umgebung mit Kafka
## Support
CUD Events
Apache Kafka mit Topics:
aas-events
submodel-events
HTTP Post mit
## Cypher Query
AAS Neo4j Integration mit
Kafka Connect und Pebble
## Templates
## Neo4j
## Wissensgraph
HTTP Post mit
## Cypher Query
KI-Agent mit
Neo4j MCP und
Vektor MCP
## Werkzeugen
## Integration
## Ereignis-
## Emissions-
## Schicht
## Nachrichten-
## Distributions-
## Schicht
## Synchronisations-
## Schicht
## Hybride
## Persistenz-
## Schicht
Abbildung 4.1: Systemarchitektur des AAS-Kafka-Neo4j-Connectors [2]
In Abbildung 4.1 wird verdeutlicht, dass die Ereignisse in dedizierte Topics in-
nerhalb des Kafka-Clusters kanalisiert werden. Es erfolgt eine logische Trennung
zwischen administrativen Operationen (aas-events) und inhaltlichen Änderungen
auf Submodell-Ebene (submodel-events). Diese Trennung ermöglicht eine paralle-
le Verarbeitung der Datenströme. Um die Datenkonsistenz innerhalb der verteil-
ten  Umgebung  zu  gewährleisten,  wird  die  eindeutige  Identifikator-ID  der  jewei-
ligen AAS als Kafka-Nachrichtenschlüssel verwendet. Da Kafka die Reihenfolge
der Nachrichten pro Partition garantiert, ist sichergestellt, dass Ereignisse für eine
spezifische Entität in der korrekten sequentiellen Abfolge beim Consumer eintref-
fen. [2]
Die  Transformation  der  JSON-basierten  Ereignisse  in  graphgerechte  Befehle
erfolgt  innerhalb  des  AAS  Neo4j  Integration  Service,  der  technisch  als  Kafka-
Connect-Plugin realisiert ist. Ein Merkmal ist der Einsatz der Pebble Templating
Engine. Anstatt die Transformationslogik fest im Programmcode zu implementie-
ren, nutzt das System deklarative YAML-Templates. Diese fungieren als Blaupau-
sen, die zur Laufzeit mit den Daten aus dem Kafka-Event angereichert werden, um
dynamisch Cypher-Abfragen zu generieren, welche per HTTP-Post an die Neo4j-
Schnittstelle übermittelt werden. Dieser Ansatz ermöglicht eine hohe Wartbarkeit,
da Anpassungen am Graphenmodell lediglich eine Änderung der Templates erfor-
dern, ohne dass ein erneutes Deployment des Connectors notwendig ist. [2]
In der Datenschicht wird die hierarchische AAS-Struktur auf ein Graphmodell
abgebildet, in dem Knoten (Labels wie :AssetAdministrationShell oder :Submodel)
und Kanten (Beziehungstypen wie HAS_SUBMODEL) die semantischen Zusam-
menhänge repräsentieren. Durch den Einsatz von Cypher-Operationen wie MER-
GE stellt der Connector sicher, dass die Graphstruktur atomar aktualisiert wird,
wodurch  Duplikate  vermieden  und  Beziehungen  konsistent  gepflegt  werden.  [2]
Die wesentlichen Bausteine dieser Pipeline sowie deren spezifische Aufgaben in-
## 15

4  Analyse der bestehenden Architektur
nerhalb des Datenflusses sind zusammenfassend in Tabelle 4.1 dargestellt. Diese
Übersicht verdeutlicht das Zusammenspiel der eingesetzten Technologien von der
Ereignisquelle bis hin zur persistenten Speicherung und KI-gestützten Abfrage. [2]
Tabelle 4.1: Komponenten der Systemarchitektur zur Ereignisverarbeitung
KomponenteFunktionaleBeschrei-
bung
## Implementierung
Event SourceEmission  von  CUD-Events
bei Zustandsänderungen
Eclipse BaSyx Repositories
Message BrokerSequenzierung  und  Vertei-
lung der Ereignisströme
## Apache Kafka
MiddlewareTemplate-basierte Transfor-
mation in Cypher-Queries
## Kafka Connect & Pebble
PersistenceSpeicherung   des   Labeled
Property Graph (LPG)
## Neo4j
AI IntegrationSchnittstelle für agentenba-
sierte Abfragen
Model Context Protocol (MCP)
4.2  Event-Struktur
Die Event-Struktur bildet die informationstechnische Grundlage für die Echtzeit-
synchronisation des KG. Das System nutzt für die Nachrichtenübertragung Events
im JSON-Format mittels Kafka, welches die Metadaten der AAS in flache, verar-
beitbare Datensätze nach dem IDTA-Standard übersetzt. Eine präzise Definition
dieser Nachrichtenformate ist unerlässlich, um sicherzustellen, dass der Connec-
tor die beabsichtigten Änderungen am Digitalen Zwilling korrekt interpretieren und
im Graphen persistieren kann. Ein typisches Ereignis für die Aktualisierung eines
Submodel-Elements (SME) umfasst neben der Identität des Submodells auch den
spezifischen Pfad (smElementPath), an dem die Änderung vorgenommen wurde.
Dieser Pfad ist für die Graphdatenbank von zentraler Bedeutung, da er eine ge-
zielte Adressierung des entsprechenden Knotens ermöglicht, ohne dass eine re-
kursive Suche über die gesamte Baumstruktur der AAS erforderlich ist. Der Kern
der Nachricht ist das smElement-Objekt, welches die Attribute gemäß dem AAS-
Metamodell kapselt. Hierzu zählen modelType (z. B. Property, File), contentType
(z.B. image/png oder application/pdf) oder valueType (z.B. xs:string), value und die
idShort. [2] Die Tabelle 4.2 erläutert die Felder eines Events anhand eines Bei-
spiels, das in Abbildung 4.2 zu sehen ist. [2]
## 16

4  Analyse der bestehenden Architektur
Abbildung 4.2: SME_UPDATED Event in Kafka
Tabelle 4.2: Definition der Felder in einem Event
FeldBedeutung für die
## Transformation
## Beispiel
typeBestimmt  die  auszuführende
## Operation
## SME_UPDATED
idEindeutige  Kennung  der  AAS
oder des Submodells
http://aas.dfki.de/ids/sm/...
modelTypeKlassifizierung   des   betroffe-
nen Elements
## File
contentTypeSpezifizierung   des   Dateifor-
mats
application/pdf
valueDer aktualisierte WertaHR0cDovL2Fhcy5kZmtp ...
idShortBezeichnung des ElementsDokumentation
smElementPathPositioninnerhalbder
Submodell-Hierarchie
## Documentation
Ein weiteres Element der Ereignisstruktur ist die sourceUrl, die den Ursprung ei-
nes Datensatzes eindeutig kennzeichnet. Dieses Feld wird primär bei Erzeugungs-
Ereignissen (CREATED) mitgeliefert und dient im Graphen als Validierungsmerk-
mal für die Datenherkunft. Im Gegensatz zu klassischen, hierarchischen Daten-
banken, deren Integrität primär durch eine feste interne Struktur gewährleistet wird,
ermöglicht die sourceUrl eine automatisierte Überprüfung über verteilte Reposito-
ries hinweg. Referenzen auf Knoten, die zwar im Graphen existieren, aber keine
sourceUrl aufweisen, lassen sich so als „dangling references“ identifizieren. Dieser
Mechanismus stellt sicher, dass in einem offenen System nicht nur Datenwerte,
sondern auch deren administrativer Kontext und semantische Herkunft lückenlos
nachvollziehbar bleiben. [2]
## 17

4  Analyse der bestehenden Architektur
4.3  Analyse der Erweiterbarkeit
Die Erweiterbarkeit der bestehenden Architektur ist ein entscheidendes Kriterium
für  die  Integration  unstrukturierter  Datenbestände.  Die  Analyse  zeigt,  dass  das
System durch seinen modularen Aufbau und den Einsatz deklarativer Komponen-
ten eine hohe Flexibilität für zukünftige Funktionserweiterungen besitzt. Diese Er-
weiterbarkeit manifestiert sich auf drei Ebenen, der Modellflexibilität, der Skalier-
barkeit  und  der  Integrationsfähigkeit  neuer  Datenbanktechnologien.  Eine  detail-
lierte Übersicht der architektonischen Erweiterungsaspekte und deren technischer
Voraussetzungen  findet  sich  in  Tabelle  4.3.  Auf  der  Ebene  der  Modellflexibilität
bietet  der  Einsatz  der  Pebble  Templating  Engine  einen  signifikanten  Vorteil.  Da
die  Transformation  von  AAS-Events  in  Datenbankbefehle  über  externe  Templa-
tes gesteuert wird, kann das System ohne Eingriffe in den Quellcode auf neue
Submodell-Spezifikationen reagieren.
Die Skalierbarkeit der Architektur wird durch die inhärenten Eigenschaften von
Apache Kafka unterstützt. Die Partitionierung von Topics erlaubt es, die Last auf
mehrere Instanzen des Kafka-Connect-Plugins zu verteilen, was eine horizonta-
le Skalierung ermöglicht. Im Hinblick auf die geplante Erweiterung um eine VDB
bietet dies die Möglichkeit, rechenintensive Aufgaben in einen separaten Verarbei-
tungspfad auszulagern. [2]
Tabelle 4.3: Analyse  der  architektonischen  Erweiterungsaspekte  und  deren  technische
## Voraussetzung
AspektTechnische VoraussetzungVorteil für die
## Erweiterung
Daten-MappingPebble YAML-TemplatesSchnelle    Integration    neuer
AAS-Typen
VerarbeitungKafka Connect TasksParallele  Extraktion  unstruk-
turierter Daten
DatenhaltungSchema-less Graph (LPG)DynamischeVerknüpfung
von Graph- und Vektordaten
InteraktionModelContextProtocol
## (MCP)
Ermöglicht Hybrid-RAG
Zuletzt unterstreicht die Analyse der Erweiterbarkeit die Bedeutung standardi-
sierter Schnittstellen wie dem MCP. Da der bestehende Connector bereits einen
MCP-Server  für  Neo4j  integriert,  ist  die  Grundlage  für  eine  skalierbare  Tool-
Landschaft gelegt. Die Erweiterbarkeit wird dadurch begünstigt, dass auch für die
VDB ein entsprechender MCP-Server angebunden werden kann. Dabei fungiert
das MCP nicht lediglich als technische Schnittstelle, sondern als eine Abstraktions-
und Validierungsebene, welche die Interaktion des KI-Agenten mit den Datenquel-
## 18

4  Analyse der bestehenden Architektur
len formalisiert. Durch die Definition expliziter Tool-Parameter innerhalb des MCP-
Dienstes wird der Agent konfiguriert, Suchanfragen durch die Mitgabe spezifischer
Metadaten  präzise  zu  qualifizieren.  Diese  strukturierte  Parameterübergabe  fun-
giert als funktionale Vorgehensweise, die das Risiko von Fehlinterpretationen und
das Einfließen irrelevanter Datenfragmente in den Kontext minimiert. Ein wesentli-
cher Vorteil dieser Architektur liegt in der konsequenten Entkopplung der Agenten-
Logik von der technischen Implementierung der Datenbanken. Dies ermöglicht es,
die zugrunde liegenden Speichersysteme zu modifizieren oder zu ergänzen, ohne
die Konfiguration des Agenten oder dessen System-Prompts anpassen zu müs-
sen.  Ein  KI-Agent  kann  somit  den  strukturierten  Kontext  aus  dem  KG  effizient
einsetzen, um die semantische Suche in der VDB auf das korrekte Asset einzu-
grenzen. Die bestehende Architektur erweist sich damit als robuste und flexible
Ausgangslage, um die Transformation von einer rein strukturierten AAS-Anzeige
hin  zu  einem  umfassenden,  dokumentenzentrierten  Assistenzsystem  zu  vollzie-
hen. [2]
## 19

## 5  Konzept
Die Transformation der AAS von einem primär dokumentenzentrierten Repository
hin zu einer aktiven, abfragbaren Wissensbasis erfordert eine hybride Systemar-
chitektur. Während die bereits analysierte Infrastruktur die strukturellen und rela-
tionalen Aspekte der AAS in einem KG abbildet, bleibt der semantische Gehalt
unstrukturierter Dokumente innerhalb des Submodells bislang unerschlossen.
Das Ziel der hier entworfenen Architektur ist die Integration einer VDB in die
bestehende,  ereignisgesteuerte  Pipeline,  um  ein  funktionsfähiges  Graph-RAG-
System zu realisieren. Ein solches System kombiniert die logische Strenge von
Graph-Traversierungen  mit  der  semantischen  Unschärfe  der  Vektorsuche,  was
insbesondere für industrielle Assistenzsysteme von Bedeutung ist, die komplexe
technische Fragen auf Basis von Handbüchern und Wartungsanweisungen beant-
worten müssen. Die Architektur ist dabei so konzipiert, dass sie die Anforderun-
gen an Skalierbarkeit, Fehlertoleranz und Kontext-Isolierung in einer Multi-Asset-
Umgebung erfüllt. Die folgenden Abschnitte beschreiben die funktionalen Schich-
ten,  das  zugrunde  liegende  Datenmodell  sowie  die  Synchronisations-  und  Infe-
renzlogik auf einer generischen, implementierungsunabhängigen Ebene.
5.1  Anforderungen an die Systemarchitektur
Das vorliegende Architekturkonzept muss eine Reihe spezifischer Anforderungen
erfüllen, um die Kopplung von strukturellem Wissen und semantischen Inhalten
effizient zu realisieren. Im Zentrum steht die Synchronisierung der hybriden Per-
sistenzschicht. Das System muss ereignisgesteuert auf Änderungen in der AAS
reagieren und dabei eine asynchrone Verarbeitung gewährleisten, damit rechen-
intensive Vektorisierungsprozesse die performanten Graph-Updates nicht blockie-
ren. Hierbei ist die Idempotenz der Dienste zwingend erforderlich, um durch deter-
ministische Identifikatoren sicherzustellen, dass mehrfach zugestellte Ereignisse
keine inkonsistenten Datenbestände oder redundanten Rechenaufwand verursa-
chen.
Ein  weiterer  Aspekt  ist  die  Filterung  und  Kontext-Isolierung.  Um  präzise  Ant-
worten in einer Multi-Asset-Umgebung zu garantieren, muss die Architektur eine
Einschränkung des Suchraums in der Vektordatenbank ermöglichen. Dies erfolgt
durch ein Metadaten-Mapping, bei dem der KG als Filter-Generator fungiert und
die Suche auf autorisierte Submodelle begrenzt.
Zusätzlich  muss  die  Architektur  eine  horizontale  Skalierbarkeit  des  Vektor-
## 20

## 5  Konzept
Service ermöglichen, um Lastspitzen bei der Dokumentenverarbeitung abzufan-
gen, während durch ein strukturerhaltendes Chunking mit definierten Überlappun-
gen die semantische Integrität und der Kontext technischer Dokumentationen über
Segmentgrenzen hinweg gewahrt bleiben.
## 5.2  Systemarchitektur
CUD-Events
BaSyx AAS
Umgebung mit Kafka
## Support
CUD-Events
CUD-Event
Apache Kafka mit Topics:
aas-events
submodel-events
HTTP Post mit
## Cypher Query
AAS Neo4j Integration mit
Kafka Connect und Pebble
## Templates
## Neo4j
## Wissensgraph
HTTP Post mit
## Cypher Query
## Wissensabfrage
KI-Agent mit
Neo4j MCP und
Vektor MCP
## Werkzeugen
## Integration
Vektoren und
## Metadaten
Vektor-ServiceVektordatenbank
## Ereignis-
## Emissions-
## Schicht
## Nachrichten-
## Distributions-
## Schicht
## Synchronisations-
## Schicht
## Hybride
## Persistenz-
## Schicht
## Abbildung 5.1: Zielarchitektur
Die Systemarchitektur basiert, wie in Abbildung 5.1 ersichtlich, auf dem Prin-
zip der losen Kopplung durch einen zentralen Nachrichten-Broker. Diese Entkopp-
lung ist notwendig, um die unterschiedlichen Verarbeitungsgeschwindigkeiten von
strukturellen Metadaten und unstrukturierten Dokumentendaten zu harmonisieren.
Im Zentrum der Überlegungen steht der Übergang von einer sequentiellen Verar-
beitung hin zu einer parallelisierten Split-Worker-Architektur.
5.2.1  Funktionale Schichten und Komponenten
Die  Architektur  gliedert  sich  in  vier  spezialisierte  Schichten,  die  über  definierte
Schnittstellen kommunizieren.
-  Ereignis-Emissions-Schicht: Die AAS-Infrastruktur fungiert als Single Source
of Truth. Jede Interaktion mit der AAS oder eines ihrer Submodels löst ein
Ereignis aus, das den vollständigen Kontext der Änderung kapselt.
## 21

## 5  Konzept
-  Nachrichten-Distributions-Schicht: Ein persistenter Broker fungiert als Log-
buch. Er garantiert die korrekte Reihenfolge der Ereignisse pro Asset und
ermöglicht es mehreren Konsumenten, dieselben Datenströme unabhängig
voneinander zu verarbeiten.
-  Synchronisations-Schicht: Hier erfolgt die funktionale Trennung in zwei spe-
zialisierte Services:
–  Graph-Service: Dieser verarbeitet strukturelle Ereignisse, um die hierar-
chischen Beziehungen innerhalb der Graphdatenbank aktuell zu halten.
–  Vektor-Service: Dieser erkennt Dokumentenreferenzen und startet eine
Pipeline  zur  Inhaltsextraktion,  Vektorisierung  und  Speicherung  in  der
## VDB.
-  Hybride Persistenz-Schicht: Diese besteht aus komplementären Datenbank-
systemen,  einer  Graphkomponente  für  relationale  Pfadabfragen  und  einer
Vektorkomponente für die Ähnlichkeitssuche.
5.2.2  Strategische Abwägung der Worker-Anordnung
Ein  wesentlicher  Bestandteil  des  Architekturentwurfs  ist  die  Evaluation  des
Synchronisationsverhaltens. Hierbei stehen zwei Konzepte im Fokus.
Single-Worker-Ansatz  (Sequentiell):  In  diesem  Modell  bedient  ein  einziger
Dienst beide Ziel-Datenbanken. Dies vereinfacht das Fehlermanagement, da eine
Transaktion erst als abgeschlossen gilt, wenn beide Systeme erfolgreich aktuali-
siert wurden, was eine starke Konsistenz ergibt. Der entscheidende Nachteil liegt
in der Latenz, da die Vektorisierung eines PDF-Dokuments langsamer ist als ein
Graph-Update. Dieser Ansatz würde den gesamten Datenfluss blockieren und die
Echtzeitfähigkeit des KG gefährden.
Split-Worker-Ansatz  (Asynchron):  Die  Zielarchitektur  setzt  auf  die  funktio-
nale  Trennung  der  Services.  Dies  ermöglicht  eine  horizontale  Skalierung  des
Vektor-Service,  während  der  Graph-Service  weiterhin  performant  operiert.  Das
System nimmt dabei eine zeitweise Inkonsistenz in Kauf. Der KG referenziert das
neue Dokument bereits, während die Vektorkomponente noch an der Einbettung
arbeitet.  Für  industrielle  Anwendungen  ist  dies  akzeptabel,  da  die  strukturelle
Navigation  oft  Vorrang  vor  der  inhaltlichen  Suche  hat.  Zudem  handelt  es  sich
bei  den  betrachteten  Dokumenten  primär  um  technische  Handbücher.  Solche
sind statische Quellen und ändern sich im Vergleich zu operativen Prozessdaten
## 22

## 5  Konzept
selten.  Dementsprechend  ist  die  Relevanz  einer  sofortigen  Verfügbarkeit  im
Vektorspeicher  gegenüber  der  strukturellen  Erfassung  im  Graphen  geringer.
Die dauerhafte Konsistenz wird durch die Übertragung der Events mittels Kafka
gewährleistet. Kafka stellt die logische Atomizität sicher, indem fehlgeschlagene
Vorgänge durch den garantierten Verarbeitungsmechanismus nachgeholt werden
müssen.
Die  folgende  Tabelle  fasst  die  Merkmale  der  Split-Worker-Architektur  zusam-
men.
Tabelle 5.1: Merkmale der Split-Worker-Architektur
MerkmalStruktur-SynchronisationInhalt-Synchronisation
PrimärzielTopologische IntegritätSemantische Erschließung
DatenformatJSON / RelationalUnstrukturierter Text / Vektoren
LatenzprofilMillisekundenSekunden bis Minuten
SkalierungVertikalHorizontal
KonsistenzStarke KonsistenzZeitweise Inkonsistenz
5.3  Datenmodell für Vektordatenbanken
Das Datenmodell definiert die logische Struktur der im Vektorspeicher abgeleg-
ten Dokumentensegmente und deren Verknüpfung mit der übergeordneten AAS-
Struktur. Die semantischen Inhalte der in den Submodellen referenzierten Doku-
mente werden so strukturiert, dass sie unter Wahrung ihres administrativen Kon-
textes effizient abgefragt werden können.
5.3.1  Metadaten-Mapping und Kontext-Isolierung
Um eine präzise Abfrage zu ermöglichen und das Risiko einer Vermischung von
Dokumenteninhalten verschiedener Maschinen zu eliminieren, wird jedes Doku-
ment in Segmente (Chunks) unterteilt. Da technische Handbücher oft lange Pas-
sagen enthalten, ist diese Zerlegung zwingend erforderlich, um das Eingabelimit
des Embedding-Modells nicht zu überschreiten. Die Architektur nutzt hierfür ein re-
kursives Trennverfahren, das gezielt versucht, logische Einheiten zu erhalten. Um
den Kontext an den Segmentgrenzen zu bewahren, wird eine definierte Überlap-
pung verwendet. Diese stellt sicher, dass zusammenhängende Informationen über
Segmentegrenzen hinweg in unterschiedlichen Segmenten repräsentiert werden.
Dies  ermöglicht  es  dem  System,  bei  Suchanfragen  den  vollständigen  semanti-
schen Kontext zu rekonstruieren und erhöht die Wahrscheinlichkeit signifikant, alle
relevanten Informationen zu erfassen.
## 23

## 5  Konzept
Jedes daraus resultierende Vektor-Objekt wird anschließend mit einem spezifi-
schen Metadatensatz angereichert, der als Filterkriterium dient. Die Datenstruktur
sieht hierfür zwei funktionale Felder vor:
-  submodelId: Diese Kennung dient der logischen Trennung der Submodels.
Sie stellt sicher, dass Suchanfragen explizit auf den Bereich eines Submo-
dels begrenzt werden können.
-  smElementPath:  Dieser  Pfad  repräsentiert  die  exakte  Position  des  Doku-
ments innerhalb der Submodel-Hierarchie. Er ist für die Synchronisations-
logik von zentraler Bedeutung, da er eine eindeutige Adressierung des Ele-
ments bei Aktualisierungs- oder Löschoperationen erlaubt, ohne dass eine
globale Suche über alle Datensätze notwendig ist.
5.3.2  Relationale Verknüpfung im KG-RAG
Obwohl die VDB konzeptionell flach strukturiert ist, wird durch die oben genannten
Metadaten eine virtuelle Beziehung zum KG hergestellt. Der Graph speichert die
komplexen Abhängigkeiten zwischen Assets, Submodellen und deren Elementen,
die Dokumentenreferenzen besitzen können.
Bei einer Suchanfrage agiert der KG als Filter-Generator. Er identifiziert über
relationale Abfragen die relevanten Pfade und IDs. Diese Ergebnisse werden als
Filterparameter an die VDB übergeben. Dadurch wird die semantische Suche ma-
thematisch auf einen präzise definierten Teilraum begrenzt, was die Genauigkeit
erhöht.
5.4  Erzeugung der Embeddings
Die Überführung unstrukturierter technischer Dokumente in mathematische Vek-
torrepräsentationen ist ein mehrstufiger Prozess innerhalb des Vektor-Service. Um
eine hohe Abfrage-Qualität zu gewährleisten, folgt die Pipeline einem Ablaufmo-
dell, das die strukturellen Besonderheiten technischer Dokumentationen berück-
sichtigt.
5.4.1  Die Service-Pipeline
Wie in Abbildung 5.2 dargestellt, durchläuft die Embedding-Erzeugung vier aufein-
anderfolgende Phasen:
-  Inhaltsakquise (Load): Nach Empfang eines relevanten Ereignisses nutzt der
Worker die darin enthaltene Referenz-URL, um das Dokument zu laden.
## 24

## 5  Konzept
Roh-Dokument
Laden des
## Dokuments
## Strukturierter
## Text
Konvertierung nach
## Markdown
Text-Chunks
Chunking des Texts
Erzeugung der
## Embeddings
## Phase 1
## Inhaltsakquise
## Phase 2
## Transformation
## Phase 3
## Partitionierung
## Phase 4
## Vektorisierung
Referenz-URL
## Event Trigger
## Vektor-
datenbank
Vektoren und
## Metadaten
Konvertierung des
Dokuments nach
## Markdown
Abbildung 5.2: Ablauf der Service-Pipeline
-  Strukturierte  Transformation  (Markdown-Konvertierung):  Um  die  semanti-
sche Qualität zu erhöhen, wird das Dokument zunächst in ein strukturiertes
Textformat  wie  Markdown  überführt.  Dieser  Zwischenschritt  ist  essenziell,
um visuelle Elemente, wie Tabellen, in eine textuelle Form zu bringen, die
für Sprachmodelle leichter interpretierbar ist. Dies verhindert, dass Layout-
Artefakte den semantischen Vektor verfälschen.
-  Partitionierung (Chunking): Der Markdown-Text wird in Segmente unterteilt,
um die Limits des Embedding-Modells einzuhalten. Ein rekursives Trennver-
fahren bewahrt dabei logische Einheiten. Durch eine Überlappung wird si-
chergestellt, dass der semantische Kontext an den Segmentgrenzen erhalten
bleibt, was die Treffgenauigkeit bei Suchanfragen deutlich erhöht.
-  Vektorisierung   (Embedding):   In   der   letzten   Phase   transformiert   ein
Embedding-Modell jedes Segment in einen hochdimensionalen Vektor. Die
so erzeugten Vektoren werden zusammen mit den Metadaten in der VDB
gespeichert.
5.4.2  Methodik der Ähnlichkeitsmessung
Die Grundlage für das spätere Wiederauffinden von Informationen ist die Berech-
nung der Korrelation zwischen einer Nutzeranfrage und einem Dokumentenfrag-
ment. Hierzu wird die Kosinus-Ähnlichkeit im Vektorraum verwendet.
## 25

## 5  Konzept
cos(θ) =
a·b
## ∥a∥·∥b∥
Um Informationsverluste an den Segmentgrenzen zu vermeiden, wird eine Über-
lappung definiert. Dies stellt sicher, dass der semantische Kontext über die Gren-
zen  hinweg  redundant  gespeichert  wird  und  auch  Informationen,  die  über  zwei
Segmente verteilt sind, auffindbar bleiben.
## 5.5  Synchronisationslogik
Die Synchronisationslogik definiert die operationalen Regeln, um die Konsistenz
zwischen dem Zustand der AAS und der hybriden Speicherschicht zu gewährleis-
ten.  Ein  Kernproblem  verteilter  Systeme  ist  hierbei  die  Gewährleistung  der  Zu-
standsstabilität bei Mehrfachaufrufen.
5.5.1  Idempotenz durch deterministische Identifikatoren
In ereignisgesteuerten Architekturen kann es aufgrund von Netzwerkfehlern oder
Rebalancierung des Brokers zur mehrfachen Bereitstellung derselben Nachricht
kommen.  Um  Datenredundanz  sowie  Inkonsistenzen  in  der  VDB  zu  vermeiden
und gleichzeitig die rechenintensive Embedding-Pipeline zu entlasten, implemen-
tiert der Vektor-Service eine Vorab-Prüfung auf Basis der vorliegenden Metadaten.
Sobald ein Kafka-Ereignis empfangen wird, nutzt der Worker die Kombination aus
submodelId und smElementPath zur eindeutigen Identifikation des Datensatzes.
Anstatt  einen  zufälligen  Primärschlüssel  zu  vergeben,  dient  dieses  Verfahren
dazu, einen stabilen Identifikator zu schaffen, der vor dem Start der Textextraktion
und Vektorisierung mit dem aktuellen Bestand der Zieldatenbank abgeglichen wird.
Existiert der Identifikator bereits, wird die Verarbeitung abgebrochen, während bei
einem neuen Element die Pipeline initiiert wird. Durch diesen Vorab-Vergleich wird
die Idempotenz des Systems sichergestellt. Ein wiederholtes Empfangen dessel-
ben Ereignisses führt zum identischen Speicherzustand, sodass teure Extraktions-
und  Embedding-Schritte  nicht  mehrfach  ausgeführt  werden.  Der  Vektor-Service
erkennt  redundante  Operationen  somit  unmittelbar,  wodurch  die  Systemlast  mi-
nimiert und die Konsistenz auch bei Duplikaten im Nachrichtenstrom oder nach
einem Systemneustart garantiert bleibt.
5.5.2  CUD-Mapping der AAS-Ereignisse
Die Logik transformiert die AAS-Ereignistypen wie folgt:
## 26

## 5  Konzept
-  CREATE:  Identifikation  als  neues  Element  mittels  Identifikator-Check  und
Start der vollständigen Pipeline.
-  UPDATE: Triggert eine Neu-Vektorisierung des Inhalts. Da sich bei Inhalts-
änderungen die Anzahl der Segmente verändern kann, folgt die Logik einer
strikten Sequenz. Zunächst berechnet die Pipeline die neuen Embeddings
für das gesamte Dokument. Nach erfolgreichem Abschluss werden alle exis-
tierenden Datensätze, die über den smElementPath dem Dokument zuge-
ordnet sind, in der VDB gelöscht. Erst danach erfolgt das Einfügen der neu-
en Vektoren. Dieser Ansatz verhindert, dass bei einer Verringerung der Do-
kumentengröße Fragmente der Vorgängerversion als veraltete Überreste im
Suchraum verbleiben.
-  DELETE: Das Löschen eines Elements führt zu einem Lösch-Event, bei dem
über einen Delete-Befehl alle Segmente entfernt werden, die mit dem ge-
löschten Pfad korrelieren.
In der softwaretechnischen Betrachtung der Datenhaltung wird üblicherweise das
CRUD-Modell (Create, Read, Update, Delete) als Referenz herangezogen. Für die
Synchronisationslogik des Vektor-Service erfährt dieses Modell jedoch eine geziel-
te Modifikation. Während die Operationen zur Erstellung (Create), Aktualisierung
(Update) und Löschung (Delete) essenziell sind, um die Synchronität zwischen der
AAS-Infrastruktur und der VDB sicherzustellen, ist eine explizite Implementierung
einer dedizierten Leselogik (Read) innerhalb der Synchronisationsschicht redun-
dant. Der lesende Zugriff auf die semantischen Informationen erfolgt entkoppelt
vom Synchronisationsprozess über die agentische Orchestrierung. Hierbei fungiert
das MCP als standardisierte Schnittstelle, die die VDB nicht als statischen Daten-
speicher, sondern als dynamisches Werkzeug für einen KI-Agenten bereitstellt.
5.5.3  Agentische Orchestrierung mittels Model Context
## Protocol
Die Abfrage erfolgt über das MCP, das die Datenbanken als Werkzeuge für einen
KI-Agenten bereitstellt. Dabei fungiert das Protokoll als Schnittstelle, die eine stan-
dardisierte Kommunikation zwischen dem KI-Agenten und Datenquellen ermög-
licht.  Es  erlaubt  dem  Agenten,  spezifische  Werkzeuge  (Tools)  und  Ressourcen
sicher abzurufen, ohne dass für jede Datenbank eine individuelle Integration not-
wendig ist.
Diese Abfrage folgt einem zweistufigen Reasoning-Prozess. Zunächst nutzt der
Agent ein Graph-Tool zur strukturellen Kontext-Eingrenzung. Anschließend werden
## 27

## 5  Konzept
diese Filter an ein Vektor-Tool übergeben, um die semantische Suche im autorisier-
ten Raum durchzuführen. Dies gewährleistet eine faktengestützte Antwortgenerie-
rung und erhöht die Zuverlässigkeit des Gesamtsystems.
## 28

## 6  Implementierung
Die Überführung der systemtheoretischen Anforderungen in eine funktionale Sys-
temarchitektur markiert den entscheidenden Schritt von der Konzeption zur opera-
tiven Anwendung des hybriden Graph-RAG-Systems. Dieser Abschnitt dokumen-
tiert die technische Realisierung und verdeutlicht, wie durch eine gezielte Kompo-
nentenauswahl und softwareseitige Eigenentwicklungen die theoretische Präzisi-
on in eine stabile Infrastruktur übersetzt wird. Dabei steht die Transformation un-
strukturierter PDF-Daten aus der AAS in maschinenlesbares, verfügbares Wissen
im Vordergrund. Durch die Kombination spezialisierter VDBs mit fortschrittlichen
Extraktions-Frameworks wird eine semantische Genauigkeit bei technischen Do-
kumentationen erreicht, die die klassische Volltextsuche übertrifft.
Die Entwicklung eines asynchronen, zustandslosen Microservices stellt dabei
sicher, dass Datenänderungen am Digitalen Zwilling in die Vektorräume fließen.
Die containerisierte Orchestrierung dieser Dienste bildet schließlich ein robustes
Fundament, das Skalierbarkeit garantiert und eine herstellerunabhängige Integra-
tion in agentenbasierte Plattformen ermöglicht. Die folgenden Erläuterungen legen
die Entscheidungskriterien für den gewählten Technologie-Stack offen, beschrei-
ben die logische Struktur des entwickelten Python-Workers und zeigen auf, wie die
finale Integration eine kontextsensitive Interaktion mit Industriedaten ermöglicht.
## 6.1  Komponentenauswahl
Die Auswahl der technologischen Basis ist entscheidend für die Skalierbarkeit und
die Antwortqualität des Gesamtsystems. In einer industriellen Umgebung müssen
die Komponenten Anforderungen an die Filtereffizienz und die Integrationsfähigkeit
in bestehende KI-Systemen erfüllen.
6.1.1  Auswahl der Vektordatenbank
Für die Speicherung der Dokumenten-Embeddings wurde ein systematischer Ver-
gleich zwischen der Nutzung der bestehenden Graphdatenbank Neo4j Community
Edition und der spezialisierten VDB Weaviate durchgeführt. Obwohl Neo4j ab der
Version 5.11 integrierte Vektor-Suchfunktionen bietet [19], wird für diesen Anwen-
dungsfall Weaviate ausgewählt. Die folgende Tabelle 6.1.1 und Analyse verdeutli-
chen die technischen Differenzen auf Basis der offiziellen Dokumentationen.
## 29

## 6  Implementierung
Tabelle 6.1: Vergleichsmatrix über Neo4J CE und Weaviate
KriteriumNeo4j
## Community Edition
## Weaviate
ArchitekturGraph-Native    mit    Vektor-
## Erweiterung [19]
KI-Native   Vektordatenbank
## [35]
Vektor-IndizierungGraph-basierter  ANN-Index
mit Lucene [19]
## Nativergraph-basierter
ANN-Index [35]
Multi-TenancyNur logisch (limitert auf 1 ak-
tive DB) [19]
Nativ(physischeShard-
## Isolation) [35]
Hybride SucheNicht nativ im Kern integriert
## [19]
## Nativ [35]
RuntimeSlotted    Runtime    (Single-
threaded) [19]
ParallelisierteAbfrage-
## Engine [35]
LizenzGPLv3 [19]BSD 3-Clause [35]
Ein  wesentliches  Entscheidungskriterium  ist  die  funktionale  Abgrenzung  der
Neo4j  Community  Edition.  Gemäß  der  offiziellen  Neo4j-Dokumentation  ist  die
Community Edition auf eine einzige aktive Datenbank pro Instanz beschränkt, was
eine  physische  Trennung  von  Mandantendaten  erschwert.  Zudem  nutzt  sie  die
Slotted Cypher Runtime, während die für Vektor-Workloads optimierte Pipelined
Runtime der Enterprise-Edition vorbehalten bleibt. Technisch basieren die Vektor-
Indizes in Neo4j auf der Apache Lucene-Bibliothek, was eine Integration in Graph-
Abfragen ermöglicht, jedoch in der Community Edition keine native hybride Suche
unterstützt. [19]
Im Gegensatz dazu ist Weaviate eine KI-native Datenbank, die von Grund auf für
hochdimensionale Vektorräume konzipiert wurde. [35] Die Entscheidung für Wea-
viate stützt sich auf folgende Vorteile:
-  Hybride Suche: Weaviate integriert die hybride Suche nativ. Dabei wird die
semantische Vektorsuche mit einer klassischen Keyword-Suche kombiniert,
die auf dem Best Matching 25 (BM25)-Algorithmus basiert. BM25 ist eine
Ranking-Funktion, die die Relevanz eines Dokuments für eine Suchanfrage
anhand der Häufigkeit der Suchbegriffe im Verhältnis zur Gesamtlänge des
Dokuments berechnet. [35] Dies ist für technische Dokumentationen essen-
ziell, um bei spezifischen Fachbegriffen oder Seriennummern präzise Treffer
zu erzielen.
-  Kontext-Isolierung: Weaviate bietet eine native Multi-Tenancy-Unterstützung,
bei der jeder Tenant einen isolierten Shard erhält. Dies garantiert, dass die
Daten  verschiedener  Assets  physisch  getrennt  bleiben  und  Suchanfragen
nur im Kontext des jeweiligen Tenants ausgeführt werden. [35]
## 30

## 6  Implementierung
-  Indizierung: Zur effizienten Suche im hochdimensionalen Raum nutzt Wea-
viate den Hierarchical Navigable Small World (HNSW)-Algorithmus. Dieser
organisiert Vektoren in einer hierarchischen Graphenstruktur, um eine ANN-
Suche mit geringer Latenz zu ermöglichen. Im Gegensatz zu linearen Such-
verfahren  bietet  HNSW  eine  hohe  Skalierbarkeit  bei  gleichbleibend  hoher
## Abfragepräzision. [35]
Zusammenfassend lässt sich festhalten, dass die Neo4j Community Edition si-
gnifikante Einschränkungen in der Skalierbarkeit und Performance für rein vektor-
basierte Workloads aufweist. Die Wahl fällt auf Weaviate, da es als spezialisierte
VDB die notwendige Kombination aus präziser hybrider Suche und strikter Man-
dantentrennung bereits im Kern bereitstellt.
6.1.2  Textextraktion mit Docling
Für die Umwandlung von PDF-Dokumenten in ein maschinenlesbares Format wird
das Framework Docling eingesetzt. Im Gegensatz zu einfacheren Bibliotheken, die
Dokumente oft lediglich als unstrukturierte Textströme behandeln, nutzt Docling
spezialisierte KI-Modelle, um die visuelle Struktur, wie zum Beispiel Tabellen, und
die semantischen Hierarchien des Quelldokuments zu verstehen. Die Architektur
von Docling stützt sich dabei auf zwei Kernkomponenten:
-  Layout-Analyse  (DocLayNet):  Ein  Computer-Vision-Modell  identifiziert  ver-
schiedene Seitenelemente wie Überschriften, Fließtexte, Listen und Bilder,
um die korrekte Lesereihenfolge beizubehalten.
-  Tabellenerkennung  (TableFormer):  Dieses  Modell  ist  darauf  spezialisiert,
komplexe Tabellenstrukturen präzise zu rekonstruieren und in strukturierte
Datenformate zu überführen.
In einem Benchmark-Vergleich von Procycons [36] erreichte Docling eine Ge-
nauigkeit von 97,9% bei der Extraktion von Tabellenzellen aus komplexen Berich-
ten. Zudem wurde eine hunderprozentige Texttreue nachgewiesen, wobei techni-
sche Begriffe und Absatzformate exakt erhalten blieben. Die Fähigkeit von Docling,
Dokumente in ein strukturiertes Markdown-Format zu überführen, ist für das nach-
geschaltete RAG-System von entscheidender Bedeutung. Es bewahrt die hierar-
chische Gliederung des Dokuments, was ein präziseres Chunking ermöglicht und
somit die Qualität der Abfragen steigert [36].
## 31

## 6  Implementierung
6.1.3  Auswahl des Embedding-Modells
Die Qualität der semantischen Abfrage hängt primär von der Fähigkeit des Mo-
dells ab, technische Nuancen in industriellen Handbüchern korrekt zu kodieren.
Um eine Herstellerabhängigkeit zu vermeiden und eine hohe Flexibilität im Betrieb
sicherzustellen, wurde das System modular konzipiert.
Im Zuge der Implementierung des Prototyps wurde Gemini verwendet. Dieses
lässt sich kostenfrei nutzen und bietet ein hohes Limit an täglichen Anfragen. Zu-
dem handelt es sich um ein multilinguales Modell, dass eine Vielzahl von Sprachen
unterstützt, wodurch gleiche Wörter aus unterschiedlichen Sprachen in den selben
Vektorraum abbilden. Dadurch kann man Fragen in verdienen Sprachen stellen,
ungeachtet der Sprache des Dokuments.
Die Auswahl und Konfiguration des Embedding-Modells erfolgt zentral über Um-
gebungsvariablen in einer .env-Datei. Hierbei können verschiedene Anbieter wie
OpenAI, Google (Gemini), Voyage AI oder Anthropic durch die Hinterlegung der
jeweiligen API-Keys dynamisch gewechselt werden. Innerhalb des Microservices
wird die Implementierung konsequent über das LangChain-Framework abstrahiert.
LangChain  bietet  eine  standardisierte  Schnittstelle  für  Embedding-Modelle,  wo-
durch  das  System  agnostisch  gegenüber  dem  spezifischen  Provider  bleibt  und
Modellwechsel ohne Eingriffe in den Quellcode möglich sind.
6.2  Erweiterung des Kafka-Connectors
Die softwareseitige Realisierung der Zielarchitektur erfolgt durch die Implementie-
rung eines in Python verfassten Microservices, der die Rolle des Vektor-Service
übernimmt. Im Gegensatz zu einer direkten Anbindung an Kafka wird dieser Ser-
vice über einen Kafka HTTP Sink Connector in die Event-Pipeline integriert.
Der Connector agiert hierbei als Vermittlungsinstanz. Er konsumiert die Ereig-
nisse aus den relevanten Kafka-Topics und leitet diese als HTTP-Post-Requests
an den Python-Service weiter. Dieser übernimmt somit die Rolle eines reaktiven
Web-Service,  der  die  eingehenden  Payloads  verarbeitet  und  die  nachgelagerte
Verarbeitungspipeline steuert.
6.2.1  Service-Architektur
Der Service ist, wie in der Systemarchitektur in Abbildung 6.1 ersichtlich, als zu-
standsloser Worker konzipiert. Er folgt einer sequenziellen Verarbeitungslogik. Je-
des Ereignis aus Kafka wird innerhalb der Consumer-Hauptschleife einzeln verar-
beitet. Die Pipeline aus Abbildung 5.2 muss vollständig durchlaufen sein, bevor der
## 32

## 6  Implementierung
Offset bestätigt und das nächste Ereignis geladen wird. Dies stellt sicher, dass die
Reihenfolge der AAS-Inhaltsänderungen exakt gewahrt bleibt.
CUD-Events
BaSyx AAS
Umgebung mit Kafka
## Support
CUD-Events
CUD-Event
Apache Kafka mit Topics:
aas-events
submodel-events
HTTP Post mit
## Cypher Query
AAS Neo4j Integration mit
Kafka Connect und Pebble
## Templates
## Neo4j
## Wissensgraph
HTTP Post mit
## Cypher Query
## Wissensabfrage
mit HTTP/gRPC
KI-Agent mit
Neo4j MCP und
Vektor MCP
## Werkzeugen
## Integration
Vektoren und
## Metadaten
mit HTTP/gRPC
Vektor-Service
in Python
## Weaviate
## Vektordatenbank
## Ereignis-
## Emissions-
## Schicht
## Nachrichten-
## Distributions-
## Schicht
## Synchronisations-
## Schicht
## Hybride
## Persistenz-
## Schicht
CUD-Event
## HTTP
HTTP Sink
## Connector
Abbildung 6.1: Systemarchitektur mit ausgewählten Komponenten
6.2.2  Implementierung der Idempotenz
Die Kernlogik umfasst CUD-Operationen basierend auf dem AAS-Metamodell:
-  Identifikation:  Die  Funktion  is_pdf  prüft  den  modelType  und  contentType.
get_ids extrahiert Identifikatoren wie die submodelId und smElementPath.
-  Identifikator-Vorabprüfung:  Ein  Identifikatoren  aus  submodelId  und  smEle-
mentPath dient als Schlüssel. Die Docling-Pipeline wird nur gestartet, wenn
der Identifikatoren neu ist oder ein Update signalisiert wurde.
-  Update-Verfahren:  Das  Verfahren  berechnet  erst  neue  Embeddings  und
löscht dann alte Datensätze in Weaviate, um alte Datenreste zu vermeiden.
Da der Worker sequenziell operiert, ist gewährleistet, dass keine Schreibvor-
gänge auf inkonsistente Zwischenstände während des Lösch- und Schreib-
vorgangs erfolgen.
6.3  Aufbau der Docker-Container
Die Bereitstellung erfolgt containerisiert mittels Docker Compose, um eine konsis-
tente Umgebung für heterogene Stacks zu gewährleisten.
## 33

## 6  Implementierung
6.3.1  Container-Dienste
Die Architektur umfasst folgende Dienste:
-  BaSyx AAS Environment: Dieser Dienst beinhaltet die AAS-Registry und das
Submodell-Repository als primäre Ereignisquellen.
-  Apache Kafka Stack: Dies ist die zentrale Event-Struktur und vereinfacht die
Infrastruktur durch eine integrierte Metadatenverwaltung. Der Stack koordi-
niert über Connect-Worker die Synchronisation des Graph-Service für Neo4j
sowie den Vektor-Service für die VDB.
-  Speicherschicht:  Die  Datenbanken  werden  mit  dedizierten  Docker  Volu-
mes betrieben, um die Integrität des KG und der Vektoren über Container-
Neustarts hinweg zu garantieren.
## 6.3.2  Konfiguration
Die  Konfiguration  erfolgt  über  .env-Dateien,  wodurch  eine  strikte  Trennung  zwi-
schen Infrastruktur-Parametern und sensiblen API-Schlüsseln gewahrt bleibt. Die
netzwerkseitige  Absicherung  wird  über  Docker  Compose  realisiert.  Durch  die
Definition dedizierter Docker-Netzwerke wird sichergestellt, dass die Datenbank-
Schnittstellen  isoliert  bleiben  und  ausschließlich  für  autorisierte  Worker-Dienste
innerhalb des Clusters erreichbar sind.
6.4  Integration in Chatbot
Die finale Wertschöpfung erfolgt über die Low-Code-Plattform Flowise, basierend
auf LangGraph. Wie in Abbildung 6.2 dargestellt, wird hierfür ein modularer „Ag-
entflow“ erstellt, der den Informationsfluss vom Benutzereingang bis zur Antwort
steuert.
6.4.1  Agentische Architektur mittels MCP
Die Integration nutzt das MCP als Standard-Schnittstelle. Im visuellen Workflow
von  Abbildung  6.2  bildet  der  rechte  Knoten  „Agent“  das  Kernstück,  an  den  die
notwendigen Werkzeuge angebunden sind. Der Agent nutzt dabei zwei spezifische
MCP-Server,  die  in  Abbildung  6.2  durch  die  zwei  Klammer-Symbole  unter  dem
Agenten-Icon repräsentiert werden. Als Modell für den Chatbot wurde gpt-4o von
OpenAI genutzt.
## 34

## 6  Implementierung
Abbildung 6.2: Flowchart eines Agentflows mit den Integrierten MCPs
-  Neo4j MCP Tool: Cypher-Abfragen zur strukturellen Analyse des Digitalen
## Zwillings.
-  Weaviate MCP Tool: Semantische Suche mit Metadaten-Filtern.
Der  Einsatz  von  MCP  ist  hierbei  von  entscheidender  Bedeutung,  denn  es
macht die präzise Filterung in Flowise erst praktikabel, da die Standard-Weaviate-
Integration keine Metadatenfilterung bietet. Die Einhaltung der Metadatenfilterung
wird  durch  die  MCP-seitige  Argument-Validierung  sichergestellt.  Anfragen  ohne
den  verpflichtenden  Parameter  submodel_id  werden  mit  einer  Exception  abge-
lehnt, was den Agenten zur Korrektur zwingt. Während der System-Prompt hilft,
dass ein Aufruf ohne submodel_id in der Praxis selten vorkommt, stellt diese co-
debasierte Validierung den eigentlichen Schutzmechanismus und die einzige ver-
lässliche Garantie für die Mandantentrennung dar, da ein Prompt allein für unsicher
wäre.
Darüber  hinaus  ermöglicht  MCP  eine  saubere  Implementierungsabstraktion.
Die  Vektordatenbank  bleibt  austauschbar  und  das  Embedding-Modell  wird  zen-
tral  im  MCP-Service  verwaltet.  Der  Agent  bekommt  lediglich  saubere,  semanti-
sche Schnittstellen wie „search_documents“ zur Verfügung gestellt und muss keine
Low-Level-Details der Vektordatenbank kennen. Dies macht den Aufbau zu einem
Paradebeispiel für den Zweck von MCP. Eine standardisierte Schnittstelle für spe-
zialisierte Funktionalität, die der Agent effizient nutzen kann, ohne die technische
Implementierung im Detail kennen zu müssen.
6.4.2  Hybrid-RAG Reasoning Loop
Der Workflow folgt einem Reasoning-Loop, der durch die Verbindungslinien zwi-
schen  Start  und  dem  Agenten  visualisiert  wird.  Zunächst  identifiziert  der  Agent
## 35

## 6  Implementierung
mittels Neo4j-Tool das betroffene Asset. Die Pfad-Informationen des Assets wer-
den  als  Filter  an  das  Weaviate-Tool  übergeben.  Die  semantische  Suche  erfolgt
exklusiv im Kontext dieses Assets, was Cross-Asset-Leakage verhindert. Das Er-
gebnis dieses Prozesses wird schließlich an den Nutzer zurückgegeben.
## 36

7  Evaluation der Funktionalität
Die Evaluation der Funktionalität prüft, ob der Hybrid-RAG-Ansatz durch die Ver-
knüpfung von KG und VDB eine faktisch korrekte Informationsextraktion ermög-
licht.  Ziel  ist  es,  die  automatisierte  Dokumentverarbeitung  für  industrielle  Assis-
tenzsysteme zu evaluieren, indem die inhaltliche Fehlerfreiheit der Antworten des
KI-Agenten gegenüber der Quelldokumentation sichergestellt wird.
7.1  Methodische Erläuterung der Testfälle
Zur Überprüfung der korrekten Beantwortung dient eine Versuchsreihe auf Basis
des autonomen mobilen Roboters MiR100. Die methodische Grundlage bildet ein
Katalog aus zehn gezielten Testfragen, die darauf ausgelegt sind, die Korrektheit
der Antworten bei unterschiedlichen Informationstypen zu validieren. Dazu gehö-
ren technische Fakten über konkrete Handlungsabläufe bis hin zu sicherheitskri-
tischen  Grenzwerten.  Die  Testfragen  nutzen  die  technische  Dokumentation  des
MiR100, die als PDF-Dokument innerhalb der AAS hinterlegt wurde.
Der  erste  Teil  umfasst  sieben  englischsprachige  Fragen  zu  technischen  Spe-
zifikationen.  Die  Korrektheit  wird  hierbei  an  der  Übereinstimmung  mit  den  Soll-
Informationen gemessen, wie etwa der Angabe der maximalen Nutzlastkapazität
von 100 kg oder der Höchstgeschwindigkeit von 1,5 m/s. Des Weiteren wird ge-
prüft, ob der Agent Systemkomponenten und deren Funktionen fehlerfrei identi-
fiziert. So muss korrekt angegeben werden, dass die Steuerung über ein Web-
Interface erfolgt und die zwei SICK-Laserscanner ein 270-Grad-Sichtfeld zur Hin-
derniserkennung bieten. Auch die Differenzierung zwischen Sensortypen, wie der
3D-Tiefenkamera zur Erkennung von Objekten auf dem Boden außerhalb der Sca-
nebene der Laser, dient als Maßstab für die richtige Wiedergabe der Fakten. Zu-
dem wird die inhaltliche Richtigkeit durch die Abfrage des Einsatzbereichs geprüft,
bei der das System die ausschließliche Eignung des MiR100 für den Innenbereich
bestätigen  muss.  Ergänzend  wird  die  Information  zur  Batterielaufzeit  abgefragt,
wobei eine korrekte Antwort für eine vollständige Ladung bis zu 3 Stunden bein-
halten muss.
Der zweite Teil besteht aus drei deutschsprachigen Fragen, welche die Korrekt-
heit bei sprachenübergreifenden Abfragen validieren. Da das Quelldokument eng-
lischsprachig ist, wird geprüft, ob die semantische Abbildung zu inhaltlich richtigen
Antworten führt. Dies umfasst Fragen zur Erstellung der Navigationskarte, sowie si-
cherheitsrelevante Grenzwerte. Ein Punkt ist die maximal zulässige Steigung des
## 37

7  Evaluation der Funktionalität
Untergrunds, die exakt mit 5 % angegeben werden muss, um als korrekt beant-
wortet zu gelten. Den Abschluss bildet die Prüfung der Reaktion beim Betreten der
Sicherheitszone durch eine Person, wobei der Agent den erzwungenen Notstopp
als einzig richtige Antwort identifizieren muss.
Die  Bewertung  erfolgt  methodisch  durch  einen  direkten  Soll-Ist-Vergleich  der
Agenten-Antworten  mit  den  verifizierten  Daten  der  Originaldokumentation.  Der
zweistufige  Prozess,  bei  dem  zunächst  der  strukturelle  Kontext  aus  Neo4j  ab-
gerufen wird, dient hierbei als Validierungsebene, um die semantische Suche in
Weaviate auf das korreket Asset einzugrenzen und somit falsche Antworten durch
Fehlzuordnungen zu vermeiden.
## 7.2  Tabellarische Ergebnisauswertung
Die systematische Überprüfung der Testfälle erfolgt durch einen Abgleich der ge-
nerierten Antworten mit den in der Dokumentation hinterlegten Referenzwerten.
Zur Dokumentation wurde für jede der zehn Anfragen eine Abbildung erstellt, die-
se sind im Anhang einsehbar, der die Ausgabe des Agenten visualisiert. Die Aus-
wertung zeigt, dass alle zehn Testfragen inhaltlich korrekt beantwortet wurden. In
der folgenden Tabelle 7.1 wird die Übereinstimmung der zentralen Fakten für eine
Auswahl der Testfälle gegenübergestellt:
Tabelle 7.1: Soll-Ist-Vergleich der Antwortkorrektheit
MerkmalSoll-Information
(Referenz)
Ist-Information
(Agent)
## Status
Max. Nutzlast100 kg100 kgBestanden
SteuerungWeb-InterfaceWeb-InterfaceBestanden
Laserscanner270°-Sichtfeld270°-SichtfeldBestanden
Max. Geschwindigkeit1,5 m/s (5,6 km/h)1,5 m/s (5,6 km/h)Bestanden
Ladedauerbis zu 3 Stundenbis zu 3 StundenBestanden
3D-KameraHinderniserkennungHinderniserkennungBestanden
EinsatzbereichNur InnenbereichNur InnenbereichBestanden
NavigationskarteIntern / CAD-ImportInternBestanden
Max. Steigung5 %5 %Bestanden
SicherheitszoneNotstoppNotstoppBestanden
Die fehlerfreie Extraktion numerischer Parameter wie der Nutzlast oder der Stei-
gungsgrenze belegt, dass die Markdown-Konvertierung durch Docling die struktu-
relle Integrität der technischen Datenblätter erfolgreich bewahrt hat. Ebenfalls zu
erwähnen ist, dass auch bei den deutschsprachigen Fragen inhaltlich richtige Ant-
worten geliefert wurden, obwohl die Primärquelle in englischer Sprache vorliegt.
Auch Tippfehlern innerhalb der Frage wie bei Anhang A.8 zu sehen, wird eine kor-
## 38

7  Evaluation der Funktionalität
rekte Antwort gegeben. Dies bestätigt die Leistungsfähigkeit des gewählten multi-
lingualen Embedding-Modells im Rahmen der Hybrid-RAG-Architektur.
7.3  Analyse des agentenbasierten
## Abfrageprozesses
Neben der inhaltlichen Korrektheit wird auch der technische Ablauf der Informati-
onsbeschaffung evaluiert. Hierfür wurde die operative Durchführung des Hybrid-
RAG Reasoning Loops des Agenten dokumentiert. Der Prozess lässt sich in drei
wesentliche Schritte unterteilen:
-  Strukturelle   Kontext-Identifikation:   Nach   Eingang   der   Nutzerfrage   nutzt
der  Agent  das  Neo4j  MCP  Tool.  Durch  eine  Cypher-Abfrage  ermittelt
er  das  betroffene  Asset  und  die  zugehörige  submodelId  des  Handover-
Documentation-Submodells. Sollte er nach dem ersten Versuch noch keine
betroffene Asset gefunden haben, probiert er es erneut. Dieses Vorgehen
zeigen die Abbildungen A.11 und A.12 aus dem Anhang.
-  Semantische  Filterung:  Die  aus  dem  KG  gewonnenen  Metadaten  werden
als  Filterparameter  an  das  Weaviate  MCP  Tool  übergeben.  Dieser  Schritt
stellt sicher, dass die semantische Suche mathematisch auf den Vektorraum
des korrekten Dokuments begrenzt wird, wodurch Information-Leakage von
anderen Assets ausgeschlossen wird. Dieser Aufruf wird in Abbildung A.13
gezeigt.
-  Ergebnissynthese:  Der  Agent  empfängt  die  relevanten  Textsegmente,  wie
zum Beispiel die Spezifikationen der SICK-Laserscanner und generiert dar-
aus die finale Antwort, die im Beispiel der Laserscanner in Abbildung A.3 zu
sehen ist.
Die Analyse bestätigt, dass das MCP eine effektive agentische Orchestrierung
ermöglicht. Der Agent nutzt die Datenbanken dabei nicht als statische Reposito-
rien. Stattdessen interagiert er über das MCP mit spezialisierten Tools. Dies stellt
eine faktengestützte Antwortgenerierung sicher, die strikt an den Kontext des je-
weiligen Assets gebunden ist.
## 39

8  Fazit und Ausblick
8.1  Zusammenfassung der Arbeit
Die  vorliegende  Bachelorarbeit  adressiert  die  Herausforderung  in  modernen
Industrie-4.0-Umgebungen, unstrukturierte Datenbestände innerhalb von AAS ef-
fizient nutzbar zu machen. Während die AAS als digitaler Repräsentant physischer
Assets bereits eine strukturierte Abbildung technologischer Parameter und hierar-
chischer Beziehungen ermöglicht, bleiben die inhaltlichen Informationen der refe-
renzierten technischen Dokumentationen für automatisierte Systeme weitgehend
unzugänglich. Ziel der Arbeit ist die Entwicklung und Implementierung einer Ar-
chitektur, die diese unstrukturierten Daten automatisiert erschließt und über eine
agentenbasierte Schnittstelle mittels hybrider RAG abfragbar macht.
Das technologische Fundament bildet die Erweiterung eines bestehenden AAS-
Kafka-Neo4j-Connectors. In dieser ereignisgesteuerten Architektur fungiert Apa-
che Kafka als zentraler Message Broker. Dieser erfasst Zustandsänderungen in-
nerhalb der BaSyx-Plattform in Echtzeit und verteilt diese an nachgelagerte Diens-
te. Ein wesentliches wissenschaftliches Ergebnis der Arbeit ist die Konzeption einer
sogenannten „Split-Worker-Strategie“. Da die Verarbeitung von PDF-Dokumente
signifikant zeitintensiver ist als die Aktualisierung struktureller Metadaten im Wis-
sensgraphen,  sieht  die  Architektur  eine  funktionale  Trennung  vor.  Der  Graph-
Service und der Vektor-Service operieren als unabhängige Konsumenten, wodurch
eine zeitweise Inkonsistenz im Vektorspeicher zugunsten der Performance des Ge-
samtsystems in Kauf genommen wird.
Für  die  semantische  Erschließung  der  Dokumente  wird  eine  spezialisierte
Service-Pipeline implementiert. Zur Textextraktion kommt das Framework „Docling“
zum Einsatz, das mittels KI-gestützter Layout-Analyse und Tabellenerkennung si-
cherstellt,  dass  die  visuelle  Struktur  technischer  Dokumente  in  ein  Markdown-
Format überführt wird. Die anschließende Segmentierung erfolgt unter Anwendung
eines rekursiven Trennverfahrens mit definiertem Überfluss, um den Kontext über
Segmentgrenzen hinweg zu bewahren. Zur Speicherung der resultierenden hoch-
dimensionalen Vektoren wurde Weaviate als KI-native Vektordatenbank gewählt.
Ausschlaggebend hierfür war der klare Fokus auf KI. Ein kritischer Aspekt der Im-
plementierung ist die Gewährleistung der Datenintegrität und Systemstabilität. Um
redundante Berechnungen und Datenredundanz zu vermeiden, nutzt der Vektor-
Service eine Idempotenz-Logik auf Basis der submodelId und des smElementPath.
Die Nutzbarmachung der Daten erfolgt schließlich über einen Hybrid-RAG Re-
## 40

8  Fazit und Ausblick
asoning Loop. Hierbei agiert ein KI-Agent über das MCP als Orchestrator. In ei-
nem zweistufigen Prozess wird zunächst der strukturelle Kontext aus dem Wis-
sensgraphen  abgerufen,  um  die  anschließende  semantische  Suche  in  der  Vek-
tordatenbank durch Metadaten-Filter präzise auf das relevante Asset einzugren-
zen. Die Evaluation des entwickelten „Proof-of-Concept“ bestätigt die Funktionali-
tät des Systems. Anhand definierter Testfälle konnte nachgewiesen werden, dass
der Agent in der Lage ist, technische Anfragen wahrheitsgetreu auf Basis der in die
AAS integrierten Dokumente zu beantworten. Die Arbeit leistet somit einen wich-
tigen Beitrag zur Transformation der AAS von einem passiven Datencontainer zu
einer aktiven, intelligenten Wissensbasis in industriellen Assistenzsystemen.
8.2  Ausblick auf zukünftige Entwicklungen
Der Ausblick auf zukünftige Entwicklungen verdeutlicht, dass die in dieser Arbeit
geschaffene  Architektur  lediglich  den  Grundstein  für  eine  umfassende  semanti-
sche Erschließung der AAS legt. Ein wesentlicher nächster Schritt besteht in der
Erweiterung des Systems auf multimodale Inhalte. Da technische Dokumentatio-
nen in der Industrie 4.0 oft von visuellen Informationen geprägt sind, reicht eine
rein textbasierte Erschließung oft nicht aus. Zukünftige Erweiterungen sollten da-
her Vision-Language-Modelle integrieren, die in der Lage sind, Bildinhalte seman-
tisch zu interpretieren und diese als Vektoren in der Datenbank abzuspeichern.
Dies würde es dem Agenten ermöglichen, Fragen zu Bauteilen zu beantworten,
die nur visuell in einem Diagramm dargestellt sind, oder Wartungsanleitungen ba-
sierend auf Bilderkennung präziser auszuwerten.
Darüber hinaus bietet die Optimierung der Embedding-Strategien ein erhebli-
ches Potenzial zur Steigerung der Abfragequalität. Während der aktuelle Proto-
typ auf Standardmodellen zur Vektorisierung basiert, könnten zukünftige Iteratio-
nen auf domänenspezifische Sprachmodelle zurückgreifen, die speziell mit tech-
nischem Vokabular aus dem Maschinen- und Anlagenbau trainiert wurden. Dies
würde die Trennschärfe bei der Suche nach sehr ähnlichen technischen Begriffen
verbessern.
Schließlich könnte die Implementierung fortschrittlicher RAG-Strategien ein er-
hebliches Potenzial bieten, um die Verlässlichkeit des Systems weiter zu steigern.
Durch den Einsatz von Self-RAG-Verfahren zur autonomen Validierung der gene-
rierten Antworten oder Reranking-Algorithmen zur präziseren Sortierung der abge-
rufenen Kontexte könnte die Relevanz der gelieferten Informationen im operativen
Betrieb kontinuierlich optimiert werden.
## 41

## Schlusswort
Zusammenfassend lässt sich festhalten, dass die im Rahmen dieser Arbeit ent-
wickelte Architektur einen funktionalen Weg aufzeigt, um die semantische Lücke
innerhalb der AAS zu schließen. Auch wenn die Implementierung als „Proof-of-
Concept“  Limitationen  hinsichtlich  der  Multimodalität  und  der  Verarbeitungsge-
schwindigkeit  aufweist,  evaluiert  sie  den  konzeptionellen  Ansatz  einer  ereignis-
gesteuerten, automatisierten Datenerschließung. Die Weiterentwicklung der AAS
von einer rein strukturgebenden digitalen Repräsentation hin zu einer aktiven, in-
telligenten Wissensbasis schafft damit die notwendige Grundlage für zukünftige
industrielle Assistenzsysteme, die Informationen nicht nur verwalten, sondern kon-
textbezogen verstehen und bereitstellen können.
## 42

## Anhang
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
Sicherheitskomponenten. Bei internen Fehlern im Sicherheitskreis geht der Roboter sofort in den Notstopp, was bedeutet,
dass alle beweglichen Teile durch mechanische Trennung spannungsfrei werden. Nur wenn die Redundanz gewährleistet
ist, kann der Notstopp zurückgesetzt und der Betrieb fortgesetzt werden.
Diese Informationen stammen aus dem Benutzerhandbuch des MiR100.
What is the maximum payload weight the MiR100 can carry on top?
The maximum payload weight that the MiR100 can carry on top is 100 kg.
How is the MiR100 controlled by the user?
The MiR100 is controlled by the user through a web interface. Users can provide the destination for product delivery, and
the MiR100 can be set up to run a fixed route, be called on demand, or perform a special operation. The vehicle has a
## Process Flow
read_neo4j_cypherread_neo4j_cypherread_neo4j_cypher
## Process Flow
read_neo4j_cypherread_neo4j_cypherread_neo4j_cyphersearch_documents
Type your question...
Abbildung A.1: Frage zu der maximalen Nutzlast
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
The maximum payload weight that the MiR100 can carry on top is 100 kg.
How is the MiR100 controlled by the user?
The MiR100 is controlled by the user through a web interface. Users can provide the destination for product delivery, and
the MiR100 can be set up to run a fixed route, be called on demand, or perform a special operation. The vehicle has a
programmable map that allows it to navigate and avoid obstacles automatically. Each MiR100 has its own network, and
specific locations can be programmed into its internal map for logistical planning.
According to the PDF documentation, the MiR100 is designed to transport materials internally within various industrial
locations, such as factories and hospitals. The user interface allows for flexible operation modes, including fixed routes
and on-demand services.
What are the three different drive modes available for the MiR100?
## _j_yp_j_yp_j_yp
## Process Flow
read_neo4j_cypherread_neo4j_cypherread_neo4j_cyphersearch_documents
## Process Flow
Type your question...
Abbildung A.2: Frage zu der Nutzersteuerung
## 43

## Anhang
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
its operation. The sensors on the vehicle are designed to detect and avoid objects above 50 mm from the floor level,
which further indicates that it is optimized for indoor environments.
What is the purpose of the two SICK laser scanners located on the front and back corners?
The SICK laser scanners located on the front and back corners of the vehicle serve several purposes:
- Visual Protection: The laser scanners provide a 270° visual protection range, which is crucial for detecting
obstacles and ensuring safe navigation in environments with people and objects.
- Obstacle Detection: They are part of the vehicle's external sensors, which include cameras and ultrasonic
sensors, to detect obstacles and adjust the vehicle's route accordingly.
- Safety and Control: The SICK safety modules facilitate communication between sensor signals and the
vehicle's control system, ensuring safe operation.
- Maintenance: Regular cleaning of the laser sensors' optics cover is recommended for optimal performance,
using specific cleaning agents and materials as per the manufacturer's guidelines.
These functionalities help the vehicle operate safely and efficiently in populated workspaces, making real-time
adjustments to its path as needed.
## Process Flow
read_neo4j_cypherread_neo4j_cyphersearch_documents
Type your question...
Abbildung A.3: Frage zu den Laserscannern
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
- Left turn
## 3. Reverse
These modes enable the MiR100 to navigate effectively in environments similar to those accessible by a wheelchair,
handling up to a 5% grade.
What is the maximum speed of the MiR100?
According to the PDF documentation, the maximum speed of the MiR100 is 1.5 meters per second (5 feet per second),
which corresponds to 5.6 kilometers per hour (3.5 miles per hour).
How long does a full battery charge take?
To provide an accurate answer, I need to know which specific asset or product you are referring to. Could you please
provide the name or identifier of the asset?
## Process Flow
read_neo4j_cypherread_neo4j_cypherread_neo4j_cyphersearch_documents
## Process Flow
Type your question...
Abbildung A.4: Frage zu der maximalen Geschwindigkeit
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
To provide an accurate answer, I need to know which specific asset or product you are referring to. Could you please
provide the name or identifier of the asset?
How long does a full battery charge take? mir100
According to the PDF documentation for the MiR100, a full battery charge takes up to 3 hours. The charger will show a
green light when the battery is fully charged. Additionally, it is noted that charging can start while the vehicle is shutting
down, which may take a couple of minutes.
What is the purpose of the 3D depth camera?
## Process Flow
## Process Flow
read_neo4j_cypherread_neo4j_cypherread_neo4j_cyphersearch_documents
## Process Flow
d4jhd4jhhdt
Type your question...
Abbildung A.5: Frage zu der Ladedauer
## 44

## Anhang
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
I searched both the structured data and the PDF documentation but found no specific information about the purpose of a
3D depth camera in the available resources. If you have more context or specific details about the asset or system you're
referring to, please let me know, and I can try searching again.
What is the purpose of the 3D depth camera? mir100
The 3D depth camera on the MiR100 is used to detect objects on the floor and outside the laser plane. This functionality
is crucial for the vehicle to navigate safely and effectively in environments where obstacles may be present. The camera
helps in identifying objects that are not detected by other sensors, ensuring the vehicle can adjust its path accordingly.
This information is sourced from the MiR100 user guide.
Is the MiR100 suitable for outdoor use?
read_neo4j_cypherread_neo4j_cyphersearch_documents
## Process Flow
read_neo4j_cypherread_neo4j_cypherread_neo4j_cyphersearch_documents
## Process Flow
Type your question...
Abbildung A.6: Frage zu den 3D-Kameras
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
The 3D depth camera on the MiR100 is used to detect objects on the floor and outside the laser plane. This functionality
is crucial for the vehicle to navigate safely and effectively in environments where obstacles may be present. The camera
helps in identifying objects that are not detected by other sensors, ensuring the vehicle can adjust its path accordingly.
This information is sourced from the MiR100 user guide.
Is the MiR100 suitable for outdoor use?
According to the PDF documentation for the MiR100, the vehicle is designed to operate on a level, dry floor. This suggests
that it is not suitable for outdoor use, as outdoor environments may not provide the level and dry conditions required for
its operation. The sensors on the vehicle are designed to detect and avoid objects above 50 mm from the floor level,
which further indicates that it is optimized for indoor environments.
What is the purpose of the two SICK laser scanners located on the front and back corners?
## Process Flow
read_neo4j_cypherread_neo4j_cypherread_neo4j_cyphersearch_documents
## Process Flow
readneo4jcypherreadneo4jcyphersearchdocuments
Type your question...
Abbildung A.7: Frage zu dem Einsatzbereich
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
Hi there! How can I help?
Hat der mir100 für die Navigaton eine Karte?
Ja, der MiR100 verfügt über eine Karte, die bei der ersten Nutzung des Fahrzeugs programmiert werden kann. Während
des Betriebs vermeidet der MiR100 automatisch Hindernisse, die nicht auf der Karte verzeichnet sind, wie Personen oder
Möbel. Die interne Karte des MiR100 enthält spezifische Orte, die für die logistische Planung genutzt werden können.
Dies ermöglicht es dem Fahrzeug, Routen zu planen und anzupassen, wenn es auf nicht kartierte Hindernisse stößt.
Laut der PDF-Dokumentation kann der Benutzer das Ziel der Produktlieferung über eine Webschnittstelle angeben, und
der MiR100 kann so eingerichtet werden, dass er eine feste Route fährt, auf Abruf gerufen wird oder eine spezielle
Mission ausführt.
Welche Steigung darf der Untergrund maximal haben?
## Process Flow
read_neo4j_cypherread_neo4j_cyphersearch_documents
ProcessFlow
Type your question...
Abbildung A.8: Frage zu der Navigationskarte
## 45

## Anhang
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
Laut der PDF-Dokumentation kann der Benutzer das Ziel der Produktlieferung über eine Webschnittstelle angeben, und
der MiR100 kann so eingerichtet werden, dass er eine feste Route fährt, auf Abruf gerufen wird oder eine spezielle
Mission ausführt.
Welche Steigung darf der Untergrund maximal haben?
Laut der PDF-Dokumentation des MiR100 darf die maximale Steigung des Untergrunds 5% nicht überschreiten. Eine
Steigung über 5% kann zu einem Rutschen des Fahrzeugs führen, was ein Risiko für Personenschäden und Schäden am
Fahrzeug darstellt.
Was passiert, wenn eine Person in die Sicherheitszone des Roboters tritt?
Wenn eine Person oder ein anderes bewegliches Objekt in die Sicherheitszone des Roboters MiR100 eintritt und der
## Process Flow
read_neo4j_cypherread_neo4j_cyphersearch_documents
## Process Flow
read_neo4j_cypherread_neo4j_cyphersearch_documents
Type your question...
Abbildung A.9: Frage zu der maximalen Steigung
Start (Input)
Agent (System Prompt)
gpt-4o
## React Flow
HybridRAG
## Clear Chat
Fahrzeug darstellt.
Was passiert, wenn eine Person in die Sicherheitszone des Roboters tritt?
Wenn eine Person oder ein anderes bewegliches Objekt in die Sicherheitszone des Roboters MiR100 eintritt und der
Planer aufgrund von Reaktionszeit, Fehlern usw. nicht reagiert, wird der Sicherheitskreis den Roboter in einen Notstopp
versetzen, und der Roboter stoppt sofort. Sobald die Person oder das Objekt die Sicherheitszone wieder verlassen hat,
wird der Notstopp automatisch zurückgesetzt.
Der MiR100 ist mit einem vollständig redundanten elektrischen Sicherheitskreis ausgestattet, einschließlich Sick-
Sicherheitskomponenten. Bei internen Fehlern im Sicherheitskreis geht der Roboter sofort in den Notstopp, was bedeutet,
dass alle beweglichen Teile durch mechanische Trennung spannungsfrei werden. Nur wenn die Redundanz gewährleistet
ist, kann der Notstopp zurückgesetzt und der Betrieb fortgesetzt werden.
Diese Informationen stammen aus dem Benutzerhandbuch des MiR100.
What is the maximum payload weight the MiR100 can carry on top?
## Process Flow
read_neo4j_cypherread_neo4j_cyphersearch_documents
Type your question...
Abbildung A.10: Frage zu der Sicherheitszone
## 46

## Anhang
MATCH (aas:AssetAdministrationShell {id: 'aas_id_from_step_2'})-[:HAS_SUBMODEL]->(sm:Submodel)-[:HAS_ELEMENT*]-
>(file:File)
WHERE file.contentType = 'application/pdf'
RETURN DISTINCT sm.id AS submodel_id, sm.idShort AS submodel_idShort, file.idShort AS file_idShort
## ```
→ Extract Submodel IDs that have PDF Files
- IMMEDIATELY call search_documents for each Submodel ID that has PDF Files:
- query: "[semantic search terms about the feature]" (translated to English if needed)
- submodel_id: <THE ACTUAL URI-FORMAT ID YOU EXTRACTED IN STEP 3>
- idShortPath: file_idShort from step 3 (if available)
- Return the answer based on the retrieved chunks
**NEVER end with "Shall I search?" or "Let me know if you want me to proceed" - JUST DO IT!**
Keep responses concise and well-structured. Avoid excessive formatting.
user
What is the purpose of the two SICK laser scanners located on the front and back corners?
assistant
No data
toolread_neo4j_cypher
Custom MCP
call_cVA5IzhQKYeXIYGkTpQkHVf4
## [
## {
## "type":"text",
## "text":"[]"
## }
## ]
assistant
No data
toolread_neo4j_cypher
Custom MCP
call_rFE2zK98zxrsFKuJtjqZ1hle
## [
## {
## "type":"text",
"text":"[{\"submodel_id\": \"http://aas.dfki.de/ids/sm/identification_10000000\", \"submodel_idShort\":
\"Identification\", \"file_idShort\": \"Documentation\"}]"
## }
## ]
assistant
## {
## "name":"read_neo4j_cypher",
## "args": {
"query":"MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]-&gt;(sm:Submodel)-[:HAS_ELEMENT*]-
&gt;(prop:Property) WHERE toLower(prop.value) CONTAINS 'sick laser scanner' RETURN DISTINCT aas.id AS
aas_id, sm.id AS submodel_id, sm.idShort AS submodel_idShort"
## },
## "type":"tool_call",
"id":"call_cVA5IzhQKYeXIYGkTpQkHVf4"
## }
Custom MCPCalled
## {
## "name":"read_neo4j_cypher",
## "args": {
"query":"MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]-&gt;(sm:Submodel)-[:HAS_ELEMENT*]-
&gt;(file:File) WHERE file.contentType = 'application/pdf' RETURN DISTINCT sm.id AS submodel_id, sm.idShort
AS submodel_idShort, file.idShort AS file_idShort"
## },
## "type":"tool_call",
"id":"call_rFE2zK98zxrsFKuJtjqZ1hle"
## }
Custom MCPCalled
## {
## "name":"search_documents",
## "args": {
"query":"purpose of SICK laser scanners on front and back corners",
## "submodel_id":"http://aas.dfki.de/ids/sm/identification_10000000",
"idShortPath":"Documentation",
## "limit":5
## },
## "type":"tool_call",
Custom MCPCalled
Abbildung A.11: Erster Neo4j MCP Aufruf
## 47

## Anhang
MATCH (aas:AssetAdministrationShell {id: 'aas_id_from_step_2'})-[:HAS_SUBMODEL]->(sm:Submodel)-[:HAS_ELEMENT*]-
>(file:File)
WHERE file.contentType = 'application/pdf'
RETURN DISTINCT sm.id AS submodel_id, sm.idShort AS submodel_idShort, file.idShort AS file_idShort
## ```
→ Extract Submodel IDs that have PDF Files
- IMMEDIATELY call search_documents for each Submodel ID that has PDF Files:
- query: "[semantic search terms about the feature]" (translated to English if needed)
- submodel_id: <THE ACTUAL URI-FORMAT ID YOU EXTRACTED IN STEP 3>
- idShortPath: file_idShort from step 3 (if available)
- Return the answer based on the retrieved chunks
**NEVER end with "Shall I search?" or "Let me know if you want me to proceed" - JUST DO IT!**
Keep responses concise and well-structured. Avoid excessive formatting.
user
What is the purpose of the two SICK laser scanners located on the front and back corners?
assistant
No data
toolread_neo4j_cypher
Custom MCP
call_cVA5IzhQKYeXIYGkTpQkHVf4
## [
## {
## "type":"text",
## "text":"[]"
## }
## ]
assistant
No data
toolread_neo4j_cypher
Custom MCP
call_rFE2zK98zxrsFKuJtjqZ1hle
## [
## {
## "type":"text",
"text":"[{\"submodel_id\": \"http://aas.dfki.de/ids/sm/identification_10000000\", \"submodel_idShort\":
\"Identification\", \"file_idShort\": \"Documentation\"}]"
## }
## ]
assistant
## {
## "name":"read_neo4j_cypher",
## "args": {
"query":"MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]-&gt;(sm:Submodel)-[:HAS_ELEMENT*]-
&gt;(prop:Property) WHERE toLower(prop.value) CONTAINS 'sick laser scanner' RETURN DISTINCT aas.id AS
aas_id, sm.id AS submodel_id, sm.idShort AS submodel_idShort"
## },
## "type":"tool_call",
"id":"call_cVA5IzhQKYeXIYGkTpQkHVf4"
## }
Custom MCPCalled
## {
## "name":"read_neo4j_cypher",
## "args": {
"query":"MATCH (aas:AssetAdministrationShell)-[:HAS_SUBMODEL]-&gt;(sm:Submodel)-[:HAS_ELEMENT*]-
&gt;(file:File) WHERE file.contentType = 'application/pdf' RETURN DISTINCT sm.id AS submodel_id, sm.idShort
AS submodel_idShort, file.idShort AS file_idShort"
## },
## "type":"tool_call",
"id":"call_rFE2zK98zxrsFKuJtjqZ1hle"
## }
Custom MCPCalled
## {
## "name":"search_documents",
## "args": {
"query":"purpose of SICK laser scanners on front and back corners",
## "submodel_id":"http://aas.dfki.de/ids/sm/identification_10000000",
"idShortPath":"Documentation",
## "limit":5
## },
## "type":"tool_call",
Custom MCPCalled
Abbildung A.12: Zweiter Neo4j MCP Aufruf
## 48

## Anhang
No data
toolread_neo4j_cypher
Custom MCP
call_rFE2zK98zxrsFKuJtjqZ1hle
## [
## {
## "type":"text",
"text":"[{\"submodel_id\": \"http://aas.dfki.de/ids/sm/identification_10000000\", \"submodel_idShort\":
\"Identification\", \"file_idShort\": \"Documentation\"}]"
## }
## ]
assistant
No data
toolsearch_documents
Custom MCP
call_WcEXmVlJbB6ntJsZtiPjyh4I
## [
## {
## "type":"text",
"text":"{\"results\":[{\"text\":\"|   2 | 12V Power Supply                 | Power to the NUC and router.
|  12 | NUC PC                                        | The main computer.                                                                    |\\n|   3 | Motor
controller                 | Manages the two motor drives.                                     |  13 | SICK laser scanner 1                          |
Front laser scanner                                                                   |\\n|   4 | Redundant drive                  | Relays controlled by
SICK modules supplying the motor controller. |  14 | SICK laser scanner 2                          | Rear laser scanner.
## |\",\"metadata\":
{\"submodel_id\":\"http://aas.dfki.de/ids/sm/identification_10000000\",\"idShortPath\":\"Documentation\",\"source\":\"Mi
R100-User-guide.pdf\"},\"distance\":0.40214282274246216},{\"text\":\"| Charging time:                       | Up to 3 hours
(0-80% 2 hours)            |\\n|--------------------------------------|------------------------------------------|\\n| SICK
laser scanners (2pcs)           |                                          |\\n| Range:                               | 270° visual protection
|\\n| Visual indicators                    |                                          |\\n| LED color light bar (on four sides): | Indication of
operating status           |\\n| Audio indicators                     |                                          |\\n| Built-in loudspeaker:                |
3 W(below 60 dB)                         |\\n| Top module                           |                                          |\",\"metadata\":
{\"submodel_id\":\"http://aas.dfki.de/ids/sm/identification_10000000\",\"idShortPath\":\"Documentation\",\"source\":\"Mi
R100-User-guide.pdf\"},\"distance\":0.40265417098999023},{\"text\":\"- 9 Place the lid and tie down the box making
sure the lid does not come undone.\\n\\n&lt;!-- image --&gt;\\n\\n&lt;!-- image --&gt;\\n\\n&lt;!-- image --&gt;\\n\\n## 6
Maintenance\\n\\nTest the vehicle regularly and clean it with a damp cloth (No compressed air).\\n\\n1. Remove dirt
fromwheels\\n2CheckthewheelsforwearandtearThecasterwheelsshouldbereplacedonceayear\\n3Clean
## Output
The SICK laser scanners located on the front and back corners of the vehicle serve several purposes:
- Visual Protection: The laser scanners provide a 270° visual protection range, which is crucial for detecting obstacles
and ensuring safe navigation in environments with people and objects.
AS submodel_idShort, file.idShort AS file_idShort"
## },
## "type":"tool_call",
"id":"call_rFE2zK98zxrsFKuJtjqZ1hle"
## }
## {
## "name":"search_documents",
## "args": {
"query":"purpose of SICK laser scanners on front and back corners",
## "submodel_id":"http://aas.dfki.de/ids/sm/identification_10000000",
"idShortPath":"Documentation",
## "limit":5
## },
## "type":"tool_call",
"id":"call_WcEXmVlJbB6ntJsZtiPjyh4I"
## }
Custom MCPCalled
read_neo4j_cypherread_neo4j_cyphersearch_documents
Abbildung A.13: Weaviate MCP Aufruf
## 49

## Literaturverzeichnis
[1]  Eclipse, Eclipse AASX Package Explorer, Eclipse, abgerufen am 28. Januar
- [Online]. Available: https://github.com/eclipse-aaspe/package-explorer
[2]  G. Sonnenberg, P. Stein, F. Espinosa, and D. Porta, “Queryable aas graphs for
ai agents: An event-driven knowledge graph integration for aas environments,”
in 2025 IEEE 30th International Conference on Emerging Technologies and
Factory Automation (ETFA), 2025, pp. 1–8.
[3]  G.  Shao,  “Manufacturing  digital  twin  standards,”  in  Proceedings  of  the
ACM/IEEE  27th  International  Conference  on  Model  Driven  Engineering
Languages  and  Systems,  ser.  MODELS  Companion  ’24.New  York,  NY,
USA:  Association  for  Computing  Machinery,  2024,  p.  370–377.  [Online].
Available: https://doi.org/10.1145/3652620.3688250
[4]  O.  Foundation,  “Opc  30270:  Industry  4.0  asset  administration  shell,”  OPC
Foundation,  Tech.  Rep.,  6  2021,  abgerufen  am  28.  Januar  2026.  [Online].
Available: https://reference.opcfoundation.org/I4AAS/v100/docs/4.1
[5]  IDTA,Part1:Metamodel,IndustrialDigitalTwinAsso-
ciatione.V.,abgerufenam28.Januar2026.[Onli-
ne].   Available:   https://industrialdigitaltwin.org/wp-content/uploads/2025/11/
IDTA-01001-3-1-2_AAS-Specification_Part1_Metamodel.pdf
[6]  ——,   Part   5:   Package   File   Format   (AASX,   Industrial   Digital   Twin
Assosciatione.V.,abgerufenam28.Januar2026.[Online].
Available:    https://industrialdigitaltwin.io/aas-specifications/IDTA-01002/v3.1/
query-language.html
[7]  D. J. Neidig, A. Orzelski, S. Pollmeier, and J. Wende, Asset Administration
Shell  Reading  Guide,  4  2021,  abgerufen  am  28.  Januar  2026.  [Online].
Available: https://industrialdigitaltwin.org/en/wp-content/uploads/2021/09/10_
asset_administration_shell_reading_guide_en_2021.pdf
[8]  IDTA,HandoverDocumentation,IndustrialDigitalTwinAs-
sociatione.V.,abgerufenam28.Januar2026.[Onli-
ne].   Available:   https://industrialdigitaltwin.org/wp-content/uploads/2023/03/
IDTA-02004-1-2_Submodel_Handover-Documentation.pdf
[9]  Basyx About, Eclipse Foundation, abgerufen am 28. Januar 2026. [Online].
Available: https://eclipse.dev/basyx/about/
## 50

## Literaturverzeichnis
[10]  Basyx  Digitization,  Eclipse  Foundation,  abgerufen  am  28.  Januar  2026.
[Online]. Available: https://eclipse.dev/basyx/digitization/
[11]  Basyx Integrated Applications, Eclipse Foundation, abgerufen am 28. Januar
- [Online]. Available: https://eclipse.dev/basyx/integrated-applications/
[12]  D. Vohra, Practical Hadoop ecosystem, 1st ed.   New York, NY: APRESS, Oct.
## 2016.
[13]  D. D. Scott, Kafka in action.   New York, NY: Manning Publications, Mar. 2022.
[14]  N. Garg, Learning Apache Kafka -, 2nd ed.Birmingham, England: Packt
## Publishing, Feb. 2015.
[15]  R. Estrada, Apache Kafka 1.0 cookbook.Birmingham, England: Packt Pu-
blishing, Apr. 2023.
[16]  G. Shapira, T. Palino, and R. Sivaram, Kafka - the definitive guide, 2nd ed.
Sebastopol, CA: O’Reilly Media, Nov. 2021.
[17]  R. van Bruggen, Learning Neo4j.Birmingham, England: Packt Publishing,
## Aug. 2014.
[18]  J. Webber, I. Robinson, and E. Elfrem, Graph Databases 2e.Sebastopol,
CA: O’Reilly Media, Jul. 2015.
[19]  Neo4j Inc., Neo4j Graph Platform Documentation, Neo4j, abgerufen am 28.
Januar 2026. [Online]. Available: https://neo4j.com/docs/
[20]  M.  T.  Pilehvar  and  J.  Camacho-Collados,  Embeddings  in  natural  langua-
ge processing, ser. Synthesis Lectures on Human Language Technologies.
## Cham, Switzerland: Springer International Publishing, Nov. 2020.
[21]  Z. H. Leonie Monigatti, “A gentle introduction to vector databases,” Weaviate,
Tech.  Rep.,  8  2023,  abgerufen  am  28.  Januar  2026.  [Online].  Available:
https://weaviate.io/blog/what-is-a-vector-database
[22]  J. J. Pan, J. Wang, and G. Li, “Survey of vector database management sys-
tems,” Oct. 2023.
[23]  “What  is  a  chatbot?”  IBM,  Tech.  Rep.,  abgerufen  am  28.  Januar  2026.
[Online]. Available: https://www.ibm.com/think/topics/chatbots
[24]  R. Ciesla, The book of chatbots.    Cham: Springer Nature Switzerland, 2024.
## 51

## Literaturverzeichnis
[25]  S.  Bader,  E.  Barnstedt,  H.  Bedenbender,  B.  Berres,  M.  Billmann,  B.  Boss,
## N. Braunisch, A. Braunmandl, E. Clauer, C. Diedrich, B. Flubacher, W. Frit-
sche, K. Garrels, A. Gatterburg, M. Hankel, S. Heppner, M. Hoffmeister, L. Jä-
nicke, M. Jochem, and C. Ziesche, “Details of the asset administration shell.
part 1 -the exchange of information between partners in the value chain of
industrie 4.0 (version 3.0rc02),” 05 2022.
[26]  ,WhatistheModelContextProtocol(MCP)?,ModelCon-
text   Protocol,   abgerufen   am   28.   Januar   2026.   [Online].   Available:
https://modelcontextprotocol.io/docs/getting-started/intro
[27]  IDTA,  AAS  Query  Language,  Industrial  Digital  Twin  Assosciation  e.  V.,
abgerufen am 28. Januar 2026. [Online]. Available: https://industrialdigitaltwin.
io/aas-specifications/IDTA-01002/v3.1/query-language.html
[28]  F. Faltin and D. Fricke, “Concept for human-machine interfaces for resilient
data extraction from digital twins,” in Proceeding of the 33rd European Safety
and Reliability Conference.   Singapore: Research Publishing Services, 2023,
pp. 3014–3019.
[29]  A. Gan, H. Yu, K. Zhang, Q. Liu, W. Yan, Z. Huang, S. Tong, and G. Hu, “Re-
trieval augmented generation evaluation in the era of large language models:
A comprehensive survey,” Apr. 2025.
[30]  “Build an unstructured data pipeline for RAG | Databricks on AWS,” 2 2025,
abgerufen  am  28.  Januar  2026.  [Online].  Available:  https://docs.databricks.
com/aws/en/generative-ai/tutorials/ai-cookbook/quality-data-pipeline-rag
[31]  B. Sarmah, B. Hall, R. Rao, S. Patel, S. Pasquali, and D. Mehta, “HybridRAG:
Integrating knowledge graphs and vector retrieval augmented generation for
efficient information extraction,” Aug. 2024.
[32]  S. Ghosh and G. Mittal, “Advancing engineering research through context-
aware  and  knowledge  graph-based  retrieval-augmented  generation,”  Front.
Artif. Intell., vol. 8, no. 1697169, p. 1697169, Nov. 2025.
[33]  V.    Mysore,    “Neo4j    GraphRAG    :    Natural    Language    Querying    for
Ontologies    and    Knowledge    Graphs,”    Medium,    12    2025,    abgerufen
am   28.   Januar   2026.   [Online].   Available:   https://medium.com/@visrow/
neo4j-graphrag-natural-language-querying-for-ontologies-and-knowledge-graphs-d08c0cec330f
[34]  S. Yu, I.-H. Kim, J. Song, S. Lee, J. Park, and S. Yoon, “Unleashing multi-hop
reasoning potential in large language models through repetition of misordered
context,” Oct. 2024.
## 52

## Literaturverzeichnis
[35]  Weaviate,  Weaviate  Documentation,  Weaviate,  abgerufen  am  28.  Januar
- [Online]. Available: https://docs.weaviate.io/weaviate
[36]  A. Javanmard, “PDF Data Extraction Benchmark 2025: Comparing Docling,
Unstructured, and LlamaParse for Document Processing,” 3 2025, abgerufen
am  28.  Januar  2026.  [Online].  Available:  https://procycons.com/en/blogs/
pdf-data-extraction-benchmark/
## 53

## Digitaler Anhang
GitHub Repository: https://github.com/dfkibasys/aas-document-rag
## 54

## Danksagung
An dieser Stelle möchte ich mich herzlich für die verständnisvolle Betreuung und
hilfreiche Beratung während der Bachelorarbeit bei Mike Reichardt, Gerhard Son-
nenberg und Dr. Daniel Porta bedanken.