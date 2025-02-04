import streamlit as st
from uuid import uuid4
import chromadb
from openai.embeddings_utils import get_embedding
from llama_index.llms.openai import OpenAI

# Skapa en ChromaDB-klient
client = chromadb.Client()
collection = client.create_collection("documents")

# Lägg till en funktion för att indexera text
def index_texts(texts, collection):
    for text in texts:
        embedding = get_embedding(text, model="text-embedding-003")
        collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"source": "manual"}],
            ids=[str(uuid4())]
        )

# Indexera din text här
texts_to_index = [
    "Internkontroll rapport – utkast
Sammanfattning
Digitalisering är en central del i Karlskoga kommuns strategi för att möta framtidens
krav och säkerställa en effektiv och hållbar verksamhet. Genom att stärka den digitala
mognaden och utveckla moderna lösningar kan kommunen förbättra både service och
resursutnyttjande, samtidigt som varje skattekrona används på bästa sätt.
Denna rapport utvärderar nuläget för kommunens arbete med digitalisering utifrån
internkontrollens genomlysning. Resultaten visar att betydande framsteg har gjorts,
särskilt inom områden som tekniska lösningar, kompetensutveckling och samordning.
Samtidigt identifieras flera utmaningar, bland annat variationer i digital kompetens,
ojämn implementering av digitaliseringsstrategin och bristande uppföljning av effekter.
För att stärka arbetet med digitalisering och säkerställa att kommunen når sina mål
krävs en kombination av kortsiktiga och långsiktiga åtgärder. Rapporten presenterar
konkreta förslag som omfattar allt från kompetensutveckling och förbättrad
samordning till införande av systematiska effektmätningar och integrering av
digitalisering i all verksamhetsutveckling.
Med rätt insatser kan Karlskoga kommun ytterligare stärka sin roll som en förebild inom
digitalisering och samtidigt skapa bättre förutsättningar för medborgare, medarbetare
och framtida generationer.
1. Inledning
• Bakgrund och syfte
Karlskoga kommun strävar efter att vara en ledande aktör inom digitalisering för
att möta framtidens samhällsutmaningar. Med krav på att leverera 125 % välfärd
med endast 75 % av dagens resurser är digitalisering en avgörande faktor för att
uppnå effektivitet och hållbarhet.
• Digitaliseringens betydelse
Fokus ligger på att förbättra kvalitet, tillgänglighet och kostnadseffektivitet
genom att optimera processer, automatisera arbetsflöden och fatta datadrivna
beslut.
• Internkontrollens roll
Rapporten granskar hur digitaliseringens möjligheter tas tillvara inom
kommunens olika förvaltningar och identifierar områden för förbättringar.
2. Omfattning och Metod
Uppdraget omfattar en kartläggning av digital mognad och kompetens inom
kommunens olika förvaltningar. Metoden inkluderar självskattningar genom DiMiOS
och DiKiOS, samt workshops och intervjuer med chefer och medarbetare för att
samla in kvalitativa data.
Internkontrolluppdraget för att utvärdera den digitala mognaden inom kommunens
förvaltningar omfattar flera steg och metoder. För att kartlägga den digitala
mognaden och kompetensen används självskattningsverktyg som DiMiOS och
DiKiOS. Dessa verktyg ger en bild av nuläget och möjliggör jämförelser över tid för
att se hur digital mognad och kompetens utvecklas.
För att få en djupare förståelse genomförs workshops och intervjuer med chefer och
medarbetare. Dessa aktiviteter syftar till att samla in kvalitativa data och skapa en
gemensam förståelse för digitaliseringsstrategins betydelse och implementering.
Vidare används en lärplattform för att kontinuerligt mäta och utveckla medarbetarnas
digitala kompetens. Plattformen erbjuder utbildningar och säkerställer att material är
lättillgängligt för att möjliggöra en effektiv digitalisering i verksamheten.
Ledarskapet spelar en central roll i arbetet, och därför genomförs workshops med
kommunledningsgruppen för att säkerställa förankring i verksamheten och enighet
kring strategins nästa steg. Cheferna får tydliga förväntningar på att prioritera och
uppmuntra digitalisering.
Denna metodik syftar till att skapa en systematisk och strategisk grund för att öka
den digitala mognaden och kompetensen inom kommunen, vilket är avgörande för
att möta framtidens krav och säkerställa en effektiv användning av resurser
• Avgränsningar
Internkontrollen fokuserar på digital mognad, hur digitaliseringsstrategin
används, och hur förvaltningarna hanterar förbättringsförslag relaterade till
digitalisering.
• Mätmetoder
Mätningar som DiMiOS och DiKiOS används för att bedöma nuläget och
utvecklingen av digital mognad och kompetens.
• Datainsamling och analys
Intervjuer och workshops med förvaltningarna har genomförts för att samla in
kvalitativ och kvantitativ data. Fokus har varit på självskattning och analyser av
konkreta initiativ som implementerats.
3. Resultat och Nulägesbeskrivning
Internkontrollen har undersökt hur Karlskoga kommuns förvaltningar arbetar med
digitalisering och implementeringen av kommunens digitaliseringsstrategi. Resultaten
visar både framsteg och utmaningar, samt stora variationer mellan förvaltningarna när
det gäller digital mognad, kompetens och strategisk prioritering.
Analysen av Karlskoga kommuns digitaliseringsarbete visar på en blandad bild. Medan
flera framgångsrika initiativ och projekt har genomförts, återstår utmaningar kring
samordning, strategisk implementering och kompetensutveckling. Resultaten visar att
digitalisering har prioriterats olika inom kommunen, vilket påverkar både mognaden
och effekten av de insatser som gjorts.
Resultaten visar att den digitala mognaden har ökat något, men det finns fortfarande
stora variationer mellan förvaltningarna. Socialförvaltningen har uttryckt kritik mot
centrala implementeringar, medan Samhälle och serviceförvaltningen har sett en
ökad förståelse för digitalisering.
• 3.1 Digital mognad i kommunen
• Mätningar från DiMiOS under 2022 och 2023 indikerar att kommunens digitala
mognad har ökat. Medarbetare har blivit mer medvetna om digitaliseringens
betydelse, vilket reflekteras i minskade ”vet ej”-svar i mätningarna.
• Den ökade mognaden är resultatet av flera samordnade insatser, såsom
utbildningar och strukturella förändringar. Exempelvis har utbildningar som
"Digitaliseringens ABC" och etableringen av forum som Digitaliseringsrådet
stärkt både kompetensen och engagemanget.
• Samtidigt finns det en ojämn fördelning av den digitala mognaden i kommunen,
med vissa verksamheter som upplevs ha kommit längre än andra. Denna
variation är kopplad till faktorer som ledarskap, tillgång till resurser och
förmågan att tillämpa strategin på ett systematiskt sätt.
•
• 3.2 Styrkor och framgångar
• Kommunen har genomfört flera framgångsrika initiativ som bidragit till att
förbättra effektiviteten och kvaliteten i verksamheterna:
• Tekniska lösningar: Digitala lås och läkemedelsrobotar har implementerats för
att förbättra effektiviteten i vissa verksamheter.
• Digital infrastruktur: Arbetet med e-tjänster och nya system har gjort det
enklare för både medarbetare och medborgare att använda kommunens tjänster
.
• Utbildning och samverkan: Program som "Digitaliseringens ABC" har ökat
kunskapen om digitalisering bland medarbetarna, och samarbeten genom KIS
och Digitaliseringsrådet har skapat plattformar för idéutbyte och strategiska
diskussioner.
•
• 3.3 Utmaningar och förbättringsområden
• Trots framgångarna finns utmaningar som påverkar digitaliseringens genomslag i
kommunen:
• Kompetens och förståelse
Kompetensnivån varierar mellan medarbetare och verksamheter, vilket
påverkar förmågan att använda digitala verktyg och implementera nya lösningar.
Det finns även ett behov av att öka förståelsen för digitaliseringens strategiska
betydelse.
• Samordning och strategisk tillämpning
Medan vissa delar av organisationen har integrerat digitaliseringsstrategin i sin
verksamhetsplanering, saknar andra en strukturerad och långsiktig strategi. Det
finns en risk att arbetet med digitalisering sker fragmentariskt utan tydlig
koppling till de övergripande målen.
• Effektmätning och uppföljning
Uppföljning av digitaliseringsprojekt sker i varierande grad. I flera fall saknas
systematisk mätning av nyttor och effekter, vilket försvårar möjligheten att dra
lärdomar och vidareutveckla arbetet.
•
• 3.4 Sammanfattning av nuläget
• Karlskoga kommun har tagit viktiga steg framåt inom digitalisering genom
utbildning, tekniska lösningar och samarbetsinitiativ. De största utmaningarna
handlar om att säkerställa en jämn fördelning av digital mognad och kompetens,
att skapa strukturer för samordning och att förbättra uppföljningen av
digitaliseringens effekter.
• För att ytterligare stärka arbetet bör kommunen fokusera på att:
• Systematiskt integrera digitalisering i alla verksamheters utvecklingsarbete.
• Stärka kompetensutvecklingen för att minska variationer i kunskap.
• Utveckla metoder för att mäta och följa upp digitaliseringens nyttor och effekter.
4. Utmaningar och Gap
Utifrån analysen av kommunens digitalisering framträder flera utmaningar och gap som
behöver adresseras för att uppnå de långsiktiga målen.
4.1 Digital kompetens
• Varierande nivåer inom och mellan förvaltningar
Den digitala kompetensen hos medarbetarna varierar stort både inom och
mellan förvaltningarna.
 Exempel: Samhälle och serviceförvaltningen rapporterar att skillnader i
datorkompetens påverkar genomförandet och nyttjandet av digitala
lösningar.
 Åtgärder: Fokusera på systematiska utbildningar och skapa en
lärplattform som stödjer individuella kompetensutvecklingsplaner.
• Digital otrygghet bland brukare och medarbetare
Socialförvaltningen har upplevt att digital otrygghet bland brukarna förhindrar
implementering av vissa tekniska lösningar, t.ex. läkemedelsrobotar.
 Åtgärder: Erbjuda utbildningar och stöd som bygger trygghet och
förståelse för digitala verktyg, både för brukare och personal.
4.2 Resursbrist och organisatoriska hinder
• Personalomsättning och resursbrist
Tillväxt- och tillsynsförvaltningen har identifierat att resursbrist och hög
personalomsättning är hinder för att driva digitalisering framåt.
 Följd: Fokus på kortsiktiga lösningar snarare än långsiktig strategi.
 Exempel: Implementeringen av system som Castor och BabOnline har
försvårats av dessa utmaningar.
• Brist på gemensamma resurser och stöd
Vissa förvaltningar, såsom Kultur- och fritidsförvaltningen, saknar IT-
stabsresurser och stöd för att kunna implementera digitaliseringsinitiativ.
 Följd: Digitalisering hanteras decentraliserat, vilket leder till ojämlikheter
i utveckling.
4.3 Prioritering och engagemang
• Bristande prioritering av digitalisering
Digitalisering är inte prioriterat i alla förvaltningar, vilket framgår tydligt hos
Skolförvaltningen.
 Exempel: Digitalisering nämns sparsamt i deras kvalitetsrapporter, och
det saknas en strategisk inriktning för att lyfta området.
 Följd: Fragmenterade initiativ och låg samordning av förbättringsförslag.
• Ojämn förankring av strategin
Även inom förvaltningar som prioriterar digitalisering finns utmaningar kring att
skapa en gemensam förståelse för vad digitalisering innebär.
 Exempel: Samhälle och serviceförvaltningen upplever att chefernas
förståelse för digitalisering ökat, men det saknas en gemensam bild av
vad området omfattar.
4.4 Effektmätning och uppföljning
• Avsaknad av systematisk mätning
Många förvaltningar saknar system för att mäta och följa upp effekterna av
digitaliseringsinitiativ.
 Exempel: Kultur- och fritidsförvaltningen har inte genomfört mätningar av
de ekonomiska eller kvalitativa effekterna av sina digitala
implementeringar.
 Följd: Svårt att dra lärdomar och säkerställa att investeringar ger önskad
effekt.
• Utmaningar med DiMiOS och DiKiOS
 Resultaten från DiMiOS upplevs ibland som för abstrakta för att dra
konkreta slutsatser.
 Förslag: Byta fokus till att mäta digital kompetens (DiKiOS) framöver för
att få mer handfasta och användbara resultat.
4.5 Fragmenterade initiativ och svag samordning
• Bristande samordning av digitalisering
Vissa förvaltningar hanterar digitalisering på ett fragmentariskt sätt, vilket
skapar ineffektivitet och försvårar enhetliga framsteg.
 Exempel: Skolförvaltningen har endast påbörjat samordning av
digitaliseringsarbetet tillsammans med IT-gruppen och rektorer, men
detta har inte konkretiserats ännu.
• Förvaltningsspecifika strategier utan helhetsperspektiv
Flera förvaltningar, såsom Tillväxt- och tillsynsförvaltningen och Kultur- och
fritidsförvaltningen, arbetar utan en tydligt definierad och implementerad
digitaliseringsstrategi.
 Följd: Avsaknad av helhetsperspektiv och långsiktig planering.
4.6 Kulturella och verksamhetsspecifika utmaningar
• Kultur- och fritidsverksamhetens natur
Vissa verksamheter, såsom Kultur- och fritidsförvaltningen, har svårt att
identifiera behov av digitalisering, eftersom mycket av deras kärnverksamhet är
analog.
 Följd: Digitalisering ses som en stödfunktion snarare än en central del av
verksamheten.
• Digitaliseringens påverkan på mellanmänskliga möten
Förvaltningar som arbetar nära medborgarna uttrycker oro för att digitala
lösningar kan minska mänskliga interaktioner.
Sammanfattningsvis är utmaningarna kopplade till digitalisering både tekniska och
organisatoriska. Genom att adressera dessa gap kan kommunen stärka sin digitala
mognad och säkerställa att digitalisering används som ett strategiskt verktyg för att
möta framtidens krav.
5. Åtgärdsförslag
För att öka Karlskoga kommuns digitaliseringstakt och säkerställa att alla förvaltningar
arbetar strategiskt och effektivt med digitalisering, föreslås följande åtgärder.
Åtgärderna är uppdelade i sådana som kan genomföras på kort sikt och sådana som är
mer strategiska och långsiktiga.
5.1 Stärk digital kompetens
Kortsiktiga åtgärder:
1. Kompetenstester för befintlig personal:
a. Inför tester som kartlägger medarbetarnas digitala kunskaper. Fokus ska
ligga på att identifiera utvecklingsområden snarare än att bedöma
prestation.
b. Skapa individuella utvecklingsplaner baserade på resultaten.
2. Målgruppsanpassade utbildningar:
a. Genomför snabba utbildningsinsatser inom områden som identifieras
som kritiska, exempelvis Microsoft Teams, Office 365 och
säkerhetsrutiner.
b. Prioritera grundläggande digitala färdigheter för anställda med låg digital
kompetens.
3. Stödmaterial och lättillgängliga resurser:
a. Tillhandahåll digitala guider, videoinstruktioner och FAQ som
medarbetare kan använda i sitt dagliga arbete.
Långsiktiga åtgärder:
1. Lärplattform för kontinuerlig utveckling:
a. Implementera en lärplattform där alla medarbetare kan delta i
modulbaserade utbildningar. Plattformen ska innehålla spårning av
utveckling och möjliggöra analys av kompetensförflyttningar.
2. Kompetenskrav vid rekrytering:
a. Inkludera krav på digital kompetens i jobbannonser. Använd tester i
rekryteringsprocessen för att säkerställa en basnivå av digital kunskap
hos nyanställda.
3. Utveckla digitala ambassadörer:
a. Identifiera och utbilda "digitala ambassadörer" inom varje förvaltning
som kan fungera som stöd och förebilder i digitaliseringsarbetet.
5.2 Effektmätning och nyttokalkyler
Kortsiktiga åtgärder:
1. Metodstöd för nyttokalkyler:
a. Utveckla ett enkelt metodstöd för att mäta nolläge och effekter av
digitaliseringsinsatser. Fokus ska vara på praktiska och snabba analyser
som inte kräver omfattande resurser.
2. Starta pilotprojekt:
a. Välj ut två till tre aktuella projekt där effektmätningar kan genomföras.
Använd dessa som testfall för att utveckla effektiva mätmetoder.
3. Chefsförankring:
a. Utbilda chefer i hur de kan kravställa och följa upp effektmätningar.
Koppla detta till befintliga verksamhetsmål för att skapa tydlighet.
Långsiktiga åtgärder:
1. Standardisera mätningar:
a. Inför systematiska mätningar av nyttor och effekter som standard i alla
digitaliseringsprojekt. Integrera dessa i verksamhetens årshjul och
planeringsprocesser.
2. Politisk efterfrågan:
a. Stärk politikens roll i att kravställa nyttokalkyler och effektmätningar.
Inkludera dessa som en del av beslutsunderlaget vid nya satsningar.
3. Datadrivet beslutsfattande:
a. Använd insamlad data från lärplattformar och mätningar för att identifiera
framgångsfaktorer och prioritera framtida satsningar.
5.3 Strategisk samordning
Kortsiktiga åtgärder:
1. Revidera digitaliseringsstrategin:
a. Anpassa den befintliga strategin till lokala behov och den kommande
nationella strategin för digitalisering (2025). Gör detta i samråd med alla
förvaltningar.
2. Populärversion av strategin:
a. Ta fram en lättillgänglig och kortfattad version av strategin som kan
spridas till alla medarbetare för att öka förståelsen och engagemanget.
3. Workshops för chefer:
a. Genomför workshops med fokus på strategiimplementering och hur
chefer kan skapa engagemang i sina verksamheter.
Långsiktiga åtgärder:
1. Förvaltningsspecifika digitaliseringsplaner:
a. Låt varje förvaltning bryta ner strategin till konkreta och mätbara mål för
sin verksamhet. Dessa planer ska inkluderas i förvaltningarnas
verksamhetsplanering.
2. Digitaliseringsråd:
a. Etablera ett kommunövergripande digitaliseringsråd som kan fungera
som stöd i strategiska frågor och säkerställa samordning mellan
förvaltningar.
3. Kulturförändring:
a. Skapa en kultur där digitalisering ses som en naturlig del av
verksamhetsutveckling genom att lyfta fram framgångsexempel och
belöna initiativ som bidrar till digital transformation.
5.4 Integrera digitalisering i allt
Kortsiktiga åtgärder:
1. Digitalisering som perspektiv:
a. Inför digitalisering som en obligatorisk del av alla utvecklingsprojekt.
Säkerställ att varje projekt utvärderas utifrån digitaliseringsmöjligheter.
2. Omvärldsbevakning:
a. Stärk kommunens arbete med omvärldsbevakning och dela regelbundet
insikter om digitala trender och lösningar.
Långsiktiga åtgärder:
1. Digitalt först:
a. Implementera "Digitalt först"-principen i alla processer och kontakter, där
digitala lösningar prioriteras utan att exkludera analoga alternativ.
2. Inkludera digitalisering i verksamhetsplanering:
a. Gör digitalisering till en integrerad del av kommunens årshjul, med mål
och uppföljning på förvaltnings- och kommunnivå.
3. Digitalt ledarskap:
a. Utveckla ett långsiktigt program för att stärka chefernas förmåga att leda
digitaliseringsinitiativ, inklusive utbildning i förändringsledning och
teknik.
6.1 Slutsatser
1. Digital mognad och kompetens varierar kraftigt
a. Förvaltningarna har olika förutsättningar och engagemang för
digitalisering. Medan vissa har gjort framsteg, saknar andra en tydlig
strategi eller prioritering.
b. Kompetensbrister är ett genomgående problem och påverkar förmågan
att implementera och utnyttja digitala lösningar.
2. Bristande effektmätning och uppföljning
a. Effektmätningar genomförs sällan, vilket gör det svårt att utvärdera nyttan
av digitaliseringsprojekt. Det saknas en gemensam modell för
uppföljning.
3. Strategi och samordning behöver förstärkas
a. Den befintliga digitaliseringsstrategin är för allmän och behöver anpassas
till varje förvaltnings behov. Förankring och tydlig kommunikation saknas
i flera led.
4. Digitalisering är inte integrerat i alla verksamheter
a. Digitalisering ses fortfarande som en separat process snarare än en del
av ordinarie verksamhetsutveckling i många delar av organisationen.
6.2 Rekommendationer och åtgärder
A. Förstärk digital kompetens och ledarskap
Kortsiktiga åtgärder:
1. Snabbspår för kompetensutveckling:
a. Genomför riktade utbildningar i digitala verktyg och säkerhet inom de
förvaltningar som har störst behov.
2. Digitaliseringsutbildning för chefer:
a. Inför en utbildningsserie för chefer om hur digitalisering kan användas
strategiskt i deras verksamheter.
Långsiktiga åtgärder:
1. Kontinuerlig kompetensutveckling:
a. Bygg in utbildning i digital kompetens som en del av kommunens årliga
kompetensutvecklingsplan. Använd en lärplattform för att följa upp
resultaten.
2. Ledarskapsprogram för digitalisering:
a. Utveckla ett program som stärker chefernas förmåga att leda digitala
förändringar, med fokus på förändringsledning och användning av data i
beslutsfattande.
B. Inför systematisk effektmätning och uppföljning
Kortsiktiga åtgärder:
1. Ta fram metodstöd:
a. Utveckla enkla verktyg för att mäta nolläge och effekter av digitalisering,
och implementera dem i pågående projekt.
2. Pilotprojekt:
a. Identifiera och utvärdera två till tre aktuella projekt där nyttokalkyler och
effektmätning kan testas.
Långsiktiga åtgärder:
1. Standardisera effektmätningar:
a. Inför krav på nyttokalkyler och effektmätningar för alla nya
digitaliseringsprojekt. Gör detta till en del av den kommunövergripande
planeringen.
2. Bygg en datadriven kultur:
a. Etablera en kultur där data och mätningar används regelbundet för att
förbättra verksamheter och fatta välgrundade beslut.
C. Revidera och förankra digitaliseringsstrategin
Kortsiktiga åtgärder:
1. Anpassa strategin:
a. Revidera den befintliga digitaliseringsstrategin utifrån den nya nationella
strategin (2025) och kommunens specifika behov.
2. Kommunicera strategin tydligt:
a. Ta fram en lättillgänglig version av strategin, exempelvis i form av en
broschyr eller en video, för att sprida förståelse och engagemang bland
medarbetare.
Långsiktiga åtgärder:
1. Förvaltningsspecifika planer:
a. Låt varje förvaltning bryta ner strategin till konkreta mål och åtgärder som
är kopplade till deras verksamhet.
2. Skapa långsiktig samordning:
a. Etablera ett digitaliseringsråd som samlar representanter från alla
förvaltningar och fungerar som en plattform för kunskapsutbyte och
koordinering.
D. Integrera digitalisering i alla verksamheter
Kortsiktiga åtgärder:
1. Digitalt perspektiv i projekt och processer:
a. Inför krav på att alla utvecklingsprojekt ska inkludera en utvärdering av
digitala möjligheter.
2. Omvärldsbevakning:
a. Stärk arbetet med omvärldsbevakning för att säkerställa att kommunen
ligger i framkant när det gäller ny teknik och trender.
Långsiktiga åtgärder:
1. Digitalisering som en del av verksamhetsutveckling:
a. Gör digitalisering till ett integrerat perspektiv i kommunens
verksamhetsplaner, årshjul och budgetprocesser.
2. Stärka medborgarupplevelsen:
a. Utveckla digitala lösningar som förbättrar servicen för medborgare,
exempelvis genom fler användarvänliga e-tjänster och dygnet-runt-
tillgång till kommunala tjänster.
E. Fira framgångar och skapa en positiv förändringskultur
Kortsiktiga åtgärder:
1. Lyft fram goda exempel:
a. Dokumentera och dela framgångsrika digitaliseringsprojekt internt för att
inspirera och skapa engagemang.
2. Belöna innovation:
a. Inför priser eller utmärkelser för medarbetare och förvaltningar som
bidrar till framgångsrika digitala initiativ.
Långsiktiga åtgärder:
1. Bygg en kultur av kontinuerlig förbättring:
a. Uppmuntra alla medarbetare att delta i digitaliseringsarbetet genom att
skapa en kultur där idéer och innovationer välkomnas.
2. Utvärdera och justera:
a. Inför regelbundna utvärderingar av digitaliseringsstrategin och anpassa
den efter behov och förändrade förutsättningar.
7. Bilagor och Referenser
• Resultat från DiMiOS och DiKiOS.
• Detaljer om genomförda intervjuer och workshops.
• Styrdokument och relevanta nationella strategier.",
    "Här är en annan text som chatten kan använda för att generera svar."
]
index_texts(texts_to_index, collection)

# Sök funktion
def search_documents(query, collection):
    query_embedding = get_embedding(query, model="text-embedding-003")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    return results['documents']

# Streamlit-app
st.title("AI Chat med dokument")

query = st.text_input("Ställ din fråga:")

if query:
    results = search_documents(query, collection)
    for result in results:
        st.write(f"**Resultat:** {result}")
