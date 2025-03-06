# External imports
import streamlit as st
from llama_index.core.llms import ChatMessage
from openai import OpenAI
from groq import Groq

# Python imports
import hmac
import os
from os import environ

# Local imports 
from functions.styling import page_config, styling
from functions.menu import menu
import config as c

### CSS AND STYLING

st.logo("images/logome.png", icon_image="images/logo_small.png")
page_config()
styling()

# Markdown for the header and description
st.markdown("""
    ### Hur kan Karlskoga kommun öka digitaliseringstakten?
    Testa chatten här nedanför och fråga efter resultat eller be om konkreta förslag på aktiviteter. Eller utmana och fråga något annat om rapporten.
""")

# Check if language is already in session_state, else initialize it with a default value
if 'language' not in st.session_state:
    st.session_state['language'] = "Svenska"  # Default language



### TRANSLATION OCH SYSTEMPROMPT

if st.session_state['language'] == "Svenska":
    chat_prompt = "Du är en hjälpsam AI-assistent. Svara på användarens frågor."
    chat_clear_chat = "Rensa chat"
    chat_hello = "Hej! Vad vill du veta om rapporten? Skriv din fråga här nedanför"
    chat_settings = "Inställningar"
    chat_choose_llm = "Välj språkmodell"
    chat_choose_temp = "Temperatur"
    chat_system_prompt = "Systemprompt"
    chat_save = "Spara"
    chat_imput_q = "Vad vill du vet om rapporten?"
elif st.session_state['language'] == "English":
    chat_prompt = "You are a helpful AI assistant. Answer the user's questions."
    chat_clear_chat = "Clear chat"
    chat_hello = "Hi! How can I help you?"
    chat_settings = "Settings"
    chat_choose_llm = "Choose language model"
    chat_choose_temp = "Temperature"
    chat_system_prompt = "System prompt"
    chat_save = "Save"
    chat_imput_q = "What do you want to talk about?"

# Här lägger vi in rapporttexten som kontext för chatten
report_text = """
[Sammanfattning
Denna rapport undersöker hur Karlskoga kommun kan öka takten i digitaliseringsarbetet för att möta nutidens och framtidens krav på effektiva, användarvänliga och hållbara digitala lösningar. En omfattande genomgång av nuläget visar på flera möjligheter till förbättring och utveckling, men också på utmaningar som måste adresseras för att framgångsrikt driva digitaliseringen framåt. 
För att öka digitaliseringstakten krävs en reviderad kommunövergripande digitaliseringsstrategi, tydligare digitalt ledarskap samt regelbundna kompetenskartläggningar med riktade utbildningsinsatser. Rapporten pekar också på vikten av att införa en enhetlig och gemensam digital plattform samt att stärka kommunens digitala infrastruktur för både invånare och medarbetare. 
Utöver de tekniska aspekterna föreslås en kulturell och organisatorisk förändring där kommunen aktivt främjar innovation, samarbete samt en öppen och trygg arbetsmiljö med en tydlig medborgarfokus. Kontinuerlig effektmätning och uppföljning av digitaliseringssatsningarna framhålls som avgörande för att kunna fatta datadrivna beslut. 
Sammantaget innehåller rapporten konkreta rekommendationer, förslag på åtgärder och strategier som syftar till att skapa förutsättningar för en långsiktig, effektiv och trygg digital transformation av Karlskoga kommun.
 
1. Inledning
 
Bakgrund
Karlskoga är en kommun i framkant som ska vara aktuell och attraktiv för invånare, näringsliv och arbetskraft idag såväl som i morgon. Vår målsättning är att vara ledande inom digitalisering för att möte framtidens samhällsförändringar. Med nya demografiska utmaningar behöver vi snart leverera 125% välfärd med endast 75% av de resurser vi har idag. För att lyckas med den uppgiften är digitalisering inte bara en fördel, utan en absolut nödvändighet. 
 Digitalisering är nyckeln till att möta framtida krav och samtidigt säkerställa att varje skattekrona används så effektivt som möjligt. Karlskoga kommun har en digitaliseringsstrategi som innefattar dessa fem huvudrubriker; digital infrastruktur, digital kompetens, digital trygghet, digital innovation och digital ledning. I mätningar som genomförts internt i kommunen kan vi se att viss utveckling skett inom digitalisering men att denna utveckling ofta är kopplat till specifika projekt. Vid internkontrollen 2023 kopplat till digitalisering där syftet var att undersöka om och hur förvaltningarna arbetar med digitaliseringsstrategin har utmaningar identifierats. Den generella digitala kompetensen varierar kraftigt i hela organisationen vilket till viss del kan kopplas till varierande engagemang och brist på digital kompetens.
 
Syfte Syftet med denna internkontroll är att identifiera hur Karlskoga kommun kan öka digitaliseringstakten för att möta framtidens krav och säkerställa att kommunen ligger i framkant inom digital utveckling. Genom att analysera hur digitaliseringsstrategin tillämpas i praktiken och vilka hinder som finns, skapas en grund för att vidta åtgärder som stärker digital kompetens, underlättar implementering av digitala lösningar och främjar ett mer datadrivet arbetssätt.
Internkontrollen syftar också till att kartlägga den digitala mognaden i organisationen, undersöka hur ledarskapet påverkar digitaliseringsarbetet samt identifiera möjligheter att effektivisera verksamheten genom digital teknik. Fokus ligger på att säkerställa att rätt resurser och stöd finns på plats för att digitalisering ska genomsyra verksamheten på ett ändamålsenligt och effektivt sätt.
Genom en systematisk granskning av digital kompetens, användning av digitala verktyg och tillgången till relevant utbildning kan kommunen skapa en stabil grund för en hållbar och långsiktig digital utveckling som möter både nationella riktlinjer och lokala behov.
 
2. Digitaliseringsstrategin – en grundläggande del i arbetet Digitaliseringsstrategin beskriver hur Karlskoga kommun ska arbeta för att dra nytta av digitaliseringens möjligheter. Målet är att förbättra kvalitet, tillgänglighet och kostnadseffektivitet genom att optimera processer, automatisera arbetsflöden och fatta datadrivna beslut. Kommunen strävar efter att vara en ledande aktör inom digitalisering för att möta framtidens samhällsförändringar och säkerställa att varje skattekrona används så effektivt som möjligt. Digitalisering ses som ett verktyg för att förbättra kommunens service och verksamhetsutveckling, inte ett mål i sig. Kommunens digitaliseringsstrategi omfattar fem huvudområden och utgår ifrån den nationella strategin, där Sverige har målet att vara bäst i världen på att använda digitaliseringens möjligheter.
Karlskoga kommuns vilja är att ligga i framkant och vara en plats för banbrytande forskning och teknikutveckling. Digitaliseringens roll i verksamhetsutveckling är central, och kommunen ska systematiskt beakta digitalisering i allt förändringsarbete. Digitaliseringen ska förbättra servicen för alla som bor, lever och verkar i Karlskoga, inklusive invånare, företag och föreningar. Kommunens digitaliseringsstrategis huvudområden är:
Digital infrastruktur
Utveckla och underhålla en robust digital infrastruktur som möjliggör snabb och säker kommunikation både internt och externt. Implementera moderna tekniska lösningar som stödjer kommunens verksamheter och förbättrar medborgarnas tillgång till digitala tjänster. Ett tydligt fokus ska ligga på invånarnas behov och att säkerställa en utbyggnad av snabbt bredband till alla kommunens invånare. Kommunen ska även verka för digitala kanaler till samarbetspartners och främja infrastruktur som stöder offentlig digital utveckling.
Digital kompetens
Alla invånare, oavsett bakgrund eller ålder, ska ges möjlighet att utveckla sin digitala kompetens. Kommunen arbetar aktivt för att öka den digitala mognaden hos både medarbetare och beslutsfattare, vilket skapar bättre förutsättningar för en inkluderande och innovativ digital utveckling. 
 
Digital trygghet
Säkerställa att digitala lösningar är säkra och skyddar medborgarnas integritet.
Implementera säkerhetsåtgärder och utbilda medarbetarna i digital säkerhet för att minimera risker och hot. Genom satsningar på informations- och cybersäkerhet skapas en trygg digital miljö för alla.
 
Digital innovation
Kommunen ska driva utvecklingen av nya digitala lösningar som effektiviserar verksamheten och förbättrar servicen till invånarna. "Digitalt först!" innebär att digitala lösningar prioriteras där det är möjligt, samtidigt som analoga alternativ finns tillgängliga när det behövs.
 
Digital Ledning
Digitalisering är en förändringsresa som kräver aktivt ledarskap. Det är viktigt att digitalisering ses som en strategisk del av kommunens utveckling. Chefer och medarbetare behöver arbeta tillsammans för att driva digital förändring, och digitala perspektiv ska vara en naturlig del av beslut och investeringar.
 
Under 2025 pågår ett omfattande arbete på både nationell och regional nivå för att utveckla och revidera gällande digitaliseringsstrategier. Som kommun kommer vi att revidera vår digitaliseringsstrategi för att den ska harmonisera med de strategier som fastställts på nationell och regional nivå.
 
3. Omfattning och nulägesbeskrivning För att skapa en nulägesbild tar denna internkontroll stöd i:  Tjänsteskrivelsen KS 2023-00655 upprättad i slutet av 2023 Sammafattning av workshop tillsammans med KnowIT 2024-02-08 
Mätningar Dimios under åren 2022, 2023 och 2024.
Sammanställning av resultat i den löpande internutbildningen Nimbler.
 
 
Sammanfattning av tjänsteskrivelse 
 
I tjänsteskrivelsen KS 2023-00655, upprättad i slutet av 2023, har man undersökt hur Karlskoga kommuns förvaltningar arbetar med digitalisering och implementeringen av kommunens digitaliseringsstrategi.
I denna tjänsteskrivelse finns en generell upplevelse att Karlskoga kommuns arbete med digitalisering är ungefär på samma nivå som i början av 2023, med vissa mindre förbättringar där nyrekryteringar och e-tjänster bidragit till ökad digital mognad. Samtidigt finns det en vilja att överge det något abstrakta begreppet ”digital mognad” till förmån för att mäta ”digital kompetens”, eftersom detta upplevs vara mer konkret och användbart för att identifiera specifika utvecklings- och utbildningsbehov.
Ett återkommande tema i nuläget är att det saknas en riktigt samordnad och kommunövergripande strategi för hur man tar tillvara på digitaliseringsinitiativ. Flera förvaltningar kämpar med liknande utmaningar, som personalomsättning, resursbrist och varierande datorkompetens, vilket gör att kunskapsluckor och behov av stöd inom gemensamma och kommunövergripande system kvarstår. Även om vissa förvaltningar har utsedda digitaliseringsansvariga eller planerar att implementera mer formella strategier, tycks dessa insatser ännu inte vara helt förankrade i en övergripande kommunal struktur.
En annan tydlig svårighet är bristen på effektmätning. Förvaltningarna genomför vissa digitala projekt, men utan att systematiskt följa upp hur väl de faller ut eller vilka besparingar eller effektivitetsvinster de medför. En del verksamheter efterfrågar därför bättre metoder för att mäta och visa på nyttan, för att motivera vidare digitalisering.
Gällande kompetenshöjande insatser uttrycks ofta önskemål om fler utbildningar och bredare stöd från IT-enhet eller digitaliseringssamordnare. Exempelvis nämns utbildningsbehov inom Microsoft Teams, Office 365 men även i specifika verksamhetssystem. Det nämns även ett behov av att öka digital trygghet hos både personal och brukare.
Slutligen är det tydligt att flera verksamheter, särskilt de med mer fysisk eller ”analog” kärnverksamhet, ser digitalisering som en stödfunktion snarare än ett mål i sig. Man ger exempel att digitalisering ska underlätta och frigöra tid för mänsklig kontakt, inte ersätta den. Även om ett mer offensivt digitaliseringsarbete kan ske inom vissa delar av kommunen, råder en allmän uppfattning om att digitalisering måste anpassas efter verksamhetens förutsättningar och tydligt kunna motiveras för att accepteras och genomföras.
Sammanfattningsvis präglas bilden i tjänsteskrivelsen av en relativt stabil digital mognad, framförallt med tanke på den samlade bilden att läget i tjänsteskrivelsen redogör för att det inte skett några större förändringar under 2023. Det framgår dock att det finns stora möjligheter till förbättringar genom mer enhetliga strategier, regelbunden effektmätning och tydligare stöd. Resultaten visar både framsteg och utmaningar, samt stora variationer mellan förvaltningarna när det gäller digital mognad, kompetens och strategisk prioritering.
Analysen av Karlskoga kommuns digitaliseringsarbete visar på en blandad bild. Medan flera framgångsrika initiativ och projekt har genomförts, återstår utmaningar kring samordning, strategisk implementering och kompetensutveckling. Resultaten visar att digitalisering har prioriterats olika inom kommunen, vilket påverkar både mognaden och effekten av de insatser som gjorts. Kortfattat kan detta sammanfattats att enskilda projekt i framkant behöver kompletteras med breddinsatser för att öka den generella kompetensen kring digitalisering och dess möjligheter. Det skulle kunna beskrivas som en spretig digital mognad med tydliga behov av vägledning i användandet av framförallt gemensamma arbetsformer i digitala miljöer inom kommunen.
 
 
Workshop – KnowIT
Den 8 februari 2024 genomfördes en workshop under ledning av Knowit, deltagare från Karlskoga kommun var kommunledningsgrupp, kvalitetsavdelning, IT-chef samt digitaliseringsstrateg. Under workshopen betonade deltagarna vikten av en tydlig och gemensam digital vision där den befintliga digitaliseringsstrategin integreras via en övergripande styrning. Ett förslag var att inrätta ett forum för chefer och strateger, vilket skulle bidra till att samordna insatserna och undvika att arbetet “springer i cirklar.”
Vidare lyftes behovet av att stärka den digitala kompetensen fram. Genom att införa utvecklingsprogram för ledningsgrupper, där teoretisk utbildning kombineras med praktisk handledning, kan den digitala mognaden höjas och digitaliseringsarbetet konkretiseras i den dagliga verksamheten.
Kulturella förändringar diskuterades, och det framkom att rädsla för förändring och brist på psykologisk trygghet hindrar innovation och samarbete. Tjänstedesign föreslogs som ett verktyg för att skapa en mer öppen och experimentell kultur med medborgarfokus.
Workshopen belyste även de tekniska och operativa utmaningarna, exempelvis ineffektiv systemintegration och underutnyttjad teknik, vilket leder till ett gap mellan digital teknik och verksamhetsbehov. Dessutom lyftes det att vardagliga driftsfrågor ofta tar så mycket tid att långsiktiga digitaliseringsinitiativ riskerar att hamna i skymundan. Slutligen betonades vikten av ett starkt politiskt engagemang och tydliga mandat för att driva digitaliseringsarbetet framåt.
Sammanfattningsvis visar workshoppen med KnowIT att en integrerad strategi, där strategisk samordning, kompetensutveckling, kulturförändring, tekniska förbättringar och politiskt stöd samverkar, är avgörande för att Karlskoga kommun ska kunna öka sin digitaliseringstakt och möta framtidens krav.
 
Dimiosmätning
Dimios används för att mäta digital mognad genom att samla in data om både tekniska aspekter (såsom IT-system och infrastruktur) och organisatoriska förutsättningar (t.ex. digital strategi, kompetens och innovationsförmåga). Resultatet visar hur väl organisationen är rustad för att möta en alltmer digitaliserad omvärld, och identifierar var insatser behövs för att öka effektiviteten och innovationskraften. Sammanfattningsvis är digital mognad en dynamisk och pågående process som innebär att man kontinuerligt arbetar med att förbättra både teknik och kultur för att maximera nyttan av digitalisering. I Dimois mäts digital mognad i två komponenter, digitalt arv och digital förmåga.
Digitalt arv 
Detta avser den befintliga digitala infrastrukturen, inklusive tidigare IT-investeringar, system och tekniska lösningar. Ett möjliggörande digitalt arv innebär att de befintliga systemen är flexibla och stödjer vidare digital utveckling, medan ett begränsande arv kan hindra innovation och anpassning.
 Digital förmåga
Detta är organisationens kapacitet att förstå, anpassa sig till och aktivt använda digital teknik för att förbättra verksamheten. Det innefattar allt från ledarskap och strategi till medarbetarnas digitala kompetens och förmågan att samarbeta kring nya digitala lösningar.  Mätningen sker genom en enkätbaserad självskattning. Fokus ligger på att använda digitalisering för verksamhetsutveckling, inte på teknisk kompetens. I enkäten förekommer frågor med förvalda svarsalternativ samt fritextmöjligheter. 
 
Resultat i Dimios
Mätningar i Dimios har genomförts under åren 2022, 2023 och 2024. Sett till de två komponenterna digitalt arv och digital förmåga som ligger till grund för den samlade bedömningen för digital mognad ser vi en stadig ökning över de tre åren. Detta innebär naturligt att den digitala mognaden även den har ökat. Den största ökningen har skett mellan mätningar 2022 och 2023 vilket sammanfaller med insatser initierade av IT-avdelningen. Dessa insatser bestod av införande av idé-caféer med syfte att fånga in frågor och idéer men även informera om lösningar som finns i organisationen samt en god möjlighet för verksamheten att ställa spontana frågor direkt kopplat till arbetet i vardagen. Dimiosresultat 2022 digitalt arv 59%, digital förmåga 47% och digital mognad 53%. Resultat 2023 digitalt arv 71%, digital förmåga 56% och digital mognad 63%. År 2024 digitalt arv 72%, digital förmåga 57% och digital mognad 64%

Statistiken ovan utgår från svaren på frågor med fördefinierade svar. För att ge en helhetsbild av mätningen presenteras nedan en sammanfattning av de fritextsvar som inkommit under mätningarna.
Sammanfattningsvis visar fritextsvaren en utvecklingskurva där kommunen långsamt övergår till en mer strukturerad och strategisk hantering av digitala lösningar och IT-system. Det framkom genomgående en positiv syn på digitala initiativ och IT-support, även om utmaningar kring användarkompetens, resursallokering och långsiktig innovation kvarstod.
Enligt de svarande ser man en utvecklingskurva där kommunen långsamt övergår till en mer strukturerad och strategisk hantering av digitala lösningar och IT-system. Kommentarerna visar att de positiva upplevelserna av digitala initiativ och IT-support är tydliga, även om flera anser att utmaningar kring användarkompetens, resursallokering och långsiktig innovation kvarstår.
År 2022, de svarande noterade att kommunen tog sina första steg mot att etablera en struktur och kontroll över digitala initiativ. Flera kommenterade att implementeringen av PM3 – som senare omarbetades till KIS – var en lovande start. Samtidigt framhölls att hela organisationen ännu inte var enad kring en gemensam vision kring digitalisering kopplat till digital mognad och digital kompetens. Det finns även en utmaning i engagemanget hos samtliga parter.
År 2023, de svarande beskrev att införandet av KIS (Karlskoga IT Samverkan) möjliggjorde för vissa förvaltningar att avancera med systemförvaltningen. Dock uttrycktes även en frustration över att standardiseringen av digitala utvecklingsprocesser fortfarande var bristfällig, att användarkompetensen var låg och att tillgången till digitala verktyg behövde förbättras. Blandade attityder kring konceptet "digital först" betonades, vilket pekade på ett fortsatt behov av bättre samarbete och enhetliga riktlinjer.
Under det senaste året upplevde de svarande att satsningarna på att stärka IT-styrningen och den digitala strategin intensifierades. Fokus låg på att utveckla informationssäkerheten och att mäta effekten av de digitala satsningarna för att bygga långsiktig kompetens. Samtidigt uppmärksammade flera att innovationsviljan och spridningen av digitala lösningar ökat, men att det fanns utmaningar med att underhålla dessa lösningar över tid. IT-avdelningen betraktades som ett värdefullt stöd, men den begränsade resursbasen påverkade möjligheten att driva innovation i full skala.
Sammanfattningsvis speglar fritextsvaren från de svarande en tydlig trend: Kommunen rör sig långsamt men säkert mot en mer strukturerad och strategisk hantering av digitala lösningar. Det råder en positiv inställning till digitalisering och innovation, men det finns också en utbredd frustration över utmaningar kopplade till användarkompetens, resursallokering och hållbarhet i de digitala satsningarna.
Nimbler
Nimblr är en molnbaserad IT-säkerhetsutbildningsplattform som med hjälp av korta, interaktiva utbildningsmoduler – så kallad micro training – kontinuerligt höjer medarbetarnas säkerhetsmedvetande. Plattformen anpassar automatiskt utbildningsinnehållet efter varje organisations unika miljö och behandlar aktuella IT-hot såsom ransomware, phishing och säker surfning. Vidare ingår realistiska simulerade attacker och uppdaterade zero-day classes, vilka utformas med kundspecifik information för att spegla verkliga förhållanden. Zero-day classes är korta moduler som kontinuerligt uppdateras med innehåll baserat på de allra senaste IT-hot och attacker, och syftar till att snabbt täppa till akuta kunskapsluckor innan nya hot blir allmänt kända eller patchade. De simulerade attackerna, som bland annat omfattar nätfiske, ransomware och andra former av social engineering, baseras på tusentals aktuella hot analyserade av säkerhetsexperter. Genom att utsätta medarbetare för dessa realistiska scenarier får de praktisk träning i att känna igen och hantera olika typer av attacker, och deras respons mäts med en avancerad algoritm som resulterar i en mätbar "Awareness Level" både individuellt och för organisationen i stort. 
Hos oss i Karlskoga kommun har denna insats visat på tydliga resultat: sedan utbildningens start har strax över 50 000 simulerade hot skickats ut i organisationen och dessa har en klickfrekvens på cirka 2 % (det vill säga att en användare klickat på länken i det simulerade hotet), där de flesta klicken inträffade i utbildningens inledande skede och därefter minskat betydligt. Denna utveckling visar en stadig ökning av medvetenhetsnivån och visar tydligt att utbildningsinsatsen stärker säkerhetsmedvetandet i organisationen.  
Resultat
Digitaliseringsarbetet i Karlskoga kommun befinner sig i en övergångsfas, där vissa framsteg har gjorts men där flera utmaningar kvarstår. Den digitala utvecklingen har hittills drivits av enskilda initiativ och en sammanhållen, kommunövergripande, strategi saknas, vilket har lett till att digital mognad och kompetens varierar kraftigt mellan olika delar av organisationen. Insatser inom IT-säkerhet och digital infrastruktur har haft positiva effekter, men utan en enhetlig strategi riskerar digitaliseringen att utvecklas ojämnt och att värdefulla initiativ inte sprids eller samordnas på ett effektivt sätt.
Digitala initiativ - varierande kompetens
Digitaliseringen inom kommunen drivs ofta av enskilda förvaltningar utan en övergripande samordning. Detta har lett till att vissa verksamheter har kommit långt i sin digitala utveckling, medan andra ligger efter. Skillnaderna i digital kompetens mellan medarbetare påverkar hur effektivt digitala verktyg används, och flera delar pekar på att det saknas stöd för att säkerställa en jämn kompetensutveckling i hela organisationen.
En annan utmaning är att det saknas en tydlig och strukturerad metod för att integrera digitala initiativ i den dagliga verksamheten. Digitalisering ses i vissa fall som ett separat område snarare än som en del av den ordinarie verksamhetsutvecklingen, vilket gör att initiativ riskerar att stanna vid projektstadiet utan att bli en naturlig del av organisationens arbetssätt. Det finns även utmaningar i att sprida initiativ och erfarenheter mellan olika verksamheter.
Digitalt ledarskap och uppföljning
En annan central utmaning som framkommer är utmaningar att nå ett tydligt digitalt ledarskap. Det saknas en övergripande struktur för att driva digitaliseringen framåt och skapa en gemensam förståelse för hur digitala lösningar kan användas strategiskt. Digitalisering är en förändringsresa som kräver aktiv styrning, men idag saknas en systematisk uppföljning av digitaliseringsinsatserna, vilket gör det svårt att mäta deras effekter och dra lärdomar inför framtida satsningar.
Effektmätning är en avgörande faktor för att kunna fatta datadrivna beslut och här har vi som organisation utmaningar. Det finns idag ingen enhetlig metod för att utvärdera digitala projekt, vilket gör det svårt att se vilka insatser som ger störst nytta. Detta riskerar att leda till att resurser investeras i lösningar som inte ger önskad effekt, samtidigt som framgångsrika initiativ inte alltid identifieras och förstärks. För att digitaliseringen ska bli en naturlig och långsiktig del av verksamheten krävs en tydligare styrning och en systematisk uppföljning av hur digitala verktyg påverkar effektivitet, arbetsmiljö och service till invånarna.
Resursbrist och kulturella hinder
En faktor som påverkar digitaliseringstakten är tillgången till resurser. Vissa förvaltningar upplever resursbrist, både i form av personal, ekonomiska medel och i vissa fall kompetens, vilket gör det svårt att genomföra digitaliseringsinsatser i den takt som vore önskvärd. Personalomsättning och varierande kompetensnivåer bidrar också till att digitaliseringsarbetet inte kan drivas jämnt över hela organisationen.
Utöver de praktiska utmaningarna finns även kulturella hinder som påverkar utvecklingen. I vissa delar av verksamheten finns en viss skepsis mot digitalisering, där tekniken ses som ett stöd snarare än en drivkraft för förändring. Det framkommer att vissa verksamheter upplever att digitaliseringen kan hota den mänskliga interaktionen och att digitala lösningar inte alltid anpassas efter verksamhetens behov. För att öka acceptansen och förståelsen för digitaliseringens möjligheter krävs ett arbete med organisationskulturen, där förändring ses som en naturlig del av verksamhetsutvecklingen snarare än som något som påtvingas utifrån. Viktigt att här poängtera är att digitaliseringen inte ska vara ett mål i sig, digitalisering ska nyttjas då den tillför mervärde eller underlättar. Rätt använd kommer digitaliseringen frigöra tid och öppna upp för mer mellanmänsklig interaktion där vi nyttjar tid tillsammans på ett klokt och värdeskapande sätt. Utmaningen här blir att identifiera var, när och vilka digitala resurser som ska nyttjas, här behöver vi vara modiga att testa och även våga misslyckas för att utvecklas framåt.
Positiva trender och utvecklingsmöjligheter
Trots utmaningar finns det flera tecken på att digitaliseringsarbetet går framåt och att det finns goda möjligheter att öka takten. Mätningar med Dimios visar att den digitala mognaden har ökat stadigt de senaste åren, särskilt mellan 2022 och 2023. Detta tyder på att det finns en vilja och en grundläggande kapacitet att arbeta mer digitalt, även om det behövs ytterligare insatser för att stärka den strategiska samordningen och kompetensutvecklingen.
Ett annat positivt tecken är att flera initiativ inom IT-säkerhet och digital kompetensutveckling har gett mätbara resultat. Exempelvis har insatserna inom Nimbler bidragit till en ökad medvetenhet om cybersäkerhet, vilket visar att riktade utbildningsinsatser kan ha stor effekt. Workshoppen med KnowIT pekar också på en vilja att arbeta mer strukturerat med digitalisering och att skapa en gemensam vision för hur kommunen ska utvecklas digitalt.
Genom att införa en enhetlig digital lärplattform och etablera forum för chefer och strateger kan kommunen skapa en mer sammanhållen digitaliseringsprocess där initiativ samordnas, kunskap sprids och resurser används mer effektivt.
Sammanfattning
Karlskoga kommun har redan tagit flera steg mot en mer digitaliserad verksamhet, men det finns fortfarande betydande utmaningar som behöver hanteras. Digitaliseringen präglas av fragmenterade initiativ och en varierande nivå av digital mognad, där vissa verksamheter har kommit långt medan andra har större behov av stöd. Utmaningar i det digitala ledarskapet och en systematisk uppföljning gör det svårt att mäta effekterna av digitaliseringsinsatserna, vilket försvårar datadrivna beslut.
Samtidigt finns det tydliga möjligheter att öka digitaliseringstakten genom att samordna initiativ, stärka digitalt ledarskap och skapa en gemensam strategi för hela kommunen. Genom att införa en central digital lärplattform, satsa på riktade utbildningsinsatser och etablera forum för strategiskt samarbete kan kommunen skapa bättre förutsättningar för en långsiktig, effektiv och hållbar digital transformation. Med en tydlig och gemensam vision kan digitalisering bli en drivkraft för verksamhetsutveckling och effektivisering, snarare än ett isolerat teknikfokus.
Efter att ha analyserat data från tjänsteskrivelsen, workshopen med KnowIT, tre års Dimiosmätningar samt resultatet från Nimbler-utbildningen framträder en tydlig bild av kommunens digitaliseringsarbete.
Digitaliseringsarbetet i Karlskoga kommun befinner sig i en övergångsfas, där vissa framsteg har gjorts men där flera utmaningar kvarstår. Den digitala utvecklingen har hittills drivits av enskilda initiativ och en sammanhållen, kommunövergripande, strategi saknas, vilket har lett till att digital mognad och kompetens varierar kraftigt mellan olika delar av organisationen. Insatser inom IT-säkerhet och digital infrastruktur har haft positiva effekter, men utan en enhetlig strategi riskerar digitaliseringen att utvecklas ojämnt och att värdefulla initiativ inte sprids eller samordnas på ett effektivt sätt.
 
 
4. Förslag på åtgärder
För att öka digitaliseringstakten i Karlskoga kommun krävs en helhetsinsats där en strategisk revidering, en gemensam digital plattform, systematisk kompetenskartläggning, stärkt ledarskap samt kontinuerlig effektmätning samverkar. Resultaten från befintliga initiativ visar att framsteg redan sker, men en enhetlig och integrerad strategi skulle ytterligare möjliggöra ett snabbare och mer hållbart digitaliseringsarbete genom dessa åtgärder:
 
Revidera digitaliseringsstrategin
Kommunens digitaliseringsstrategi bör revideras i linje med regeringens nya nationella riktlinjer för 2025 (Strategiska prioriteringar för digitaliseringspolitiken 2025–2030 - Mot ett digitalt Sverige 2030, u.d.), vilket innebär att en lokal behovsanalys genomförs och verksamheterna involveras via samråd och workshops. Genom att ta fram en populärversion av strategin, kompletterad med korta videor och infografik, ökas förståelsen och medvetenheten hos medarbetare.
 
Gemensam kunskapsbank
Införandet av en gemensam digital plattform är en central åtgärd i detta arbete. En strukturerad och central plattform gör det möjligt för alla medarbetare att få tillgång till nödvändiga verktyg, utbildningar och information som stärker den digitala kompetensen. Plattformen bör inte enbart fungera som en statisk kunskapsbank, utan även erbjuda interaktiva element såsom diskussionsforum, handledning och kanske rent av spelifierade utbildningsmoduler. Genom att integrera regelbundna kompetenstester i plattformen skapas förutsättningar för individanpassade utvecklingsplaner och en kontinuerlig uppföljning av den digitala mognaden. I denna plattform finns även ett onboardingprogram för nyrekryterade, vilket bidrar till att skapa en enhetlig och hållbar kompetensbas.
 
Skapa utbildningsmaterial
Vi behöver stärka kulturen med fokus på öppenhet, trygghet, innovation och samarbete bör främjas. Detta kan uppnås genom användning av tjänstedesign samt införande av digitala ambassadörsprogram där medarbetare med hög digital kompetens sprider kunskap och inspiration. Utbildningar ska samlas i den gemensamma kunskapsbanken.
 
Kompetenskartläggning
En systematisk initial kartläggning av medarbetarnas digitala färdigheter är avgörande för att identifiera eventuella kompetensluckor. Detta bidrar till att rätt utbildningsmaterial kan produceras för att täcka dessa kompetensluckor. Genom att löpande genomföra tester och matcha resultaten med riktade utbildningsinsatser via lärplattform kan kommunen stärka den långsiktiga kompetensutvecklingen och även se om utbildningsmaterialet som produceras ger resultat. Genom att kombinera data från plattformen med undersökningar, som Dimios, skapas ett heltäckande beslutsunderlag som möjliggör datadrivna uppföljningar och gör det möjligt att fatta besult om åtgärder kopplat till kompetensutvecklande insatser. Då Dimios mäter digital mognad bör denna undersökning kompletteras med Dikois eller liknande för mätning av digital kompetens
 
 
Leda i digitalisering
Stärkt digitalt ledarskap och samordning är också en central del i arbetet. Personalledare ska ha möjlighet att få det stöd som krävs för att driva digitaliseringsarbetet framåt. Att erbjuda kommunövergripande forum för personalledare möjliggör en gemensam vision och bidrar till att undvika att arbetet hamnar i silos utan samverkan. Dessa forum ska vara verksamhetsnära där praktiska arbetsuppgifter ska ha en stor del för att skapa trygghet och förståelse hos personalledare. Som personalledare ska vi möjliggöra och uppmuntra våra verksamheter att testa nya digitala lösningar, kanske i mindre pilotprojekt. ]
"""

# Om ingen systemprompt finns sparad, sätt då en standardprompt som inkluderar rapporten
if 'system_prompt' not in st.session_state:
    st.session_state.system_prompt = f"{chat_prompt}\n\nDu svarar endast baserat på följande rapport:\n{report_text}"

# Check and set default values if not set in session_state
if "llm_temperature" not in st.session_state:
    st.session_state["llm_temperature"] = 0.7
if "llm_chat_model" not in st.session_state:
    st.session_state["llm_chat_model"] = "OpenAI GPT-4o mini"

### SIDEBAR
#menu()

### MAIN PAGE

col1, col2 = st.columns(2)

with col1:
    if st.button(f"{chat_clear_chat}", type="secondary"):
        # Nollställ chatt-historiken med en hälsning från assistenten
        st.session_state.messages = [{"role": "assistant", "content": f"{chat_hello}"}]

# Only show settings if user is admin
with col2:
    if st.session_state.get("is_admin", False):
        with st.expander(f"{chat_settings}"):
            llm_model = st.selectbox(
                f"{chat_choose_llm}",
                ["OpenAI GPT-4o", "OpenAI GPT-4o mini", "OpenAI o1-preview", "OpenAI o1-mini"],
                index=["OpenAI GPT-4o", "OpenAI GPT-4o mini", "OpenAI o1-preview", "OpenAI o1-mini"].index(st.session_state["llm_chat_model"]),
            )
            llm_temp = st.slider(
                f"{chat_choose_temp}",
                min_value=0.0,
                max_value=1.0,
                step=0.1,
                value=st.session_state["llm_temperature"],
            )
            # Uppdatera session_state direkt
            st.session_state["llm_chat_model"] = llm_model
            st.session_state["llm_temperature"] = llm_temp
            
            model_map = {
                "OpenAI GPT-4o": "gpt-4o",
                "OpenAI GPT-4o mini": "gpt-4o-mini",
                "OpenAI o1-preview": "o1-preview", 
                "OpenAI o1-mini": "o1-mini"
            }
            st.markdown("###### ")
            with st.form("my_form"):
                prompt_input = st.text_area(f"{chat_system_prompt}", st.session_state.system_prompt, height=200)
                st.session_state.system_prompt = prompt_input   
                st.form_submit_button(f"{chat_save}")

# Display current model in sidebar only for admins
if st.session_state.get("is_admin", False):
    model_map = {
        "OpenAI GPT-4o": "gpt-4o",
        "OpenAI GPT-4o mini": "gpt-4o-mini",
        "OpenAI o1-preview": "o1-preview", 
        "OpenAI o1-mini": "o1-mini"
    }
    if "OpenAI" in st.session_state["llm_chat_model"]:
        st.sidebar.success("Språkmodell: " + st.session_state["llm_chat_model"])
    else:
        st.sidebar.success("Språkmodell: " + st.session_state["llm_chat_model"])

# Initiera chatt-historiken om den inte finns
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": f"{chat_hello}"}]

# Visa chattmeddelanden med streamlits chat_message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Om innehållet är en bild-URL
        if message["content"].startswith("http"):
            st.image(message["content"])
        else:
            st.markdown(message["content"])

# Hämta systemprompten
system_prompt = st.session_state.system_prompt

# Använd st.chat_input för att fånga upp användarens fråga
if prompt := st.chat_input(f"{chat_imput_q}"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Förbered meddelanden: här prependas systemprompten till varje användarmeddelande
        processed_messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                content_with_prompt = system_prompt + " " + m["content"]
                processed_messages.append({"role": m["role"], "content": content_with_prompt})
            else:
                processed_messages.append(m)

        # Anropa vald LLM via OpenAI eller Groq
        if "OpenAI" in st.session_state["llm_chat_model"]:
            if c.deployment == "streamlit":
                client = OpenAI(api_key=st.secrets.openai_key)
            else:
                client = OpenAI(api_key=environ.get("openai_key"))
    
            for response in client.chat.completions.create(
                model=model_map[st.session_state["llm_chat_model"]],
                temperature=st.session_state["llm_temperature"],
                messages=processed_messages,
                stream=True,
            ):
                if response.choices[0].delta.content:
                    full_response += str(response.choices[0].delta.content)
                message_placeholder.markdown(full_response + "▌")  
        else:
            if c.deployment == "streamlit":
                client = Groq(api_key=st.secrets.groq_key)
            else:
                client = Groq(api_key=environ.get("groq_key"))
            # Ta bort eventuell 'avatar'-nyckel för Groq-meddelanden
            processed_messages_no_avatar = [{"role": m["role"], "content": m["content"]} for m in processed_messages]
            stream = client.chat.completions.create(
                messages=processed_messages_no_avatar,
                model=model_map[st.session_state["llm_chat_model"]],
                temperature=st.session_state["llm_temperature"],
                max_tokens=1024,
                top_p=1,
                stop=None,
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += str(chunk.choices[0].delta.content)
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
