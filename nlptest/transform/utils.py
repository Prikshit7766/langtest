from collections import defaultdict
from typing import Dict, List

import pandas as pd

from nlptest.utils.custom_types import NERPrediction, Sample, SequenceLabel, NEROutput, SequenceClassificationOutput

DEFAULT_PERTURBATIONS = [
    "uppercase",
    "lowercase",
    "titlecase",
    "add_punctuation",
    "strip_punctuation",
    "add_typo",
    "american_to_british",
    "british_to_american",
    "add_context",
    "add_contractions",
    "swap_entities",
    "replace_to_male_pronouns",
    "replace_to_female_pronouns",
    "replace_to_neutral_pronouns",
    "number_to_word"
    "add_ocr_typo"
]

PERTURB_CLASS_MAP = {
    "uppercase": 'UpperCase',
    "lowercase": 'LowerCase',
    "titlecase": 'TitleCase',
    "add_punctuation": 'AddPunctuation',
    "strip_punctuation": 'StripPunctuation',
    "add_typo": 'AddTypo',
    "american_to_british": 'ConvertAccent',
    "british_to_american": 'ConvertAccent',
    "add_context": 'AddContext',
    "add_contractions": 'AddContraction',
    "swap_entities": 'SwapEntities',
    "replace_to_male_pronouns": "GenderPronounBias",
    "replace_to_female_pronouns": "GenderPronounBias",
    "replace_to_neutral_pronouns": "GenderPronounBias",
    "number_to_word": "NumberToWord",
    "add_ocr_typo": "AddOcrTypo"
}

# @formatter:off
A2B_DICT = {"accessorize": "accessorise", "accessorized": "accessorised", "accessorizes": "accessorises",
            "accessorizing": "accessorising", "acclimatization": "acclimatisation", "acclimatize": "acclimatise",
            "acclimatized": "acclimatised", "acclimatizes": "acclimatises", "acclimatizing": "acclimatising",
            "accouterments": "accoutrements", "eon": "aeon", "eons": "aeons", "aerogram": "aerogramme",
            "aerograms": "aerogrammes", "airplane": "aeroplane", "airplanes": "aeroplanes", "esthete": "aesthete",
            "esthetes": "aesthetes", "esthetic": "aesthetic", "esthetically": "aesthetically",
            "esthetics": "aesthetics", "etiology": "aetiology", "aging": "ageing", "aggrandizement": "aggrandisement",
            "agonize": "agonise", "agonized": "agonised", "agonizes": "agonises", "agonizing": "agonising",
            "agonizingly": "agonisingly", "almanac": "almanack", "almanacs": "almanacks", "aluminum": "aluminium",
            "amortizable": "amortisable", "amortization": "amortisation", "amortizations": "amortisations",
            "amortize": "amortise", "amortized": "amortised", "amortizes": "amortises", "amortizing": "amortising",
            "amphitheater": "amphitheatre", "amphitheaters": "amphitheatres", "anemia": "anaemia", "anemic": "anaemic",
            "anesthesia": "anaesthesia", "anesthetic": "anaesthetic", "anesthetics": "anaesthetics",
            "anesthetize": "anaesthetize", "anesthetized": "anaesthetized", "anesthetizes": "anaesthetizes",
            "anesthetizing": "anaesthetizing", "anesthetist": "anaesthetist", "anesthetists": "anaesthetists",
            "analog": "analogue", "analogs": "analogues", "analyze": "analyse", "analyzed": "analysed",
            "analyzes": "analyses", "analyzing": "analysing", "anglicize": "anglicise", "anglicized": "anglicised",
            "anglicizes": "anglicises", "anglicizing": "anglicising", "annualized": "annualised",
            "antagonize": "antagonise", "antagonized": "antagonised", "antagonizes": "antagonises",
            "antagonizing": "antagonising", "apologize": "apologise", "apologized": "apologised",
            "apologizes": "apologises", "apologizing": "apologising", "appall": "appal", "appalls": "appals",
            "appetizer": "appetiser", "appetizers": "appetisers", "appetizing": "appetising",
            "appetizingly": "appetisingly", "arbor": "arbour", "arbors": "arbours", "archeological": "archaeological",
            "archeologically": "archaeologically", "archeologist": "archaeologist", "archeologists": "archaeologists",
            "archeology": "archaeology", "ardor": "ardour", "armor": "armour", "armored": "armoured",
            "armorer": "armourer", "armorers": "armourers", "armories": "armouries", "armory": "armoury",
            "artifact": "artefact", "artifacts": "artefacts", "authorize": "authorise", "authorized": "authorised",
            "authorizes": "authorises", "authorizing": "authorising", "ax": "axe", "backpedaled": "backpedalled",
            "backpedaling": "backpedalling", "banister": "bannister", "banisters": "bannisters", "baptize": "baptise",
            "baptized": "baptised", "baptizes": "baptises", "baptizing": "baptising", "bastardize": "bastardise",
            "bastardized": "bastardised", "bastardizes": "bastardises", "bastardizing": "bastardising",
            "battleax": "battleaxe", "balk": "baulk", "balked": "baulked", "balking": "baulking", "balks": "baulks",
            "bedeviled": "bedevilled", "bedeviling": "bedevilling", "behavior": "behaviour",
            "behavioral": "behavioural", "behaviorism": "behaviourism", "behaviorist": "behaviourist",
            "behaviorists": "behaviourists", "behaviors": "behaviours", "behoove": "behove", "behooved": "behoved",
            "behooves": "behoves", "bejeweled": "bejewelled", "belabor": "belabour", "belabored": "belaboured",
            "belaboring": "belabouring", "belabors": "belabours", "beveled": "bevelled", "bevies": "bevvies",
            "bevy": "bevvy", "biased": "biassed", "biasing": "biassing", "binging": "bingeing",
            "bougainvillea": "bougainvillaea", "bougainvilleas": "bougainvillaeas", "bowdlerize": "bowdlerise",
            "bowdlerized": "bowdlerised", "bowdlerizes": "bowdlerises", "bowdlerizing": "bowdlerising",
            "breathalyze": "breathalyse", "breathalyzed": "breathalysed", "breathalyzer": "breathalyser",
            "breathalyzers": "breathalysers", "breathalyzes": "breathalyses", "breathalyzing": "breathalysing",
            "brutalize": "brutalise", "brutalized": "brutalised", "brutalizes": "brutalises",
            "brutalizing": "brutalising", "busses": "buses", "bussing": "busing", "cesarean": "caesarean",
            "cesareans": "caesareans", "caliber": "calibre", "calibers": "calibres", "caliper": "calliper",
            "calipers": "callipers", "calisthenics": "callisthenics", "canalize": "canalise", "canalized": "canalised",
            "canalizes": "canalises", "canalizing": "canalising", "cancelation": "cancellation",
            "cancelations": "cancellations", "canceled": "cancelled", "canceling": "cancelling", "candor": "candour",
            "cannibalize": "cannibalise", "cannibalized": "cannibalised", "cannibalizes": "cannibalises",
            "cannibalizing": "cannibalising", "canonize": "canonise", "canonized": "canonised",
            "canonizes": "canonises", "canonizing": "canonising", "capitalize": "capitalise",
            "capitalized": "capitalised", "capitalizes": "capitalises", "capitalizing": "capitalising",
            "caramelize": "caramelise", "caramelized": "caramelised", "caramelizes": "caramelises",
            "caramelizing": "caramelising", "carbonize": "carbonise", "carbonized": "carbonised",
            "carbonizes": "carbonises", "carbonizing": "carbonising", "caroled": "carolled", "caroling": "carolling",
            "catalog": "catalogue", "cataloged": "catalogued", "catalogs": "catalogues", "cataloging": "cataloguing",
            "catalyze": "catalyse", "catalyzed": "catalysed", "catalyzes": "catalyses", "catalyzing": "catalysing",
            "categorize": "categorise", "categorized": "categorised", "categorizes": "categorises",
            "categorizing": "categorising", "cauterize": "cauterise", "cauterized": "cauterised",
            "cauterizes": "cauterises", "cauterizing": "cauterising", "caviled": "cavilled", "caviling": "cavilling",
            "centigram": "centigramme", "centigrams": "centigrammes", "centiliter": "centilitre",
            "centiliters": "centilitres", "centimeter": "centimetre", "centimeters": "centimetres",
            "centralize": "centralise", "centralized": "centralised", "centralizes": "centralises",
            "centralizing": "centralising", "center": "centre", "centered": "centred", "centerfold": "centrefold",
            "centerfolds": "centrefolds", "centerpiece": "centrepiece", "centerpieces": "centrepieces",
            "centers": "centres", "channeled": "channelled", "channeling": "channelling",
            "characterize": "characterise", "characterized": "characterised", "characterizes": "characterises",
            "characterizing": "characterising", "checkbook": "chequebook", "checkbooks": "chequebooks",
            "checkered": "chequered", "chili": "chilli", "chimera": "chimaera", "chimeras": "chimaeras",
            "chiseled": "chiselled", "chiseling": "chiselling", "circularize": "circularise",
            "circularized": "circularised", "circularizes": "circularises", "circularizing": "circularising",
            "civilize": "civilise", "civilized": "civilised", "civilizes": "civilises", "civilizing": "civilising",
            "clamor": "clamour", "clamored": "clamoured", "clamoring": "clamouring", "clamors": "clamours",
            "clangor": "clangour", "clarinetist": "clarinettist", "clarinetists": "clarinettists",
            "collectivize": "collectivise", "collectivized": "collectivised", "collectivizes": "collectivises",
            "collectivizing": "collectivising", "colonization": "colonisation", "colonize": "colonise",
            "colonized": "colonised", "colonizer": "coloniser", "colonizers": "colonisers", "colonizes": "colonises",
            "colonizing": "colonising", "color": "colour", "colorant": "colourant", "colorants": "colourants",
            "colored": "coloured", "coloreds": "coloureds", "colorful": "colourful", "colorfully": "colourfully",
            "coloring": "colouring", "colorize": "colourize", "colorized": "colourized", "colorizes": "colourizes",
            "colorizing": "colourizing", "colorless": "colourless", "colors": "colours",
            "commercialize": "commercialise", "commercialized": "commercialised", "commercializes": "commercialises",
            "commercializing": "commercialising", "compartmentalize": "compartmentalise",
            "compartmentalized": "compartmentalised", "compartmentalizes": "compartmentalises",
            "compartmentalizing": "compartmentalising", "computerize": "computerise", "computerized": "computerised",
            "computerizes": "computerises", "computerizing": "computerising", "conceptualize": "conceptualise",
            "conceptualized": "conceptualised", "conceptualizes": "conceptualises",
            "conceptualizing": "conceptualising", "connection": "connexion", "connections": "connexions",
            "contextualize": "contextualise", "contextualized": "contextualised", "contextualizes": "contextualises",
            "contextualizing": "contextualising", "cozier": "cosier", "cozies": "cosies", "coziest": "cosiest",
            "cozily": "cosily", "coziness": "cosiness", "cozy": "cosy", "councilor": "councillor",
            "councilors": "councillors", "counseled": "counselled", "counseling": "counselling",
            "counselor": "counsellor", "counselors": "counsellors", "crenelated": "crenellated",
            "criminalize": "criminalise", "criminalized": "criminalised", "criminalizes": "criminalises",
            "criminalizing": "criminalising", "criticize": "criticise", "criticized": "criticised",
            "criticizes": "criticises", "criticizing": "criticising", "crueler": "crueller", "cruelest": "cruellest",
            "crystallization": "crystallisation", "crystallize": "crystallise", "crystallized": "crystallised",
            "crystallizes": "crystallises", "crystallizing": "crystallising", "cudgeled": "cudgelled",
            "cudgeling": "cudgelling", "customize": "customise", "customized": "customised", "customizes": "customises",
            "customizing": "customising", "decentralization": "decentralisation", "decentralize": "decentralise",
            "decentralized": "decentralised", "decentralizes": "decentralises", "decentralizing": "decentralising",
            "decriminalization": "decriminalisation", "decriminalize": "decriminalise",
            "decriminalized": "decriminalised", "decriminalizes": "decriminalises",
            "decriminalizing": "decriminalising", "defense": "defence", "defenseless": "defenceless",
            "defenses": "defences", "dehumanization": "dehumanisation", "dehumanize": "dehumanise",
            "dehumanized": "dehumanised", "dehumanizes": "dehumanises", "dehumanizing": "dehumanising",
            "demeanor": "demeanour", "demilitarization": "demilitarisation", "demilitarize": "demilitarise",
            "demilitarized": "demilitarised", "demilitarizes": "demilitarises", "demilitarizing": "demilitarising",
            "demobilization": "demobilisation", "demobilize": "demobilise", "demobilized": "demobilised",
            "demobilizes": "demobilises", "demobilizing": "demobilising", "democratization": "democratisation",
            "democratize": "democratise", "democratized": "democratised", "democratizes": "democratises",
            "democratizing": "democratising", "demonize": "demonise", "demonized": "demonised",
            "demonizes": "demonises", "demonizing": "demonising", "demoralization": "demoralisation",
            "demoralize": "demoralise", "demoralized": "demoralised", "demoralizes": "demoralises",
            "demoralizing": "demoralising", "denationalization": "denationalisation", "denationalize": "denationalise",
            "denationalized": "denationalised", "denationalizes": "denationalises",
            "denationalizing": "denationalising", "deodorize": "deodorise", "deodorized": "deodorised",
            "deodorizes": "deodorises", "deodorizing": "deodorising", "depersonalize": "depersonalise",
            "depersonalized": "depersonalised", "depersonalizes": "depersonalises",
            "depersonalizing": "depersonalising", "deputize": "deputise", "deputized": "deputised",
            "deputizes": "deputises", "deputizing": "deputising", "desensitization": "desensitisation",
            "desensitize": "desensitise", "desensitized": "desensitised", "desensitizes": "desensitises",
            "desensitizing": "desensitising", "destabilization": "destabilisation", "destabilize": "destabilise",
            "destabilized": "destabilised", "destabilizes": "destabilises", "destabilizing": "destabilising",
            "dialed": "dialled", "dialing": "dialling", "dialog": "dialogue", "dialogs": "dialogues",
            "diarrhea": "diarrhoea", "digitize": "digitise", "digitized": "digitised", "digitizes": "digitises",
            "digitizing": "digitising", "disk": "disc", "discolor": "discolour", "discolored": "discoloured",
            "discoloring": "discolouring", "discolors": "discolours", "disks": "discs", "disemboweled": "disembowelled",
            "disemboweling": "disembowelling", "disfavor": "disfavour", "disheveled": "dishevelled",
            "dishonor": "dishonour", "dishonorable": "dishonourable", "dishonorably": "dishonourably",
            "dishonored": "dishonoured", "dishonoring": "dishonouring", "dishonors": "dishonours",
            "disorganization": "disorganisation", "disorganized": "disorganised", "distill": "distil",
            "distills": "distils", "dramatization": "dramatisation", "dramatizations": "dramatisations",
            "dramatize": "dramatise", "dramatized": "dramatised", "dramatizes": "dramatises",
            "dramatizing": "dramatising", "draft": "draught", "draftboard": "draughtboard",
            "draftboards": "draughtboards", "draftier": "draughtier", "draftiest": "draughtiest", "drafts": "draughts",
            "draftsman": "draughtsman", "draftsmanship": "draughtsmanship", "draftsmen": "draughtsmen",
            "draftswoman": "draughtswoman", "draftswomen": "draughtswomen", "drafty": "draughty",
            "driveled": "drivelled", "driveling": "drivelling", "dueled": "duelled", "dueling": "duelling",
            "economize": "economise", "economized": "economised", "economizes": "economises",
            "economizing": "economising", "edema": "edoema", "editorialize": "editorialise",
            "editorialized": "editorialised", "editorializes": "editorialises", "editorializing": "editorialising",
            "empathize": "empathise", "empathized": "empathised", "empathizes": "empathises",
            "empathizing": "empathising", "emphasize": "emphasise", "emphasized": "emphasised",
            "emphasizes": "emphasises", "emphasizing": "emphasising", "enameled": "enamelled",
            "enameling": "enamelling", "enamored": "enamoured", "encyclopedia": "encyclopaedia",
            "encyclopedias": "encyclopaedias", "encyclopedic": "encyclopaedic", "endeavor": "endeavour",
            "endeavored": "endeavoured", "endeavoring": "endeavouring", "endeavors": "endeavours",
            "energize": "energise", "energized": "energised", "energizes": "energises", "energizing": "energising",
            "enroll": "enrol", "enrolls": "enrols", "enthrall": "enthral", "enthralls": "enthrals",
            "epaulet": "epaulette", "epaulets": "epaulettes", "epicenter": "epicentre", "epicenters": "epicentres",
            "epilog": "epilogue", "epilogs": "epilogues", "epitomize": "epitomise", "epitomized": "epitomised",
            "epitomizes": "epitomises", "epitomizing": "epitomising", "equalization": "equalisation",
            "equalize": "equalise", "equalized": "equalised", "equalizer": "equaliser", "equalizers": "equalisers",
            "equalizes": "equalises", "equalizing": "equalising", "eulogize": "eulogise", "eulogized": "eulogised",
            "eulogizes": "eulogises", "eulogizing": "eulogising", "evangelize": "evangelise",
            "evangelized": "evangelised", "evangelizes": "evangelises", "evangelizing": "evangelising",
            "exorcize": "exorcise", "exorcized": "exorcised", "exorcizes": "exorcises", "exorcizing": "exorcising",
            "extemporization": "extemporisation", "extemporize": "extemporise", "extemporized": "extemporised",
            "extemporizes": "extemporises", "extemporizing": "extemporising", "externalization": "externalisation",
            "externalizations": "externalisations", "externalize": "externalise", "externalized": "externalised",
            "externalizes": "externalises", "externalizing": "externalising", "factorize": "factorise",
            "factorized": "factorised", "factorizes": "factorises", "factorizing": "factorising", "fecal": "faecal",
            "feces": "faeces", "familiarization": "familiarisation", "familiarize": "familiarise",
            "familiarized": "familiarised", "familiarizes": "familiarises", "familiarizing": "familiarising",
            "fantasize": "fantasise", "fantasized": "fantasised", "fantasizes": "fantasises",
            "fantasizing": "fantasising", "favor": "favour", "favorable": "favourable", "favorably": "favourably",
            "favored": "favoured", "favoring": "favouring", "favorite": "favourite", "favorites": "favourites",
            "favoritism": "favouritism", "favors": "favours", "feminize": "feminise", "feminized": "feminised",
            "feminizes": "feminises", "feminizing": "feminising", "fertilization": "fertilisation",
            "fertilize": "fertilise", "fertilized": "fertilised", "fertilizer": "fertiliser",
            "fertilizers": "fertilisers", "fertilizes": "fertilises", "fertilizing": "fertilising", "fervor": "fervour",
            "fiber": "fibre", "fiberglass": "fibreglass", "fibers": "fibres", "fictionalization": "fictionalisation",
            "fictionalizations": "fictionalisations", "fictionalize": "fictionalise", "fictionalized": "fictionalised",
            "fictionalizes": "fictionalises", "fictionalizing": "fictionalising", "filet": "fillet",
            "fileted": "filleted", "fileting": "filleting", "filets": "fillets", "finalization": "finalisation",
            "finalize": "finalise", "finalized": "finalised", "finalizes": "finalises", "finalizing": "finalising",
            "flutist": "flautist", "flutists": "flautists", "flavor": "flavour", "flavored": "flavoured",
            "flavoring": "flavouring", "flavorings": "flavourings", "flavorless": "flavourless", "flavors": "flavours",
            "flavorsome": "flavoursome", "fetal": "foetal", "fetid": "foetid", "fetus": "foetus", "fetuses": "foetuses",
            "formalization": "formalisation", "formalize": "formalise", "formalized": "formalised",
            "formalizes": "formalises", "formalizing": "formalising", "fossilization": "fossilisation",
            "fossilize": "fossilise", "fossilized": "fossilised", "fossilizes": "fossilises",
            "fossilizing": "fossilising", "fraternization": "fraternisation", "fraternize": "fraternise",
            "fraternized": "fraternised", "fraternizes": "fraternises", "fraternizing": "fraternising",
            "fulfill": "fulfil", "fulfillment": "fulfilment", "fulfills": "fulfils", "funneled": "funnelled",
            "funneling": "funnelling", "galvanize": "galvanise", "galvanized": "galvanised", "galvanizes": "galvanises",
            "galvanizing": "galvanising", "gamboled": "gambolled", "gamboling": "gambolling", "gasses": "gases",
            "gage": "gauge", "gaged": "gauged", "gages": "gauges", "gaging": "gauging",
            "generalization": "generalisation", "generalizations": "generalisations", "generalize": "generalise",
            "generalized": "generalised", "generalizes": "generalises", "generalizing": "generalising",
            "ghettoize": "ghettoise", "ghettoized": "ghettoised", "ghettoizes": "ghettoises",
            "ghettoizing": "ghettoising", "gypsies": "gipsies", "glamorize": "glamorise", "glamorized": "glamorised",
            "glamorizes": "glamorises", "glamorizing": "glamorising", "glamor": "glamour",
            "globalization": "globalisation", "globalize": "globalise", "globalized": "globalised",
            "globalizes": "globalises", "globalizing": "globalising", "gluing": "glueing", "goiter": "goitre",
            "goiters": "goitres", "gonorrhea": "gonorrhoea", "gram": "gramme", "grams": "grammes",
            "graveled": "gravelled", "gray": "grey", "grayed": "greyed", "graying": "greying", "grayish": "greyish",
            "grayness": "greyness", "grays": "greys", "groveled": "grovelled", "groveling": "grovelling",
            "groin": "groyne", "groins": "groynes", "grueling": "gruelling", "gruelingly": "gruellingly",
            "griffin": "gryphon", "griffins": "gryphons", "gynecological": "gynaecological",
            "gynecologist": "gynaecologist", "gynecologists": "gynaecologists", "gynecology": "gynaecology",
            "hematological": "haematological", "hematologist": "haematologist", "hematologists": "haematologists",
            "hematology": "haematology", "hemoglobin": "haemoglobin", "hemophilia": "haemophilia",
            "hemophiliac": "haemophiliac", "hemophiliacs": "haemophiliacs", "hemorrhage": "haemorrhage",
            "hemorrhaged": "haemorrhaged", "hemorrhages": "haemorrhages", "hemorrhaging": "haemorrhaging",
            "hemorrhoids": "haemorrhoids", "harbor": "harbour", "harbored": "harboured", "harboring": "harbouring",
            "harbors": "harbours", "harmonization": "harmonisation", "harmonize": "harmonise",
            "harmonized": "harmonised", "harmonizes": "harmonises", "harmonizing": "harmonising",
            "homeopath": "homoeopath", "homeopathic": "homoeopathic", "homeopaths": "homoeopaths",
            "homeopathy": "homoeopathy", "homogenize": "homogenise", "homogenized": "homogenised",
            "homogenizes": "homogenises", "homogenizing": "homogenising", "honor": "honour", "honorable": "honourable",
            "honorably": "honourably", "honored": "honoured", "honoring": "honouring", "honors": "honours",
            "hospitalization": "hospitalisation", "hospitalize": "hospitalise", "hospitalized": "hospitalised",
            "hospitalizes": "hospitalises", "hospitalizing": "hospitalising", "humanize": "humanise",
            "humanized": "humanised", "humanizes": "humanises", "humanizing": "humanising", "humor": "humour",
            "humored": "humoured", "humoring": "humouring", "humorless": "humourless", "humors": "humours",
            "hybridize": "hybridise", "hybridized": "hybridised", "hybridizes": "hybridises",
            "hybridizing": "hybridising", "hypnotize": "hypnotise", "hypnotized": "hypnotised",
            "hypnotizes": "hypnotises", "hypnotizing": "hypnotising", "hypothesize": "hypothesise",
            "hypothesized": "hypothesised", "hypothesizes": "hypothesises", "hypothesizing": "hypothesising",
            "idealization": "idealisation", "idealize": "idealise", "idealized": "idealised", "idealizes": "idealises",
            "idealizing": "idealising", "idolize": "idolise", "idolized": "idolised", "idolizes": "idolises",
            "idolizing": "idolising", "immobilization": "immobilisation", "immobilize": "immobilise",
            "immobilized": "immobilised", "immobilizer": "immobiliser", "immobilizers": "immobilisers",
            "immobilizes": "immobilises", "immobilizing": "immobilising", "immortalize": "immortalise",
            "immortalized": "immortalised", "immortalizes": "immortalises", "immortalizing": "immortalising",
            "immunization": "immunisation", "immunize": "immunise", "immunized": "immunised", "immunizes": "immunises",
            "immunizing": "immunising", "impaneled": "impanelled", "impaneling": "impanelling",
            "imperiled": "imperilled", "imperiling": "imperilling", "individualize": "individualise",
            "individualized": "individualised", "individualizes": "individualises",
            "individualizing": "individualising", "industrialize": "industrialise", "industrialized": "industrialised",
            "industrializes": "industrialises", "industrializing": "industrialising", "inflection": "inflexion",
            "inflections": "inflexions", "initialize": "initialise", "initialized": "initialised",
            "initializes": "initialises", "initializing": "initialising", "initialed": "initialled",
            "initialing": "initialling", "install": "instal", "installment": "instalment",
            "installments": "instalments", "installs": "instals", "instill": "instil", "instills": "instils",
            "institutionalization": "institutionalisation", "institutionalize": "institutionalise",
            "institutionalized": "institutionalised", "institutionalizes": "institutionalises",
            "institutionalizing": "institutionalising", "intellectualize": "intellectualise",
            "intellectualized": "intellectualised", "intellectualizes": "intellectualises",
            "intellectualizing": "intellectualising", "internalization": "internalisation",
            "internalize": "internalise", "internalized": "internalised", "internalizes": "internalises",
            "internalizing": "internalising", "internationalization": "internationalisation",
            "internationalize": "internationalise", "internationalized": "internationalised",
            "internationalizes": "internationalises", "internationalizing": "internationalising",
            "ionization": "ionisation", "ionize": "ionise", "ionized": "ionised", "ionizer": "ioniser",
            "ionizers": "ionisers", "ionizes": "ionises", "ionizing": "ionising", "italicize": "italicise",
            "italicized": "italicised", "italicizes": "italicises", "italicizing": "italicising", "itemize": "itemise",
            "itemized": "itemised", "itemizes": "itemises", "itemizing": "itemising", "jeopardize": "jeopardise",
            "jeopardized": "jeopardised", "jeopardizes": "jeopardises", "jeopardizing": "jeopardising",
            "jeweled": "jewelled", "jeweler": "jeweller", "jewelers": "jewellers", "jewelry": "jewellery",
            "judgment": "judgement", "kilogram": "kilogramme", "kilograms": "kilogrammes", "kilometer": "kilometre",
            "kilometers": "kilometres", "labeled": "labelled", "labeling": "labelling", "labor": "labour",
            "labored": "laboured", "laborer": "labourer", "laborers": "labourers", "laboring": "labouring",
            "labors": "labours", "lackluster": "lacklustre", "legalization": "legalisation", "legalize": "legalise",
            "legalized": "legalised", "legalizes": "legalises", "legalizing": "legalising", "legitimize": "legitimise",
            "legitimized": "legitimised", "legitimizes": "legitimises", "legitimizing": "legitimising",
            "leukemia": "leukaemia", "leveled": "levelled", "leveler": "leveller", "levelers": "levellers",
            "leveling": "levelling", "libeled": "libelled", "libeling": "libelling", "libelous": "libellous",
            "liberalization": "liberalisation", "liberalize": "liberalise", "liberalized": "liberalised",
            "liberalizes": "liberalises", "liberalizing": "liberalising", "license": "licence", "licensed": "licenced",
            "licenses": "licences", "licensing": "licencing", "likable": "likeable", "lionization": "lionisation",
            "lionize": "lionise", "lionized": "lionised", "lionizes": "lionises", "lionizing": "lionising",
            "liquidize": "liquidise", "liquidized": "liquidised", "liquidizer": "liquidiser",
            "liquidizers": "liquidisers", "liquidizes": "liquidises", "liquidizing": "liquidising", "liter": "litre",
            "liters": "litres", "localize": "localise", "localized": "localised", "localizes": "localises",
            "localizing": "localising", "louver": "louvre", "louvered": "louvred", "louvers": "louvres",
            "luster": "lustre", "magnetize": "magnetise", "magnetized": "magnetised", "magnetizes": "magnetises",
            "magnetizing": "magnetising", "maneuverability": "manoeuvrability", "maneuverable": "manoeuvrable",
            "maneuver": "manoeuvre", "maneuvered": "manoeuvred", "maneuvers": "manoeuvres",
            "maneuvering": "manoeuvring", "maneuverings": "manoeuvrings", "marginalization": "marginalisation",
            "marginalize": "marginalise", "marginalized": "marginalised", "marginalizes": "marginalises",
            "marginalizing": "marginalising", "marshaled": "marshalled", "marshaling": "marshalling",
            "marveled": "marvelled", "marveling": "marvelling", "marvelous": "marvellous",
            "marvelously": "marvellously", "materialization": "materialisation", "materialize": "materialise",
            "materialized": "materialised", "materializes": "materialises", "materializing": "materialising",
            "maximization": "maximisation", "maximize": "maximise", "maximized": "maximised", "maximizes": "maximises",
            "maximizing": "maximising", "meager": "meagre", "mechanization": "mechanisation", "mechanize": "mechanise",
            "mechanized": "mechanised", "mechanizes": "mechanises", "mechanizing": "mechanising",
            "medieval": "mediaeval", "memorialize": "memorialise", "memorialized": "memorialised",
            "memorializes": "memorialises", "memorializing": "memorialising", "memorize": "memorise",
            "memorized": "memorised", "memorizes": "memorises", "memorizing": "memorising", "mesmerize": "mesmerise",
            "mesmerized": "mesmerised", "mesmerizes": "mesmerises", "mesmerizing": "mesmerising",
            "metabolize": "metabolise", "metabolized": "metabolised", "metabolizes": "metabolises",
            "metabolizing": "metabolising", "meter": "metre", "meters": "metres", "micrometer": "micrometre",
            "micrometers": "micrometres", "militarize": "militarise", "militarized": "militarised",
            "militarizes": "militarises", "militarizing": "militarising", "milligram": "milligramme",
            "milligrams": "milligrammes", "milliliter": "millilitre", "milliliters": "millilitres",
            "millimeter": "millimetre", "millimeters": "millimetres", "miniaturization": "miniaturisation",
            "miniaturize": "miniaturise", "miniaturized": "miniaturised", "miniaturizes": "miniaturises",
            "miniaturizing": "miniaturising", "minibusses": "minibuses", "minimize": "minimise",
            "minimized": "minimised", "minimizes": "minimises", "minimizing": "minimising",
            "misbehavior": "misbehaviour", "misdemeanor": "misdemeanour", "misdemeanors": "misdemeanours",
            "misspelled": "misspelt", "miter": "mitre", "miters": "mitres", "mobilization": "mobilisation",
            "mobilize": "mobilise", "mobilized": "mobilised", "mobilizes": "mobilises", "mobilizing": "mobilising",
            "modeled": "modelled", "modeler": "modeller", "modelers": "modellers", "modeling": "modelling",
            "modernize": "modernise", "modernized": "modernised", "modernizes": "modernises",
            "modernizing": "modernising", "moisturize": "moisturise", "moisturized": "moisturised",
            "moisturizer": "moisturiser", "moisturizers": "moisturisers", "moisturizes": "moisturises",
            "moisturizing": "moisturising", "monolog": "monologue", "monologs": "monologues",
            "monopolization": "monopolisation", "monopolize": "monopolise", "monopolized": "monopolised",
            "monopolizes": "monopolises", "monopolizing": "monopolising", "moralize": "moralise",
            "moralized": "moralised", "moralizes": "moralises", "moralizing": "moralising", "motorized": "motorised",
            "mold": "mould", "molded": "moulded", "molder": "moulder", "moldered": "mouldered",
            "moldering": "mouldering", "molders": "moulders", "moldier": "mouldier", "moldiest": "mouldiest",
            "molding": "moulding", "moldings": "mouldings", "molds": "moulds", "moldy": "mouldy", "molt": "moult",
            "molted": "moulted", "molting": "moulting", "molts": "moults", "mustache": "moustache",
            "mustached": "moustached", "mustaches": "moustaches", "mustachioed": "moustachioed",
            "multicolored": "multicoloured", "nationalization": "nationalisation",
            "nationalizations": "nationalisations", "nationalize": "nationalise", "nationalized": "nationalised",
            "nationalizes": "nationalises", "nationalizing": "nationalising", "naturalization": "naturalisation",
            "naturalize": "naturalise", "naturalized": "naturalised", "naturalizes": "naturalises",
            "naturalizing": "naturalising", "neighbor": "neighbour", "neighborhood": "neighbourhood",
            "neighborhoods": "neighbourhoods", "neighboring": "neighbouring", "neighborliness": "neighbourliness",
            "neighborly": "neighbourly", "neighbors": "neighbours", "neutralization": "neutralisation",
            "neutralize": "neutralise", "neutralized": "neutralised", "neutralizes": "neutralises",
            "neutralizing": "neutralising", "normalization": "normalisation", "normalize": "normalise",
            "normalized": "normalised", "normalizes": "normalises", "normalizing": "normalising", "odor": "odour",
            "odorless": "odourless", "odors": "odours", "esophagus": "oesophagus", "esophaguses": "oesophaguses",
            "estrogen": "oestrogen", "offense": "offence", "offenses": "offences", "omelet": "omelette",
            "omelets": "omelettes", "optimization": "optimisation", "optimizations": "optimisations",
            "optimize": "optimise", "optimized": "optimised", "optimizes": "optimises", "optimizing": "optimising",
            "organization": "organisation", "organizational": "organisational", "organizations": "organisations",
            "organize": "organise", "organized": "organised", "organizer": "organiser", "organizers": "organisers",
            "organizes": "organises", "organizing": "organising", "orthopedic": "orthopaedic",
            "orthopedics": "orthopaedics", "ostracize": "ostracise", "ostracized": "ostracised",
            "ostracizes": "ostracises", "ostracizing": "ostracising", "outmaneuver": "outmanoeuvre",
            "outmaneuvered": "outmanoeuvred", "outmaneuvers": "outmanoeuvres", "outmaneuvering": "outmanoeuvring",
            "overemphasize": "overemphasise", "overemphasized": "overemphasised", "overemphasizes": "overemphasises",
            "overemphasizing": "overemphasising", "oxidization": "oxidisation", "oxidize": "oxidise",
            "oxidized": "oxidised", "oxidizes": "oxidises", "oxidizing": "oxidising", "pederast": "paederast",
            "pederasts": "paederasts", "pediatric": "paediatric", "pediatrician": "paediatrician",
            "pediatricians": "paediatricians", "pediatrics": "paediatrics", "pedophile": "paedophile",
            "pedophiles": "paedophiles", "pedophilia": "paedophilia", "paleolithic": "palaeolithic",
            "paleontologist": "palaeontologist", "paleontologists": "palaeontologists", "paleontology": "palaeontology",
            "paneled": "panelled", "paneling": "panelling", "panelist": "panellist", "panelists": "panellists",
            "paralyze": "paralyse", "paralyzed": "paralysed", "paralyzes": "paralyses", "paralyzing": "paralysing",
            "parceled": "parcelled", "parceling": "parcelling", "parlor": "parlour", "parlors": "parlours",
            "particularize": "particularise", "particularized": "particularised", "particularizes": "particularises",
            "particularizing": "particularising", "passivization": "passivisation", "passivize": "passivise",
            "passivized": "passivised", "passivizes": "passivises", "passivizing": "passivising",
            "pasteurization": "pasteurisation", "pasteurize": "pasteurise", "pasteurized": "pasteurised",
            "pasteurizes": "pasteurises", "pasteurizing": "pasteurising", "patronize": "patronise",
            "patronized": "patronised", "patronizes": "patronises", "patronizing": "patronising",
            "patronizingly": "patronisingly", "pedaled": "pedalled", "pedaling": "pedalling",
            "pedestrianization": "pedestrianisation", "pedestrianize": "pedestrianise",
            "pedestrianized": "pedestrianised", "pedestrianizes": "pedestrianises",
            "pedestrianizing": "pedestrianising", "penalize": "penalise", "penalized": "penalised",
            "penalizes": "penalises", "penalizing": "penalising", "penciled": "pencilled", "penciling": "pencilling",
            "personalize": "personalise", "personalized": "personalised", "personalizes": "personalises",
            "personalizing": "personalising", "pharmacopeia": "pharmacopoeia", "pharmacopeias": "pharmacopoeias",
            "philosophize": "philosophise", "philosophized": "philosophised", "philosophizes": "philosophises",
            "philosophizing": "philosophising", "filter": "philtre", "filters": "philtres", "phony": "phoney",
            "plagiarize": "plagiarise", "plagiarized": "plagiarised", "plagiarizes": "plagiarises",
            "plagiarizing": "plagiarising", "plow": "plough", "plowed": "ploughed", "plowing": "ploughing",
            "plowman": "ploughman", "plowmen": "ploughmen", "plows": "ploughs", "plowshare": "ploughshare",
            "plowshares": "ploughshares", "polarization": "polarisation", "polarize": "polarise",
            "polarized": "polarised", "polarizes": "polarises", "polarizing": "polarising",
            "politicization": "politicisation", "politicize": "politicise", "politicized": "politicised",
            "politicizes": "politicises", "politicizing": "politicising", "popularization": "popularisation",
            "popularize": "popularise", "popularized": "popularised", "popularizes": "popularises",
            "popularizing": "popularising", "pouf": "pouffe", "poufs": "pouffes", "practice": "practise",
            "practiced": "practised", "practices": "practises", "practicing": "practising", "presidium": "praesidium",
            "presidiums": "praesidiums", "pressurization": "pressurisation", "pressurize": "pressurise",
            "pressurized": "pressurised", "pressurizes": "pressurises", "pressurizing": "pressurising",
            "pretense": "pretence", "pretenses": "pretences", "primeval": "primaeval",
            "prioritization": "prioritisation", "prioritize": "prioritise", "prioritized": "prioritised",
            "prioritizes": "prioritises", "prioritizing": "prioritising", "privatization": "privatisation",
            "privatizations": "privatisations", "privatize": "privatise", "privatized": "privatised",
            "privatizes": "privatises", "privatizing": "privatising", "professionalization": "professionalisation",
            "professionalize": "professionalise", "professionalized": "professionalised",
            "professionalizes": "professionalises", "professionalizing": "professionalising", "program": "programme",
            "programs": "programmes", "prolog": "prologue", "prologs": "prologues", "propagandize": "propagandise",
            "propagandized": "propagandised", "propagandizes": "propagandises", "propagandizing": "propagandising",
            "proselytize": "proselytise", "proselytized": "proselytised", "proselytizer": "proselytiser",
            "proselytizers": "proselytisers", "proselytizes": "proselytises", "proselytizing": "proselytising",
            "psychoanalyze": "psychoanalyse", "psychoanalyzed": "psychoanalysed", "psychoanalyzes": "psychoanalyses",
            "psychoanalyzing": "psychoanalysing", "publicize": "publicise", "publicized": "publicised",
            "publicizes": "publicises", "publicizing": "publicising", "pulverization": "pulverisation",
            "pulverize": "pulverise", "pulverized": "pulverised", "pulverizes": "pulverises",
            "pulverizing": "pulverising", "pummel": "pummelled", "pummeled": "pummelling", "pajama": "pyjama",
            "pajamas": "pyjamas", "pizzazz": "pzazz", "quarreled": "quarrelled", "quarreling": "quarrelling",
            "radicalize": "radicalise", "radicalized": "radicalised", "radicalizes": "radicalises",
            "radicalizing": "radicalising", "rancor": "rancour", "randomize": "randomise", "randomized": "randomised",
            "randomizes": "randomises", "randomizing": "randomising", "rationalization": "rationalisation",
            "rationalizations": "rationalisations", "rationalize": "rationalise", "rationalized": "rationalised",
            "rationalizes": "rationalises", "rationalizing": "rationalising", "raveled": "ravelled",
            "raveling": "ravelling", "realizable": "realisable", "realization": "realisation",
            "realizations": "realisations", "realize": "realise", "realized": "realised", "realizes": "realises",
            "realizing": "realising", "recognizable": "recognisable", "recognizably": "recognisably",
            "recognizance": "recognisance", "recognize": "recognise", "recognized": "recognised",
            "recognizes": "recognises", "recognizing": "recognising", "reconnoiter": "reconnoitre",
            "reconnoitered": "reconnoitred", "reconnoiters": "reconnoitres", "reconnoitering": "reconnoitring",
            "refueled": "refuelled", "refueling": "refuelling", "regularization": "regularisation",
            "regularize": "regularise", "regularized": "regularised", "regularizes": "regularises",
            "regularizing": "regularising", "remodeled": "remodelled", "remodeling": "remodelling", "remold": "remould",
            "remolded": "remoulded", "remolding": "remoulding", "remolds": "remoulds",
            "reorganization": "reorganisation", "reorganizations": "reorganisations", "reorganize": "reorganise",
            "reorganized": "reorganised", "reorganizes": "reorganises", "reorganizing": "reorganising",
            "reveled": "revelled", "reveler": "reveller", "revelers": "revellers", "reveling": "revelling",
            "revitalize": "revitalise", "revitalized": "revitalised", "revitalizes": "revitalises",
            "revitalizing": "revitalising", "revolutionize": "revolutionise", "revolutionized": "revolutionised",
            "revolutionizes": "revolutionises", "revolutionizing": "revolutionising", "rhapsodize": "rhapsodise",
            "rhapsodized": "rhapsodised", "rhapsodizes": "rhapsodises", "rhapsodizing": "rhapsodising",
            "rigor": "rigour", "rigors": "rigours", "ritualized": "ritualised", "rivaled": "rivalled",
            "rivaling": "rivalling", "romanticize": "romanticise", "romanticized": "romanticised",
            "romanticizes": "romanticises", "romanticizing": "romanticising", "rumor": "rumour", "rumored": "rumoured",
            "rumors": "rumours", "saber": "sabre", "sabers": "sabres", "saltpeter": "saltpetre", "sanitize": "sanitise",
            "sanitized": "sanitised", "sanitizes": "sanitises", "sanitizing": "sanitising", "satirize": "satirise",
            "satirized": "satirised", "satirizes": "satirises", "satirizing": "satirising", "savior": "saviour",
            "saviors": "saviours", "savor": "savour", "savored": "savoured", "savories": "savouries",
            "savoring": "savouring", "savors": "savours", "savory": "savoury", "scandalize": "scandalise",
            "scandalized": "scandalised", "scandalizes": "scandalises", "scandalizing": "scandalising",
            "skeptic": "sceptic", "skeptical": "sceptical", "skeptically": "sceptically", "skepticism": "scepticism",
            "skeptics": "sceptics", "scepter": "sceptre", "scepters": "sceptres", "scrutinize": "scrutinise",
            "scrutinized": "scrutinised", "scrutinizes": "scrutinises", "scrutinizing": "scrutinising",
            "secularization": "secularisation", "secularize": "secularise", "secularized": "secularised",
            "secularizes": "secularises", "secularizing": "secularising", "sensationalize": "sensationalise",
            "sensationalized": "sensationalised", "sensationalizes": "sensationalises",
            "sensationalizing": "sensationalising", "sensitize": "sensitise", "sensitized": "sensitised",
            "sensitizes": "sensitises", "sensitizing": "sensitising", "sentimentalize": "sentimentalise",
            "sentimentalized": "sentimentalised", "sentimentalizes": "sentimentalises",
            "sentimentalizing": "sentimentalising", "sepulcher": "sepulchre", "sepulchers": "sepulchres",
            "serialization": "serialisation", "serializations": "serialisations", "serialize": "serialise",
            "serialized": "serialised", "serializes": "serialises", "serializing": "serialising",
            "sermonize": "sermonise", "sermonized": "sermonised", "sermonizes": "sermonises",
            "sermonizing": "sermonising", "sheik": "sheikh", "shoveled": "shovelled", "shoveling": "shovelling",
            "shriveled": "shrivelled", "shriveling": "shrivelling", "signalize": "signalise",
            "signalized": "signalised", "signalizes": "signalises", "signalizing": "signalising",
            "signaled": "signalled", "signaling": "signalling", "smolder": "smoulder", "smoldered": "smouldered",
            "smoldering": "smouldering", "smolders": "smoulders", "sniveled": "snivelled", "sniveling": "snivelling",
            "snorkeled": "snorkelled", "snorkeling": "snorkelling", "snowplow": "snowploughs",
            "socialization": "socialisation", "socialize": "socialise", "socialized": "socialised",
            "socializes": "socialises", "socializing": "socialising", "sodomize": "sodomise", "sodomized": "sodomised",
            "sodomizes": "sodomises", "sodomizing": "sodomising", "solemnize": "solemnise", "solemnized": "solemnised",
            "solemnizes": "solemnises", "solemnizing": "solemnising", "somber": "sombre",
            "specialization": "specialisation", "specializations": "specialisations", "specialize": "specialise",
            "specialized": "specialised", "specializes": "specialises", "specializing": "specialising",
            "specter": "spectre", "specters": "spectres", "spiraled": "spiralled", "spiraling": "spiralling",
            "splendor": "splendour", "splendors": "splendours", "squirreled": "squirrelled",
            "squirreling": "squirrelling", "stabilization": "stabilisation", "stabilize": "stabilise",
            "stabilized": "stabilised", "stabilizer": "stabiliser", "stabilizers": "stabilisers",
            "stabilizes": "stabilises", "stabilizing": "stabilising", "standardization": "standardisation",
            "standardize": "standardise", "standardized": "standardised", "standardizes": "standardises",
            "standardizing": "standardising", "stenciled": "stencilled", "stenciling": "stencilling",
            "sterilization": "sterilisation", "sterilizations": "sterilisations", "sterilize": "sterilise",
            "sterilized": "sterilised", "sterilizer": "steriliser", "sterilizers": "sterilisers",
            "sterilizes": "sterilises", "sterilizing": "sterilising", "stigmatization": "stigmatisation",
            "stigmatize": "stigmatise", "stigmatized": "stigmatised", "stigmatizes": "stigmatises",
            "stigmatizing": "stigmatising", "subsidization": "subsidisation", "subsidize": "subsidise",
            "subsidized": "subsidised", "subsidizer": "subsidiser", "subsidizers": "subsidisers",
            "subsidizes": "subsidises", "subsidizing": "subsidising", "succor": "succour", "succored": "succoured",
            "succoring": "succouring", "succors": "succours", "sulfate": "sulphate", "sulfates": "sulphates",
            "sulfide": "sulphide", "sulfides": "sulphides", "sulfur": "sulphur", "sulfurous": "sulphurous",
            "summarize": "summarise", "summarized": "summarised", "summarizes": "summarises",
            "summarizing": "summarising", "swiveled": "swivelled", "swiveling": "swivelling", "symbolize": "symbolise",
            "symbolized": "symbolised", "symbolizes": "symbolises", "symbolizing": "symbolising",
            "sympathize": "sympathise", "sympathized": "sympathised", "sympathizer": "sympathiser",
            "sympathizers": "sympathisers", "sympathizes": "sympathises", "sympathizing": "sympathising",
            "synchronization": "synchronisation", "synchronize": "synchronise", "synchronized": "synchronised",
            "synchronizes": "synchronises", "synchronizing": "synchronising", "synthesize": "synthesise",
            "synthesized": "synthesised", "synthesizer": "synthesiser", "synthesizers": "synthesisers",
            "synthesizes": "synthesises", "synthesizing": "synthesising", "siphon": "syphon", "siphoned": "syphoned",
            "siphoning": "syphoning", "siphons": "syphons", "systematization": "systematisation",
            "systematize": "systematise", "systematized": "systematised", "systematizes": "systematises",
            "systematizing": "systematising", "tantalize": "tantalise", "tantalized": "tantalised",
            "tantalizes": "tantalises", "tantalizing": "tantalising", "tantalizingly": "tantalisingly",
            "tasseled": "tasselled", "technicolor": "technicolour", "temporize": "temporise",
            "temporized": "temporised", "temporizes": "temporises", "temporizing": "temporising",
            "tenderize": "tenderise", "tenderized": "tenderised", "tenderizes": "tenderises",
            "tenderizing": "tenderising", "terrorize": "terrorise", "terrorized": "terrorised",
            "terrorizes": "terrorises", "terrorizing": "terrorising", "theater": "theatre",
            "theatergoer": "theatregoer", "theatergoers": "theatregoers", "theaters": "theatres",
            "theorize": "theorise", "theorized": "theorised", "theorizes": "theorises", "theorizing": "theorising",
            "ton": "tonne", "tons": "tonnes", "toweled": "towelled", "toweling": "towelling", "toxemia": "toxaemia",
            "tranquilize": "tranquillize", "tranquilized": "tranquillized", "tranquilizer": "tranquillizer",
            "tranquilizers": "tranquillizers", "tranquilizes": "tranquillizes", "tranquilizing": "tranquillizing",
            "tranquility": "tranquilly", "transistorized": "transistorised", "traumatize": "traumatise",
            "traumatized": "traumatised", "traumatizes": "traumatises", "traumatizing": "traumatising",
            "traveled": "travelled", "traveler": "traveller", "travelers": "travellers", "traveling": "travelling",
            "travelog": "travelogue", "travelogs": "travelogues", "trialed": "trialled", "trialing": "trialling",
            "tricolor": "tricolour", "tricolors": "tricolours", "trivialize": "trivialise",
            "trivialized": "trivialised", "trivializes": "trivialises", "trivializing": "trivialising",
            "tumor": "tumour", "tumors": "tumours", "tunneled": "tunnelled", "tunneling": "tunnelling",
            "tyrannize": "tyrannise", "tyrannized": "tyrannised", "tyrannizes": "tyrannises",
            "tyrannizing": "tyrannising", "tire": "tyre", "tires": "tyres", "unauthorized": "unauthorised",
            "uncivilized": "uncivilised", "underutilized": "underutilised", "unequaled": "unequalled",
            "unfavorable": "unfavourable", "unfavorably": "unfavourably", "unionization": "unionisation",
            "unionize": "unionise", "unionized": "unionised", "unionizes": "unionises", "unionizing": "unionising",
            "unorganized": "unorganised", "unraveled": "unravelled", "unraveling": "unravelling",
            "unrecognizable": "unrecognisable", "unrecognized": "unrecognised", "unrivaled": "unrivalled",
            "unsavory": "unsavoury", "untrammeled": "untrammelled", "urbanization": "urbanisation",
            "urbanize": "urbanise", "urbanized": "urbanised", "urbanizes": "urbanises", "urbanizing": "urbanising",
            "utilizable": "utilisable", "utilization": "utilisation", "utilize": "utilise", "utilized": "utilised",
            "utilizes": "utilises", "utilizing": "utilising", "valor": "valour", "vandalize": "vandalise",
            "vandalized": "vandalised", "vandalizes": "vandalises", "vandalizing": "vandalising",
            "vaporization": "vaporisation", "vaporize": "vaporise", "vaporized": "vaporised", "vaporizes": "vaporises",
            "vaporizing": "vaporising", "vapor": "vapour", "vapors": "vapours", "verbalize": "verbalise",
            "verbalized": "verbalised", "verbalizes": "verbalises", "verbalizing": "verbalising",
            "victimization": "victimisation", "victimize": "victimise", "victimized": "victimised",
            "victimizes": "victimises", "victimizing": "victimising", "videodisk": "videodisc",
            "videodisks": "videodiscs", "vigor": "vigour", "visualization": "visualisation",
            "visualizations": "visualisations", "visualize": "visualise", "visualized": "visualised",
            "visualizes": "visualises", "visualizing": "visualising", "vocalization": "vocalisation",
            "vocalizations": "vocalisations", "vocalize": "vocalise", "vocalized": "vocalised",
            "vocalizes": "vocalises", "vocalizing": "vocalising", "vulcanized": "vulcanised",
            "vulgarization": "vulgarisation", "vulgarize": "vulgarise", "vulgarized": "vulgarised",
            "vulgarizes": "vulgarises", "vulgarizing": "vulgarising", "watercolor": "watercolour",
            "watercolors": "watercolours", "weaseled": "weaselled", "weaseling": "weaselling",
            "westernization": "westernisation", "westernize": "westernise", "westernized": "westernised",
            "westernizes": "westernises", "westernizing": "westernising", "womanize": "womanise",
            "womanized": "womanised", "womanizer": "womaniser", "womanizers": "womanisers", "womanizes": "womanises",
            "womanizing": "womanising", "woolen": "woollen", "woolens": "woollens", "woolies": "woollies",
            "wooly": "woolly", "worshiped": "worshipped", "worshiping": "worshipping", "worshiper": "worshipper",
            "yodeled": "yodelled", "yodeling": "yodelling", "yogurt": "yoghurt", "yogurts": "yoghurts"}
# @formatter:on

TYPO_FREQUENCY = {
    "a": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 594, 1, 42401, 1, 1, 1, 10893, 3882, 1, 3062],
    "b": [1, 1, 1, 1, 1, 16112, 21182, 10826, 1, 1, 1, 1, 1, 19375, 1, 1, 1, 1, 1, 1, 1, 6146, 1, 1, 1, 1],
    "c": [1, 1, 1, 19151, 1, 15124, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 37974, 1, 1, 7444, 1, 1, 1, 1],
    "d": [1, 1, 1, 1, 39499, 16091, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 64063, 80813, 1, 1, 7848, 10614, 2018, 1, 1],
    "e": [1, 1, 1, 1, 1, 17080, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 76503, 75665, 1, 1, 1, 13193, 1, 1, 1],
    "f": [1, 1, 1, 1, 1, 1, 13344, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 18722, 1, 20980, 1, 5822, 1, 1, 1, 1],
    "g": [1, 1, 1, 1, 1, 1, 1, 10144, 1, 1, 1, 1, 1, 23414, 1, 1, 1, 22092, 1, 30296, 1, 5093, 1, 1, 5295, 1],
    "h": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2663, 1, 1, 11486, 11859, 1, 1, 1, 1, 1, 23856, 10462, 1, 1, 1, 1, 1],
    "i": [1, 1, 1, 1, 1, 1, 1, 1, 1, 699, 9983, 40985, 1, 1, 82987, 1, 1, 1, 1, 1, 63669, 1, 1, 1, 1, 1],
    "j": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1248, 1, 3464, 2011, 1, 1, 1, 1, 1, 1, 568, 1, 1, 1, 1, 1],
    "k": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14651, 8496, 1, 8366, 1, 1, 1, 1, 1, 5455, 1, 1, 1, 1, 1],
    "l": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 43713, 30126, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "m": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 23433, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "n": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "o": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 18072, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "p": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "q": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2041, 1, 1, 1, 728, 1, 1, 1],
    "r": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 54571, 1, 1, 1, 1, 1, 1],
    "s": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 17079, 3613, 1, 7300],
    "t": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13286, 1],
    "u": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6783, 1],
    "v": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "w": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "x": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 516],
    "y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "z": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}

CONTRACTION_MAP = {'is not': "isn't", 'are not': "aren't", 'cannot': "can't", 'could not': "couldn't", 'did not':
    "didn't", 'does not': "doesn't", 'do not': "don't", 'had not': "hadn't", 'has not': "hasn't", 'have not': "haven't",
                   'he is': "he's", 'how did': "how'd", 'how is': "how's", 'I would': "I'd", 'I will': "I'll",
                   'I am': "I'm", 'i would': "i'd", 'i will': "i'll", 'i am': "i'm", 'it would': "it'd",
                   'it will': "it'll", 'it is': "it's", 'might not': "mightn't", 'must not': "mustn't",
                   'need not': "needn't", 'ought not': "oughtn't", 'shall not': "shan't", 'she would': "she'd",
                   'she will': "she'll", 'she is': "she's", 'should not': "shouldn't", 'that would': "that'd",
                   'that is': "that's", 'there would': "there'd", 'there is': "there's", 'they would': "they'd",
                   'they will': "they'll", 'they are': "they're", 'was not': "wasn't", 'we would': "we'd",
                   'we will': "we'll", 'we are': "we're", 'were not': "weren't", 'what are': "what're",
                   'what is': "what's", 'when is': "when's", 'where did': "where'd", 'where is': "where's",
                   'who will': "who'll", 'who is': "who's", 'who have': "who've", 'why is': "why's",
                   'will not': "won't", 'would not': "wouldn't", 'you would': "you'd", 'you will': "you'll",
                   'you are': "you're"}

# Curated from the United States Census Bureau surveys
white_names = {
    "first_names": ["Sage", "Jeremy", "Alisa", "Shaya", "Barbara", "Savannah", "Sonny", "Kate", "Jenna", "Yossi",
                    "Lauren", "Alexia", "Eva", "Chiara", "Kaitlyn", "Lilia", "Leah", "Lucille", "Siena", "Henchy",
                    "Tyler", "Hope", "Clementine", "Paige", "Finley", "Jason", "Michael", "Taylor", "Mohamed",
                    "Milania", "Elise", "Lucy", "Sylvie", "Shlome", "Blake", "Stephen", "Brady", "Maxwell", "Ayelet",
                    "Yocheved", "Noam", "Jana", "Elimelech", "Emmy", "Morris", "Younis", "Moishe", "Freya", "Batsheva",
                    "Nico", "Zain", "Amelie", "Mohammed", "Ava", "Harper", "Reizy", "Lielle", "Malak", "Shevy",
                    "Liliana", "Lily", "Leona", "Ephraim", "Freida", "Valerie", "Alina", "Kevin", "Perl", "Rhett",
                    "Jace", "Jaxson", "Amara", "Fishel", "Goldie", "Kyle", "Avery", "Viviana", "Sabrina", "Xavier",
                    "Ariela", "Vincenzo", "Marc", "David", "Sidney", "Issac", "Hayden", "Yitta", "Yeshaya", "Yaakov",
                    "Evelyn", "Hayes", "Dashiell", "Katerina", "Hazel", "Sabina", "Myles", "Bryan", "Karas", "Annabel",
                    "Alan", "Bina", "Amina", "Lorenzo", "Alexis", "Finn", "Frady", "Adalyn", "Hanna", "James", "Imran",
                    "Jasmine", "Arabella", "Nolan", "Shloma", "Yonatan", "Perel", "Alter", "Marco", "Rafael", "Frieda",
                    "Guy", "Samantha", "Cleo", "Griffin", "Nathan", "Chavy", "Eliza", "Reed", "Louise", "Peretz",
                    "Isla", "Hadassa", "Meyer", "Chelsea", "Chesky", "Olive", "Blimy", "Aya", "Anthony", "Ezra",
                    "Shraga", "Timothy", "Dovid", "Iymona", "Abdullah", "Seth", "Gianna", "Kamila", "Lyla", "Calvin",
                    "Michaela", "Cora", "Liora", "Max", "Phoenix", "Devora", "Paisley", "Sarah", "Ameer", "Daria",
                    "Ashley", "Evan", "Roizy", "Rocco", "Blair", "Erik", "Aria", "Claire", "Kian", "Emmeline",
                    "Shukrona", "Daniela", "Bryce", "Esther", "Celia", "Nova", "Elsa", "Trany", "Hadley", "Brynlee",
                    "Eric", "Walker", "Laith", "Xander", "Tucker", "Bentzion", "Celeste", "Antonia", "Rhys", "Yahya",
                    "Parizoda", "Kyler", "Vivienne", "Vincent", "Raya", "Lucas", "Arya", "Hailey", "Nechama", "Theo",
                    "Joel", "Phoebe", "Yael", "Lukas", "Saoirse", "Valentina", "Tristan", "Otto", "Brian", "Andrew",
                    "Lilian", "Mika", "Dominic", "Ezriel", "Chaya", "Devin", "Toby", "Willow", "Meilech", "William",
                    "Weston", "Aliza", "Maryam", "Jaxon", "Yassin", "Ansel", "Theodora", "Richard", "Nash", "Owen",
                    "Noa", "Dalia", "Gavin", "Elliot", "Chany", "Esty", "Amalia", "Hamza", "Blima", "Antonio", "Hassan",
                    "Ada", "Luciana", "Eloise", "Helen", "Maximilian", "Juliette", "Samira", "Giovanna", "Daphne",
                    "Diana", "Gwendolyn", "Skylar", "Elya", "Marlowe", "Arielle", "Dominick", "Arthur", "Ella",
                    "Abdulloh", "Charlie", "Elliana", "Avraham", "Harlow", "Isaac", "Mabel", "Georgia", "Faigy", "Sima",
                    "Amira", "Mendy", "Kenneth", "Yechezkel", "Reuven", "Shneur", "Maya", "Luke", "Eleanor", "Tzivia",
                    "Madison", "Quinn", "Henry", "Maggie", "Luka", "Augustus", "Ayala", "Imogen", "Gabriel", "Lilly",
                    "Millie", "Shloimy", "Waylon", "Maeve", "Meir", "Menashe", "Ryder", "Zayn", "Nikita", "Gregory",
                    "Shimon", "Emersyn", "Noelle", "Damian", "Khloe", "Devorah", "Leon", "Aleksander", "Frederick",
                    "Laura", "Joanna", "Magnolia", "Adina", "Florence", "Bodhi", "Ilan", "Billie", "Carly", "Yachet",
                    "Cheskel", "Zoey", "Giulia", "Sonia", "Sam", "Mackenzie", "John", "Aryeh", "Alessia", "Micah",
                    "Sammy", "Emanuel", "Zalmen", "Yisrael", "Bridget", "Giuseppe", "Nathaniel", "Emmanuel", "Delilah",
                    "Ilana", "Kira", "Laila", "Alec", "Kaya", "Avi", "Adrian", "Tzirel", "Sawyer", "Gabriela", "Orly",
                    "Mirel", "Cassandra", "Keira", "Carter", "Camila", "Scarlett", "Gianluca", "Raizel", "Olivia",
                    "Kennedy", "Aurora", "Frank", "Vienna", "Mechel", "Rivka", "Chava", "Bianca", "Casey", "Braxton",
                    "Sara", "Oren", "Elaina", "Justin", "Felix", "Omar", "Jane", "Ariel", "Mateo", "Kacper", "Yitzchok",
                    "Layan", "Rowan", "Desmond", "Olympia", "Ruth", "Louisa", "Nicholas", "Robert", "Saul", "Serafina",
                    "Christian", "Ronan", "Adrianna", "Tova", "Yasmina", "Vanessa", "Gracie", "Lev", "Paul", "Ethan",
                    "Nadia", "Eliot", "Tess", "Adeline", "Binyamin", "Sari", "Madelyn", "Angelica", "Stephanie",
                    "Emilia", "Samuel", "Ben", "Gabriella", "Diyora", "Shmiel", "Elisa", "Rina", "Lillian", "Ari",
                    "Raizy", "Angelo", "Reid", "Madina", "Aviva", "Georgina", "Brandon", "Beckham", "Morgan", "Marie",
                    "Mushka", "Alana", "Grey", "Ariella", "Basya", "Youssef", "Maxim", "Burech", "Levi",
                    "Cecilia", "Mila", "Mira", "Camden", "Mendel", "Nina", "Emery", "Mason", "Eden", "Eleni", "Winston",
                    "Breindy", "Tallulah", "Miriam", "Naftuli", "Liana", "Matteo", "Pinchas", "Elodie", "Alyssa",
                    "Eluzer", "Elisheva", "Livia", "Ahmed", "Joaquin", "Baruch", "Lydia", "Sadie", "Steven", "Yisroel",
                    "Sophia", "Celine", "Amrom", "Judah", "Selim", "Ellis", "Kai", "Naftali", "Christopher", "Sama",
                    "Arden", "Julie", "Peter", "Faiga", "Ahmad", "Clark", "Joshua", "Simi", "Jordyn", "Reuben", "Luca",
                    "Jude", "Jakob", "Spencer", "Lina", "Harry", "Moses", "Shaindel", "Tehila", "Miri", "Edward",
                    "Nicolas", "Francesca", "Amir", "Abubakr", "Libby", "Anton", "Salvatore", "Stanley", "Jacob",
                    "Hindy", "Baila", "Mark", "Simcha", "Isabella", "Marina", "Ibrohim", "Thomas", "Ahuva", "Joyce",
                    "Anas", "Ahron", "Yaseen", "Connor", "Melina", "Fiona", "Zane", "Sloane", "Aliya", "Selma", "Arlo",
                    "Greta", "Stella", "Jameson", "Knox", "Megan", "Tamara", "Wilder", "Mary", "Genevieve", "Theodore",
                    "Timur", "Lara", "Elijah", "Yida", "Elias", "Viktor", "Yara", "Colin", "Toba", "Dillon",
                    "Alexander", "Brantley", "Elliott", "Riva", "Ryleigh", "Elena", "Hershel", "Leyla", "Margaret",
                    "Simon", "Leonidas", "Tamar", "Hersh", "Harley", "Chloe", "Zachary", "Yitty", "Abraham", "Jasper",
                    "Easton", "Josephine", "Esme", "Vera", "Carolina", "Barrett", "Moshe", "Eliana", "Nava", "Raphael",
                    "Shulem", "Ashton", "Hunter", "Beau", "Adam", "Malka", "Ori", "Rochel", "Axel", "Umar", "Melissa",
                    "Catherine", "Sophie", "Shayna", "Natalia", "Erin", "Graham", "Harvey", "Lilliana", "Helena",
                    "Giada", "Shea", "Ester", "Nora", "Anya", "Enzo", "Yanky", "Atlas", "Goldy", "Liba", "Aleksandra",
                    "Bruchy", "Jesse", "Louis", "Mollie", "Suri", "Linda", "Zakaria", "Jonah", "Sienna", "Angelina",
                    "River", "Cooper", "Sholom", "Layla", "Devory", "Henny", "Rena", "Derek", "Isabel", "Duvid", "Elle",
                    "Fradel", "Wolf", "Juliana", "Juliet", "Bailey", "Alexa", "Shoshana", "Simone", "Josef", "Santino",
                    "Hillel", "Carmine", "Mohammad", "Meshilem", "Herman", "Reagan", "Alicia", "Clara", "Rebecca",
                    "Abe", "Gaia", "Daniella", "Nicole", "Dua", "Raymond", "Jessica", "Charlotte", "Shaul", "Julian",
                    "Yehoshua", "Julius", "Margaux", "Muhammad", "Anisa", "Polina", "Brooklyn", "Dante", "Jakub",
                    "Giuliana", "Addison", "Shifra", "Alexandra", "Naomi", "Salma", "Katie", "Shia", "Sury", "Russell",
                    "Brooke", "Lucia", "Etty", "Aaron", "Muslima", "Julianna", "Silas", "Avrum", "Summer", "Eitan",
                    "Oscar", "Shaindy", "Yasmin", "Matilda", "Ayla", "Yitzchak", "Lila", "Preston", "Estelle", "Isaiah",
                    "Brody", "Donovan", "Mindy", "Briella", "Lazer", "Jackson", "Shalom", "Norah", "Atara", "Lucien",
                    "Colton", "Maisie", "Anderson", "Reem", "Juniper", "Michal", "Akiva", "Chana", "Kiera", "Tobias",
                    "Cecelia", "Yehudah", "Aubrey", "Yides", "Idy", "Zissy", "Dina", "Yona", "Shmuel", "Giancarlo",
                    "Leibish", "Talia", "Neil", "Nuchem", "Katelyn", "Matthew", "Daisy", "Jamie", "Nachman",
                    "Kinsley", "Yidel", "Albert", "Fraidy", "Farida", "Emmett", "Dylan", "Eyad", "Rose", "Liam", "Dana",
                    "Austin", "Filip", "Harrison", "Ayden", "Menucha", "Madeline", "Anastasia", "Angela", "Mordechai",
                    "Lana", "Gavriel", "Grayson", "Evangeline", "Iris", "Isabelle", "Brayden", "Greyson", "Batya",
                    "Scott", "Rosalie", "Anna", "Alma", "Remy", "Milo", "Aiden", "Nikolas", "Frances", "Elizabeth",
                    "Chanie", "Tziporah", "Adriana", "Reese", "Pierce", "Remington", "Mina", "Jad", "Yehudis",
                    "Brianna", "Everly", "Allison", "Winnie", "George", "Giovanni", "Emma", "Berish", "Zoe", "Yechiel",
                    "Zev", "Julia", "Adelina", "Wyatt", "Colette", "Nicolette", "Chaim", "Lipa", "Eliyahu",
                    "Alessandra", "Milan", "Bradley", "Veronica", "Caroline", "Yoel", "Avigail", "Lucian", "Adele",
                    "Muhammad ali", "Audrey", "Mikaela", "Ellie", "Natalie", "Adelaide", "Avrohom", "Hinda", "Callie",
                    "Maia", "Dahlia", "Vivian", "Hershy", "Mayar", "Gemma", "Ines", "Orion", "Caitlin", "Beatrix",
                    "Faith", "Kareem", "Declan", "Margot", "Cassidy", "Aurelia", "Melanie", "Leila", "Hana",
                    "Francesco", "Allen", "Shaina", "Ruchel", "Josie", "Lia", "Emerson", "Yousef", "Danielle",
                    "Massimo", "Rayan", "Nosson", "Kristina", "Cameron", "Camilla", "Ali", "Logan", "Riley",
                    "Alexandria", "Brielle", "Veronika", "Usher", "Penelope", "Marielle", "Sebastian", "Ivan", "Daniel",
                    "Ian", "Violet", "Nikolai", "Tzipora", "Luna", "Aziza", "Efraim", "Victor", "Arye", "Cody",
                    "Jacqueline", "Eli", "Kaia", "Piper", "Beatrice", "Alice", "Frida", "Claudia", "Ruchy", "Francis",
                    "Michelle", "Rory", "Poppy", "Ryan", "Katherine", "Molly", "Marcus", "Noor", "Otis", "Avital",
                    "Samir", "Parker", "Rachel", "Teagan", "Dawson", "Eliezer", "Leonard", "Beckett", "Rifka", "Jade",
                    "Noach", "Blakely", "Alessandro", "Kathryn", "Brynn", "Rosa", "Aidan", "Anne", "Amanda",
                    "Devoiry", "Caleb", "Philip", "Jayden", "Lola", "Amirjon", "Drew", "Gittel", "Dean", "Amy", "Roman",
                    "Shane", "Hendy", "Archer", "Sylvia", "Rifky", "Mia", "Finnegan", "Solomon", "Binyomin", "Edith",
                    "Shloime", "Asher", "Hannah", "Atticus", "Tomas", "Everett", "Abigail", "Presley", "Arianna",
                    "Sofia", "Rivky", "Mikayla", "Serena", "Crosby", "Gideon", "Martin", "Idris", "Lincoln", "Denis",
                    "Camille", "Gia", "Chris", "Bella", "Tzvi", "Cyrus", "Madeleine", "Shlomo", "Jennifer", "Emir",
                    "Jax", "Malky", "Maksim", "Sydney", "Stefan", "Maximus", "Giselle", "Sami", "Yosef", "Zainab",
                    "Roiza", "Annabelle", "Romy", "Elan", "Ralph", "Milana", "Virginia", "Pearl", "Mayer", "Aviel",
                    "Ruby", "Pessy", "Renee", "Mordche", "Jonathan", "Hugo", "Yonah", "Menachem", "Jolie", "Rivkah",
                    "Sean", "Aron", "Jordan", "Kylie", "Leia", "Yusuf", "Kayla", "Oliver", "Jasmina",
                    "Gabrielle", "Bennett", "Walter", "Imona", "Holden", "Willa", "Boruch", "Everleigh", "Hadassah",
                    "Frimet", "Ariana", "Ryker", "Astrid", "Judy", "Emily", "Cole", "Wesley", "Malika", "Brooks",
                    "Brendan", "Grace", "Ember", "Victoria", "Aisha", "Dion", "Alex", "Remi", "Joseph", "Lilah", "Lea",
                    "Josiah", "Rahaf", "Julien", "Sasha", "Motty", "Yakov", "Benjamin", "Mariam", "Marcel", "Eve",
                    "Pinchus", "Gitty", "Leo", "Benzion", "Evie", "Farah", "Hudson", "Rosie", "Meira", "Grant", "Noah",
                    "Landon", "Zelda", "Golda", "Malek", "Leonardo", "Autumn", "Maria", "Peyton", "Evelina", "Aspen",
                    "Colt", "Izabella", "Shira", "Perry", "Caden", "Makayla", "Brucha", "Ivy", "Patrick", "Liv",
                    "Kieran", "Thea", "Zara", "Dennis", "Tzippy", "Cormac", "Charles", "Elina", "Mae", "Yehuda",
                    "Conor", "Ibrahim", "Kaylee", "Amelia", "Christina", "Bracha", "Athena", "Berl", "Maverick",
                    "Leora", "Jack", "Milena", "Aharon", "Ana", "Kobe", "Moishy", "Jake", "Raelynn", "Jay", "Oskar",
                    "Melania", "Tessa", "Aydin", "Paloma", "Fatima", "Lena", "Chase", "Malcolm", "Dov", "Bentley",
                    "Raquel", "Malik", "Yasmine"],
    "last_names": ["Holcomb", "Gallant", "Mayes", "Franklin", "Westphal", "Goff", "Fitzpatrick", "Mcvey", "Churchill",
                   "Matteson", "Worrell", "Kieffer", "Whiteside", "Bills", "Bledsoe", "Brownlee", "Barrows", "Courtney",
                   "Breedlove", "Feldman", "Brandenburg", "Eagle", "Mears", "Bunting", "Thompson", "Garman", "Hope",
                   "Clancy", "Whitaker", "Whalen", "Hodge", "Culpepper", "Bruno", "Robison", "Neeley",
                   "Roeder", "Baxter", "Keller", "Donato", "Wheaton", "Wilburn", "Jackman", "Abernathy", "Seeley",
                   "Belt", "Hawks", "Medley", "Birch", "Gough", "Mcneely", "Armstrong", "Colbert", "Christianson",
                   "Huston", "Magnuson", "Dietz", "Morrissey", "Greer", "Kyle", "Mcgarry", "Mull", "Fusco", "Higgins",
                   "Gooch", "Snook", "Goss", "Nilson", "Beattie", "Rife", "Hayes", "Franks", "Salisbury",
                   "Ruggiero", "Deboer", "Rowland", "Embry", "Powers", "Pate", "Shapiro", "Herzog", "Reedy", "Buehler",
                   "Unger", "Cassell", "Finn", "Harrington", "Frankel", "Ritchey", "Dorn", "Christy", "Tyson",
                   "Martindale", "Mccurdy", "Thayer", "Corrigan", "Wills", "Jansen", "Hail", "Bingham", "Ramey",
                   "Searcy", "Alford", "Redmon", "Delong", "Thorpe", "Beers", "Belanger", "Tackett", "Michels",
                   "Calvin", "Kwiatkowski", "Ring", "Blum", "Lackey", "Rutledge", "Farrar", "Crump", "Gorham", "Bryson",
                   "Southerland", "Blodgett", "Bradshaw", "Copeland", "Woodward", "Borges", "Horne",
                   "Nicholson", "Samson", "Givens", "Windham", "Pepper", "Markham", "Finch", "Greco", "Mcclintock",
                   "Carey", "Voss", "Moseley", "Mize", "Hitt", "Owens", "Brittain", "Barros", "Isaacs", "Baskin",
                   "Mortensen", "Rainey", "Somers", "Sowers", "Hurst", "Royal", "Crawford", "Broussard", "Hamilton",
                   "Ahrens", "Eldridge", "Bradbury", "Wallen", "Otto", "Fisk", "Gaston",
                   "Rust", "Franke", "Andrew", "Patten", "Lindgren", "Showalter", "Wilkins", "Willingham", "Weston",
                   "Pruitt", "Brenner", "Clements", "Hathaway", "Bandy", "Clement", "Purcell", "Mcalister", "Gilligan",
                   "Bartholomew", "Lantz", "Rossi", "Latimer", "Sinclair", "Sherrill", "Healey", "Pelletier", "Thigpen",
                   "Aldrich", "Reuter", "Brumfield", "Neville", "Fay", "Brannon", "Taber", "Murphy", "Edwards",
                   "Henley", "Mckee", "Partridge", "Mcneill", "Collins", "Robins", "Brewer", "Weinstein", 
                   "Oates", "Cass", "Romeo", "Salem", "Rich", "Mcgowan", "Irby", "Curtin", "Lay", "Lavender",
                   "Broughton", "Snider", "Palmer", "Holmes", "Gabriel", "Gresham", "Morse", "Manning", "Schumann",
                   "Vanhorn", "Ricker", "Whitten", "Rockwell", "Chaney", "Conlon", "Keenan", "Markley", "Ryder",
                   "Woods", "Ellington", "Gregory", "Mccollum", "Kee", "Deutsch", "Reece", "Kincaid", "Clay", "Millard",
                   "Freitas", "Witte", "Oliveira", "Snell", "Posey", "Ogrady", "Lacroix", "Mcclanahan", "Bosch",
                   "Fitzsimmons", "Spellman", "Phelps", "Mcguire", "Dubose", "Mcinnis", "Langlois", "Buell",
                   "Willson", "Hagen", "Eisenberg", "Cates", "Sherman", "Costello", "Whitman", "Tierney", "Mckinley",
                   "Kling", "Muller", "Bradford", "Lavoie", "Coyle", "Kingsley", "Friedman", "Barnes", "Saylor",
                   "Jarrell", "Weatherford", "Mckeever", "Dupre", "Lambert", "Eads", "Boles", "Gruber", "Talbot",
                   "Mcginley", "Kaufmann", "Hammond", "Carter", "Walling", "Cosgrove", "Oconnor", "Rutkowski",
                   "Mcgregor", "Hanson", "Casey", "Gearhart", "Leone", "Neely", "Rohr", "Ridenour", "Hartmann",
                   "Tanner", "Gower", "Ward", "Stamps", "Ponder", "Paulson", "Pettigrew", "Cockrell", "Stoltzfus",
                   "Hartzell", "Clemens", "Kunkel", "Rhoads", "Winstead", "Meyers", "Mckeon", "Donley", "Graves",
                   "Brand", "Hedges", "Bonham", "Hubbard", "Pinson", "Saul", "Harman", "Hartnett", "Baugh", "Gunn",
                   "Hutcheson", "Mcnabb", "Combs", "Meek", "Larsen", "Schwab", "Weil", "Tinsley", "Roderick", "Fitch",
                   "Lively", "Seaton", "Hargrave", "Puckett", "Geary", "Ott", "Sutton", "Gatlin", "Dobbs", "Jett",
                   "Moser", "Callahan", "Gaskin", "Gleason", "Randolph", "Card", "Beckham", "Fulkerson", "Melvin",
                   "Grey", "Michalski", "Deloach", "Aiken", "Tabor", "Pippin", "Estes", "Hoyle", "Jones",
                   "Penny", "Roberts", "Stuart", "Hooker", "Lacy", "Summers", "Emery", "Weldon", "Cotter", "Holder",
                   "Orton", "Mccarthy", "Rains", "Keeling", "Weed", "Wegner", "Guarino", "Cohn", "Gilson", "Medlin",
                   "Gunther", "Sadler", "Johnston", "Yoder", "Stidham", "Judge", "Witt", "Dockery", "Zeigler",
                   "Lovell", "Blackwell", "Waters", "Cantrell", "Clark", "Hodgson", "Farley", "Herrick", "Snowden",
                   "Moses", "Fabian", "Mancini", "Friedrich", "Leroy", "Mccann", "Mckenney", "Troutman",
                   "Ferry", "Southard", "Libby", "Minor", "Ethridge", "Traylor", "Stanley", "Tilton", "Beeler",
                   "Mcgovern", "Garber", "Treadway", "Guenther", "Buxton", "Lange", "Grubb", "Dick", "Tatum", "Rayburn",
                   "Fernandes", "Connor", "Hodges", "Moorman", "Carson", "Peterman", "Mccormack", "Conger", "Helm",
                   "Key", "Messick", "Buffington", "Warden", "Herbst", "Wadsworth", "Fortner", "Wheatley", "Pannell",
                   "Poston", "Emmons", "Applegate", "Cox", "Frazer", "Ross", "Baron", "Mead", "Mcbride", "Dillon",
                   "Schindler", "Stoker", "Turk", "Alexander", "Rasmussen", "Lawson", "Mckelvey", "Steel", "Mccarty",
                   "Swanson", "Zielinski", "Byrne", "Brunner", "Nugent", "Bayer", "Houck", "Cupp", "Craven", "Dubois",
                   "Hobson", "Wicker", "Deal", "Booher", "Adam", "Crane", "Rock", "Wentworth", "Goebel", "Shull",
                   "Martell", "Rash", "Nielson", "Kitchens", "Parent", "Kozlowski", "Barber", "Lilley", "Dumas",
                   "Sorensen", "Valente", "Harvey", "Munson", "Munn", "Martz", "Pringle", "Goodrich", "Gillis",
                   "Martini", "Minton", "Call", "Varney", "Weems", "Gross", "Keefe", "Dove", "Hale", "Bourgeois",
                   "Skipper", "Cramer", "Flanagan", "Lanham", "Farmer", "Dunlap", "Gardner", "Ketchum", "Mcmurray",
                   "Sales", "Fleming", "Hintz", "Roark", "Gerlach", "Bales", "Strange", "Wilson", "Mcclain", "Byrd",
                   "Nix", "Beaulieu", "Oglesby", "Adcock", "Stroud", "Schulte", "Leclair", "Stuckey", "Baggett",
                   "Heaton", "Clary", "Merkel", "Reagan", "Gosnell", "East", "Miley", "Read", "Lovejoy", "Sabo",
                   "Huskey", "Boston", "Burger", "Lindley", "Smithson", "Wilkerson", "Starr", "Jerome", "Gilley",
                   "Fenner", "Russell", "Guidry", "Gates", "Mccord", "Wimberly", "Amato", "Whiteman", "Fogle", "Waller",
                   "Enos", "Bowers", "Gottlieb", "Glaser", "Floyd", "Sager", "Harter", "Lundy", "Koster", "Mancuso",
                   "Stringer", "Barth", "Dowd", "Loftus", "Meehan", "Donovan", "Hoover", "Maclean", "Laney", "Byrnes",
                   "Martel", "Riedel", "Milam", "Stull", "Woodworth", "Steele", "Seidel", "Burgess", "Coons", "Neill",
                   "Pugh", "Waite", "Head", "Marvin", "Camara", "Moulton", "Bianchi", "Brockman", "Sells",
                   "Crutchfield", "Maier", "Roy", "Rousseau", "Alderman", "Stamper", "Fuqua", "Register",
                   "Erdman", "Erb", "Albert", "Heath", "Duckworth", "Roland", "Staples", "Boling", "Lehmann", "Horn",
                   "Fredericks", "Mcallister", "Oakley", "Nickerson", "Handley", "Bowen", "Basile", "Frick", "Langford",
                   "Oaks", "Holtz", "Beaver", "Sisco", "Pierson", "Halsey", "Sprouse", "Beiler", "Zimmermann", "Keys",
                   "Andrews", "Judd", "Roller", "Mackey", "Merrick", "Weinberg", "Lauer", "Weiner", "Keel",
                   "Christensen", "Granger", "Hardy", "Stovall", "Gonsalves", "Wickham", "Mcknight", "Isaacson",
                   "Milburn", "Evers", "Kenny", "Chadwick", "Bray", "Redmond", "Shoemaker", "Cochrane", "Lovelace",
                   "Lynch", "Bowden", "Mcmillan", "Rollins", "Reich", "Gilbertson", "Scherer", "Sowell", "Patterson",
                   "Whiting", "Holt", "Grover", "Eckert", "Tibbs", "Crews", "Burnett", "Adler", "Renner", "Royer",
                   "Grasso", "Sneed", "Seals", "Wainwright", "Weiler", "Yarbrough", "Smyth", "Redman", "Falk", "Shank",
                   "Durham", "Welsh", "Wentz", "Hunt", "Belcher", "Renfro", "Rizzo", "Marques", "Coffman", "Patton",
                   "Hendricks", "Crist", "Schiller", "Hales", "Caputo", "Lind", "Russo", "Shuler", "Legg", "Etheridge",
                   "Chaffin", "Goldstein", "Janes", "Starnes", "Pyles", "Greenberg", "Gibbons", "Carroll", "Scarbrough",
                   "Bassett", "Riley", "Hammer", "Roth", "Falcone", "Herron", "Albers", "Burley", "Matlock", "Fry",
                   "Leblanc", "Mcmaster", "Macdonald", "Damron", "Boone", "Hogg", "Cody", "Kenyon", "Mckenna",
                   "Erwin", "Whitmore", "Fenton", "Marcus", "Sargent", "Blackman", "Kuykendall", "Whited", "Blakely",
                   "Keil", "Stine", "Albertson", "Conrad", "Raines", "Daly", "Mickelson", "Fountain", "Wharton",
                   "Gilman", "Bannister", "Thurman", "Spurgeon", "Bracken", "Gordon", "Triplett", "Fletcher", "Kress",
                   "Archer", "Dunne", "Reis", "Culver", "Hill", "Reilly", "Asher", "Hannah", "Hughes", "Friend",
                   "Marek", "Sherry", "Daigle", "Clausen", "Ames", "Drake", "Presley", "Crosby", "Felts", "Gagne",
                   "Whelan", "Kurtz", "Galvin", "Linn", "Brice", "Borden", "Byers", "Wheat", "Denney", "Simmons",
                   "Bain", "Trombley", "Mattson", "Marx", "Iverson", "Richards", "Shelton", "Brubaker", "Albanese",
                   "Chastain", "Hurt", "Coley", "Oconnell", "Flora", "Baldwin", "Kish", "Alley", "Sander", "Grande",
                   "Unruh", "Tracey", "Pulley", "Mcwhorter", "Trotter", "Cooney", "Ludwig", "Rathbun", "Mills", "Earl",
                   "Wimmer", "Whittington", "Jordan", "Clemmons", "Houghton", "Sheppard", "Holman", "Hahn", "Newberry",
                   "Griffith", "Camp", "Turner", "Glover", "Blanchard", "Cummins", "Cheek", "Baumgartner", "Seaman",
                   "Frame", "Bruner", "Sellers", "Croft", "Glasgow", "Conaway", "Proffitt", "Winchester", "Gooding",
                   "Judy", "Daley", "Needham", "Gillen", "Durand", "Hague", "Rawson", "Paxton", "Bagley", "Whitworth",
                   "Morley", "Desantis", "Hillman", "Cowart", "Gann", "Wooden", "Sayers", "Monson", "Osullivan",
                   "Slayton", "Mcelroy", "Layman", "Benjamin", "Mcclelland", "Roden", "Choate", "Oshea", "Kuhn",
                   "Manley", "Bohn", "Hanks", "Haase", "Keener", "Dahl", "Garrett", "Beckman", "Neal", "Morrill", "Ivy",
                   "Pitman", "Keeton", "Augustine", "Sylvester", "Street", "Huggins", "Switzer", "Worley", "Shaw",
                   "Fort", "Leigh", "Salyer", "Allred", "Dodge", "Witmer", "Weiss", "Furlong", "Cady", "Maloney",
                   "Jack", "Mendenhall", "Maddox", "Halverson", "Nunley", "Wasson", "Pauley", "Jay", "Bauer", "Enright",
                   "Holliday", "Metzler", "Sexton", "Amos", "Hetrick", "Bittner", "Lundquist", "Malcolm", "Truitt",
                   "Lord", "Bentley", "Mcdevitt", "Livingston", "Coppola", "Mcdade", "Ezell", "Scarborough",
                   "Fullerton", "Ferraro", "Britton", "Mccartney", "Mcnally", "Massey", "Odonnell", "Jacobsen",
                   "Musick", "Trent", "Stevens", "Blount", "Sessions", "Huntley", "Sammons", "Winslow", "Wojcik",
                   "Spurlock", "Thomson", "Yates", "Lundgren", "Pulliam", "Meier", "Bischoff", "Rosenberger",
                   "Myrick", "Brinson", "Eller", "Pritchett", "Ricketts", "Hall", "Woolley", "Mcconnell", "Mcafee",
                   "Corbett", "Horner", "Groves", "Barkley", "Whittle", "Blank", "Boswell", "Blackwood",
                   "Tisdale", "Burrows", "Rosen", "Taylor", "Shannon", "Paulsen", "Thorne", "Norton", "Straub", "Brady",
                   "Atchison", "Stoll", "Snipes", "Lancaster", "Shaver", "Waldron", "Rosser", "Borders", "Mcmillen",
                   "Post", "Ladd", "Cushing", "Holbrook", "Gray", "Harper", "Painter", "Phelan", "Heilman", "Masterson",
                   "Wenzel", "Gurley", "Causey", "Steinmetz", "Sprague", "Christie", "Casper", "Mccall", "Rider",
                   "Heck", "Schmid", "Schweitzer", "Slattery", "Heims", "Bolt", "Snyder", "Loper", "Welker", "Griffis",
                   "Sweat", "Mckeown", "Gatewood", "Morrell", "Halstead", "David", "Ingram", "Baird", "Miner", "Fleck",
                   "Fagan", "Allman", "Bruce", "Ware", "Hazel", "Grenier", "Rudd", "Bahr", "Bryan", "Hamby", "Shepard",
                   "Boatwright", "Bernstein", "Redden", "Crocker", "Nolan", "Butcher", "Haines", "Bricker", "Boyce",
                   "Nance", "Mashburn", "Newton", "Toler", "Sumner", "Reaves", "Carden", "Nathan", "Silverstein",
                   "Reed", "Foreman", "Ashe", "Hickey", "Anthony", "Martins", "Lemaster", "Doll", "Grogan", "Stebbins",
                   "Mayberry", "Anglin", "Higginbotham", "Mccue", "Linville", "Larose", "Carbone", "Seibert",
                   "Warfield", "Pickens", "Walz", "Ries", "Greene", "Mertz", "Jenks", "Destefano", "Walters", "Nettles",
                   "Lowery", "Teixeira", "Putnam", "Volpe", "Gauthier", "Hanlon", "Walker", "Ragan", "Tucker", "Rubino",
                   "Kirk", "Stepp", "Leslie", "Shelby", "Jernigan", "Downey", "Woolsey", "Palermo", "Schreiber",
                   "Arndt", "Salter", "Pease", "Barnard", "Hussey", "Lucas", "Walsh", "Vincent", "Silver", "Bivens",
                   "Bussey", "Hartwell", "Jacobs", "Bernhardt", "Deyoung", "Counts", "Farrow", "Lutz", "Strain",
                   "Dreyer", "Hofer", "Schmitz", "Milner", "Oden", "Parkinson", "Romano", "Hibbard", "Staggs", "Mcvay",
                   "Nash", "Owen", "Johnson", "Glenn", "Toney", "Mcdonough", "Whitcomb", "Purdy", "Loyd", "Quick",
                   "Slaughter", "Doolittle", "Marchese", "Montague", "Doughty", "Earley", "Swafford", "Pieper",
                   "Conley", "Kruger", "Ragland", "Harlow", "Carmichael", "Garrison", "Shanks", "Michel", "Weller",
                   "Huff", "Hacker", "Cobb", "Larue", "Guillory", "Speer", "Cato", "Hoff", "Madison", "Benoit",
                   "Flowers", "Lipscomb", "Langston", "Mckenzie", "Howland", "Andres", "Dayton", "Donnelly", "Potter",
                   "Clouse", "Shirley", "Downs", "Hecht", "Stubblefield", "Matheny", "Walther", "Selby", "Stark",
                   "Rutherford", "Bergeron", "Eggleston", "Simpkins", "Reiter", "Rohrer", "Knoll", "Lusk", "Jorgensen",
                   "Gannon", "Jarvis", "Lindberg", "Newman", "Wiseman", "Schreiner", "Perdue", "Burdick", "Galbraith",
                   "Garvin", "Boren", "Frederick", "Priest", "Beverly", "Valenti", "Smothers", "Bartley", "Burnside",
                   "Larkin", "Lamb", "Agnew", "Spitzer", "Mccutcheon", "Shipman", "Mackenzie", "Himes", "Wheeler",
                   "Ely", "Cottrell", "Munro", "Plunkett", "Dickerson", "Williford", "Leary", "Ruff", "Sample", "Niles",
                   "Stephan", "Badger", "Cordell", "Robertson", "Creighton", "Creech", "Briggs", "Hoffman", "Reinhart",
                   "Richmond", "Bolen", "Cornelius", "Pendleton", "Olmstead", "Mangum", "Basham", "Vetter", "Barr",
                   "Marquardt", "Erickson", "Holland", "Faulkner", "Melton", "Haynes", "Heffernan", "Whyte", "Skidmore",
                   "Adams", "Minnick", "Towne", "Greiner", "Mccormick", "Crawley", "Ruble", "Prewitt", "Roddy", "Heil",
                   "Sheets", "Marker", "Atkinson", "Wilkes", "Cushman", "Wilt", "Palumbo", "Pogue", "Ruth",
                   "Littlefield", "Newby", "Stinnett", "Mcmullen", "Wozniak", "Keeler", "Havens", "Grisham", "Shaffer",
                   "Castellano", "Wilbur", "Greathouse", "Poe", "Holley", "Barnhill", "Rankin", "Lennon", "Koch",
                   "Larson", "Arsenault", "Rosenfeld", "Hooper", "Darr", "Kremer", "Binkley", "Merrill", "Miller",
                   "Vickers", "Hare", "Whitley", "Cotton", "Jobe", "Dickinson", "Morgan", "Rinaldi", "Kaminski",
                   "Riggs", "Thibodeaux", "Bostick", "Deangelo", "Ralston", "Lanning", "Hoffmann", "Connors",
                   "Mcarthur", "Valentine", "Bair", "Eden", "Mattox", "Crabtree", "Schenk", "Timmerman", "Pagano",
                   "Whatley", "Mendes", "Hancock", "Boothe", "Linder", "Theis", "Bankston", "Rector", "Horton", "Roe",
                   "Gibson", "Wright", "Tharp", "Hutson", "Clarkson", "Colley", "Sousa", "Kasper", "Muir",
                   "Peter", "Mccrary", "Beavers", "Farkas", "Gilchrist", "Robson", "Moore", "Ford", "Beck", "Bice",
                   "Hager", "Irwin", "Temple", "Dover", "Hough", "Rooney", "Goforth", "Watkins", "Corbin", "Blalock",
                   "Headley", "Shipp", "Ransom", "Estep", "Adair", "Gilliland", "Biddle", "Wilke", "Prosser", "Gerard",
                   "Wells", "Bollinger", "Pearson", "Boyer", "Hanes", "Kenney", "Bock", "Noland", "Corey", "Thomas",
                   "Joyce", "Mcpherson", "Monahan", "Pickett", "Hutton", "Tubbs", "Derr", "Reeves", "Seiler", "Lott",
                   "Cahill", "Lemke", "Cline", "Henke", "Maki", "Lund", "Burkett", "Wise", "Hackett", "Mallory", "Bone",
                   "Jacobson", "Byler", "Saunders", "Haag", "Dodson", "Mccorkle", "Flannery", "Lake", "Thomsen",
                   "Brantley", "Winn", "Hardman", "Regan", "Ginn", "Bernard", "Mccallum", "Haggard", "Simon", "Mooney",
                   "Luttrell", "Jasper", "Mundy", "Windsor", "Coulter", "Acker", "Duff", "Lawrence", "Mccaffrey",
                   "Gulley", "Simms", "Hull", "Thames", "Ackley", "Vanmeter", "Minter", "Worth", "Pettis", "Donaldson",
                   "Sands", "Whitmire", "Mercer", "Duffy", "Stanfield", "Gaskins", "Engel", "Lohr", "Bloom", "Barton",
                   "Teal", "Parrott", "Mandel", "Kirby", "Pope", "Klein", "Wellman", "Mcdowell", "Redding", "Hinkle",
                   "Baughman", "Quirk", "Stockwell", "Goolsby", "Blaylock", "Moe", "Seitz", "Criswell",
                   "Chandler", "Mchugh", "Almeida", "Yocum", "Fuller", "Johansen", "Rickard", "Sampson", "Sacco",
                   "Schaeffer", "Burr", "Groth", "Hand", "Trainor", "Burroughs", "Bettencourt", "Schoonover",
                   "Lockwood", "Karr", "Dupont", "Fraley", "Hermann", "Ripley", "Andrus", "Bailey", "Bosley", "Schulz",
                   "Autry", "Hess", "Simone", "Neff", "Mccracken", "Eason", "Kimball", "Redd", "Wilks", "Sams",
                   "Spicer", "Springer", "Utley", "Sumpter", "Pratt", "Fogarty", "Thornton", "Frantz", "Orth",
                   "Julian", "Laws", "Sorenson", "Piper", "Cornwell", "Whaley", "Seymour", "Hershberger", "Conner",
                   "Perrin", "Hornsby", "Hutchins", "Lafleur", "Garner", "Best", "Crain", "Mcnamara", "Sikes", "Roche",
                   "Sears", "Spears", "Shipley", "Saleh", "Parish", "Killian", "Smart", "Stewart", "Barbour", "Edgar",
                   "Brock", "Bachman", "Sheridan", "Wirth", "Copley", "Ferrara", "Preston", "Murrell",
                   "Gilliam", "Broyles", "Guinn", "Kinard", "Fischer", "Schmidt", "Harwood", "Joiner", "Battles",
                   "Mabe", "Snead", "Poulin", "Dangelo", "Tuttle", "Winter", "Seward", "Wynne", "Barron", "Goddard",
                   "Dickey", "Dyson", "Busby", "Billings", "Gamble", "Childress", "Burke", "Gilbert", "Ebert", "Funk",
                   "Bucher", "Fine", "Albright", "Baran", "Pinto", "Kirchner", "Garland", "Beatty", "Marquis", "Dupree",
                   "Pike", "Waiters", "Grubbs", "Paterson", "Rowley", "Custer", "Stockton", "Raynor", "Tate", "Guess",
                   "Deluca", "Mccloud", "Arnold", "Ridley", "Krantz", "Noyes", "Lovett", "Bolin", "Norman", "Prince",
                   "Herrin", "Bratcher", "Pickering", "Grayson", "Frye", "Lanier", "Hensley", "Crider",
                   "Wessel", "Keim", "Eggers", "Fryer", "Ennis", "Gill", "Carlson", "Bechtel", "Vogel", "Gagnon",
                   "Oleary", "Scott", "Wick", "Fiore", "Wampler", "Burt", "Bunch", "Schultz", "Stott",
                   "Mcwilliams", "Breaux", "Payne", "Hutchison", "Giese", "Hair", "Willett", "Keane", "Button",
                   "Settle", "Hedrick", "Linton", "Burrow", "Castleberry", "Ferrari", "Easterling", "Ferreira",
                   "Bertram", "Bonner", "Penrod", "Myers", "Wyatt", "Lenz", "Davis", "Bordelon", "Cleary", "Conover",
                   "Moen", "Walton", "Troyer", "Ragsdale", "Watt", "Schneider", "Vinson", "Weathers", "Bristol",
                   "Jester", "Olson", "Findley", "Watters", "Ledford", "Gerber", "Desimone", "Stowe", "Hines", "Wyman",
                   "Goode", "Harris", "Godfrey", "Dehart", "Novotny", "Heffner", "Matthews", "Crowder", "Kramer",
                   "Kendrick", "Huss", "Napier", "Kehoe", "Mcgill", "Heflin", "Moll", "Casto", "Hyland", "Beam",
                   "Gregg", "Donald", "Montgomery", "Braun", "Emerson", "Kidder", "Benton", "Petersen", "Cavanaugh",
                   "Withers", "Meade", "Furr", "Logan", "Kozak", "Clifford", "Irvine", "Packer", "Justice",
                   "Huddleston", "Dailey", "Brophy", "Riordan", "Stillwell", "Victor", "Lassiter", "Hopson", "Humphrey",
                   "Dye", "Grady", "Conte", "Dwyer", "Kaplan", "Hudgins", "Corder", "Skelton", "Ryan", "Greenlee",
                   "Keene", "Meeker", "Mullins", "Toomey", "Swartz", "Armour", "Otis", "Mcmahon", "Griffiths",
                   "Bontrager", "Marino", "Beckett", "Bernier", "Noll", "Wallis", "Schott", "Ledbetter",
                   "Earnest", "Steen", "Chestnut", "Runyon", "Ferris", "Crum", "Johnsen", "Kingston", "Silverman",
                   "Dean", "Pickard", "Hart", "Knowles", "Mcintosh", "Majors", "Ogden", "Shane", "Pool", "Krebs", "Eby",
                   "Bail", "Coats", "Solomon", "Faust", "Fahey", "Clough", "Brennan", "Field", "Stein", "Nixon",
                   "Harbin", "Sparkman", "Palm", "Abel", "Westmoreland", "Haight", "Parson", "Petty", "Lincoln",
                   "Worthington", "Gorski", "Buchholz", "Gallagher", "Kidwell", "Hoag", "Aiello", "Cherry", "Wilhite",
                   "Holly", "Noe", "Lombardo", "Laird", "Neumann", "Bourque", "Brinkman", "Slater", "Hauser", "Gee",
                   "Gillespie", "Everhart", "Hutto", "Cason", "Beil", "Sanderson", "Krieger", "Bowles", "Farr",
                   "Vandyke", "Hatfield", "Clemons", "Pearl", "Mayer", "Odom", "Ruby", "Samples", "Kiefer", "Sharpe",
                   "Barger", "Swisher", "Warner", "Cheatham", "Church", "Landis", "Whipple", "Leavitt", "Paquette",
                   "Boehm", "Coon", "Cantwell", "Marion", "Mcneil", "Bennett", "Keck", "Hartley", "Bruns",
                   "Flick", "Wray", "Cope", "Engle", "Dougherty", "Graf", "Provost", "Sharkey", "Beasley",
                   "Hyatt", "Sturgill", "Butts", "Shinn", "Barnett", "Plummer", "Hawkins", "Brooks", "Lumpkin", "Keyes",
                   "Barone", "Spalding", "Rodrigues", "Boss", "Leighton", "Rhea", "Meador", "Dube", "Woody",
                   "Mcleod", "Huebner", "Dion", "Stout", "Rogers", "Lundberg", "Adkins", "Capps", "Carrier", "Clapp",
                   "Canfield", "Fox", "Friesen", "Slone", "Doherty", "Tripp", "Thatcher", "Butterfield", "Barlow",
                   "Buckner", "Lafferty", "Stover", "Hurley", "Bull", "Drury", "Wasserman", "Hampton",
                   "Mccauley", "Landon", "Hardwick", "Beeson", "Vargo", "Fellows", "Cummings", "Swank", "Wolford",
                   "Pace", "Brunson", "Vick", "Herr", "Ingle", "Kline", "Comstock", "Honeycutt", "Holcombe", "Goad",
                   "Lehman", "Currier", "Bullock", "Hennessy", "Rau", "Forsythe", "Hatton", "Lyons", "Troy", "Ibrahim",
                   "Dowell", "Locke", "Dellinger", "Ridgeway", "Haller", "Stauffer", "Southern", "Eastman", "Shockley",
                   "Westbrook", "Savage", "Whitson", "Houser", "Dvorak", "Nelms", "Murdock", "Chase", "Fredrickson",
                   "Shumate", "Herrington", "Vogt", "Porter", "Milton", "Chester", "Champion", "Groff", "Dixon",
                   "Lemay", "Yost", "Gary", "Colson", "Arnett", "Riggins", "Merchant", "Dickson", "Carney", "Howes",
                   "Stevenson", "Haas", "Kerns", "Bader", "Cote", "Heckman", "Collett", "Falls", "Cowan",
                   "Metzger", "Thornburg", "Severson", "Olds", "Rinehart", "Kern", "Finley", "Knutson", "Nesmith",
                   "Michaud", "Michael", "Schrock", "Davenport", "Atkins", "Blake", "Hewitt", "Dutton", "Sewell",
                   "Madsen", "Foote", "Sherwood", "Coleman", "Morris", "Workman", "Gaffney", "Lapointe", "Woodcock",
                   "Stacy", "Harrelson", "Dempsey", "Prater", "Flynn", "Reichert", "Scholl", "Kiley", "Kidd", "Pyle",
                   "Walden", "Bolton", "Lorenz", "Chambers", "Hansen", "Partin", "Fraser", "Goodwin", "Fairbanks",
                   "Cloutier", "Huffman", "Billingsley", "Boyles", "Lewis", "Bates", "Crites", "Mohr",
                   "Stephens", "Marks", "Rauch", "Shell", "Venable", "Anders", "Sims", "Barrow",
                   "Breen", "Everson", "Horowitz", "Winters", "Horning", "Whitlock", "Muse", "Varner", "Zink",
                   "Mcintire", "Bliss", "Poore", "Doss", "Dagostino", "Griffin", "Hollis", "Woodbury", "Kohl",
                   "Huntington", "Ham", "Hulse", "Dykes", "Willoughby", "Strother", "Booth", "Kroll", "Garrity",
                   "Plank", "Adamson", "Craddock", "Mcginnis", "Luther", "Ernst", "Devlin", "Grigsby", "Hays",
                   "Pinkerton", "Backus", "Mclemore", "Dill", "Ellison", "Rea", "Stock", "Jeffries", "Reardon", "Blair",
                   "Graff", "Townsend", "Richardson", "Mohler", "Merritt", "Moriarty", "Fugate", "Lathrop", "Fannin",
                   "Moreau", "Layne", "Pollack", "Swope", "Waldrop", "Gale", "Justus", "Teel", "Sigler", "Moffitt",
                   "Willard", "Schumacher", "Cranford", "Wayne", "Bremer", "Landrum", "Clanton", "Durbin", "Kellogg",
                   "Braswell", "Whitehurst", "Fink", "Rupp", "Kiser", "Kovacs", "Mclain", "Lightfoot", "Hailey", "Hite",
                   "Gainey", "Roush", "Forsyth", "Paine", "Haney", "Cohen", "Swan", "Jamieson", "Thibodeau", "Hulsey",
                   "Fortune", "Kinsey", "Waddell", "Berger", "Diamond", "Ferrell", "Carnes", "Kent", "Baxley",
                   "Dombrowski", "Boudreaux", "Gaddis", "Trimble", "Monaghan", "Fazio", "Hinson", "Pederson",
                   "Sandberg", "Hembree", "Haggerty", "Gavin", "Giddens", "Mabry", "Keegan", "Foley", 
                   "Bostic", "Knudson", "Schilling", "Harless", "Pedersen", "Gore", "Blackburn", "Pellegrino", "Poland",
                   "Schell", "Cloud", "Hubert", "Beach", "Bigelow", "Siler", "Talley", "Cain", "Jonas", "Pitts",
                   "Metcalf", "Conn", "Arthur", "Currie", "Tarr", "Waterman", "Wood", "Peek", "Rutter", "Chapman",
                   "Isaac", "Carman", "Roach", "Healy", "Bickel", "Goncalves", "Altman", "Derrick", "Proctor", "Cannon",
                   "Beall", "Boyle", "Doucette", "Corwin", "Colwell", "Eaton", "Hutchings", "Morrow", "Longo", "Jaeger",
                   "Morehead", "Briscoe", "Lilly", "Chrisman", "Merrell", "Mcgrath", "Berg", "Sperry",
                   "Corley", "Denning", "Taft", "Lavigne", "Damico", "Mullis", "Crooks", "Rushing", "Hoppe", "Conti",
                   "Kesler", "Ehlers", "Holton", "Cooley", "Dallas", "Beyer", "Rigsby", "Randall", "Alcorn", "Knight",
                   "Hilliard", "Aldridge", "Joyner", "Mosier", "Bragg", "Blocker", "Ogle", "Zimmer", "Isom",
                   "Buck", "Pond", "Seal", "Hume", "Goodson", "Kilgore", "Babb", "Hoyt", "Meeks", "Keith", "Brothers",
                   "Lapp", "Underhill", "Stjohn", "Sawyer", "Bratton", "Nagy", "Sachs", "Kennedy", "Newkirk", "Hatcher",
                   "Satterfield", "Rosenthal", "Schlegel", "Thorn", "Smail", "Kilpatrick", "Koester", "Parr", "Cathey",
                   "Grabowski", "Fennell", "Amaral", "Wendt", "Sipes", "Akers", "Oneal", "Bethel", "Koehn", "Stoddard",
                   "Strickland", "Rowan", "Tilley", "Batson", "Howard", "Shore", "Gentry", "Ridge", "Brumley", "Robert",
                   "Blankenship", "Newsome", "Butler", "Blackmon", "Timm", "Tomlin", "Durant", "Rice", "Hoy", "Howell",
                   "Radford", "Cronin", "Davey", "Paul", "Bond", "Reynolds", "Bright", "Richey", "Horvath", "Moss",
                   "Hannon", "Daugherty", "Thomason", "Scanlon", "Werner", "Janssen", "Cornett", "Rawlings",
                   "Blanchette", "Storm", "Brandon", "Newcomb", "Devito", "Williamson", "Esposito", "Robinette",
                   "Sasser", "Duval", "Beale", "Trout", "Sanders", "Brink", "Pollock", "Ballard", "Gunter", "Browning",
                   "Mason", "Peak", "Gipson", "Spring", "Moreland", "Kersey", "Holm", "Hardin", "Phillips", "Sauer",
                   "Mckinney", "Ballinger", "Mahaffey", "Packard", "Scruggs", "Schnell", "Stokes", "Loving", "Kerr",
                   "Oreilly", "Ellis", "Peltier", "Christopher", "Barney", "Simpson", "Mccune", "Frazier", "Kempf",
                   "Mulder", "Mcrae", "Barnette", "Mckinnon", "Dix", "Lawton", "Farrington", "Elrod", "Roby", "Mullin",
                   "Gable", "Covert", "Kemper", "Platt", "Kemp", "Forster", "Harp", "Laster", "Piazza", "Bower",
                   "Tibbetts", "Cartwright", "Monk", "Carr", "Chamberlin", "Leggett", "Hankins", "Parnell", "Cleveland",
                   "Kistler", "Vandenberg", "Clem", "Penn", "Romine", "Begley", "Fiedler", "Trowbridge", "Koller",
                   "Mccoy", "Weir", "Thacker", "Gladden", "Appel", "Burris", "Burton", "Westfall", "Knox", "Cromer",
                   "Atwood", "Christman", "Jameson", "Kay", "Lehr", "Beaudoin", "Burden", "Harlan", "Glass", "Denny",
                   "Hawley", "Hogan", "Schmitt", "Henderson", "Lowry", "Fain", "Slack", "Batten", "Mcmichael",
                   "Elliott", "Kimmel", "Dow", "Littleton", "Norwood", "Clegg", "Harley", "Hackney", "Stubbs", "Easton",
                   "Tyree", "Correll", "Fontenot", "Levine", "Wakefield", "Albrecht", "Shade", "Purvis", "Barrett",
                   "Powell", "Clawson", "Isbell", "Hearn", "Tenney", "Wild", "Ashton", "Hunter", "Grantham", "Kirkland",
                   "Rowe", "Hopkins", "Bogart", "Crockett", "Titus", "Tracy", "Britt", "Jablonski", "Krug",
                   "Ritchie", "Beaty", "Bickford", "Graham", "Berkowitz", "Mott", "Campbell", "Stanton", "Bach",
                   "Denham", "Ewing", "Mace", "Pereira", "Shea", "Callaway", "Carlton", "Logue", "Schaefer", 
                   "Mathis", "Ostrander", "Blanton", "Carlin", "Schatz", "Kimble", "Graber", "Saxton", "Shook",
                   "Devries", "Peterson", "Glick", "Handy", "Mcgee", "Sanford", "Cade", "Hyde", "Fortier", "Hildebrand",
                   "Cornell", "Rawls", "Orourke", "Cooper", "Mccombs", "Harms", "Wilkie", "Moffett", "Harmon", "Wolf",
                   "Streeter", "Warren", "Langdon", "Ulmer", "Stiles", "Sanborn", "Krauss", "Compton",
                   "Dunham", "Moran", "Salerno", "Gould", "Vann", "Feller", "Nesbitt", "Lunsford", "Flint", "Gandy",
                   "Thornhill", "Hendrickson", "Stallings", "Matson", "Hirsch", "Chism", "Marr", "Laughlin", "Dewey",
                   "Calabrese", "Siebert", "Aaron", "Brownell", "Sweeney", "Brinkley", "Daily", "Dodd", "Carver",
                   "Malloy", "Menard", "Colvin", "Kendall", "Odell", "Correia", "Nelson", "Parisi", "Singer", "Cyr",
                   "Neel", "Peebles", "Brody", "Schwarz", "Lane", "Flanders", "Mulligan", "Burchett", "Barclay",
                   "Souza", "Caudle", "Berry", "Bohannon", "Jewell", "Culbertson", "Anderson", "Oneill",
                   "Perkins", "Landry", "Hay", "Bass", "Tobias", "Rhodes", "Costa", "Carpenter", "Keaton", "Dalton",
                   "Santoro", "Hawthorne", "Childers", "Vitale", "Peace", "Quigley", "Neil", "Hynes", "Lytle", "Robb",
                   "Kuehn", "Greenwood", "Swann", "Deaton", "Pack", "Colby", "Lawless", "Hundley", "Gillette", "Knotts",
                   "Ingalls", "Rose", "Seifert", "Harrison", "Pitt", "Spriggs", "Sisson", "Koenig", "Grice", "Cardwell",
                   "Rubin", "Meredith", "Knowlton", "Burnette", "Eaves", "Bell", "Carlisle", "Raney", "Beauchamp",
                   "Gold", "Parris", "Dodds", "Reimer", "Hammett", "Prentice", "Hein", "Ohara", "Sorrell", "Raley",
                   "Turley", "Fuchs", "Allison", "Condon", "Corcoran", "Hargis", "Covington", "Quinlan", "Langley",
                   "Kovach", "Geiger", "Gustafson", "Watts", "Wilcox", "Lerner", "Roberson", "Ferrante", "Gifford",
                   "Younger", "Mackay", "Schroeder", "Kelly", "Mchale", "Hendrick", "Maggard", "Spires", "Pfeifer",
                   "Gilmore", "Pape", "Mahoney", "Mathias", "Lacey", "Toth", "Jeffrey", "Hildreth", "Peck", "Monaco",
                   "Marlow", "Eck", "Motley", "Gay", "Coburn", "Shay", "Marsh", "Tavares", "Cassidy", "Putman",
                   "Szymanski", "Barfield", "Pearce", "Hanley", "Bland", "Okeefe", "Herbert", "Peters", "Prather",
                   "Conway", "Dunning", "Samuelson", "Rowell", "Peacock", "Flood", "Cosby", "Foster", "Vickery",
                   "Mcdermott", "Whitehead", "Fritz", "Guido", "Kraft", "Usher", "Garnett", "Crouch", "Davidson",
                   "Beal", "Pappas", "Bridges", "Geller", "Jenkins", "Rudolph", "Hyman", "Watson", "Lowman", "Roper",
                   "Pritchard", "Francis", "Burdette", "Feeney", "Monroe", "Cormier", "Boudreau", "Grossman",
                   "Mcdonnell", "Keiser", "Hannan", "Leonard", "Major", "Picard", "Whitlow", "Moon", "Hummel",
                   "Lindner", "Hamm", "Mauro", "Bird", "Branham", "Inman", "Lindsay", "Wingate", "Barry", "Fitzgerald",
                   "Womack", "Andre", "Burk", "Nunn", "Glynn", "Foss", "Rambo", "Drew", "Stearns", "Alves", "Hoskins",
                   "Mccurry", "Spear", "Barbee", "Shanahan", "Ness", "Nadeau", "Hefner", "Osborn", "Simons", "Dial",
                   "Beard", "Clifton", "Crandall", "Goble", "Hagan", "Henning", "Ambrose", "Baum", "Skaggs", "Pomeroy",
                   "Everett", "Lemieux", "Burleson", "Geer", "Whittaker", "Hayward", "Potts", "Bishop", "Vance",
                   "Sullivan", "Slade", "Mobley", "Hawes", "Drummond", "Tomlinson", "Hills", "Connell", "Steffen",
                   "Wertz", "Stinson", "Brewster", "Hemphill", "Calvert", "Stump", "Gantt", "Sizemore", "Madden",
                   "Sutherland", "Boland", "Bianco", "Hastings", "Tompkins", "Schrader", "Wyant", "Dunbar",
                   "Reitz", "Ainsworth", "Gomes", "Marler", "Elkins", "Steinberg", "Musser", "Morrison", "Houle",
                   "Kaiser", "Doyle", "Parks", "Hamlin", "Coffin", "Walter", "Stephenson", "Bowling", "Benner", "Hiatt",
                   "Vollmer", "Ives", "Marshall", "Shearer", "Rodgers", "Beardsley", "Savoy", "Joslin", "Neilson",
                   "Logsdon", "Wylie", "Coughlin", "Otoole", "Doran", "Shepherd", "Orlando", "Goldberg", "Musselman",
                   "Sides", "Fried", "Hopper", "Bronson", "Craig", "Ivey", "Maurer", "Casteel", "Landers", "Mcculloch",
                   "Lea", "Ramsay", "Schoen", "Stegall", "Kuntz", "Boettcher", "Hardison", "Siegel", "Elmore",
                   "Martens", "Goins", "Caldwell", "Crow", "Tennant", "Mathews", "Koontz", "Mclaughlin",
                   "Mcgraw", "Nagel", "Webb", "Grant", "Kraus", "Nutt", "Peyton", "Wagoner", "Brackett",
                   "Crenshaw", "Benson", "Downing", "Wilkinson", "Mueller", "Perry", "Mays", "Wolfe", "Kohn", "Huey",
                   "Vaccaro", "Hightower", "Mosher", "Ayers", "Geyer", "Plante", "Dennis", "Griggs", "Root",
                   "Fournier", "Horan", "Becker", "Carl", "Lowe", "Kitchen", "Ritter", "Turpin", "Woodruff", "Heller",
                   "Pollard", "Mann", "Reeder", "Ray", "Bryant", "Ayres", "Hooks", "Brower", "Starling", "Darnell",
                   "Griswold", "Trammell", "Willey", "Pendergrass", "Asbury", "Ammons", "Perryman", "Epperson",
                   "Duggan", "Tuck", "Nelsen", "Mayo", "Archibald", "Grimes", "Berryman", "Fontaine", "Liles",
                   "Sage", "Douglass", "Boggs", "Hostetler", "Tice", "Wynn", "Bowlin", "Boucher", "Lindsey", "Jacques",
                   "Wallace", "Talbert", "Jamison", "Templeton", "Faircloth", "Barnhart", "Faber", "Houston", "Stroup",
                   "Messer", "Joy", "Testa", "Diehl", "Barker", "Wooten", "Broderick", "Bush", "Tyler", "Arrington",
                   "Green", "Colburn", "Wicks", "Brannan", "Rush", "Crowell", "Dell", "Pennington", "Reno", "Stephen",
                   "Maxwell", "Nobles", "Bourne", "Mckay", "Kahn", "Ashby", "Creamer", "Schaffer", "Nielsen", "Newell",
                   "Mcqueen", "Link", "Sturgeon", "Greenwell", "Abrams", "Richman", "Spangler",
                   "Keating", "Shively", "Whitt", "Ratcliff", "Smoot", "Mcfarland", "Kelley", "Welch", "Angell",
                   "Avery", "Spiegel", "Yeager", "Keyser", "Hayden", "Hargrove", "Lang", "Fish", "Curtis", "Foy",
                   "Petrie", "Dunaway", "Shirk", "Caudill", "Ahern", "Ziegler", "Sheffield", "Shackelford", "Cecil",
                   "Molloy", "Haskell", "James", "Comer", "Hanna", "Bobo", "Easter", "Holloway", "Hurd", "Abell",
                   "Morey", "Mello", "Staton", "Ferguson", "Mccallister", "Nye", "Guy", "Wahl", "Mcnutt", "Shumaker",
                   "Mayfield", "Stclair", "Ackerman", "Chisholm", "Payton", "Mast", "Means", "Meyer", "Ballew", "Mahan",
                   "Noel", "Farrell", "Nemeth", "Laporte", "Furman", "Gossett", "Lankford", "Forrester", "Laplante",
                   "Krueger", "Hamel", "Benedict", "Stapleton", "Bogan", "Mowery", "Mount", "Cagle", "Mclean", "Lloyd",
                   "Ashley", "Poling", "Stacey", "Sheldon", "Beebe", "Lance", "Mccarter", "Jorgenson", "Tallman",
                   "Brogan", "Walls", "Macleod", "Rohde", "Terrell", "Eddy", "Steiner", "Egan", "Leger", "Felton",
                   "Mitchell", "Oswald", "Rouse", "Vanwinkle", "Winkler", "Freed", "Dickens", "Halvorson", "Hass",
                   "Slocum", "Mccloskey", "Overton", "Strand", "Hadley", "Pressley", "Allan", "Childs", "Grove",
                   "Kinder", "Kelsey", "Bess", "Grimm", "Chamberlain", "Dale", "Kolb", "Herrmann", "Lyon", "Heiser",
                   "Medeiros", "Damon", "Weigel", "Schuler", "Fanning", "Cromwell", "Koss", "Keen", "Irving", "Mauldin",
                   "Forte", "Ferro", "Bergman", "Bundy", "Scroggins", "Poole", "Shrader", "Richard", "Grim", "Parry",
                   "Mather", "Mixon", "Haugen", "Cutler", "Farber", "Higdon", "Swain", "Tiller", "Fishman", "Sibley",
                   "Ricci", "Pullen", "Donohue", "Elliot", "Mansfield", "Fincher", "Jolley", "Dennison", "Waltz",
                   "Mcclure", "Echols", "Tobin", "Burnham", "Abney", "Nunes", "Kane", "Sparrow", "Rausch", "Underwood",
                   "Graziano", "Johnstone", "Fisher", "Rainwater", "Youngblood", "Magee", "Osborne", "Heim",
                   "Buckingham", "Washburn", "Lefebvre", "Blevins", "Christenson", "Ash", "Bacon", "Yount", "Ratliff",
                   "Calkins", "Andersen", "Mazza", "Mulcahy", "Luke", "Steadman", "Quinn", "Loy", "Henry", "Kerrigan",
                   "Gaddy", "Dietrich", "Duke", "Mercier", "Schafer", "Bear", "Moeller", "Bedford", "Travers",
                   "Kessler", "Lindquist", "Pinkston", "Deangelis", "Buss", "Heinrich", "Segal", "Box", "Wooldridge",
                   "Schulze", "Mcmahan", "Buchanan", "Harrell", "Burks", "Pittman", "Irvin", "Doe", "Poindexter",
                   "Bagwell", "Middleton", "Fultz", "Allard", "Overstreet", "Vail", "Germain", "Lamar", "Cook",
                   "Turnbull", "Vanover", "Mcreynolds", "Scoggins", "Florence", "Sommer", "Wing", "John", "Koehler",
                   "Mahon", "Lemons", "Sapp", "Pryor", "Mcdaniels", "Ramsey", "Steward", "Devine", "Goodin", "Layton",
                   "Morton", "Scully", "Jarrett", "Calhoun", "Rupert", "Kester", "Withrow", "Skinner", "Ashworth",
                   "Nutter", "Hoke", "Cornish", "Christ", "Grissom", "Edmondson", "Martinson", "Trapp", "Charlton",
                   "Masters", "Cooke", "Frank", "Wren", "Prescott", "Schofield", "Wofford", "Wiese", "Maher",
                   "Sandlin", "Goldman", "Wiley", "Bertrand", "Coble", "Demarco", "Wolff", "Woodall", "Dobbins",
                   "Loveless", "Levin", "Loomis", "Squires", "Willis", "Bunn", "Mccabe", "Strom", "Goldsmith", "Stack",
                   "Desmond", "Hogue", "Mccain", "Crowe", "Greenwald", "Higgs", "Schuster", "Foltz", "Nicholas",
                   "German", "Christian", "Wilde", "Hauck", "Schubert", "Kirkwood", "Forrest", "Farris",
                   "Vieira", "Strong", "Nowak", "Schwartz", "Upchurch", "Donahue", "Phipps", "Webber", "Stafford",
                   "Wenger", "Seay", "Haddock", "Mcgrew", "Betts", "Stoner", "Coyne", "Swearingen", "Angelo",
                   "Reid", "Page", "Duckett", "Free", "Hammonds", "Zook", "Jeffers", "Boyd", "Cullen", "Snow",
                   "Flanigan", "Dewitt", "Fontana", "Vaughan", "Frost", "Stutzman", "Talbott", "Humphries", "Doane",
                   "Driscoll", "Biggs", "Wiggins", "Cone", "Levi", "Knott", "Chappell", "Dudley", "Nagle", "Howe",
                   "Binder", "Ellsworth", "Lyman", "Shifflett", "Hallman", "Keefer", "Collier", "Slagle", "Staley",
                   "Burkhart", "Gorman", "Hitchcock", "Haddad", "Stpierre", "Burney", "Goodman", "Lister", "Devore",
                   "Oneil", "Canady", "Hebert", "Kearney", "Wisniewski", "Browne", "Smalley", "Johns", "Gaither",
                   "Weber", "Horst", "Rand", "Spencer", "Schlosser", "Dalrymple", "Gibbs", "Harry", "Silvers", "Abbott",
                   "Edmonds", "Sarver", "Wiles", "Buckley", "Rader", "Weidner", "Hennessey", "Jacob", "Homan",
                   "Mcclellan", "Haskins", "Mcfarlane", "Hardesty", "Noonan", "Waugh", "Curry", "Mark", "Knapp",
                   "Hickman", "Szabo", "Keeney", "Clayton", "Murray", "Herndon", "Gabel", "Harden", "Baer", "Beckwith",
                   "Looney", "Hamblin", "Stern", "Mcdaniel", "Raber", "Elam", "Mcadams", "Duvall", "Fries", "Coates",
                   "Wilder", "Dooley", "Sell", "Couch", "Heinz", "Crook", "Couture", "Maas", "Bunker", "Lewandowski",
                   "Giordano", "Maguire", "Hawk", "Budd", "Mariano", "Zimmerman", "Smallwood", "Abraham",
                   "Soper", "Henson", "Parrish", "Akin", "Dugger", "Sisk", "Lentz", "Hiller", "Timmons", "Freedman",
                   "Mccreary", "Mcfall", "Creel", "Comeaux", "Babcock", "Freund", "Simonson", "Lester", "Kopp",
                   "Soares", "Jensen", "Voigt", "Catalano", "Denton", "Coffey", "Finney", "Todd", "Haley", "Norris",
                   "Omalley", "Bauman", "Orr", "Maples", "Fike", "Hobbs", "Earle", "Ladner", "Hutchens", "Vaughn",
                   "Klinger", "Ulrich", "Guest", "Bullard", "Forbes", "Wilbanks", "Newland", "Kauffman", "Guthrie",
                   "Whitney", "Sharp", "Piatt", "Almond", "Bartels", "Wall", "Brent", "Brush", "Fairchild", "Berman",
                   "Mcnulty", "Langer", "Culp", "Milligan", "Behrens", "Dees", "Giles", "Ostrowski", "Morelli",
                   "Herman", "Freeland", "Volk", "Agee", "Spooner", "Mcintyre", "Teague", "Helms", "Raymond", "Daniels",
                   "Manson", "Hicks", "Addison", "Irons", "Newsom", "Sommers", "Spence", "Bowser", "Rapp", "Maynard",
                   "Mccullough", "Oakes", "Dowdy", "Manuel", "Battaglia", "Bean", "Padgett", "Shields", "Coy", "Getz",
                   "Ouellette", "Pruett", "Knudsen", "Webster", "Sheehan", "Kelso", "Danielson", "Moyer", "Ashcraft",
                   "Sparks", "Tremblay", "Nall", "Carvalho", "Grooms", "Decker", "Qualls", "Hudson", "Fulton", "Curran",
                   "Robbins", "Hollingsworth", "Danner", "Stratton", "Martino", "Dionne", "Garvey", "Saxon", "Gage",
                   "Busch", "Driggers", "Evangelista", "Rhoades", "Kearns", "Kohler", "Messina", "Mattingly", "Lemon",
                   "Welborn", "Branson", "Dugan", "Humphreys", "Betz", "Mcclung", "Tidwell", "Noble", "Damato",
                   "Connolly", "Braden", "Guffey", "Millar", "Clevenger", "Pierce", "Bergstrom", "Davies", "Austin",
                   "Burkholder", "Burkhardt", "Craft", "Hofmann", "Cary", "Price", "Mattison", "Darby", "Reinhardt",
                   "Parsons", "Epstein", "Starkey", "Flaherty", "Poirier", "Hendrix", "Harding", "Duncan", "Reese",
                   "Mcdougal", "Shuman", "Spivey", "Nichols", "Kelleher", "Dotson", "George", "Thorson", "Weis",
                   "Snodgrass", "Lowell", "Dillard", "Herring", "Sutter", "Fallon", "Marcum", "Castle", "Sterling",
                   "Bounds", "Wetzel", "Hutchinson", "Gingerich", "Oldham", "Fulmer", "Bradley", "Rees", "Galloway",
                   "Amundson", "Merriman", "Levy", "Chitwood", "Jewett", "Gallo", "Kirkpatrick", "Cruse", "Hinds",
                   "Hazen", "Rosenberg", "Jenson", "Caswell", "Burge", "Wagner", "Kaufman", "Latham", "Rosenbaum",
                   "Davison", "Girard", "Weaver", "Batchelor", "Hochstetler", "Clarke", "Allen", "Rudy", "Pfeiffer",
                   "Leahy", "Mcdonald", "Mchenry", "Lear", "Spradlin", "Bearden", "Napolitano", "Meadows", "Nolen",
                   "Cunningham", "Cameron", "Hammons", "Terry", "Ault", "Gentile", "Upton", "Foust", "Sturm",
                   "Sebastian", "Taggart", "Gardiner", "Daniel", "Conroy", "Stanford", "Brandt", "Hatch", "Trahan",
                   "Blythe", "Connelly", "Brant", "Champagne", "Nation", "Hylton", "Farnsworth", "Maness", "Huber",
                   "Richter", "Crisp", "Meister", "Frasier", "Evans", "Metz", "Easley", "Burchfield", "Parker",
                   "Michaels", "Tully", "Jacoby", "Dawson", "Spaulding", "Thurston", "Draper", "Randazzo", "Shelley",
                   "Caron", "Shafer", "Bender", "Neuman", "Dias", "Doty", "Atwell", "Carnahan", "Mcmanus", "Mayhew",
                   "Reiss", "Schramm", "Mazur", "Cousins", "Mullen", "Riddle", "Harwell", "Sayre", "Cochran", "Popp",
                   "Curley", "Lopes", "Breeden", "Maxey", "Burch", "Pence", "Bowman", "Finnegan", "Cheney", "Bateman",
                   "Crouse", "Block", "Lynn", "Wade", "Kuhns", "Osburn", "Krause", "Storey", "Suggs", "Leach",
                   "Levesque", "Jennings", "Martin", "Burns", "Jeffery", "Jolly", "Smith", "Rafferty", "Karl",
                   "Wilhelm", "Greenfield", "Vaught", "Lombardi", "Crowley", "Franz", "Stahl", "Tipton", "Dunn",
                   "Shultz", "Gunderson", "Kraemer", "Folsom", "Vines", "Coker", "Weimer", "Ralph", "Lawler", "Fortin",
                   "Obrien", "Morin", "Delaney", "Brill", "Matheson", "Gall", "Travis", "Conklin", "Freeman",
                   "Naylor", "Peeples", "Wallin", "Eubanks", "Covey", "Urban", "Hartman", "Dexter", "Oliver",
                   "Thrasher", "Russ", "Holden", "Coggins", "Yancey", "Cash", "Bouchard", "Robinson", "Christiansen",
                   "Zeller", "Godwin", "Durkin", "Helton", "Brown", "Kowalski", "Baumann", "Broome", "Garris",
                   "Kissinger", "Nickel", "Hammock", "Cole", "Dent", "Salmon", "Hester", "Luce", "Olsen", "Grace",
                   "Vernon", "Worden", "Woodard", "Malone", "Hood", "Pettit", "Ervin", "Forman", "Caruso", "Akins",
                   "Steed", "Hamrick", "Tillery", "Nail", "Fowler", "Bare", "Dobson", "Moody", "Leo", "Sykes", "Elder",
                   "Novak", "Massie", "Yager", "Demers", "Thiel", "Chapin", "Bartlett", "Mclendon", "Bobbitt", "Hook",
                   "Lindstrom", "Lockhart", "Dolan", "Baker", "Katz", "Goetz", "Frey", "Branch", "Patrick", 
                   "Kaye", "Shores", "Mcewen", "Vest", "Kirsch", "Lieberman", "Dupuis", "Lyle", "Waggoner", "Faulk",
                   "Pemberton", "Coe", "Sloan", "Hinton", "Mock", "Swenson", "Dykstra", "Strauss", "Coombs", "Darling",
                   "Mcfadden", "Derosa", "Hilton", "Clinton", "Dorman", "Smiley", "Jankowski", "Strunk", "Mccool",
                   "Bristow", "Dowling", "Dasilva", "Molnar", "Kinney", "Murry", "Kruse", "Pfaff", "Kunz", "Dyer",
                   "Harkins"]}

black_names = {
    "first_names": ["Chambliss", "Beason", "Harold", "Dortch", "Mccalla", "Eley", "Liggins", "Cuffee", "Tesfaye",
                    "Caruthers", "Bilal", "Sheriff", "Dorsett", "Kaylin", "Asia", "Savannah", "Ezekiel", "Ishmael",
                    "Lauren", "Joy", "Leah", "Fanta", "Hope", "Tyler", "Kayden", "Paige", "Tori", "Mohamed", "Ariyah",
                    "Jason", "Michael", "Taylor", "Elise", "Blake", "Stephen", "Maxwell", "Samiyah", "Ibrahima",
                    "Mohammed", "Aicha", "Ava", "Harper", "Dwayne", "Abdul", "Wynter", "Lily", "Empress", "Zaniyah",
                    "Kevin", "Jaxson", "Amara", "Jace", "Dream", "Deborah", "Kyle", "Samara", "Avery", "Xavier",
                    "Zamir", "Marc", "David", "Hayden", "Kennedi", "Jasiah", "Janiyah", "Myles", "Bryan", "Zahir",
                    "Ousmane", "Jada", "Legend", "Amina", "Alexis", "Lorenzo", "Kyrie", "James", "Jewel", "Jasmine",
                    "Nolan", "Tiana", "Isis", "Jalen", "Anaya", "Royce", "Samantha", "Nathan", "Precious",
                    "Payton", "Gianni", "Mariah", "Chelsea", "Trinity", "Timothy", "Anthony", "Noel", "Ezra", "Nala",
                    "Seth", "Harmony", "Gianna", "Kaylani", "Jayda", "Calvin", "Kamiyah", "Jared", "Phoenix", "Kymani",
                    "Egypt", "Sarah", "Ameer", "Jayla", "Ashley", "Evan", "Bryson", "Kristian", "Zhuri", "Aria",
                    "Terrell", "Bryce", "Sekou", "Esther", "Nigel", "Nova", "Heavenly", "Janiya", "Royalty",
                    "Eric", "Maison", "Jamir", "Aissata", "Amaya", "Messiah", "Kelsey", "Adonis",
                    "Sapphire", "Lucas", "Musa", "Arya", "Hailey", "Zuri", "Joel", "Tristan", "Amar'e", "Malaysia",
                    "Brian", "Amora", "Alijah", "Andrew", "Dominic", "Devin", "Jaheim", "Kimora", "William", "Jaxon",
                    "Maryam", "Kourtney", "Alvin", "Khadija", "Richard", "Sevyn", "Owen", "Kamari", "Gavin", "Amiyah",
                    "Antonio", "Hassan", "Abdoulaye", "Tamia", "Amirah", "Abdoul", "Zaiden", "Alani", "Jonas", "Skylar",
                    "Arielle", "Dominick", "Ella", "Isaac", "Amira", "Kenneth", "Derrick", "Makhi", "Maya", "Luke",
                    "Madison", "Amiya", "Henry", "Mckenzie", "Kaleb", "Gabriel", "Princess", "Madisyn", "Kyree",
                    "Jaylin", "Khalil", "Journey", "Sanaa", "Gregory", "Serenity", "Khloe", "Leon", "Amber", "Lamar",
                    "Dallas", "Zoey", "Mackenzie", "John", "Kenzo", "Micah", "Malachi", "Alpha", "Carmelo", "Nalani",
                    "Nathaniel", "Emmanuel", "Caiden", "Laila", "Aliyah", "Adrian", "Keith", "Carter", "Amani",
                    "Scarlett", "Olivia", "Jahmir", "Miracle", "Kennedy", "Angel", "Aurora", "Demi", "Azaria", "Zariah",
                    "Jaliyah", "Justin", "Omar", "Ariel", "Azariah", "Dakota", "Nana", "Milani", "Nicholas", "Robert",
                    "Kiara", "Christian", "Saint", "Aissatou", "Adrianna", "Zayden", "Amare", "Vanessa", "Ricardo",
                    "Paul", "Ethan", "Nadia", "Samuel", "Gabriella", "Stephanie", "Amia", "Lillian", "Hawa", "Brandon",
                    "Morgan", "Alana", "Janelle", "Sanai", "Ariella", "Shayla", "Zion", "Destiny", "Levi",
                    "Aden", "Mila", "Maliyah", "Camden", "Saige", "Mason", "Eden", "Alyssa", "Ahmed", "Steven", "Devon",
                    "Sophia", "Celine", "Judah", "Kadiatou", "Emmanuella", "Symphony", "Kai", "Christopher", "Kenzie",
                    "Lauryn", "Joshua", "Armani", "Jordyn", "Malia", "Kylee", "Edward", "Nicolas", "Soraya", "Amir",
                    "Mamadou", "Kamren", "Mouhamed", "Jacob", "Awa", "Mark", "Corey", "Isabella", "Thomas", "Londyn",
                    "Connor", "Khari", "Carson", "Rylee", "Imani", "Zane", "Nehemiah", "Megan", "Moussa", "Taliyah",
                    "Elijah", "Skyla", "Yara", "Elias", "Alexander", "Zachary", "Abraham", "Chloe", "Chanel", 
                    "Eliana", "Ace", "Raphael", "Karter", "Jamari", "Skyler", "Hunter", "Nazir", "Ashton",
                    "Adam", "Taraji", "Kameron", "Makenzie", "Kiyan", "Janae", "Jaden", "Natalia", "Erin", "Aubree",
                    "Shaniya", "Nahla", "Chace", "Mahamadou", "Zyaire", "Nasir", "Jesse", "Kaiden", "Jonah", "Sienna",
                    "Angelina", "Layla", "Cali", "Zora", "Nevaeh", "Skye", "Ariah", "Alexa", "Khaleesi", "Bailey",
                    "Jayceon", "Simone", "Nyla", "Damani", "Sarai", "Sariah", "Alicia", "Lailah", "Rebecca", "Jessica",
                    "Kristen", "Julian", "Charlotte", "Julius", "Essence", "Muhammad", "Brooklyn", "Addison",
                    "Nathanael", "Alexandra", "Naomi", "Sariyah", "Marley", "Brooke", "Oumar", "Aaron", "Shiloh",
                    "Summer", "Aniyah", "Maimouna", "Saniyah", "Jermaine", "Kaden", "Preston", "Isaiah", "Donovan",
                    "Jackson", "Winter", "Kori", "Terrence", "Aubrey", "Jaylen", "Quincy", "Talia", "Amari", "Genesis",
                    "Marquis", "Aboubacar", "Matthew", "Kaliyah", "Amayah", "Kali", "Dylan", "Liam", "Ayden",
                    "Austin", "Darren", "Nia", "Cheyenne", "Prince", "Grayson", "Isabelle", "Brayden", "Greyson",
                    "Aiden", "Nylah", "Tabitha", "Elizabeth", "Thierno", "Brianna", "Aminata", "George", "Giovanni",
                    "Emma", "Amadou", "Shawn", "Zoe", "Zendaya", "Lyric", "Julia", "Isiah", "Wyatt", "Amanda", "Damari",
                    "Tianna", "Milan", "Bradley", "Audrey", "Dior", "Natalie", "Orion", "Mariama", "Samiya",
                    "Kareem", "Cassidy", "Boubacar", "Melanie", "Leila", "Blessing", "Aaliyah", "Shania", "Danielle",
                    "Jaiden", "Kalani", "Cameron", "Ali", "Jeremiah", "Logan", "Maurice", "Riley", "Daniel",
                    "Jamar", "Brielle", "Justice", "Penelope", "Sebastian", "Alexandria", "Luna", "Ian", "Violet",
                    "Victor", "Darius", "Mya", "Cody", "Camren", "Eli", "Michelle", "Ryan", "Oumou", "Marcus", "Samir",
                    "Rachel", "Nailah", "Mekhi", "Zaire", "Jade", "Major", "Makai", "Zahara", "Aidan", "Ermias",
                    "Aniya", "Caleb", "Jayden", "Andre", "Kingston", "Rodney", "Roman", "Shane", "Mia", "Solomon",
                    "Asher", "Zaria", "Hannah", "Kailee", "Bria", "Abigail", "Arianna", "Sofia", "Mikayla", "Emani",
                    "Omari", "Camille", "Gia", "Chris", "Bella", "Saniya", "Sydney", "Zachariah", "Maximus", "Abrielle",
                    "Giselle", "Zainab", "Annabelle", "Jelani", "Kyro", "Kenya", "Kehlani", "Jamel", "Travis", "Ismael",
                    "Jonathan", "Bintou", "Sean", "Jordan", "Kylie", "Yusuf", "Kayla", "Gabrielle", "Kyla",
                    "Kairo", "Khadijah", "Ariana", "Fatoumata", "Emily", "Jabari", "Grace", "Victoria", "Jayce",
                    "Aisha", "Alex", "Joseph", "Fatou", "Josiah", "Sasha", "Benjamin", "Mariam", "Leo", "Chad", "Noah",
                    "Landon", "Autumn", "Peyton", "Reign", "Jayson", "Caden", "Makayla", "Patrick", "Princeton", "Zara",
                    "King", "Savion", "Charles", "Sade", "Amelia", "Troy", "Ibrahim", "Skylah", "Kaylee", "Athena",
                    "Christina", "Zahra", "Cayden", "Jamal", "Journee", "Melody", "Ayanna", "Leilani", "Heaven",
                    "Kendra", "Fatima", "Chase", "Malcolm", "Malik"],
    "last_names": ["Mimms", "Feaster", "Goodwyn", "Lofton", "Mckinnie", "Goldsby", "Govan", "Littlejohn", "Tookes",
                   "Mcgary", "Steptoe", "Drakes", "Marrow", "Danzy", "Yearby", "Kindred", "Upshaw", "Randle", "Abram",
                   "Oliphant", "Mcclean", "Guillaume", "Brewington", "Bowie", "Townsel", "Mohamud", "Waddy", "Fells",
                   "Wynter", "Luckett", "Beaubrun", "Sayles", "Prophet", "Swaby", "Dabney", "Myles", "Ba", "Leaks",
                   "Dacosta", "Mcmillian", "Napper", "Knighten", "Dunigan", "Saffold", "Carruthers", "Knighton",
                   "Purifoy", "Turay", "Woodhouse", "Alston", "Manns", "Olive", "Ulysse", "Fortson", "Olivier",
                   "Harvell", "Fludd", "Brim", "Ligon", "Phoenix", "Wimbush", "Brathwaite", "Dade", "Callender",
                   "Sills", "Brayboy", "Lightner", "Kamau", "Jimmerson", "Mcnair", "Varnado", "Dugas", "Georges",
                   "Brockington", "Opoku", "Spell", "Fenderson", "Balogun", "Jiles", "Reddick", "Purnell", "Saddler",
                   "Peavy", "Fulmore", "Devaughn", "Ofori", "Christmas", "Whitfield", "Hassan", "Deans", "Murph",
                   "Francois", "Dozier", "Camper", "Starks", "Coulibaly", "Garth", "Kates", "Threatt", "Mickle",
                   "Simmonds", "Gleaton", "Mcghee", "Pender", "Mitchem", "Augustus", "Ebanks", "Pegram", "Chinn",
                   "Zackery", "Desta", "Howze", "Beamon", "Peterkin", "Sealey", "Ceasar", "Marable", "Rhone",
                   "Kittrell", "Binion", "Cofer", "Eaddy", "Mcelveen", "Treadwell", "Nathaniel", "Bias", "Braggs",
                   "Emmanuel", "Okeke", "Gholston", "Agyemang", "Mumford", "Nabors", "Rascoe", "Hatten", "Mincey",
                   "Hagins", "Estime", "Tyus", "Horsey", "Mahone", "Crayton", "Braxton", "Lett", "Singletary",
                   "Lampkin", "Teasley", "Fant", "Nur", "Sharif", "Bufford", "Mcgruder", "Gethers", "Benbow", "Abner",
                   "Hagos", "Crumpton", "Granberry", "Ashford", "Rumph", "Sturgis", "Tekle", "Rideaux", "Seldon",
                   "Tart", "Barner", "Fenwick", "Ferdinand", "Powe", "Obryant", "Gerald", "Metoyer", "Amerson",
                   "Appling", "Rosemond", "Samuels", "Rochester", "Hamer", "Duplessis", "Pledger", "Paschal", "Bester",
                   "Mcneal", "Flakes", "Edward", "Claxton", "Tharpe", "Word", "Leake", "Leverett", "Mccrea", "Spells",
                   "Batiste", "Woodson", "Twitty", "Toombs", "Jerry", "Bridgewater", "Lathan", "Conyers", "Louissaint",
                   "Rembert", "Warsame", "Rome", "Desir", "Woolfolk", "Pitre", "Forney", "Sonnier", "Hughley",
                   "Eskridge", "Lamour", "Leftwich", "Ollison", "Vasser", "Ester", "Scales", "Trice", "Cheeks",
                   "Tolson", "Feagin", "Leflore", "Fowlkes", "Tolliver", "Stribling", "Gowdy", "Boney", "Pridgen",
                   "Nero", "Jemison", "Cesar", "Dew", "Haynie", "Hagler", "Bannerman", "Colston", "Meekins", "Abdalla",
                   "Destin", "Okoye", "Tutt", "Mcclary", "Armstead", "Battiste", "Hogans", "Cureton", "Shephard",
                   "Silas", "Glaze", "Kaba", "Broomfield", "Gillum", "Seabrook", "Blanding", "Dunston", "Mallard",
                   "Boler", "Gaye", "Choice", "Pete", "Strozier", "Torain", "Aikens", "Pinnock", "Duren", "Halliburton",
                   "Grimsley", "Kanu", "Ellerbe", "Raiford", "Footman", "Staten", "Askew", "Capers", "Caffey",
                   "Eddings", "Kizer", "Stfleur", "Mccollough", "Karim", "Blackshear", "Headen", "Chatman",
                   "Desrosiers", "Fortenberry", "Hughey", "Gumbs", "Brickhouse", "Milan", "Gourdine", "Engram", "Lubin",
                   "Sumler", "Pettway", "Funchess", "Criss", "Seawright", "Speaks", "Grier", "Abercrombie", "Caine",
                   "Hilaire", "Roquemore", "Squire", "Scaife", "Carothers", "Mckoy", "Dixson", "Larkins", "Bruton",
                   "Hadnot", "Blakes", "Noor", "Stoudemire", "Kornegay", "Hurdle", "Hoard", "Donnell", "Adjei",
                   "Revels", "Parchment", "Peake", "Sawyers", "Glasper", "Rosier", "Rooks", "Harvin", "Prosper",
                   "Calloway", "Gaillard", "Moncrief", "Kellam", "Dendy", "Barnwell", "Benford", "Dones", "Springfield",
                   "Tarpley", "Demps", "Seales", "Roebuck", "Caston", "Zanders", "Jama", "Crossley", "Antoine",
                   "Crumbley", "Napoleon", "Hassell", "Sesay", "Nickson", "Sthilaire", "Blakeney", "Barksdale",
                   "Crudup", "Bethea", "Peoples", "Portis", "Westley", "Joseph", "Turnage", "Pipkins", "Keita",
                   "Auguste", "Hamlett", "Asare", "Dossantos", "Lomax", "Coney", "Osei", "Harewood", "Lauderdale",
                   "Desouza", "Holbert", "Spates", "Ogletree", "Gayle", "Hibbert", "Stlouis", "Knuckles", "Cooks",
                   "Gaspard", "Boulware", "Altidor", "Bynoe", "Casseus", "Gelin", "Antwi", "Roane", "Harrigan",
                   "Bozeman", "Burrage", "Joubert", "Rene", "Braziel", "Mohamed", "Boozer", "Broadnax", 
                   "Exantus", "Tynes", "Beckford", "Streater", "Pearsall", "Fears", "Abdi", "Owusu", "Dieujuste",
                   "Lark", "Hewlett", "Jessie", "Bobb", "Vaughns", "Croom", "Yancy", "Marc", "Merriweather", "Sidney",
                   "Spikes", "Kimber", "Weekes", "Fluker", "Jarmon", "Alexis", "Richburg", "Kamara", "Ruffin", "Bembry",
                   "Somerville", "Swinson", "Barthelemy", "Primus", "Koger", "Millender", "Getachew", "Bolling",
                   "Virgil", "Paulk", "Cobbs", "Abdullah", "Prejean", "Colter", "Salomon", "Satchell", "Steverson",
                   "Holliman", "Horsley", "Odum", "Brigham", "Cousin", "Galbreath", "Durr", "Gadsden", "Mcbean",
                   "Heard", "Enoch", "Fobbs", "Granderson", "Duhon", "Stampley", "Caraway", "Quarles",
                   "Holness", "Musa", "Spinks", "Stanback", "Hickmon", "Hedgepeth", "Pankey", "Haughton", "Suber",
                   "Belizaire", "Chisolm", "Saintil", "Assefa", "Hepburn", "Hunte", "Mikell", "Bouldin", "Avant",
                   "Wilmore", "Culbreath", "Adebayo", "Mcclendon", "Flemming", "Scriven", "Searles", "Alphonse",
                   "Tanksley", "Morant", "Breland", "Millen", "Nembhard", "Elmi", "Phillip", "Mcfarlin", "Mouzon",
                   "Talton", "Tellis", "Ivery", "Mccrae", "Lindo", "Banner", "Darden", "Myrie", "Dejean", "Traore",
                   "Mckie", "Kimbrough", "Bethune", "Bettis", "Hardaway", "Maxie", "Woodland", "Longmire", "Hankerson",
                   "Corbitt", "Tyner", "Suttles", "Fofana", "Guilford", "Ladson", "Diggs", "Gant", "Scarlett",
                   "Goodridge", "Saintlouis", "Moten", "Pernell", "Ghee", "Lawhorn", "Farquharson", "Burse", "Peeler",
                   "Surratt", "Garmon", "Leday", "Orange", "Moorer", "Lattimore", "Cargill", "Cottman", "Pough",
                   "Laing", "Lockett", "Macon", "Pinder", "Vital", "Gwynn", "Copper", "Urquhart", "Chalmers", "Gaynor",
                   "Swinton", "Booker", "Peppers", "Saintfleur", "Celestine", "Stjean", "Wiltshire", "Eady", "Thrower",
                   "Goree", "Salley", "Tulloch", "Core", "Outlaw", "Tims", "Judkins", "Joshua", "Winbush", "Profit",
                   "Earls", "Hypolite", "Holsey", "Yeboah", "Sumter", "Groce", "Jeanjacques", "Maiden",
                   "Jamerson", "Bonaparte", "Clinkscales", "Hagood", "Bolden", "Gallman", "Casimir", "Minnis",
                   "Edmunds", "Blassingame", "Dilworth", "Faustin", "Munford", "Jeanbaptiste", "Kassa", "Celestin",
                   "Zachary", "Toussaint", "Fulcher", "Chevalier", "Diallo", "Ollie", "Raphael", "Kennard", "Latimore",
                   "Doctor", "Baskerville", "Tribble", "Toomer", "Sauls", "Funches", "Youmans", "Spruill", "Griffen",
                   "Lampkins", "Jules", "Tilghman", "Williams", "Emory", "Cauley", "Sabb", "Stackhouse", "Bellard",
                   "Gustave", "Westbrooks", "Doucet", "Brister", "Nickens", "Hairston", "Jeanphilippe", "Wadley",
                   "Grate", "Gilmer", "Wash", "Gambrell", "Mims", "Mallett", "Innocent", "Muhammad", "Mouton",
                   "Zachery", "Moye", "Nowell", "Quarterman", "Monteiro", "Humes", "Jackson", "Plowden", "Cisse",
                   "Furlow", "Lucien", "Lyles", "Salters", "Rasberry", "Lamothe", "Dangerfield", "Pye", "Yearwood",
                   "Goines", "Ferebee", "Bluford", "Wardlaw", "Windom", "Pounds", "Grisby", "Kearse", "Clayborne",
                   "Carmouche", "Leverette", "Witcher", "Gause", "Porterfield", "Lampley", "Baptist", "Peay",
                   "Elie", "Gladney", "Shoulders", "Downer", "Veasley", "Citizen", "Cauthen", "Byron", "Pouncy",
                   "Coachman", "Sumlin", "Edmond", "Romain", "Dancy", "Wilbert", "Bah", "Facey", "Whigham", "Rufus",
                   "Frierson", "Mondesir", "Mccray", "Boxley", "Carty", "Dunson", "Stepney", "Loggins", "Ceesay",
                   "Zeno", "Hollins", "Bickham", "Hardeman", "Cotten", "Mcadoo", "Ndiaye", "Goodlow", "Batts",
                   "Mcswain", "Wellington", "Denson", "Watlington", "Priester", "Chiles", "Edison", "Gravely",
                   "Horace", "Kindle", "Dismuke", "Philip", "Bacchus", "Mingo", "Pinkard", "Mangrum", "Mickles",
                   "Mazyck", "Gatson", "Eaglin", "Toliver", "Alemu", "Melson", "Keels", "Denis", "Goggins", "Regis",
                   "Belgrave", "Palmore", "Kargbo", "Claiborne", "Mustafa", "Bashir", "Cooksey", "Victorian", "Bent",
                   "Mensah", "Boutte", "Belton", "Hargett", "Adeyemi", "Tunstall", "Yusuf", "Gayles", "Foxworth",
                   "Njoroge", "Pierre", "Peele", "Maynor", "Munroe", "Maina", "Penson", "Loftin", "Gaymon", "Wesley",
                   "Berhe", "Board", "Mcbeth", "Ebron", "Twyman", "Buford", "Bey", "Lakes", "Flournoy", "Warrick",
                   "Farah", "Render", "Ricks", "Hemingway", "Ealy", "Holifield", "Hardrick", "Spraggins", "Macklin",
                   "Laurent", "Finklea", "Partee", "Brutus", "Burrus", "Applewhite", "Mccrimmon", "Mcphail", "Mckinzie",
                   "Mosely", "Narcisse", "Troupe", "Biggers", "Days", "Deshields", "Vanburen", "Hartfield",
                   "Caver", "Wigfall", "Riles", "Mebane", "Gallimore", "Stallworth", "Baylor", "Pettaway", "Deloatch",
                   "Watley", "Paige", "Roney", "Jason", "Welcome", "Nwankwo", "Foxx", "Blanks", "Stennis", "Goods",
                   "Barrie", "Swanigan", "Gammage", "Dandridge", "Amey", "Gilkey", "Fordham", "Hollowell", "Armand",
                   "Mack", "Delk", "Moton", "Birdsong", "Mcmiller", "Erving", "Mayers", "Artis", "Stenson", "Pelzer",
                   "Reliford", "Jeanlouis", "Boykin", "Holloman", "Bridgeforth", "Mickens", "Lafrance", "Spann",
                   "Royster", "Philippe", "Worthy", "Benn", "Rankins", "Rountree", "Bekele", "Granville", "Addo",
                   "Sain", "Tull", "Blakley", "Bracy", "Rabb", "Gholson", "Kitt", "Debose", "Cuyler", "Belk",
                   "Dominique", "Chenault", "Henton", "Mccutchen", "Rockett", "Hinnant", "Brewton", "Deloney", "Mapp",
                   "Essex", "Mayweather", "Negash", "Baltimore", "William", "Bost", "Mcelrath", "Chery", "Rorie",
                   "Hickerson", "Stringfellow", "Crittendon", "Haji", "Mckissick", "Rone", "Jeanty", "Speller",
                   "Cofield", "Leath", "Bunton", "Foye", "Pascal", "Richie", "Goosby", "Sow", "Southall", "Ousley",
                   "Shorter", "Rutland", "Dublin", "Prophete", "Broom", "Grissett", "Roseboro", "Melancon", "Geter",
                   "Marcelin", "Constant", "Beyene", "Latson", "Ceaser", "Mclin", "Kennon", "Phifer",
                   "Bolds", "Jasmin", "Lafayette", "Catchings", "Singleton", "Cottingham", "Metayer", "Depina",
                   "Ardoin", "Spiller", "Totten", "Moultrie", "Godbolt", "Keitt", "Conwell", "Vassell", "Omar",
                   "Everette", "Daughtry", "Rashid", "Rivers", "Norfleet", "Trawick", "Ewell", "Acheampong", "Heron",
                   "Severe", "Legette", "Janvier", "Haye", "Mcnealy", "Surles", "Bartee", "Drayton", "Maclin",
                   "Yohannes", "Beauford", "Ransome", "Kershaw", "Nwosu", "Mccullum", "Kenner", "Guerrier", "Aden",
                   "Acklin", "Fielder", "Rhoden", "Winston", "Ravenell", "Porch", "Alleyne", "Adan", "Toles",
                   "Abdullahi", "Golston", "Jelks", "Riddick", "Mines", "Faison", "Lesane", "Magwood", "Millner",
                   "Cumberbatch", "Buggs", "Thiam", "Hartsfield", "Jeune", "Speight", "Frimpong", "Muldrow", "Gainer",
                   "Gallon", "Dewberry", "Patillo", "Goodrum", "Mcmillon", "Abebe", "Hussein", "Shavers", "Barham",
                   "Rozier", "Colquitt", "Buie", "Haywood", "Jordon", "Malveaux", "Swint", "Mike", "Triggs", "Charity",
                   "Flemings", "Haile", "Mciver", "Denmark", "Ivory", "Belser", "Coward", "Forest", "Doby", "Lipsey",
                   "Arceneaux", "Wingfield", "Mansaray", "Bellinger", "Mwangi", "Lillard", "Kimani", "Eugene",
                   "Lockridge", "Drakeford", "Hollie", "Coles", "Barefield", "Ducksworth", "Etienne", "Rounds", "Herd",
                   "Gilyard", "Mccants", "Mclaurin", "Luckey", "Nowlin", "Pryce", "Boddie", "Coaxum", "Gordan",
                   "Asamoah", "Strachan", "Ledet", "Majette", "Mccowan", "Garnes", "Shumpert", "Brisco", "Winfield",
                   "Pitchford", "Wiltz", "Spearman", "Woolridge", "Stitt", "Koonce", "Tarver", "Nevels", "Bivins",
                   "Barley", "Esters", "Sealy", "Forde", "Mcclinton", "Toure", "Sangster", "Marcellus",
                   "Pipkin", "Kebede", "Cadet", "Postell", "Matthew", "Windley", "Hymes", "Senegal", "Fearon",
                   "Medlock", "Ginyard", "Boykins", "Baines", "Bowe", "Nunnally", "Ismail", "Thompkins", "Winder",
                   "Coston", "Jeancharles", "Mathieu", "Lockley", "Tabron", "Gatling", "Gooden", "Edgerton", "Square",
                   "Parham", "Whetstone", "Burrell", "Purdie", "Gittens", "Gathers", "Elston", "Pullins", "Straughter",
                   "Bing", "Simien", "Appiah", "Walcott", "Mekonnen", "Dicks", "Fitts", "Bacote", "Bouie", "Sandy",
                   "Berhane", "Hardiman", "Glasco", "Turnipseed", "Mackie", "Goudeau", "Rasheed", "Drown",
                   "Showers", "Donelson", "Fauntleroy", "Hector", "Milliner", "Bibb", "Frink", "Maurice", "Wesson",
                   "Filsaime", "Metellus", "Dewalt", "Goodloe", "Nalls", "Witherspoon", "Sturdivant",
                   "Boatman", "Wilbourn", "Kone", "Odoms", "Session", "Dedeaux", "Lacour", "Inniss", "January",
                   "Jeanfrancois", "Eberhart", "Rawlins", "Shackleford", "Kinnard", "Honore", "Hickson", "Tuggle",
                   "Salaam", "Hibbler", "Bowens", "Koroma", "Caines", "Gardener", "Deberry", "Rachal", "Dennard",
                   "Funderburk", "Brevard", "Mcdougle", "Sankey", "Dorsey", "Chapple", "Wortham", "Beacham", "Dargan",
                   "Sheard", "Pass", "Copes", "Giddings", "Hatter", "Venson", "Liddell", "Pinckney", "Thaxton", "Dash",
                   "Castille", "Thurmond", "Fall", "Jean", "Osby", "Epps", "Ryals", "Gadson", "Swindell", "Dingle",
                   "Alexandre", "Saulsberry", "Seabrooks", "Scipio", "Alex", "Felder", "Becton", "Bienaime", "Prude",
                   "Weeden", "Dawes", "Crew", "Taplin", "Thrash", "Fredrick", "Swinney", "Cousar", "Towns", "Asberry",
                   "Anyanwu", "Wilborn", "Brodie", "Middlebrook", "Weatherspoon", "Exum", "Weary", "Blue", "Wisdom",
                   "Whitsett", "Atwater", "Wilford", "Shears", "Ramseur", "Mcmillion", "Ned", "Luster", "Levingston",
                   "Binns", "Sledge", "Sorrells", "Pinkney", "Osbourne", "Josey", "Waldon", "Stowers", "Stroman",
                   "Townes", "Seck", "Bynum", "Mccaskill", "Mcdougald", "Belle", "Ballentine", "Sistrunk", "Poteat",
                   "Booze", "Gueye", "Kyles", "Burkhalter", "Asfaw", "Grandberry", "Albritton", "Veney", "Mohammed",
                   "Mcmorris", "Gales", "Ranson", "Billups", "Nedd", "Mcduffie", "Durden", "Sessoms", "Pompey",
                   "Beckles", "Mars", "Taliaferro", "Claude", "Ojo", "Puryear", "Glaspie", "Morman", "Polk", "Golding",
                   "Pleasant", "Garrick", "Wimbley", "Yarborough", "Crooms", "Hyppolite", "Gilliard", "Primm", "Kellum",
                   "Pegues", "Chappelle", "Byas", "Mitchel", "Boateng", "Maple", "Womble", "Goldston",
                   "Summerville", "Standifer", "Bastien", "Gist", "Cobbins", "Ryans", "Coffee", "Mcilwain", "Cowans",
                   "Bogle", "Rochelle", "Lenoir", "Threadgill", "Jimerson", "Banton", "Demby", "Sydnor", "Futrell",
                   "Braithwaite", "Hazzard", "Wilcher", "Peart", "Larry", "Hillard", "Blaise", "Cromartie", "Eiland",
                   "Moise", "Pride", "Hailu", "Ussery", "Broadway", "Dantzler", "Goings", "Flagg", "Leathers", "Cozart",
                   "Boakye", "Nicks", "Sandifer", "Greaves", "Heyward", "Baynes", "Hardnett", "Legrand", "Gayden",
                   "Sharper", "Byars", "Bazemore", "Nesbit", "Washington", "Seymore", "Broadus", "Pettiford", "Percy",
                   "Guice", "Asante", "Burkes", "Sherrod", "Edmonson", "Elamin", "Philpot", "Ancrum", "Roundtree",
                   "Shivers", "Jessup", "Hilson", "Roscoe", "Conerly", "Emanuel", "Torrence", "Browder", "Sarpong",
                   "Mceachin", "Prioleau", "Scurry", "Kinchen", "Daye", "Nwachukwu", "Guyton", "Passmore", "Caesar",
                   "Weathersby", "Bellamy", "Erby", "Pires", "Frison", "Cephas", "Stukes", "Waring", "Bazile", "Jeter",
                   "Menefee", "Nurse", "Murchison", "Arline", "Wint", "Jefferies", "Petithomme", "Wingo", "Burwell",
                   "Okonkwo", "Dawkins", "Boose", "Samuel", "Mccree", "Sheikh", "Ben", "Shanklin", "Watford", "Berkley",
                   "Tillis", "Bridgeman", "Ringgold", "Truesdale", "Shorts", "Drain", "Charlot", "Walston", "Custis",
                   "Crittenden", "Chaplin", "Stancil", "Cannady", "Sellars", "Wormley", "Tillman", "Abraha", "Draughn",
                   "Highsmith", "Turman", "Polite", "Tessema", "Blakemore", "Ajayi", "Hagans", "Carraway", "Augustin",
                   "Ealey", "Lawal", "Woodley", "Okoro", "Glanton", "Dorris", "Gaines", "Junior", "Laguerre", "Philips",
                   "Braham", "Golson", "Chatmon", "Lagrone", "Tabb", "Bonds", "Osman", "Njoku", "Rayford", "Veal",
                   "Mosby", "Dunmore", "Bynes", "Carrington", "Theodore", "Grays", "Blow", "Gillard", "Blanc",
                   "Hutcherson", "Staggers", "Browner", "Goodall", "Fonville", "Okafor", "Drummer", "Abron", "Jeudy",
                   "Jefferson", "Dowdell", "Stith", "Delva", "Carswell", "Lipford", "Calixte", "Bracey", "Runnels",
                   "Greenidge", "Simeon", "Cuthbertson", "Diggins", "Kidane", "Winfrey", "Skeete", "Settles",
                   "Fluellen", "Stjulien", "Maye", "Northington", "Massenburg", "Louis", "Dinkins", "Weatherly",
                   "Nealy", "Chavers", "Pharr", "Bangura", "Worthen", "Dorvil", "Bizzell", "Spratt", "Manigault",
                   "Lumpkins", "Blunt", "Grundy", "Boynton", "Emile", "Broady", "Slaton", "Charleston", "Styles",
                   "Shuford", "Speights", "Bonsu", "Eddins", "Blackshire", "Mathurin", "Dunkley", "Semien",
                   "Jalloh", "Clyburn", "Mcduffy", "Avent", "Hervey", "Aubrey", "Woodberry", "Rucker", "Bagby", "Leak",
                   "Dansby", "Duhart", "Carmon", "Pasley", "Alfred", "Spratley", "Wafer", "Blaine", "Mcgriff",
                   "Culberson", "Edouard", "Remy", "Smalls", "Archie", "Timberlake", "Lenard", "Obi", "Grayer", "Dear",
                   "Crutcher", "Pettus", "Brookins", "Shropshire", "Petit", "Blakney", "Tarrant", "Belin", "Hambrick",
                   "Petitfrere", "Cullins", "Fudge", "Hosey", "Dews", "Trotman", "Middlebrooks", "Volcy", "Springs",
                   "Wideman", "Favors", "Sy", "Blakey", "Tadesse", "Holston", "Shabazz", "Sanon", "Grandison", "Ragin",
                   "Davie", "Pippins", "Waites", "Hoskin", "Peete", "Leavell", "Rodney", "Slay", "Mosley", "Demery",
                   "Braddy", "Bookman", "Satterwhite", "Diop", "Deas", "Kirksey", "Moorehead", "Banks", "Rolle",
                   "Cyrus", "Haggins", "Haygood", "Littles", "Kendricks", "Conteh", "Woodford", "Bibbs", "Fullwood",
                   "Marbury", "Vereen", "Babineaux", "Mullings", "Fairley", "Sylla", "Whitted", "Pirtle",
                   "Shine", "El", "Hearns", "Jeanpierre", "Clardy", "Otey", "Canty", "Woodfork", "Dukes",
                   "Cosey", "Sylvain", "Baptiste", "Ambroise", "Clayborn", "Julien", "Lashley", "Lesure", "Chavis",
                   "Cephus", "Tolbert", "Wyche", "Newson", "Bankhead", "Willie", "Rhymes", "Theus", "Eatmon", "Coakley",
                   "Charles", "Breckenridge", "Voltaire", "Renfroe", "Senior", "Pilgrim", "Hatchett", "Hamlet",
                   "Hazelwood", "Husband", "Pierrelouis"]}

hispanic_names = {
    "first_names": ["Llano", "Ignacio", "Illescas", "Gimenez", "Maravilla", "Siordia", "Vives", "Olivero", "Rocha",
                    "Tlatelpa", "Zuleta", "Tenesaca", "Moralez", "Limon", "Alvizo", "Kaylin", "Emil", "Franklin",
                    "Isaias", "Annalise", "Jeremy", "Savannah", "Ezekiel", "Kate", "Montserrat", "Lauren", "Alexia",
                    "Miah", "Eva", "Kaitlyn", "Leah", "Zabdiel", "Cristopher", "Brayan", "Kayden", "Kayleigh",
                    "Julissa", "Tyler", "Crystal", "Cristian", "Paige", "Paola", "Jason", "Michael", "Taylor", "Bruno",
                    "Fernanda", "Blake", "Stephen", "Maxwell", "Alonso", "Emmy", "Ariadna", "Ean", "Lianna", "Liah",
                    "Stacy", "Amelie", "Ava", "Denise", "Liliana", "Lily", "Jessie", "Rosemary", "Valerie", "Carlos",
                    "Alina", "Kevin", "Jaxson", "Aimee", "Jace", "Amara", "Deborah", "Tiffany", "Kyle", "Annie",
                    "Cristina", "Samara", "Wendy", "Avery", "Viviana", "Sabrina", "Xavier", "Marc", "David", "Issac",
                    "Jasiah", "Evelyn", "Bruce", "Leanna", "Hazel", "Lian", "Myles", "Bryan", "Alan", "Nathaly", "Jada",
                    "Lorenzo", "Alexis", "Amina", "Legend", "Gael", "Kyrie", "James", "Eileen", "Jasmine", "Arabella",
                    "Nolan", "Tiana", "Savanna", "Jocelyn", "Isis", "Marco", "Anaya", "Royce", "Rafael", "Samantha",
                    "Jencarlos", "Nathan", "Elian", "Hayley", "Derick", "Eliza", "Gianni", "Mariah", "Aitana",
                    "Chelsea", "Trinity", "Timothy", "Anthony", "Noel", "Ezra", "Johan", "Seth", "Alba", "Harmony",
                    "Gianna", "Kaylani", "Jayda", "Kamila", "Jared", "Max", "Phoenix", "Dayana", "Elvin", "Sarah",
                    "Jayla", "Kaylie", "Ashley", "Stacey", "Bryson", "Evan", "Erik", "Aria", "Claire", "Daniela",
                    "Eddy", "Bryce", "Santiago", "Lizbeth", "Esther", "Nova", "Kailey", "Perla", "Eric", "Allan",
                    "Xander", "Maison", "Celeste", "Leslie", "Amaya", "Messiah", "Joziah", "Kelsey", "Jaslyn", 
                    "Adonis", "Vincent", "Lucas", "Karina", "Estrella", "Hailey", "Lukas", "Zuri", "Joel", "Arya",
                    "Yael", "Tristan", "Valentina", "Brian", "Kayson", "Andrew", "Dominic", "Lesly", "Devin",
                    "Maximiliano", "Nancy", "Larry", "William", "Jaxon", "Aileen", "Alvin", "Richard", "Galilea",
                    "Marjorie", "Owen", "Gavin", "Elliot", "Amalia", "Dariel", "Antonio", "Katelynn", "Luciana",
                    "Kimberly", "Helen", "Maximilian", "Amirah", "Juliette", "Anahi", "Angelique", "Samira", "Daphne",
                    "Diana", "Alani", "Luz", "Skylar", "Jonas", "Alaina", "Brenda", "Arielle", "Yaniel", "Dominick",
                    "Ella", "Lyanna", "Charlie", "Elliana", "Jaylee", "Isaac", "Natasha", "Amira", "Gerardo", "Kenneth",
                    "Maya", "Romeo", "Luke", "Madison", "Henry", "Alissa", "Mckenzie", "Guadalupe", "Kaleb", "Andres",
                    "Alondra", "Randy", "Keyla", "Iker", "Gabriel", "Jariel", "Shirley", "Irene", "Jaylin", "Sherlyn",
                    "Arian", "Geraldine", "Emilio", "Zayn", "Alejandra", "Arturo", "Gregory", "Serenity", "Armando",
                    "Damian", "Khloe", "Leon", "Marisol", "Amber", "Kailyn", "Laura", "Jaziel", "Eliel", "Monica",
                    "Jahir", "Zoey", "Mackenzie", "John", "Jaylyn", "Dilan", "Alessia", "Noemi", "Micah", "Emanuel",
                    "Danny", "Heidi", "Carmelo", "Nathaniel", "Leilany", "Emmanuel", "Delilah", "Caiden", "Laila",
                    "Aliyah", "Mariana", "Adrian", "Gabriela", "Jasmin", "Aldo", "Cassandra", "Denisse", "Miracle",
                    "Camila", "Scarlett", "Olivia", "Roger", "Yamilet", "Alejandro", "Carter", "Angel", "Felipe",
                    "Aurora", "Frank", "Hailie", "Ronaldo", "Bianca", "Mayson", "Jaliyah", "Sara", "Amberly", "Jazmine",
                    "Renata", "Justin", "Felix", "Omar", "Selena", "Miguel", "Alaia", "Ariel", "Mateo", "Rihanna",
                    "Jayleen", "Johnny", "Nashla", "Danna", "Ruth", "Milani", "Jayren", "Nicholas", "Lionel", "Saul",
                    "Robert", "Nayla", "Kiara", "Christian", "Adrianna", "Zayden", "Carla", "Anabelle", "Pablo",
                    "Tatiana", "Vanessa", "Ricardo", "Diego", "Paul", "Ethan", "Nadia", "Adeline", "Cindy", "Angelica",
                    "Jaslene", "Madelyn", "Stephanie", "Emilia", "Magaly", "Samuel", "Lenny", "Gabriella", "Elisa",
                    "Lillian", "Briana", "Angelo", "Yair", "Brandon", "Alana", "Marlon", "Melvin", "Januel", "Ariella",
                    "Janelle", "Shayla", "Ivanna", "Jordi", "Zion", "Raul", "Denzel", "Levi", "Cecilia",
                    "Aden", "Mila", "Jimena", "Antonella", "Nina", "Destiny", "Abby", "Mason", "Valery", "Zaid",
                    "Miriam", "Liana", "Matteo", "Jaycob", "Keily", "Alyssa", "Daleyza", "Adan", "Joaquin", "Scarlet",
                    "Sadie", "Steven", "Sophia", "Celine", "Sergio", "Kai", "Christopher", "Roselyn", "Javier", "Julie",
                    "Peter", "Cataleya", "Joshua", "Armani", "Sarahi", "Anabel", "Luca", "Malia", "Meghan", "Fabian",
                    "Pamela", "Kylee", "Edward", "Nicolas", "Francesca", "Amir", "Kayleen", "Heidy", "Jacob", "Amaia",
                    "Jonael", "Junior", "Yamileth", "Mark", "Gerard", "Arely", "Karla", "Giovanny", "Isabella",
                    "Cristofer", "Thomas", "Adalynn", "Londyn", "Melina", "Connor", "Nataly", "Andrea", "Salome",
                    "Imani", "Luis", "Rylee", "Angeline", "Dara", "Stella", "Megan", "Jerry", "Theodore", "Elijah",
                    "Alberto", "Aleena", "Skyla", "Elias", "Janiel", "Yariel", "Alexander", "Elena", "Leyla",
                    "Leonidas", "Anabella", "Zachary", "Abraham", "Mike", "Harley", "Chloe", "Mauricio", "Josue",
                    "Chanel", "Josephine", "Cairo", "Haylee", "Alfredo", "Carolina", "Eliana", "Ace", "Jose", "Karter",
                    "Damien", "Angely", "Violeta", "Ashton", "Roberto", "Skyler", "Hunter", "Jazzlyn", "Adam", "Darwin",
                    "Adelyn", "Jefferson", "Aylin", "Axel", "Carmen", "Dulce", "Yandel", "Melissa", "Catherine",
                    "Sophie", "Jaden", "Natalia", "Johanna", "Haley", "Kailani", "Micaela", "Itzel", "Aubree", "Enzo",
                    "Giovani", "April", "Milagros", "Mathew", "Jesse", "Louis", "Mario", "Ximena", "Kaiden", "Jonah",
                    "Sienna", "Jimmy", "Cynthia", "Angelina", "Jaime", "Juan", "Layla", "Enrique", "Cali", "Derek",
                    "Paula", "Isabel", "Nevaeh", "Cesar", "Juliana", "Eddie", "Wilson", "Juliet", "Ariah", "Khaleesi",
                    "Alexa", "Eliam", "Jayceon", "Nyla", "Arianny", "Sarai", "Sariah", "Alicia", "Clara", "Rebecca",
                    "Ronald", "Miley", "Daniella", "Nicole", "Raymond", "Jessica", "Charlotte", "Julian", "Melany",
                    "Julius", "Dante", "Katie", "Nathanael", "Addison", "Alexandra", "Naomi", "Misael", "Esteban",
                    "Monserrat", "Brooke", "Lucia", "Edwin", "Aaron", "Julianna", "Manuel", "Summer", "Edgar", "Aniyah",
                    "Oscar", "Yasmin", "Marcos", "Ayla", "Maite", "Nelson", "Kaden", "Preston", "Isaiah", "Marcelo",
                    "Ariadne", "Pedro", "Donovan", "Briella", "Jackson", "Yahir", "Neymar", "Emiliano", "Anderson",
                    "Priscilla", "Marvin", "Arlette", "Aubrey", "Ruben", "Andy", "Jaylen", " olivia", "Amari",
                    "Genesis", "Katelyn", "Matthew", "Daisy", "Jamie", "Albert", "Amayah", "Fernando", "Kali",
                    "Dylan", "Rose", "Liam", "Dana", "Erika", "Austin", "Kelvin", "Harrison", "Ayden", "Madeline",
                    "Nia", "Isabella ", "Anastasia", "Angela", "Prince", "Alyson", "Britney", "Grayson", "Evangeline",
                    "Iris", "Isabelle", "Lennox", "Brayden", "Greyson", "Anna", "Alma", "Milo", "Nashley", "Aiden",
                    "Nashly", "Nylah", "Elizabeth", "Adriana", "Everly", "Brianna", "Allison", "Ezequiel", "George",
                    "Giovanni", "Emma", "Shawn", "Bethany", "Jazmin", "Zoe", "Zander", "Elianna", "Nayeli", "Kenny",
                    "Lizeth", "Kassandra", "Camilo", "Francisco", "Julia", "Kelly", "Steve", "Miranda", "Freddy",
                    "Arleth", "Alia", "Amanda", "Analia", "Caroline", "Alessandra", "Milan", "Nyah", "Veronica",
                    "Bradley", "Jaelynn", "Adele", "Byron", "Litzy", "Valentin", "Mathias", "Audrey", "Keila", "Jorge",
                    "Jeffrey", "Mikaela", "Johnathan", "Ellie", "Natalie", "Ayleen", "Maia", "Dahlia", "Vivian",
                    "Isabela", "Orion", "Moises", "Faith", "Hanley", "Annabella", "Kendrick", "Melanie", "Allyson",
                    "Leila", "Rodrigo", "Allen", "Jesus", "Aaliyah", "Adelynn", "Lia", "Yerik", "Danielle", "Adriel",
                    "Jaylah", "Thiago", "Jaiden", "Hector", "Valeria", "Cameron", "Camilla", "Jeremiah",
                    "Logan", "Eduardo", "Riley", "Daniel", "Nathalie", "Brielle", "Justice", "Penelope", "Sebastian",
                    "Ivan", "Luna", "Izaiah", "Ian", "Violet", "Ailani", "Victor", "Adiel", "Julio", "Mya", "Emely",
                    "Eli", "Jacqueline", "Alisson", "Alice", "Francis", "Michelle", "Ryan", "Katherine", "Belen",
                    "Marcus", "Sandra", "Samir", "Rachel", "Liz", "Johann", "Jaylene", "Jade", "Edison", "Alessandro",
                    "Esmeralda", "Aidan", "Lindsay", "Rosa", "Elsie", "Ashly", "Jeremias", "Ermias", "Caleb", "Andre",
                    "Maximo", "Lola", "Jayden", "Dean", "Ambar", "Amy", "Roman", "Shane", "Alayna", "Jadiel", "Mia",
                    "Uriel", "Asher", "Hannah", "Tomas", "Bryanna", "Anais", "Abel", "Abigail", "Arianna", "Sofia",
                    "Mikayla", "Yadiel", "Martin", "Lincoln", "Lesley", "Camille", "Gia", "Chris", "Karen", "Bella",
                    "Jennifer", "Jax", "Brittany", "Jair", "Elvis", "Maximus", "Laia", "Giselle", "Jazlyn", "Annabelle",
                    "Matthias", "Dereck", "Ruby", "Kehlani", "Joselyn", "Travis", "Ismael", "Yesenia", "Jonathan",
                    "Hugo", "Aleah", "Jolie", "Stephany", "Sean", "Alahia", "Jordan", "Leia", "Kylie", 
                    "Kayla", "Oliver", "Erick", "Gabrielle", "Walter", "Catalina", "Kairo", "Elianny", "Jean",
                    "Orlando", "Krystal", "Ariana", "Marilyn", "Alison", "Ingrid", "Emily", "Wesley", "Grace",
                    "Victoria", "Jayce", "Aisha", "Alanis", "Alex", "Joseph", "Josiah", "Yaretzi", "Lea", "Alanna",
                    "Sasha", "Julien", "Kaelyn", "Benjamin", "Gustavo", "Leo", "Hudson", "Nathalia", "Noah", "Landon",
                    "Leonardo", "Autumn", "Maria", "Damaris", "Peyton", "Yaritza", "Izabella", "Abdiel", "Abril",
                    "Jayson", "Makayla", "Patrick", "Ivy", "Angie", "Yareli", "Valentino", "Zara", "King", "Dennis",
                    "Charles", "Matias", "Leandro", "Amelia", "Skylah", "Kaylee", "Christina", "Athena", "Cayden",
                    "Maverick", "Melody", "Jack", "Bryant", "Maddox", "Aliah", "Brianny", "Ana", "Leilani", "Heaven",
                    "Jake", "Jay", "Jeancarlos", "Kendra", "Paloma", "Fatima", "Brigitte", "Jaelyn", "Leonel", "Avril",
                    "Jael", "Chase", "Raquel"],
    "last_names": ["Ortis", "Deharo", "Buelna", "Diazlopez", "Ibanez", "Caicedo", "Teniente", "Casado", "Calderon",
                   "Virrueta", "Arita", "Mancillas", "Rostro", "Ponce", "Iraheta", "Lizardi", "Monjaraz", "Pavon",
                   "Gardea", "Hernandez", "Tafolla", "Vejar", "Estupinan", "Cavazos", "Cipriano", "Manon",
                   "Casarrubias", "Mosquera", "Ruiz", "Oyola", "Sigala", "Nieblas", "Zendejas", "Raygoza", "Loaiza",
                   "Canelo", "Pintado", "Aguirre", "Fleites", "Pita", "Cerezo", "Mancia", "Ospina", "Velazquez",
                   "Zarate", "Infante", "Bermudes", "Villatoro", "Disla", "Almaraz", "Jalomo", "Villar", "Masias",
                   "Noriega", "Cervera", "Ruvalcaba", "Estremera", "Chevere", "Ugarte", "Equihua", "Caba", "Argueta",
                   "Rincon", "Botero", "Arellano", "Aceves", "Granillo", "Terrazas", "Graciano", "Samaniego", "Machin",
                   "Ramires", "Hiraldo", "Sardinas", "Aviles", "Carchi", "Yanes", "Inoa", "Jaramillo", "Servin",
                   "Vasquez", "Anzures", "Recio", "Ballinas", "Pedroza", "Olivieri", "Montesdeoca", "Esparza",
                   "Resendez", "Villalba", "Marentes", "Verdejo", "Lugo", "Mansilla", "Aristizabal", "Mundo", "Mancha",
                   "Basilio", "Zevallos", "Cuervo", "Devora", "Grillo", "Delao", "Gonzalezgarcia", "Perez", "Pinal",
                   "Salcido", "Zambrano", "Puig", "Santiago", "Talamantes", "Rojo", "Tenezaca", "Nova", "Jarquin",
                   "Verduzco", "Perla", "Sustaita", "Vidana", "Herrejon", "Suastegui", "Ochoa", "Puello", "Moreno",
                   "Lung", "Villagomez", "Campillo", "Virella", "Huitron", "Amarillas", "Perea", "Marmolejos", "Raya",
                   "Armenta", "Rodriguez", "Guallpa", "Font", "Paulin", "Urbano", "Garciasanchez", "Deluna", "Tristan",
                   "Gines", "Pabon", "Vaquera", "Ventura", "Troche", "Osuna", "Moreira", "Collazo", "Pineda", "Tena",
                   "Pavia", "Portal", "Maysonet", "Noa", "Laurel", "Escamilla", "Alvira", "Alzate", "Plazola",
                   "Azevedo", "Vale", "Godoy", "Dorantes", "Sermeno", "Buentello", "Nieves", "Ardon", "Vicente",
                   "Chiquito", "Banda", "Olivares", "Olivos", "Barra", "Cantillo", "Vallejo", "Ticas", "Cienfuegos",
                   "Rada", "Macareno", "Picasso", "Lopezgarcia", "Marte", "Facio", "Leiva", "Mederos", "Sanmartin",
                   "Gerardo", "Campa", "Saavedra", "Colmenero", "Navarrete", "Guadalupe", "Rosales", "Corrales",
                   "Tavarez", "Acosta", "Cosme", "Salais", "Funes", "Lepe", "Narez", "Asencio", "Quinteros", "Zarco",
                   "Irigoyen", "Meraz", "Regino", "Garciaramirez", "Pecina", "Tijerina", "Barradas", "Magallanes",
                   "Delvillar", "Madero", "Cardoza", "Cepeda", "Guajardo", "Olarte", "Toledo", "Donoso", "Terrones",
                   "Silva", "Barboza", "Bravo", "Solorzano", "Ordones", "Catalan", "Licea", "Amado", "Duenez", "Salas",
                   "Adrian", "Bedoy", "Caban", "Jasso", "Mas", "Calles", "Sotelo", "Alcazar", "Morel", "Felipe",
                   "Dubon", "Puentes", "Cuadra", "Zubia", "Sanabria", "Amigon", "Calva", "Olivar", "Mena", "Villalobos",
                   "Solorio", "Fundora", "Puente", "Jiron", "Desantiago", "Zavaleta", "Moraga", "Rosario", "Ipina",
                   "Aldaz", "Rosiles", "Ferman", "Bisono", "Bugarin", "Mendoza", "Aispuro", "Tobar", "Suarez", "Espana",
                   "Herrero", "Martines", "Goto", "Brizuela", "Barcenas", "Alamillo", "Ricardo", "Elizarraraz", "Diego",
                   "Maese", "Orona", "Domingues", "Merced", "Murrieta", "Enciso", "Barba", "Febles", "Uriegas", "Alers",
                   "Elenes", "Alvarenga", "Cubillos", "Monreal", "Centeno", "Aguiniga", "Aldama", "Guardiola",
                   "Vizcaino", "Lamas", "Belmares", "Gatica", "Ferrufino", "Cabanillas", "Yebra", "Mazariego",
                   "Soltero", "Barreras", "Mayorga", "Maynes", "Siqueiros", "Gamarra", "Villasenor", "Casas", "Pratts",
                   "Hipolito", "Chirinos", "Cordon", "Mares", "Minjares", "Candela", "Olivo", "Balderas", "Becerril",
                   "Urrutia", "Cordero", "Olivarez", "Castanon", "Revilla", "Eguia", "Valtierra", "Oviedo", "Gaytan",
                   "Olivencia", "Negron", "Pereida", "Lizcano", "Larranaga", "Lujano", "Urrea", "Sorto", "Carachure",
                   "Mariscal", "Cifuentes", "Rangel", "Pequeno", "Blandon", "Luis", "Pujol", "Canchola", "Barrales",
                   "Salceda", "Cadiz", "Becerra", "Lucena", "Chaves", "Curbelo", "Colina", "Cruzmartinez", "Dutan",
                   "Lara", "Villalva", "Velarde", "Riveros", "Altamirano", "Figuereo", "Mulero", "Galeano", "Rueda",
                   "Cid", "Lumbreras", "Perezmartinez", "Chavira", "Planas", "Granado", "Villacis", "Silvera",
                   "Lezcano", "Fermin", "Grajales", "Roberto", "Lino", "Esqueda", "Rojas", "Pelayo", "Rosado", "Lainez",
                   "Alpizar", "Ovalles", "Canizales", "Alcon", "Camberos", "Romero", "Idrovo", "Negrete", "Eusebio",
                   "Coreas", "Delvalle", "Mier", "Carabajal", "Ramirezhernand", "Cardenas", "Andrade", "Lua",
                   "Perezrodriguez", "Delarosa", "Bermudez", "Natera", "Ribas", "Guereca", "Melendez", "Gamino",
                   "Labrada", "Araya", "Rebollo", "Bobadilla", "Juan", "Corporan", "Portalatin", "Limones", "Pech",
                   "Casasola", "Trigueros", "Hinojosa", "Diaz", "Alvarado", "Arellanes", "Allende", "Berlanga",
                   "Bedoya", "Sepeda", "Tiburcio", "Esteban", "Alcantara", "Febres", "Casados", "Arebalo", "Orejel",
                   "Caballero", "Zabala", "Guandique", "Posada", "Fiallo", "Cuadros", "Valiente", "Carlo", "Recendez",
                   "Payano", "Herrera", "Izquierdo", "Bencosme", "Arista", "Copado", "Aquilar", "Gonzaga", "Tercero",
                   "Maturino", "Santibanez", "Pastor", "Valdes", "Mota", "Depena", "Freyre", "Cayetano", "Flores",
                   "Briones", "Montes", "Limas", "Mijares", "Gama", "Riojas", "Lopez", "Lamboy", "Heredia", "Palafox",
                   "Olmos", "Narciso", "Contrera", "Araiza", "Barcelo", "Zurita", "Feliciano", "Melero", "Monsalve",
                   "Martindelcamp", "Marcelino", "Delacerda", "Landa", "Cuevas", "Carrasquillo", "Ortiz", "Suriel",
                   "Izaguirre", "Calzadilla", "Pinero", "Arriola", "Encinas", "Chevez", "Gaxiola", "Quiroga",
                   "Hercules", "Adame", "Borbon", "Vidaurri", "Barroso", "Yepez", "Herrarte", "Enriquez", "Francisco",
                   "Nino", "Ledesma", "Mandujano", "Delahoz", "Salazar", "Moron", "Pozos", "Samudio", "Poblano",
                   "Baylon", "Pallares", "Esquilin", "Casillas", "Picazo", "Briceno", "Jimenez", "Mencia", "Candia",
                   "Aldaba", "Cansino", "Pizano", "Garfias", "Alfaro", "Guzman", "Zarazua", "Monrroy", "Jesus",
                   "Piedrahita", "Agramonte", "Arauz", "Olivas", "Zazueta", "Aguero", "Castillo", "Raymundo", "Cahue",
                   "Narvaez", "Deltoro", "Rivero", "Camejo", "Lona", "Linan", "Melo", "Marrujo", "Delira", "Rubalcaba",
                   "Bastidas", "Cea", "Silvas", "Frayre", "Niebla", "Rentas", "Cabada", "Loja", "Duarte", "Chapa",
                   "Lavin", "Favela", "Fontanez", "Rivadeneira", "Ramirezgarcia", "Labra", "Bodden", "Corral", "Abila",
                   "Jaso", "Afanador", "Montenegro", "Taboada", "Negrin", "Fuentez", "Menchaca", "Clavijo", "Pantoja",
                   "Bernabe", "Desoto", "Baez", "Melchor", "Matos", "Lagunes", "Sala", "Marin", "Noyola", "Rivas",
                   "Urquidi", "Garciagonzalez", "Ocana", "Espitia", "Gallardo", "Delosrios", "Davalos", "Enriques",
                   "Aguillar", "Garza", "Moncivais", "Arguijo", "Viruet", "Valderrama", "Buenrostro", "Leyva", 
                   "Arciga", "Constanza", "Merida", "Morera", "Alvarez", "Ruybal", "Quintanar", "Somoza", "Hoyos",
                   "Gaeta", "Farfan", "Ornelas", "Casco", "Chicas", "Tineo", "Almendarez", "Castano", "Rodela",
                   "Perezsanchez", "Camarillo", "Escalante", "Alas", "Restrepo", "Carrizales", "Barreiro", "Gallegos",
                   "Vilchis", "Corvera", "Garnica", "Urdiales", "Llerena", "Medero", "Lovo", "Gonzalezlopez", "Erives",
                   "Hinostroza", "Huertas", "Uvalle", "Villaverde", "Virgen", "Longoria", "Talamantez", "Ovando",
                   "Osorio", "Tagle", "Blas", "Serpas", "Canedo", "Barahona", "Victoria", "Penaranda", "Guerrero",
                   "Salguero", "Espin", "Sagrero", "Aracena", "Peguero", "Montelongo", "Mairena", "Baltazar", "Olmeda",
                   "Lizardo", "Castilleja", "Arreaga", "Saez", "Ozuna", "Cantu", "Magallon", "Medellin", "Mungia",
                   "Elvira", "Lastra", "Minchala", "Maestas", "Lasalle", "Retana", "Abril", "Cotto", "Apolinar",
                   "Aguilera", "Favila", "Pinon", "Castelan", "Popoca", "Murrietta", "Barcena", "Veliz", "Carbajal",
                   "Galvan", "Arrellano", "Grijalva", "Laredo", "Loa", "Fregoso", "Euceda", "Bibian", "Borrego",
                   "Rogue", "Silverio", "Carapia", "Pargas", "Criollo", "Venzor", "Benavidez", "Henriquez", "Alcorta",
                   "Urquidez", "Inzunza", "Gerena", "Villafana", "Ureno", "Mosqueda", "Mendizabal", "Servellon",
                   "Vieyra", "Cabrera", "Carrillo", "Viramontes", "Morillo", "Ron", "Torrez", "Calleros", "Bran",
                   "Servantes", "Carcamo", "Aranda", "Costilla", "Taborda", "Constantino", "Perezperez", "Santizo",
                   "Covarrubias", "Marron", "Delapena", "Bustillos", "Mestas", "Quevedo", "Rizo", "Pineiro", "Batista",
                   "Jeronimo", "Paulino", "Arocha", "Botello", "Montero", "Echeverry", "Baeza", "Navarro", "Gervacio",
                   "Sabillon", "Vela", "Deniz", "Ceron", "Herandez", "Gaviria", "Badillo", "Panuco", "Villada",
                   "Somarriba", "Castruita", "Veloz", "Guevara", "Carlos", "Medina", "Platero", "Olalde", "Otano",
                   "Penafiel", "Alcocer", "Blancarte", "Vara", "Velaquez", "Campusano", "Arevalo", "Mojarro", "Llanos",
                   "Reveles", "Valcarcel", "Paxtor", "Ciriaco", "Murillo", "Gaitan", "Larin", "Villafranco", "Lemos",
                   "Curiel", "Campuzano", "Vallejos", "Dolores", "Montejano", "Andujo", "Montalvan", "Gongora",
                   "Cruzlopez", "Gamero", "Urizar", "Garica", "Olvera", "Remache", "Nevarez", "Parga", "Uscanga",
                   "Aguillon", "Archila", "Olaya", "Montijo", "Cardoso", "Monteon", "Rodriguezlopez", "Naranjo",
                   "Campo", "Bucio", "Oregel", "Gauna", "Torres", "Arizmendi", "Quinto", "Amparan", "Cuesta", "Roybal",
                   "Tamayo", "Lupercio", "Galvis", "Sevilla", "Loya", "Lobo", "Tostado", "Borrero", "Guadarrama",
                   "Perera", "Lago", "Bejarano", "Razo", "Rufino", "Maqueda", "Plasencia", "Barreto", "Amaya",
                   "Agredano", "Panameno", "Carretero", "Delreal", "Govea", "Salaiz", "Estudillo", "Andazola", "Delara",
                   "Renteria", "Quispe", "Miramontes", "Magallan", "Rubi", "Lascano", "Tonche", "Rosendo", "Escobedo",
                   "Aldrete", "Piedra", "Gracia", "Salasar", "Munos", "Cadavid", "Rebolledo", "Basurto", "Pliego",
                   "Esperanza", "Polanco", "Delafuente", "Durazo", "Deloera", "Legaspi", "Vivas", "Delatorre", "Brenes",
                   "Delahoya", "Viera", "Palacio", "Rosillo", "Merlos", "Bartolo", "Escorcia", "Nuno", "Amaro",
                   "Facundo", "Seda", "Noboa", "Valera", "Canela", "Coca", "Santiesteban", "Escarcega", "Picon",
                   "Clemente", "Galban", "Bribiesca", "Chavarria", "Vivanco", "Vicuna", "Urquizo", "Ayala", "Benito",
                   "Matute", "Toribio", "Barrio", "Preciado", "Mendiola", "Echevarria", "Langarica", "Mellado", "Licon",
                   "Luque", "Yanez", "Carrizal", "Algarin", "Arvizu", "Decastro", "Leon", "Alverio", "Mesa", "Moncayo",
                   "Cedillos", "Hinojos", "Patino", "Jacinto", "Ferrera", "Alavez", "Isaza", "Montiel", "Olveda",
                   "Villalon", "Espericueta", "Jerez", "Mancera", "Losada", "Oquendo", "Crespin", "Donis", "Constancio",
                   "Jara", "Cancel", "Iribe", "Landeros", "Cortinas", "Arceo", "Catano", "Santacruz", "Benites", "Joya",
                   "Vega", "Sicairos", "Ybanez", "Alban", "Garcialopez", "Cruzhernandez", "Fuerte", "Tarin", "Calzada",
                   "Castilla", "Lopezlopez", "Natal", "Ojeda", "Travieso", "Olavarria", "Viloria", "Larosa",
                   "Pesqueira", "Carreto", "Loredo", "Fortuna", "Soberanis", "Bonet", "Pastrana", "Benavides",
                   "Sahagun", "Navia", "Simental", "Arzate", "Bazaldua", "Picado", "Majano", "Batz", "Mejia", "Obeso",
                   "Carmona", "Carrasco", "Santillanes", "Pinales", "Mestre", "Acevedo", "Aliaga", "Serrata", "Fuertes",
                   "Victorino", "Carvajal", "Marinez", "Bringas", "Candelaria", "Turrubiates", "Luevanos", "Sabino",
                   "Neria", "Arenas", "Banales", "Maceda", "Quintanilla", "Rua", "Lima", "Buitrago", "Zavala",
                   "Fulgencio", "Pozo", "Sambrano", "Zamarripa", "Inocencio", "Joaquin", "Ernandez", "Garibay", "Maez",
                   "Javier", "Camarena", "Soberanes", "Quinones", "Trillo", "Cigarroa", "Aponte", "Leyba", "Lupian",
                   "Ugalde", "Marez", "Suazo", "Batalla", "Alderete", "Morones", "Albarran", "Nicolas", "Anton",
                   "Alcoser", "Garrido", "Tabares", "Loza", "Zuluaga", "Lomas", "Menjivar", "Rodas", "Valderas",
                   "Guadiana", "Santillana", "Ybarra", "Chavez", "Cendejas", "Vigil", "Pons", "Colindres", "Blancas",
                   "Alday", "Nicasio", "Onate", "Godines", "Rosas", "Marmol", "Inga", "Anchondo", "Moronta", "Elias",
                   "Capellan", "Campoverde", "Baca", "Patricio", "Quito", "Santa", "Galeas", "Alvardo", "Canal",
                   "Corniel", "Guijarro", "Revolorio", "Najar", "Arambula", "Sisneros", "Cerrillo", "Nava", "Gasca",
                   "Cardozo", "Espino", "Sosa", "Serratos", "Uranga", "Garcia", "Crisanto", "Faz", "Carmen", 
                   "Quirarte", "Rosero", "Alamo", "Alamilla", "Arana", "Agosto", "Pulgarin", "Feliz", "Madril",
                   "Bernardo", "Cantarero", "Marcia", "Casaus", "Pellot", "Castillon", "Cisneros", "Veras", "Cossio",
                   "Tiscareno", "Bueso", "Ramirezlopez", "Noguez", "Quiroz", "Obregon", "Bardales", "Vinas", "Olmo",
                   "Haro", "Zetina", "Gomez", "Correa", "Salinas", "Maza", "Padua", "Enrique", "Paula", "Balderrama",
                   "Santander", "Clavel", "Vigo", "Argote", "Lomeli", "Rengifo", "Bedolla", "Vivar", "Escudero",
                   "Villagrana", "Rosalez", "Segovia", "Perezgonzalez", "Mendosa", "Montalvo", "Valencia", "Martinez",
                   "Minaya", "Quizhpi", "Mayorquin", "Vergara", "Arreola", "Bonilla", "Chagoya", "Roldan", "Fleitas",
                   "Casique", "Morado", "Zacarias", "Barrera", "Delaguila", "Comas", "Raigoza", "Marcelo", "Aldaco",
                   "Placido", "Pedro", "Ruedas", "Novoa", "Bibiano", "Huesca", "Moscoso", "Vazques", "Bencomo", "Goris",
                   "Gusman", "Vilches", "Caldera", "Pazmino", "Porto", "Pera", "Carbonell", "Candido", "Santini",
                   "Frometa", "Crispin", "Tienda", "Teran", "Duron", "Armendarez", "Castrejon", "Orengo", "Brito",
                   "Machorro", "Bracamontes", "Bolivar", "Diez", "Frausto", "Pizarro", "Zatarain", "Castorena",
                   "Ceniceros", "Porras", "Casiano", "Armijo", "Canto", "Puga", "Jaquez", "Castellon",
                   "Nazario", "Peraza", "Reinoso", "Pagan", "Amador", "Caceres", "Nambo", "Corella", "Higuera",
                   "Castro", "Salamanca", "Adorno", "Olguin", "Cervantes", "Cabral", "Sesma", "Ortez", "Calleja",
                   "Hermida", "Topete", "Lemus", "Camilo", "Monterroza", "Maisonet", "Liriano", "Alegria", "Haros",
                   "Medrano", "Pelaez", "Chirino", "Colon", "Leija", "Carballo", "Ocasio", "Monge", "Montealegre",
                   "Figueredo", "Galarza", "Armas", "Albarado", "Morua", "Lizarraga", "Arias", "Bosquez", "Laboy",
                   "Lerma", "Quijas", "Villafranca", "Sillas", "Fernandez", "Morell", "Luquin", "Cabello", "Lora",
                   "Delacruz", "Genao", "Arispe", "Rubalcava", "Estevez", "Valero", "Pesina", "Gonzalezperez",
                   "Meneses", "Esquibel", "Carillo", "Palomar", "Antigua", "Zermeno", "Delfin", "Leal", "Montesino",
                   "Erazo", "Mera", "Delcastillo", "Alvares", "Buitron", "Balladares", "Soria", "Liz", "Pardo", "Toro",
                   "Poveda", "Uribe", "Roa", "Obando", "Zamarron", "Zavalza", "Leanos", "Barrios", "Ferreras", "Boza",
                   "Freire", "Carreno", "Chaires", "Mattos", "Sabedra", "Vaquerano", "Monegro", "Horta", "Burgos",
                   "Coto", "Esquer", "Gaucin", "Serrato", "Tomas", "Nogueras", "Galeno", "Echeverria", "Penaloza",
                   "Cerda", "Capetillo", "Almanza", "Rayo", "Loor", "Segundo", "Soliz", "Juarbe", "Huaman", "Carnero",
                   "Berumen", "Zepeda", "Alcantar", "Saucedo", "Villamil", "Garriga", "Farinas", "Rogel",
                   "Martinezhernan", "Mancilla", "Marenco", "Cervantez", "Massa", "Garduno", "Palos", "Redondo",
                   "Baltodano", "Gabaldon", "Urzua", "Ferreyra", "Ancira", "Muneton", "Plata", "Bermeo", "Orosco",
                   "Godina", "Garzon", "Cazares", "Franqui", "Balcazar", "Navarette", "Mancinas", "Cruz", "Cruzado",
                   "Albino", "Albor", "Gonzales", "Latorre", "Berganza", "Consuegra", "Santana", "Osoria", "Cortina",
                   "Pino", "Yerena", "Figueroa", "Merchan", "Villalvazo", "Vierra", "Avelino", "Magadan", "Gascon",
                   "Castrillon", "Loayza", "Custodio", "Muratalla", "Maltez", "Cabrales", "Manjarrez", "Ocegueda",
                   "Losoya", "Ahumada", "Duenas", "Araujo", "Quiros", "Ramon", "Cespedes", "Pruneda", "Vaquero",
                   "Pantaleon", "Najera", "Portilla", "Puebla", "Amezcua", "Escareno", "Solivan", "Calero", "Pareja",
                   "Cajigas", "Hidrogo", "Rodriges", "Montejo", "Garciacruz", "Remigio", "Trigo", "Fuentes", "Ogando",
                   "Penuelas", "Urquiza", "Delgado", "Rabadan", "Umanzor", "Grau", "Huezo", "Pereda", "Barraza",
                   "Gandarilla", "Varela", "Ribera", "Lazalde", "Guebara", "Cornejo", "Padin", "Banos", "Morgado",
                   "Samano", "Rios", "Dominquez", "Agudelo", "Calvillo", "Guerra", "Andujar", "Melgarejo",
                   "Hincapie", "Huante", "Malagon", "Valeriano", "Hernandezlopez", "Marroquin", "Sencion", "Navedo",
                   "Maciel", "Suniga", "Corredor", "Menendez", "Chaidez", "Valerio", "Azua", "Hernandezperez",
                   "Vicencio", "Aparicio", "Texidor", "Pupo", "Encalada", "Sabala", "Venegas", "Escalona", "Calixto",
                   "Paniagua", "Desantos", "Chica", "Pedraza", "Dominguez", "Renderos", "Heras", "Pazos", "Roig",
                   "Ulloa", "Dena", "Aldape", "Berrones", "Cebreros", "Azcona", "Cuautle", "Garciarodrigue", "Napoles",
                   "Chairez", "Fausto", "Campos", "Grado", "Tanguma", "Sanches", "Chino", "Lagos", "Aguila", "Molano",
                   "Basulto", "Aleman", "Quinonez", "Lanuza", "Palaguachi", "Alegre", "Machado", "Solares", "Lorenzo",
                   "Delavega", "Requena", "Sequeira", "Ferrer", "Silvestre", "Saldarriaga", "Callejas", "Lozoya",
                   "Aquino", "Hermosillo", "Loreto", "Jusino", "Rayas", "Anaya", "Cedano", "Montellano", "Gavina",
                   "Bohorquez", "Pinzon", "Ocon", "Quezada", "Nodarse", "Patron", "Bueno", "Saenz", "Balli", "Donjuan",
                   "Suero", "Ortegon", "Barbosa", "Cuello", "Burruel", "Soriano", "Mazon", "Cora", "Membreno",
                   "Godinez", "Junco", "Cubias", "Morano", "Canizalez", "Arvizo", "Compean", "Gotay", "Arriaza",
                   "Orellana", "Paez", "Viana", "Vidrio", "Tabarez", "Roca", "Vidals", "Moro", "Cabanas", "Celestino",
                   "Cuen", "Telles", "Juarez", "Plascencia", "Navas", "Oregon", "Arreguin", "Rivera", "Estrella",
                   "Capo", "Manso", "Bauza", "Madriz", "Pujols", "Siguenza", "Monterroso", "Zagal", "Lasso", "Venancio",
                   "Torralba", "Montufar", "Varona", "Badilla", "Villagran", "Leos", "Arango", "Licona", "Florencio",
                   "Fletes", "Quintana", "Peralez", "Triana", "Alcala", "Rutz", "Candelas", "Riveron", "Espaillat",
                   "Solache", "Luz", "Jovel", "Corea", "Valdivieso", "Carrero", "Celaya", "Cazarez", "Rod", "Pintor",
                   "Arzola", "Trevino", "Garciagarcia", "Cambron", "Isais", "Cornelio", "Guardado", "Sapien",
                   "Basaldua", "Henao", "Orduno", "Caraveo", "Lantigua", "Jauregui", "Aburto", "Belloso", "Valenciano",
                   "Vasques", "Chamorro", "Munoz", "Vazquez", "Garciaflores", "Paz", "Fragoso", "Paiz", "Velasco",
                   "Vento", "Puac", "Espinal", "Arcia", "Roque", "Damian", "Asuncion", "Oliveras", "Brambila",
                   "Galeana", "Orea", "Lagunas", "Bautista", "Escutia", "Bejar", "Manzano", "Gregorio", "Prieto",
                   "Sardina", "Delrio", "Gorostieta", "Chacon", "Monje", "Reyez", "Carpio", "Minjarez", "Soler",
                   "Febus", "Villamar", "Cedeno", "Arteaga", "Angel", "Lanza", "Gamboa", "Cepero", "Gonzalez",
                   "Barreda", "Umana", "Lopezperez", "Arce", "Ortega", "Verdin", "Nungaray", "Espejo", "Conde",
                   "Aragon", "Castelo", "Motta", "Irizarry", "Crespo", "Tobon", "Treto", "Escoto", "Lule", "Guizar",
                   "Vegas", "Corpus", "Claros", "Vidales", "Marty", "Florentino", "Dorado", "Garciaperez", "Bermea",
                   "Belmontes", "Griego", "Marmolejo", "Grullon", "Montesinos", "Levario", "Savedra", "Banuelos",
                   "Ordaz", "Bocanegra", "Trejo", "Arzu", "Lopezramirez", "Nuncio", "Santillan", "Castrillo", "Tafoya",
                   "Morales", "Corchado", "Concha", "Perezgarcia", "Acuna", "Sarabia", "Sagastume", "Magana", "Osorto",
                   "Acedo", "Acebedo", "Arocho", "Lucio", "Rodriques", "Palencia", "Labrador", "Gallego", "Manzanares",
                   "Silveira", "Campas", "Lazo", "Cueva", "Padro", "Olea", "Frias", "Mirabal", "Cecena", "Madrigal",
                   "Murga", "Arechiga", "Milian", "Sias", "Pinilla", "Liberato", "Robaina", "Placencia", "Dehoyos",
                   "Cirilo", "Anguiano", "Delcampo", "Alvear", "Basquez", "Monarrez", "Fabela", "Victoriano", "Dearmas",
                   "Silguero", "Toscano", "Bracero", "Ponciano", "Angulo", "Serafin", "Zelaya", "Bosque",
                   "Martinezcruz", "Coronel", "Alberto", "Barcia", "Bermejo", "Gastelum", "Villareal", "Fontes",
                   "Marquez", "Deanda", "Pleitez", "Lucatero", "Perales", "Magdaleno", "Deras", "Paramo", "Grajeda",
                   "Monjaras", "Tenorio", "Cantoran", "Gandara", "Jaimes", "Abundiz", "Pico", "Puerta", "Aguiar",
                   "Pocasangre", "Calvo", "Torrico", "Parrales", "Munguia", "Perezcruz", "Marban", "Villarroel",
                   "Savala", "Murguia", "Pesantez", "Rebollar", "Echeverri", "Alarid", "Zapata", "Zetino", "Prada",
                   "Peralta", "Corzo", "Giron", "Deleon", "Armendariz", "Uresti", "Monroy", "Zambrana", "Arencibia",
                   "Arroyave", "Lozano", "Guijosa", "Espindola", "Abeyta", "Villafan", "Cubas", "Bolanos", "Posadas",
                   "Zamora", "Albarez", "Hilario", "Pizana", "Ariza", "Saldana", "Uriarte", "Proano", "Espinola",
                   "Alvidrez", "Resendiz", "Giraldo", "Belmonte", "Valladolid", "Villafuerte", "Saravia", "Mondragon",
                   "Delosangeles", "Santo", "Alarcon", "Baiza", "Mazariegos", "Floresgarcia", "Portela", "Vallecillo",
                   "Aldana", "Merlo", "Machuca", "Gudino", "Bernardino", "Irias", "Urdaneta", "Clara", "Arballo",
                   "Lorenzana", "Encinias", "Olmedo", "Breceda", "Cuba", "Tamez", "Guitron", "Avilez", "Dionicio",
                   "Ciprian", "Natividad", "Sandoval", "Arcila", "Casimiro", "Corona", "Llamas", "Peinado", "Solano",
                   "Zuniga", "Celis", "Loera", "Marcos", "Fiscal", "Luera", "Zuno", "Alonzo", "Ballester", "Gavidia",
                   "Cereceres", "Burrola", "Hernandezcruz", "Tarango", "Vanegas", "Justiniano", "Berroa", "Portugal",
                   "Mar", "Padron", "Bustos", "Lacayo", "Zamudio", "Navejas", "Onofre", "Manriquez", "Ocanas",
                   "Diosdado", "Agustin", "Pascual", "Quijada", "Sauceda", "Cuebas", "Arciniega", "Aybar", "Aguayo",
                   "Delangel", "Lizama", "Mireles", "Muralles", "Milanes", "Marcial", "Vitela", "Santos", 
                   "Checo", "Vides", "Moreta", "Viteri", "Rascon", "Cardiel", "Terrero", "Burgueno", "Florian",
                   "Dejesus", "Macedo", "Verdugo", "Sais", "Duque", "Urioste", "Morataya", "Chinchilla", "Collado",
                   "Gutierres", "Poncedeleon", "Arroyos", "Almeda", "Chavero", "Zumba", "Amparo", "Victorio", "Aguado",
                   "Saragosa", "Belman", "Galindez", "Bailon", "Arrieta", "Ceja", "Tinoco", "Salvatierra", "Mayen",
                   "Betances", "Escalera", "Anzaldua", "Salado", "Ramirezramirez", "Pla", "Osornio", "Pando", "Lobos",
                   "Barranco", "Ceballos", "Buendia", "Bustillo", "Maradiaga", "Luna", "Tejada", "Guillermo", "Colocho",
                   "Julio", "Villicana", "Flamenco", "Rovira", "Segarra", "Balbuena", "Lafuente", "Breton",
                   "Santistevan", "Cota", "Cruzgarcia", "Villescas", "Huerta", "Arroyo", "Amezquita", "Dieguez", "Ley",
                   "Encarnacion", "Ayon", "Artiaga", "Marine", "Costales", "Delgadillo", "Cabezas", "Navarrette",
                   "Tacuri", "Baros", "Rosa", "Ambrosio", "Almazan", "Matus", "Maximo", "Neri", "Parras", "Alejo",
                   "Orihuela", "Granados", "Ocampo", "Tadeo", "Turrubiartes", "Urquilla", "Trujillo", "Astacio",
                   "Delossantos", "Renovato", "Berrio", "Banegas", "Parrilla", "Velasquez", "Ledezma", "Sedillo",
                   "Caro", "Barrientos", "Crisostomo", "Landin", "Cerrato", "Fimbres", "Antuna", "Cardona", "Ramirez",
                   "Santillano", "Morocho", "Cantero", "Gordillo", "Mateos", "Oyervides", "Modesto", "Samora",
                   "Oliveros", "Cerna", "Valle", "Abundis", "Urias", "Gurule", "Beltre", "Abad", "Lechuga",
                   "Villalovos", "Canas", "Aguilar", "Chaparro", "Muniz", "Fraire", "Orozco", "Benavente", "Rosete",
                   "Iturralde", "Interiano", "Castello", "Cano", "Serna", "Lobato", "Chavarin", "Arcos", "Alferez",
                   "Jiminez", "Tovar", "Patlan", "Elvir", "Delamora", "Ronquillo", "Casares", "Arboleda", "Monzon",
                   "Cartagena", "Alanis", "Cancino", "Pedregon", "Romo", "Sanmiguel", "Fresquez", "Tejeda",
                   "Mascarenas", "Astorga", "Daza", "Pena", "Gomezgarcia", "Burciaga", "Archibeque", "Landaverde",
                   "Leonardo", "Salcedo", "Valles", "Padilla", "Urbina", "Pichardo", "Osegueda", "Isidoro", "Elizalde",
                   "Meza", "Elizondo", "Manzo", "Claudio", "Verde", "Mesta", "Chagolla", "Mero", "Marcano", "Almaguer",
                   "Calcano", "Jimenes", "Cortez", "Alameda", "Paredez", "Jacome", "Fraga", "Balandran", "Avelar",
                   "Nanez", "Coria", "Palomera", "Montalbo", "Miera", "Briseno", "Osorno", "Mangual", "Carreon",
                   "Rayon", "Chico", "Deherrera", "Arredondo", "Garcilazo", "Riera", "Zorrilla", "Salaz", "Millan",
                   "Zaldivar", "Vialpando", "Deavila", "Gayton", "Gloria", "Vaca", "Arevalos", "Mantilla", "Lizaola",
                   "Reynosa", "Monterrosa", "Nogales", "Hernandezgarci", "Artiga", "Villarreal", "Cobian", "Arizpe",
                   "Morga", "Galvez", "Secundino", "Oceguera", "Atencio", "Almodovar", "Lezama", "Malacara",
                   "Castrellon", "Pedrosa", "Lopezmartinez", "Valenzuela", "Ramos", "Alonso", "Tinajero", "Alfonso",
                   "Zapien", "Canul", "Borunda", "Delpozo", "Iriarte", "Bargas", "Abreu", "Minero", "Gavilanes",
                   "Nadal", "Echavarria", "Salgado", "Gil", "Pomales", "Fajardo", "Urena", "Guel", "Estrada", "Beltran",
                   "Martinezlopez", "Domenech", "Baquero", "Yniguez", "Orrego", "Parra", "Presas", "Barco", "Tirado",
                   "Espiritu", "Cobo", "Fraijo", "Arguelles", "Amesquita", "Aceituno", "Eugenio", "Perezramirez",
                   "Enamorado", "Roblero", "Piceno", "Rafael", "Sotomayor", "Reyes", "Portillo", "Sanchezlopez",
                   "Rubio", "Vences", "Alva", "Zea", "Alba", "Garibaldi", "Subia", "Lopezhernandez", "Villegas",
                   "Mayoral", "Adames", "Iglesias", "Gaspar", "Garciamartinez", "Cuellar", "Ruelas", "Inda", "Frutos",
                   "Murcia", "Revuelta", "Cerros", "Mendieta", "Zayas", "Falcon", "Mercado", "Berrios", "Viveros",
                   "Torre", "Gurrola", "Morelos", "Baza", "Henandez", "Monteagudo", "Turcios", "Guillen", "Corado",
                   "Mayor", "Riviera", "Aguas", "Ontiveros", "Linares", "Lopezgonzalez", "Oros", "Carranza", "Fiallos",
                   "Calix", "Loeza", "Fierro", "Calvario", "Lamadrid", "Sarria", "Paredes", "Quirino", "Hernandes",
                   "Catala", "Cristobal", "Prudencio", "Mojica", "Garsia", "Dedios", "Morquecho", "Antillon", "Villeda",
                   "Antonio", "Feria", "Serrano", "Pereyra", "Muriel", "Arriaga", "Villafane", "Pimentel", "Cortes",
                   "Zertuche", "Esquivel", "Larios", "Puma", "Cibrian", "Sanchezgarcia", "Doria", "Pasillas", "Mora",
                   "Montemayor", "Montez", "Aros", "Arguello", "Vielma", "Bastida", "Robledo", "Liera", "Madera",
                   "Almada", "Olan", "Nerio", "Luviano", "Villasana", "Navar", "Maya", "Atilano", "Faria", "Gaona",
                   "Valadez", "Lucero", "Blanco", "Cedillo", "Sevillano", "Ibarra", "Castellanos", "Zenteno", "Rey",
                   "Garces", "Garciahernande", "Marrero", "Rochin", "Alcaraz", "Herrada", "Sixtos", "Sotolongo",
                   "Alejos", "Mata", "Prado", "Borjas", "Lajara", "Lebron", "Pina", "Barriga", "Toral", "Carrion",
                   "Velazco", "Capote", "Aguinaga", "Forero", "Galicia", "Perezhernandez", "Trevizo", "Merino",
                   "Lopezsanchez", "Jacobo", "Vargas", "Galan", "Delpino", "Valdiviezo", "Plancarte", "Borrayo",
                   "Elizarraras", "Alejandro", "Almonte", "Palomo", "Quintero", "Andino", "Geronimo", "Duenes",
                   "Monrreal", "Iracheta", "Caraballo", "Sanchez", "Bretado", "Orta", "Salmeron", "Felix", "Perdomo",
                   "Lema", "Tello", "Vizcarrondo", "Miguel", "Mateo", "Lux", "Cordoba", "Soza", "Flecha", "Madueno",
                   "Borquez", "Sarmiento", "Segoviano", "Pablo", "Delaluz", "Nieto", "Borboa", "Sarinana", "Mercedes",
                   "Rabago", "Ruis", "Sierra", "Ulibarri", "Villavicencio", "Dimas", "Avendano", "Muro", "Abarca",
                   "Mijangos", "Cuadrado", "Escatel", "Campana", "Betancur", "Germosen", "Yslas", "Zubiate",
                   "Martinezperez", "Vila", "Unzueta", "Tapia", "Mira", "Tavera", "Ambriz", "Sandate", "Cubero",
                   "Camero", "Quesada", "Ferrel", "Najarro", "Lira", "Sanjuan", "Troncoso", "Palmerin", "Marti",
                   "Huizar", "Bernal", "Lujan", "Tejera", "Milla", "Robles", "Melendrez", "Saiz", "Florez", "Oropeza",
                   "Montana", "Villalpando", "Carranco", "Palomino", "Melara", "Borja", "Escajeda", "Sifuentes",
                   "Camacho", "Sauseda", "Bazan", "Delcid", "Gramajo", "Mejorado", "Regalado", "Martir", "Diazdeleon",
                   "Lopezrodriguez", "Santamaria", "Neira", "Ordonez", "Galaviz", "Cesena", "Orantes", "Reynaga",
                   "Medel", "Archuleta", "Calle", "Moncada", "Ambrocio", "Vilchez", "Arvelo", "Yescas", "Barragan",
                   "Malpica", "Serano", "Taveras", "Colin", "Celedon", "Vizcarra", "Gonsales", "Blea", "Llanas",
                   "Barocio", "Mauricio", "Orduna", "Molinar", "Candelario", "Delapaz", "Astudillo", "Vera", "Carino",
                   "Berber", "Molina", "Olivera", "Jacquez", "Yzaguirre", "Jose", "Payan", "Barrientes", "Velasques",
                   "Agudo", "Delariva", "Davila", "Beato", "Montilla", "Montoya", "Cosio", "Franco", "Villarruel",
                   "Palma", "Valdespino", "Noguera", "Laguna", "Arizaga", "Sibrian", "Moctezuma", "Marchena",
                   "Mendivil", "Coronado", "Lopera", "Baena", "Ballesteros", "Samayoa", "Sostre", "Valdovinos",
                   "Constante", "Cobos", "Almanzar", "Lares", "Garay", "Llanes", "Fierros", "Sotello", "Olague",
                   "Sinchi", "Colmenares", "Villa", "Carrera", "Canales", "Marines", "Bonifacio", "Bello", "Baltierra",
                   "Jaime", "Malave", "Galo", "Betancourt", "Casias", "Nolasco", "Delagarza", "Rodarte", "Cerritos",
                   "Melgoza", "Luciano", "Justo", "Urbieta", "Lazcano", "Carreras", "Reza", "Peres", "Radilla",
                   "Sedano", "Tolentino", "Abalos", "Caamano", "Balboa", "Corro", "Provencio", "Rico", "Iniguez",
                   "Avellaneda", "Canseco", "Arjona", "Soto", "Parada", "Galindo", "Reina", "Conejo", "Avila",
                   "Colunga", "Marquina", "Bahena", "Degante", "Apodaca", "Quiles", "Avalos", "Cantor", "Lombera",
                   "Funez", "Alejandre", "Cuenca", "Federico", "Novelo", "Carias", "Monsivais", "Cabeza", "Rauda",
                   "Matamoros", "Pinedo", "Ramales", "Toledano", "Borjon", "Chiriboga", "Arrazola", "Baires", "Rayos",
                   "Holguin", "Cordova", "Camargo", "Solis", "Urgiles", "Felan", "Gudiel", "Azpeitia", "Farias",
                   "Fernando", "Barrantes", "Melgar", "Cadenas", "Miron", "Barrientez", "Valdez", "Cintron", "Siller",
                   "Avitia", "Quiroa", "Partida", "Villacorta", "Islas", "Recendiz", "Depaz", "Beas", "Reyesgarcia",
                   "Liranzo", "Serra", "Recinos", "Aramburo", "Valdivia", "Galdamez", "Santoyo", "Mina", "Zeledon",
                   "Riquelme", "Montano", "Isidro", "Acero", "Viscarra", "Espinoza", "Guaman", "Saito", "Rael",
                   "Miranda", "Delbosque", "Castaneda", "Jurado", "Sanz", "Luevano", "Macario", "Espada", "Valentin",
                   "Lozada", "Reyna", "Jorge", "Ortuno", "Ascencio", "Sanroman", "Cabreja", "Rodriquez", "Familia",
                   "Villalta", "Talavera", "Alicea", "Gonsalez", "Hurtado", "Aboytes", "Antunez", "Maldonado",
                   "Caudillo", "Figeroa", "Socarras", "Anzaldo", "Dorta", "Saldierna", "Morejon", "Dilone", "Ardila",
                   "Rolon", "Batres", "Serpa", "Sainz", "Class", "Baldonado", "Valladares", "Londono", "Jaimez",
                   "Rondon", "Oseguera", "Sena", "Otero", "Cevallos", "Garate", "Pimienta", "Lopezcruz", "Gutierrez",
                   "Alatorre", "Terriquez", "Villanueva", "Fonseca", "Cajamarca", "Penate", "Granda", "Balleza",
                   "Laracuente", "Macias", "Gamez", "Larrea", "Barillas", "Chihuahua", "Bustamante", "Palomares",
                   "Barona", "Grimaldo", "Villela", "Zaragoza", "Rendon", "Resto", "Galaz", "Artiles", "Polo", "Roman",
                   "Conchas", "Concepcion", "Cacho", "Melena", "Fiorentino", "Delcarmen", "Contreras", "Argumedo",
                   "Alaniz", "Avina", "Arbelaez", "Palacios", "Severino", "Vidal", "Zamorano", "Pacheco", "Verastegui",
                   "Pulido", "Morena", "Hidalgo", "Ovalle", "Ravelo", "Mejias", "Higareda", "Trejos", "Perezlopez",
                   "Gomezlopez", "Dealba", "Esquivias", "Zaldana", "Barela", "Muzquiz", "Cadena", "Barberena",
                   "Casarez", "Montanez", "Coss", "Espinosa", "Mascorro", "Canez", "Neyra", "Sepulveda", "Reta",
                   "Quijano", "Delosreyes", "Escandon", "Trinidad", "Esteves", "Matta", "Paucar", "Talamante",
                   "Manrique", "Melecio", "Mendez", "Duran", "Bracamonte", "Tabora", "Casanova", "Cisnero", "Lazaro",
                   "Loyola", "Panduro", "Bojorquez", "Marchan", "Reynoso", "Mujica", "Villalona", "Urenda", "Ruano",
                   "Sola", "Yepes", "Maes", "Oliva", "Cueto", "Brea", "Vallin", "Barajas", "Uriostegui", "Segura",
                   "Moya", "Banderas", "Andrades", "Lovato", "Pompa", "Nunez", "Maria", "Morfin", "Castor", "Laureano",
                   "Trochez", "Valverde", "Salto", "Raudales", "Velez", "Escobar", "Capistran", "Martinezgarcia",
                   "Matias", "Leandro", "Portales", "Coello", "Urieta", "Benitez", "Tellez", "Bayona", "Degollado",
                   "Rijo", "Marrufo", "Dorame", "Guity", "Colorado", "Saldivar", "Salvador", "Abrego"]}

native_american_names = {
    "last_names": ["Rosetta", "Todechine", "Jock", "Custalow", "Blacklance", "Stcyr", "Littledog", "Charette", "Sunday",
                   "Tritt", "Gene", "Tecumseh", "Tarbell", "Capitan", "Poyer", "Swimmer", "Navajo", "Blackbear",
                   "Holgate", "Tubby", "Fragua", "Maybee", "Silversmith", "Malmay", "Dubray", "Braveheart", "Wallette",
                   "Tallbull", "Bigbear", "Osceola", "Redeagle", "Goodbird", "Shomo", "Leask", "Blackeagle", "Treat",
                   "Medicinehorse", "Lameman", "Dixey", "Davids", "Bark", "Mcanally", "Keeto", "Larvie", "Hilderbrand",
                   "Greybear", "Beaudry", "Burshia", "Harker", "Mouse", "Tommy", "Killion", "Whiteface", "Nastacio",
                   "Douville", "Liner", "Maracle", "Lossiah", "Cly", "Tsinnijinnie", "Vandiver", "Shorthair", "Colombe",
                   "Becenti", "Atene", "Poolaw", "Prue", "Oldbear", "Chair", "Waseta", "Bitsue", "Ironwing",
                   "Vermillion", "Peynetsa", "Sepulvado", "Alden", "Whitehair", "Ironcloud", "Billy", "Daw",
                   "Yellowhair", "Whitewolf", "Nosie", "Littlethunder", "Hollowhorn", "Hillis", "Fleury", "Printup",
                   "Martine", "Pappan", "Gooday", "Moquino", "Mohawk", "Nason", "Dushkin", "Topping", 
                   "Killsnight", "Gust", "Finkbonner", "Edaakie", "Stiffarm", "Butterfly", "Skinaway", "Shanta",
                   "Cosen", "Cisco", "Cadotte", "Blackdeer", "Capoeman", "Tsinnie", "Danforth", "Atcitty", "Bitsoi",
                   "Demoski", "Ghost", "Angaiak", "Belgarde", "Charley", "Valliere", "Lasiloo", "Ike", "Pinkham",
                   "Fasthorse", "Truax", "Parkhurst", "Whiteowl", "Longee", "Mountain", "Spottedeagle", "Andreas",
                   "Elm", "Littlebear", "Cozad", "Deswood", "Lehi", "Warrington", "Bigeagle", "Twiss", "Valley",
                   "Hubbell", "Labatte", "Adakai", "Apachito", "Flute", "Arviso", "Talk", "Klain", "Max", "Standridge",
                   "Woodman", "Manygoats", "Schurz", "Toya", "Herrod", "Kingfisher", "Eades", "Reevis", "Whiteplume",
                   "Stabler", "Evan", "Bitsoie", "Cassa", "Beyale", "Lieb", "Valandra", "Vallo", "Wildcat", "Girty",
                   "Suina", "Lamebull", "Yandell", "Drennan", "Funmaker", "Renville", "Mesteth", "Decory", "Gordy",
                   "Garfield", "Gardipee", "Redstar", "Wassillie", "Fred", "Hooke", "Verrett", "Ivanoff", "Lecompte",
                   "Juneau", "Wahnee", "Delozier", "Deerinwater", "Maney", "Shangin", "Twitchell", "Jumper",
                   "Runningcrane", "Enjady", "Grinnell", "Masten", "Laverdure", "Haskie", "Demarrias", "Redeye",
                   "Parisien", "Trueblood", "Cayaditto", "Yellowbird", "Bohanan", "Broncheau", "Yahola", "Bercier",
                   "Whitecloud", "Seminole", "Tobey", "Sarracino", "Willow", "Littlewolf", "Neztsosie", "Whitebird",
                   "Denoyer", "Yellowhorse", "Norcross", "Bowekaty", "Adson", "Youpee", "Blackbird", "Bevins", "Enno",
                   "Ganadonegro", "Brien", "Ezernack", "Duane", "Paddock", "Goodbear", "Cayou", "Tessay", "Whitehat",
                   "Rhodd", "Cypress", "Foret", "Ofield", "Ducheneaux", "Decorah", "Yellowboy", "Halwood", "Tohannie",
                   "Williston", "Roubideaux", "Slim", "Gambler", "Declay", "Fastwolf", "Belcourt", "Hornbuckle",
                   "Hoskie", "Carlile", "Thinn", "Blackwater", "Rattler", "Blacksmith", "Nicolai", "Charlie",
                   "Charbonneau", "Trosclair", "Stick", "Notafraid", "Salway", "Sando", "Teeple", "Bellanger", "Ramone",
                   "Kalmakoff", "Suke", "Valdo", "Kenneth", "Pickup", "Diver", "Keeble", "Ayze", "Deacon",
                   "Buster", "Frankson", "Hogner", "Eaglestar", "Gopher", "Whitebear", "Makil", "Marcellais", "Barse",
                   "Pioche", "Stops", "Nockideneh", "Mustache", "Quiver", "Wauneka", "Polacca", "Ojibway", "Tunney",
                   "Mangan", "Blackcloud", "Stalker", "Cuch", "Slinkey", "Sagataw", "Alloway", "Bekis", "Sully",
                   "Lomayaktewa", "Zahne", "Dry", "Haukaas", "Dundas", "Billie", "Chickaway", "Bushman", "Gonnie",
                   "Smoker", "Redwine", "Kanuho", "Bitsui", "Leno", "Wayman", "Latray", "Bodfish", "Maize", "Isham",
                   "Oxendine", "Roanhorse", "Smiling", "Bonnie", "Birdshead", "Fryberg", "Blackowl", "Barnaby",
                   "Walkingstick", "Delorme", "Tullie", "Sherlock", "Quaderer", "Blackcrow", "Freemont", "Saunooke",
                   "Kie", "Pigeon", "Nephew", "Boni", "Comby", "Standingbear", "Bagola", "Kenton", "Fulwilder", "Cata",
                   "Stgermaine", "Todacheene", "Raper", "Bia", "Haven", "Stately", "Jojola", "Yazzie", "Ironhawk",
                   "Poitra", "Charboneau", "Homer", "Pitka", "Bigby", "Monette", "Brunet", "Natonabah", "Newago",
                   "Kessay", "Rabbit", "Killsinwater", "Twocrow", "Watchman", "Dazen", "Montour", "Benge", "Chischilly",
                   "Katchatag", "Hosteen", "Blackhawk", "Arquette", "Fixico", "Sevenstar", "Gervais", "Justin",
                   "Mexicano", "Botts", "Payer", "Redcloud", "Seyler", "Jeanotte", "Hilburn", "Beans", "Bert", "Fuson",
                   "Horsechief", "Garbow", "Brisbois", "Johnny", "Laroche", "Hatathlie", "Stead", "Heminger", "Babbitt",
                   "Bitsinnie", "Highelk", "Evanoff", "Malaterre", "Logg", "Dauphinais", "Chancellor", "Battise",
                   "Bonito", "Broncho", "Danks", "Doxtator", "Tallchief", "Carrick", "Ironshell", "Monte",
                   "Heavyrunner", "Madplume", "Solet", "Lazore", "Flett", "Chaisson", "Honie", "Blackfox", "Clah",
                   "Vivier", "Limberhand", "Girdner", "Spino", "Shangreaux", "Demientieff", "Birdinground", "Edmo",
                   "Dosela", "Bordeaux", "Tall", "Quinton", "Wind", "Claymore", "Manheimer", "Deschine", "Burd",
                   "Shortman", "Mccovey", "Harney", "Zunie", "Salois", "Twoeagle", "Seabolt", "Smoke", "Whiterock",
                   "Blossom", "Drywater", "Doney", "Poncho", "Whitewater", "Chief", "Bill", "Grass", "Traversie",
                   "Whiteeyes", "Bitsuie", "Beston", "Spottedwolf", "Arch", "Russel", "Mexican", "Bullbear",
                   "Cournoyer", "Rondeau", "Tsoodle", "Coriz", "Augare", "Shakespeare", "Roehl", "Lafave", "Echohawk",
                   "Goodluck", "Vanderpool", "Quam", "Yankton", "Tahy", "Kindelay", "Spry", "Kipp", "Tony", "Benny",
                   "Lente", "Labarge", "Boivin", "Stash", "Parisian", "Naha", "Stclaire", "Amyotte", "Steven", "Decora",
                   "Abrahamson", "Gritts", "Jandreau", "Gasper", "Shije", "Fallis", "Bible", "Yelloweagle", "Kinsel",
                   "Redhair", "Rouillard", "Leviner", "Worcester", "Largo", "Mccurtain", "Moose", "Waukau", "Sisto",
                   "Blackie", "Deese", "Dickenson", "Factor", "Neptune", "Lamere", "Allery", "Bowker", "Cambridge",
                   "Nicholai", "Twohearts", "Tsethlikai", "Meshell", "Azure", "Blueeyes", "Owle", "Jourdain",
                   "Eagleman", "Descheny", "Secody", "Tourtillott", "Holmberg", "Graymountain", "Tachine", "Yallup",
                   "Laclair", "Dardar", "Peneaux", "Analla", "Deckard", "Pancho", "Tocktoo", "Morningstar",
                   "Archambault", "Battiest", "Marchand", "Youngbird", "Fallsdown", "Redhouse", "Watahomigie", "Alcott",
                   "Mescal", "Numkena", "Deverney", "Brunette", "Teton", "Stands", "Alexie", "Mcnac", "Antone",
                   "Greeley", "Herder", "Brake", "Ninham", "Eustace", "Benallie", "Ahhaitty", "Hostler", "Honea",
                   "Loring", "Goulet", "Metoxen", "Parton", "Clyde", "Smallcanyon", "Horse", "Benally", "Ballot",
                   "Gilpin", "Bighorse", "Bedoni", "Redwing", "Pilcher", "Dougi", "Lirette", "Whitebuffalo", "Tsosie",
                   "Lodrigue", "Yellowhawk", "Canuto", "Whiteshirt", "Bigboy", "Sockey", "Cottier", "Madosh",
                   "Whisenhunt", "Slick", "Mcculley", "Paquin", "Shamblin", "Jimmie", "Bowannie", "Whitehouse",
                   "Ellenwood", "Ebarb", "Segay", "Slivers", "Devereaux", "Nomee", "Siers", "Snowball", "Tulley",
                   "Skenadore", "Laughter", "Leith", "Kameroff", "Decoteau", "Russette", "Belone", "Chasinghawk",
                   "Denetsosie", "Twist", "Weasel", "Etcitty", "Iceman", "Trudell", "Belonga", "Lafontaine", "Brave",
                   "Silverhorn", "Jimmy", "Thunder", "Brunk", "Wesaw", "Paxson", "Oakgrove", "Naquin", "Tommie",
                   "Littledave", "Wheelock", "Fawcett", "Blackhorse", "Mix", "Gunhammer", "Rope", "Larock", "Keeswood",
                   "Wero", "Eddie", "Cesspooch", "Torivio", "Waupoose", "Descheenie", "Skye", "Mcgirt", "Bighorn",
                   "Chatlin", "Ivins", "Procell", "Laplant", "Apache", "Thundercloud", "Lonebear", "Rodrigue",
                   "Realbird", "Livers", "Siow", "Keplin", "Marris", "Redhorn", "Kaquatosh", "Bigcrow", "Pahe",
                   "Whitford", "Hot", "Vielle", "Tortice", "Julius", "Arrow", "Swayney", "Dollar", "Goudreau",
                   "Longsoldier", "Ami", "Wilber", "Lohnes", "Goombi", "Terrance", "Cohoe", "Altaha", "Desjarlais",
                   "Bettelyoun", "Clairmont", "Ladeaux", "Booqua", "Loonsfoot", "Wassilie", "Frechette", "Redowl",
                   "Gunville", "Spottedelk", "Narcia", "Yeahquo", "Turtle", "Lafountain", "Baptisto", "Ahasteen",
                   "Oscar", "Woodell", "Soap", "Whitefeather", "Leclaire", "Fineday", "Morigeau", "Otten", "Drift",
                   "Blackgoat", "Wadena", "Goggleye", "Calabaza", "Shendo", "Cheatwood", "Whitebull", "Caulder", "Leaf",
                   "Stites", "Dock", "Silk", "Norberto", "Jourdan", "Martineau", "Paisano", "Gregoire", "Redshirt",
                   "Bullis", "Warrior", "Arcoren", "Stensgar", "Nofire", "Labelle", "Bahe", "Adolph", "Caddo", "Croy",
                   "Littlebird", "Desiderio", "Lussier", "Lafromboise", "Colelay", "Roan", "Polty", "Hoptowit", "Andy",
                   "Courville", "Begay", "Buffalohead", "Gouge", "Peaches", "Poorbear", "Barbone", "Yazza", "Farve",
                   "Bigpond", "Laducer", "Weahkee", "Belvin", "Ranger", "Jumbo", "Keezer", "Trancosa", "Mousseau",
                   "Cassadore", "Big", "Sawney", "Edenshaw", "Swallow", "Snake", "Halona", "Soulier", "Waskey",
                   "Catron", "Denetso", "Orso", "Hugs", "Spoonhunter", "Seneca", "Vandever", "Skenandore", "Joe",
                   "Holyan", "Basina", "Twinn", "Gachupin", "Callison", "Bitsilly", "Standingrock", "Lefthandbull",
                   "Purser", "Narcho", "Baloo", "Deroche", "Nickey", "Henio", "Goldtooth", "Honanie", "Cheromiah",
                   "Begody", "Larocque", "Tahe", "Tisi", "Cuny", "Paden", "Redday", "Chippewa", "Deatherage",
                   "Dreadfulwater", "Blatchford", "Keyonnie", "Bluebird", "Verret", "Thunderhawk", "Littlewhiteman",
                   "Runningbear", "Gokey", "Hunnicutt", "Billsie", "Tomah", "Standing", "Chapo", "Littlewind", "Steve",
                   "Buffalo", "Goseyun", "Redbird", "Corbine", "Villebrun", "Duboise", "Looper", "Lebeau", "Cheater",
                   "Reano", "Chinana", "Rolin", "Yepa", "Perrault", "Melot", "Clitso", "Mcgehee", "Walkingeagle",
                   "Blackwolf", "Larney", "Kellywood", "Abeita", "Muskrat", "Billey", "Marrietta", "Yellowman",
                   "Laroque", "Bow", "Lalio", "Cree", "Countryman", "Chavarillo", "Sleeper", "Buckles", "Pelt", "Fatt",
                   "Catches", "Stopp", "Hillaire", "Firethunder", "Garrow", "Ludlow", "Dumont", "Primeaux", "Payment",
                   "Armajo", "Chatto", "Bohanon", "Fleetwood", "Kerley", "Feather", "Kingbird", "Twobulls", "Arpan",
                   "Bushyhead", "Ballou", "Lestenkof", "Standingelk", "Osife", "Amiotte", "Dumarce", "Poupart",
                   "Kallestewa", "Orcutt", "Lansing", "Lowrey", "Nick", "Bruguier", "Desautel", "Weddell", "Powless",
                   "Eriacho", "Berryhill", "Kisto", "Postoak", "Whiteeagle", "Tilden", "Etsitty", "Parfait", "Crank",
                   "Kokrine", "Milford", "Dake", "Claw", "Secatero", "Redelk", "Spang", "Lavallie", "Iron",
                   "Kaulaity", "Evon", "Messerly", "Hyden", "Skeets", "Chiago", "Dann", "Waln", "Impson",
                   "Antelope", "Loftis", "Brunelle", "Kettle", "Littleman", "Cowboy", "Dedman", "Picotte", "Redfeather",
                   "Skeet", "Brockie", "Peone", "Todacheenie", "Marceau", "Burbank", "Goodshield", "Grimmett", "Oldman",
                   "Silago", "Rexford", "Namoki", "Summerfield", "Haskan", "Oats", "Spottedbear", "Panther", "Gladue",
                   "Springwater", "Talayumptewa", "Kompkoff", "Colegrove", "Gobert", "Pecos", "Lasley", "Olanna",
                   "Zuni", "Denetclaw", "Wanna", "Denison", "Deere", "Windyboy", "Tabaha", "Deer", "Swett", "Vanzile",
                   "Racine", "Trottier", "Redfox", "Demontiney", "Active", "Werito", "Dull", "Chosa", "Columbus",
                   "Sylestine", "Bedonie", "Runninghawk", "Janis", "Bigman", "Alberts", "Bourdon", "Poorman", "Drapeau",
                   "Longie", "Delgarito", "Matt", "Bob", "Birdtail", "Astor", "Badonie", "Greymountain", "Cadman",
                   "Littlelight", "Olney", "Jeff", "Whitekiller", "Gishie", "Bancroft", "Nayokpuk", "Hugo",
                   "Jumpingeagle", "Tobacco", "Chalepah", "Manymules", "Teller", "Mcgeshick", "Archambeau", "Aday",
                   "Rickman", "Aleck", "Nez", "Bitsie", "Laughing", "Flyinghorse", "Cate", "Sixkiller", "Whitehawk",
                   "Merculief", "Buckman", "Tartsah", "Saunsoci", "Rustin", "Kitcheyan", "Lupe", "Tatsey", "Tapaha",
                   "Ethelbah", "Werk", "Demmert", "Bresette", "Pearman", "Defoe", "Loretto", "Fourkiller", "Guerue",
                   "Laforge", "Bobelu", "Neadeau", "Grignon", "Attakai", "Shorty", "Americanhorse", "Dejolie", "Carle",
                   "Creppel", "Greyeyes", "Pepion", "Dupris", "Tyndall", "Keams", "Gourneau", "Ketcher", "Lafountaine",
                   "Whitehorse", "Gwin", "Youngman", "Cosay", "Vicenti", "Northrup", "Minthorn", "Lonewolf", "Teehee",
                   "Pourier", "Mckerchie", "Dugi", "Brigman", "Shoemake", "Dayzie", "Bremner", "Nault", "Gourd", "Noah",
                   "Onefeather", "Whiteshield", "Ladue", "Coho", "Buzzard", "Parrie", "Zephier", "Quickbear",
                   "Turcotte", "Scraper", "Autaubo", "Herne", "Conners", "Morsette", "Hummingbird", "Bissonette",
                   "Byington", "Ridgway", "Stillday", "Locklear", "Corn", "Schuyler", "Muskett", "Manuelito", "Star",
                   "Blackelk", "Causley", "Peshlakai", "Mute", "Pewo", "Drum", "Bread", "Vanpelt", "Mose",
                   "Begaye", "Lefthand", "Spottedhorse", "Yoe", "Redhorse", "Pakootas", "Locust", "Badoni", "Clown",
                   "Lamont", "Seaboy", "Jake", "Bilagody", "Watashe", "Hinman", "Concho", "Notah", "Guardipee", "Lena",
                   "Speck", "Laduke", "Chuculate", "Waska", "Youngbear", "Feathers", "Pine", "Elk", "Eskeets",
                   "Tonasket", "Redbear", "Tah", "Maupin", "Eder", "Rave"]}

asian_names = {
    "first_names": ["Tailor", "Bhalla", "Look", "Roh", "Hao", "Bi", "Bunag", "Char", "Ravi", "Sunny", "Balasubramaniam",
                    "Yoshimoto", "Nay", "Shu", "Subramanian", "Moala", "Parveen", "Jeremy", "Gary", "Alisa", "Savannah",
                    "Zayan", "Arham", "Kate", "Sharon", "Jenna", "Alisha", "Leela", "Lauren", "Eva", "Kaitlyn",
                    "Mikael", "Joy", "Leah", "Tyler", "Kayden", "Crystal", "Mohamed", "Jason", "Myra", "Michael",
                    "Taylor", "Elise", "Lucy", "Maxwell", "Ayesha", "Zain", "Mohammed", "Erica", "Ava", "Harper",
                    "Doris", "Abdul", "Farhan", "Carina", "Lily", "Jessie", "Valerie", "Selina", "Alina", "Kevin",
                    "Amara", "Mandy", "Jace", "Eshal", "Tiffany", "Annie", "Samara", "Kyle", "Wendy", "Avery", "Shreya",
                    "Sabrina", "Xavier", "Anisha", "David", "Hayden", "Evelyn", "Bruce", "Leanna", "Hazel", "Bryan",
                    "Alan", "Amina", "Alexis", "Shayaan", "Lisa", "James", "Eileen", "Hanna", "Jasmine", "Nolan",
                    "Jocelyn", "Christy", "Anaya", "Kazi", "Samantha", "Nathan", "Raina", "Isla", "Alston", "Chelsea",
                    "Timothy", "Anthony", "Abdullah", "Ahad", "Gianna", "Jannatul", "Calvin", "Max", "Sarah", "Ashley",
                    "Jannat", "Sheldon", "Evan", "Aria", "Claire", "Kian", "Jun", "Veer", "Esther", "Elsa", "Diya",
                    "Eric", "Xander", "Yahya", "Amaya", "Vincent", "Arya", "Musa", "Lucas", "Hailey", "Karina", "Theo",
                    "Phoebe", "Tristan", "Brian", "Andrew", "Damon", "Devin", "Krish", "Md", "William", "Tanisha",
                    "Queenie", "Maryam", "Aliza", "Aileen", "Alvin", "Khadija", "Richard", "Owen", "Inaya", "Gavin",
                    "Elliot", "Hamza", "Hassan", "Ada", "Liyana", "Kimberly", "Helen", "Maximilian", "Daphne", "Manha",
                    "Diana", "Skylar", "Ishaan", "Arthur", "Ella", "Isaac", "Amira", "Sabiha", "Kenneth", "Derrick",
                    "Maya", "Luke", "Eleanor", "Madison", "Henry", "Arisha", "Maggie", "Kaleb", "Gabriel", "Shirley",
                    "Irene", "Ryder", "Zayn", "Niam", "Arjun", "Khloe", "Leon", "Amber", "Laura", "Joanna", "Bodhi",
                    "Zoey", "John", "Micah", "Danny", "Bonnie", "Saifan", "Nathaniel", "Emmanuel", "Kingsley", "Nikhil",
                    "Kira", "Aliyah", "Ophelia", "Adrian", "Jolin", "Keira", "Ahnaf", "Carter", "Scarlett", "Olivia",
                    "Angel", "Aurora", "Frank", "Sara", "Justin", "Felix", "Safa", "Selena", "Omar", "Rayyan", "Ariel",
                    "Armaan", "Johnny", "Nicholas", "Robert", "Kiara", "Christian", "Vanessa", "Ayra", "Ethan", "Cindy",
                    "Samuel", "Madelyn", "Gabriella", "Stephanie", "Emilia", "Vicky", "Lillian", "Brandon", "Miya",
                    "Ariella", "Levi", "Cecilia", "Aden", "Mila", "Mira", "Nina", "Mason", "Maliha", "Eden", "Abby",
                    "Winston", "Liana", "Tony", "Alyssa", "Livia", "Ahmed", "Lydia", "Syeda", "Kimi", "Steven",
                    "Sophia", "Celine", "Aayat", "Kai", "Christopher", "Peter", "Ahmad", "Joshua", "Luca", "Spencer",
                    "Lina", "Harry", "Ananya", "Edward", "Safwan", "Amir", "Sulaiman", "Stanley", "Jacob", "Aarav",
                    "Ivaan", "Feynman", "Mark", "Isabella", "Thomas", "Joyce", "Connor", "Fiona", "Carson", "Aliya",
                    "Stella", "Megan", "Jerry", "Theodore", "Elijah", "Aleena", "Abrar", "Elias", "Colin", "Alexander",
                    "Elena", "Simon", "Zachary", "Chloe", "Subhan", "Jasper", "Josephine", "Vera", "Rayna", "Eliana",
                    "Eshan", "Skyler", "Hunter", "Lawrence", "Ashton", "Adam", "Anson", "Catherine", "Sophie", "Jaden",
                    "Erin", "Enzo", "Nora", "Anya", "Louis", "Linda", "Sienna", "Cynthia", "Jimmy", "Angelina", "Yu",
                    "Layla", "Derek", "Isabel", "Samaira", "Adyan", "Eddie", "Wilson", "Alexa", "Ayan", "Eason",
                    "Mohammad", "Alicia", "Clara", "Rebecca", "Jessica", "Nicole", "Dua", "Raymond", "Julian",
                    "Charlotte", "Muhammad", "Anisa", "Katie", "Alexandra", "Naomi", "Edwin", "Aaron", "Reina",
                    "Summer", "Aayan", "Oscar", "Rohaan", "Elaine", "Lila", "Nelson", "Kaden", "Preston", "Isaiah",
                    "Jackson", "Norah", "Tahmid", "Shayan", "Anderson", "Terrence", "Hoorain", "Priscilla", "Andy",
                    "Roy", "Neil", "Matthew", "Katelyn", "Daisy", "Jamie", "Albert", "Dylan", "Liam", "Erika",
                    "Ayden", "Harrison", "Austin", "Darren", "Madeline", "Riya", "Angela", "Alfred", "Tenzin", "Tasnim",
                    "Grayson", "Ismail", "Iris", "Isabelle", "Jenny", "Brayden", "Bowen", "Anna", "Aiden", "Syed",
                    "Sarina", "Elizabeth", "Ricky", "Mina", "Brianna", "Allison", "Winnie", "Queena", "George", "Emma",
                    "Shawn", "Zoe", "Jia", "Kenny", "Kelly", "Julia", "Miranda", "Wyatt", "Amanda", "Caroline", "Anika",
                    "Bradley", "Audrey", "Ayaan", "Jeffrey", "Hao", "Ellie", "Natalie", "Vivian", "Sahil", "Sunny",
                    "Vihaan", "Faith", "Tina", "Eunice", "Leila", "Melanie", "Hana", "Hashim", "Saif", "Allen",
                    "Haniya", "Aaliyah", "Lia", "Rayan", "Cameron", "Ali", "Inaaya", "Nabiha", "Logan", "Terry",
                    "Riley", "Daniel", "Penelope", "Ivan", "Sebastian", "Luna", "Ian", "Violet", "Victor", "Aizah",
                    "Ayat", "Cody", "Jacqueline", "Eli", "Kaia", "Anjali", "Alice", "Hafsa", "Azaan", "Michelle",
                    "Ryan", "Katherine", "Marcus", "Noor", "Parker", "Rachel", "Edison", "Rehan", "Aidan", "Anne",
                    "Caleb", "Nusrat", "Jayden", "Kingston", "Gordon", "Amy", "Dean", "Roman", "Anayah", "Alayna",
                    "Sylvia", "Mia", "Asher", "Hannah", "Abigail", "Arianna", "Sofia", "Sherry", "Aarya", "Aahil",
                    "Serena", "Martin", "Lincoln", "Gia", "Chris", "Karen", "Bella", "Cyrus", "Madeleine", "Jennifer",
                    "Annika", "Sydney", "Elvis", "Giselle", "Mustafa", "Zainab", "Annabelle", "Connie", "Rohan", "Ruby",
                    "Renee", "Travis", "Aaryan", "Jonathan", "Hugo", "Christine", "Sean", "Jordan", "Arvin", "Kylie",
                    "Yusuf", "Kayla", "Oliver", "Aiza", "Muntaha", "Janice", "Jacky", "Khadijah", "Meera", "Ariana",
                    "Judy", "Emily", "Wesley", "Brendan", "Grace", "Xin", "Rhea", "Victoria", "Aisha", "Alex", "Joseph",
                    "Josiah", "Mahnoor", "Kabir", "Benjamin", "Mariam", "Hudson", "Leo", "Angus", "Noah", "Landon",
                    "Leonardo", "Emaan", "Benson", "Aditya", "Caden", "Patrick", "Angie", "Ivy", "Anabia", "Zara",
                    "Kyson", "Eshaal", "Yuna", "Charles", "Elina", "Amelia", "Ibrahim", "Kaylee", "Athena", "Christina",
                    "Zahra", "Cayden", "Melody", "Jack", "Hareem", "Jake", "Jay", "Zoya", "Aryan", "Aydin", "Fatima",
                    "Lena", "Chase"],

    "last_names": ["Nhan", "Yao", "Jou", "Buenaventura", "Shwe", "Lou", "Thai", "Shirai", "Mai", "Bhasin",
                   "Senthilkumar", "Zulueta", "Sor", "Jen", "Soundara", "Francia", "Miah", "Abidi", "Pancholi",
                   "Muranaka", "Chao", "Ramesh", "Koyama", "Vakharia", "Chang", "Kawabata", "Tengan", "Caballes",
                   "Manivong", "Cun", "Lhamo", "Hirano", "Arun", "Hum", "Hariharan", "Manaloto", "Ni", "Chen", "Len",
                   "Tani", "Huq", "Chiba", "Kalra", "Kham", "Sinha", "Miyoshi", "Manalastas", "Matsuoka", "Balagtas",
                   "Matharu", "Ao", "Matsuno", "Latif", "Nayyar", "Yon", "Hsiao", "Tamashiro", "Bath", "Halim", "Acoba",
                   "Soy", "Jamil", "Almario", "Kosaka", "Shakeel", "Soliven", "Tandoc", "Kafley", "Dayal", "Minhas",
                   "Potluri", "Kuwahara", "Ramasamy", "Ramones", "Goel", "Pathan", "Batra", "Fan", "Mukai", "Huda",
                   "Aftab", "Kazi", "Azad", "Tsu", "Nishiyama", "Zhai", "Rosal", "Makwana", "Matsuura", "Shum",
                   "Charania", "Talati", "Lagman", "Im", "Ramchandani", "Sanluis", "Barua", "Tesoro", "Sham", "Jared",
                   "Karnik", "Phouthavong", "Lo", "Saluja", "Taneja", "Quadri", "Kwok", "Cinco", "Torio", "Farooqi",
                   "Sikder", "Noguchi", "Goh", "Nakai", "Rozario", "Qian", "Shafi", "Guiang", "Somera", "Pandey",
                   "Mian", "Song", "Katayama", "Sanpedro", "Apte", "Hoo", "Ghosh", "Jow", "Salud", "Prum", "Cho",
                   "Danh", "Tamondong", "Pagdilao", "Dancel", "Tewari", "Jan", "Asai", "Rana", "Sachdev", "Halder",
                   "Hayakawa", "Narasimhan", "Sahai", "Bansal", "Thakur", "Sawada", "Hor", "Tham", "Foronda",
                   "Thammavongsa", "Vue", "Nonaka", "Miyahara", "Huy", "Lagasca", "Chon", "Kamal", "Shiraishi", "Chap",
                   "Pao", "Advincula", "Sapkota", "Talukder", "Naseem", "Kundu", "Sakuma", "Voong", "Hur", "Nip",
                   "Yokoyama", "Ravindran", "Wi", "Veloso", "Meas", "Kanno", "Sridharan", "Quizon", "Ren", "Kishore",
                   "Shahi", "Matsui", "Nepomuceno", "Thakker", "Mahajan", "Thapa", "Soo", "Hirani", "Akhtar", "Riaz",
                   "Lomboy", "Lei", "Hwang", "Khatoon", "Maqsood", "Tiu", "Mir", "Miyazaki", "Andal", "Menon", "Joung",
                   "Shang", "Jew", "Siddiqui", "Mascarenhas", "Kaya", "Khan", "Shergill", "Sandhu", "Mok", "Wah",
                   "Ramalingam", "Madarang", "Tonga", "Majumder", "Bagga", "Liem", "Edralin", "Tuong", "Basa", "Bista",
                   "Nath", "Zheng", "Sahni", "Sohail", "Pho", "Khare", "Lock", "Naidu", "Yum", "Yun", "Kothari",
                   "Rizal", "Liu", "Duggal", "Chern", "La", "Rama", "Tiwana", "Om", "Sherpa", "Teruya", "Mohapatra",
                   "Nand", "Szeto", "Thapar", "Parayno", "Qadri", "Takano", "Takaki", "Ikram", "Paw", "Guan", "Fang",
                   "Zhou", "Ona", "Sohi", "Foo", "Bayani", "Manzoor", "Quiambao", "More", "Si", "Tupas", "Yoshioka",
                   "Furuta", "Nakanishi", "Junio", "Kiang", "Soohoo", "Wijaya", "Villaruz", "Oba", "Ibay", "Banu",
                   "Murayama", "Toyama", "Khosla", "Shastri", "Kang", "Yousaf", "Khadka", "Sundararajan", "Halili",
                   "Biju", "Venkat", "Ya", "Jin", "Amir", "Yoon", "Sarin", "Chaudhri", "Madamba", "Tsutsui", "Terada",
                   "Payumo", "Touch", "Chim", "Narine", "Dev", "Seok", "Kodali", "Durrani", "Saesee", "Tsou", "Sul",
                   "Amante", "Basra", "Luthra", "Karthikeyan", "Hung", "Fong", "Galiza", "Jaffer", "Konishi",
                   "Benedicto", "Jeng", "Paraiso", "Haq", "Lalani", "Shee", "Mainali", "Isip", "Varkey", "Weng", "Kum",
                   "Sachdeva", "Malonzo", "Sakaguchi", "Uong", "Manlapaz", "Araki", "Motiwala", "Acharya", "Varshney",
                   "Mehdi", "Dhir", "Cung", "Nakatani", "Tripathi", "Kalidindi", "Bo", "Atienza", "Yin", "Suri", "Kil",
                   "Chuong", "Chien", "Sriram", "Lan", "Jindal", "Ruan", "Ganguly", "Phon", "Kadakia", "Mamaril",
                   "Asano", "Pol", "Vaghela", "Zahid", "Challa", "Bassi", "Hori", "Pong", "Siddiqi", "Khanal",
                   "Sultana", "Dabu", "Thao", "Zhuang", "Ioane", "Mathur", "Phann", "Villaflor", "Rajagopalan",
                   "Nishioka", "Matsuyama", "Naito", "Sua", "Ran", "Nessa", "Hanif", "Maeng", "Asis", "Cheuk",
                   "Narayanan", "Ozaki", "Sanghera", "Akram", "Pun", "Lama", "Hafeez", "Lacuesta", "Menezes",
                   "Jayaraman", "Tang", "Ashraf", "Vahora", "Chhetri", "Cariaga", "Otani", "Shakir", "Delkcruz", "Wada",
                   "Kikuchi", "Pok", "Hem", "Shafiq", "Shankar", "Master", "Kansara", "Cai", "Phung", "Yue", "Mitra",
                   "Paudel", "Sim", "Akamine", "Nisa", "Mahal", "Panjwani", "Kale", "Shenoy", "Qi", "Dinh", "Adnan",
                   "Htoo", "Subramaniam", "Policarpio", "Huang", "Paule", "Bolosan", "Chilukuri", "Chuck", "Yamanaka",
                   "Chacko", "Asim", "Ravikumar", "Desai", "Navalta", "Timsina", "Banaag", "Bae", "Ngai", "Vasudevan",
                   "Chi", "Mahadevan", "Mehta", "Baluyut", "Macadangdang", "Nguon", "Sardar", "Yem", "Jian",
                   "Vemulapalli", "Kishi", "Rim", "Pillar", "Yumul", "Ksor", "Mesina", "Nabong", "Balachandran", "Par",
                   "Vuu", "Ki", "Razzak", "Lata", "Shamsi", "Zhao", "Mizuno", "Choudhry", "Prabhu", "Adusumilli", "Suh",
                   "Sanyal", "Agnihotri", "Taketa", "Ke", "Dewan", "Jeong", "Pu", "Naval", "Munshi", "Basco", "Shamim",
                   "Nee", "Yalamanchili", "Prashad", "Wakabayashi", "Rangarajan", "Koshy", "Villarin", "Luc", "Patnaik",
                   "Magbanua", "Mistry", "Pervaiz", "Masaki", "Sue", "Dhanani", "Austria", "Langi", "Biswa", "Farooq",
                   "Phan", "Patwardhan", "Koh", "Vashi", "Ulep", "Koneru", "Manivanh", "Ma", "Cherukuri", "Yamagata",
                   "Tyagi", "Bella", "Ramiro", "Mohabir", "Matsumura", "Bahl", "Lieu", "Saelee", "Malabanan", "Wee",
                   "Surti", "Tomita", "Momin", "Afzal", "Kotha", "Jadhav", "Malhotra", "Ear", "Takhar", "Salam", "Ngu",
                   "Sattar", "Noronha", "Tee", "Alvi", "Nagano", "Thind", "Seshadri", "Der", "Hon", "Pillai", "Das",
                   "Siwakoti", "Jaswal", "Noda", "Jani", "Shams", "Puno", "Sengupta", "Hok", "Wai", "Oki", "Woon",
                   "Kun", "Arshad", "Teves", "Yonamine", "Murthy", "Hans", "Oka", "Aktar", "Koirala", "Arcilla",
                   "Iyengar", "Haroon", "Kobashigawa", "Kapadia", "Chiang", "Abuan", "Nayar", "Capulong", "Maknojia",
                   "Malek", "Ijaz", "Ghani", "Vaidya", "Chaturvedi", "Choun", "Ngo", "Lew", "Leng", "Bedi", "Jahangir",
                   "Kataria", "Subedi", "Chaudhari", "Panda", "Manalac", "Quraishi", "Dasari", "Chugh", "Somasundaram",
                   "Ashfaq", "Fazal", "Fok", "Shabbir", "Jaffery", "Duldulao", "Ramamoorthy", "Bao", "Jabbar",
                   "Yamamura", "Baloch", "Saran", "Yeom", "Saing", "Oo", "Cha", "Pathammavong", "Babu", "Abedin", "Xia",
                   "Kashyap", "Malik", "Chiu", "Gaviola", "Soeung", "Vongphakdy", "Hua", "Jang", "Nim", "Taira",
                   "Chinen", "Ngan", "Chawla", "Nagarajan", "Hamamoto", "Iftikhar", "Shibata", "Mangal", "Sutaria",
                   "Untalan", "Beharry", "Enomoto", "Furuya", "Miyahira", "Rho", "Tsuda", "Suthar", "De", "Badua",
                   "Chue", "Alikhan", "Qamar", "Masih", "Din", "Sahi", "Thi", "Chhum", "Bhatia", "Deshmukh",
                   "Gupta", "Hing", "Lapid", "Sankar", "Cabacungan", "Rafique", "Tanveer", "Guintu", "Gatdula", "Yagi",
                   "Chatterjee", "Yasin", "Hossain", "Chandrasekar", "Guo", "Macapagal", "Rafi", "Thang", "Bong",
                   "Shishido", "Imran", "Hizon", "Zhang", "Kothapalli", "Shiroma", "Cendana", "Bano", "Farooqui",
                   "Hsiung", "Soh", "Nayak", "Pili", "Sampath", "Seth", "Ando", "Cul", "Espina", "Lam", "Ige", "Banez",
                   "Rajan", "Khangura", "Cabana", "Amano", "Iwai", "Bhullar", "Nishi", "Narang", "Loi", "Sanghvi",
                   "Igarashi", "Magsino", "Irfan", "Murugesan", "Matsushima", "Sugimoto", "Safdar", "Tiwari", "Sahoo",
                   "Handa", "Kho", "Takada", "Hirose", "Puri", "Sawant", "Shahid", "Ramaswamy", "Khanom", "Manu",
                   "Orpilla", "Basnet", "Mangahas", "Aung", "Xiao", "Adhikari", "Mazhar", "Sayani", "Jiwani", "Mayeda",
                   "Park", "Lakshmanan", "Son", "Macaraeg", "Mallari", "Yung", "Takeshita", "Mushtaq", "Shiao", "Sekar",
                   "Chiao", "Rabbani", "Naing", "Dsilva", "Omori", "Nakamura", "Chio", "Ouch", "Azeem", "Soong", "Ejaz",
                   "Chhoeun", "Lyu", "Rajagopal", "Takemoto", "Tejani", "Paik", "Tuan", "Islam", "Pa", "Hui", "Hashmi",
                   "Bhatnagar", "Xi", "Ou", "Xayavong", "Phou", "Tonnu", "Uno", "Zee", "Uppalapati", "Ramiscal",
                   "Rawal", "Chander", "Bajpai", "Bun", "Rathore", "Alipio", "Kandasamy", "Co", "Vohra", "Capistrano",
                   "Choe", "Ally", "Paguirigan", "Pokharel", "Shanmugam", "Qadir", "Kwock", "Tam", "Sher", "Rafiq",
                   "Sicat", "Chhim", "Chong", "Mam", "Neupane", "Mong", "Ngov", "Sui", "Manoharan", "Aggarwal",
                   "Kurien", "Iida", "Guevarra", "Punjabi", "Chakraborty", "Quintos", "Le", "Imperial", "Luy", "Yasui",
                   "Kien", "Teo", "Mi", "Chiou", "Kwak", "Lakhani", "Ai", "Sathe", "Magpantay", "Saephan", "Kapur",
                   "Sarwar", "Laxamana", "Oun", "Rahman", "Songco", "Varadarajan", "Karri", "Sorn", "Xiang", "Aranas",
                   "Sugai", "Magar", "Barot", "Dhimal", "Jabeen", "Pasco", "Perumal", "Sankaran", "Ghaffar", "Jha",
                   "Noh", "Doan", "Amin", "Takenaka", "Salim", "Siddiq", "Ishaq", "Shoji", "Nasim", "Hin", "Kawashima",
                   "Kou", "Pradeep", "Yeo", "Liew", "Dass", "Tonthat", "Dcosta", "Randhawa", "Tada", "Penaflor",
                   "Chughtai", "Upreti", "Bandi", "Ouyang", "Chahal", "Ramcharan", "Pangan", "Kancharla", "Seang",
                   "Chhabra", "Sayavong", "Ueno", "Goyal", "Deng", "Chokshi", "Pyo", "Jassal", "Krishna", "Alapati",
                   "Ramkumar", "Chua", "Sulit", "Suguitan", "Sehgal", "Rajkumar", "Yep", "Purewal", "Ping", "Chann",
                   "Cheah", "Mannan", "Villena", "Venugopal", "Latu", "Ong", "Gowda", "Kwong", "Phal", "Ganti", "Soon",
                   "Manahan", "Ilyas", "Kieu", "Nijjar", "Gopinath", "Pilapil", "Maniar", "Khuon", "Moua",
                   "Balasubramanian", "Suk", "Akula", "Tuason", "Tith", "Situ", "Qiao", "Paulo", "Vaswani", "Toor",
                   "Thakkar", "Biswas", "Villaruel", "Nagpal", "Ching", "Leung", "Mukhopadhyay", "Philipose", "Purohit",
                   "Tanaka", "Suy", "Panicker", "Ghotra", "Regmi", "Chiong", "Lie", "Shetty", "Dy", "Dam",
                   "Arunachalam", "Inthavong", "Ganapathy", "Ek", "Amjad", "Hemani", "Ashok", "Meghani", "Catacutan",
                   "Kar", "Kishimoto", "No", "Du", "Lapuz", "Buan", "Toda", "Liou", "Sanjose", "Rattan",
                   "Chattopadhyay", "Dolma", "Okubo", "Goon", "Saraf", "Yokota", "Panganiban", "Boparai", "Prasla",
                   "Macatangay", "Usmani", "Lun", "Mandal", "Oberoi", "Cam", "Namba", "Razon", "Yu", "Zou", "Pandit",
                   "Matsuo", "Gaur", "Phommachanh", "Mui", "Kamdar", "Razzaq", "Kannan", "Cheang", "Teoh", "Bawa",
                   "Walla", "Dhingra", "Katta", "Maung", "Lingad", "Khuu", "Kaneko", "Youn", "Palisoc", "Jiang", "Vinh",
                   "Kha", "Jong", "Gorospe", "Natarajan", "Baguio", "Agpaoa", "Kamiya", "Borromeo", "Olaes", "Pagaduan",
                   "Dhungana", "Kamboj", "Varanasi", "Louie", "Balk", "Yasmin", "Akella", "Wei", "Khattak", "Kondo",
                   "Mac", "Tariq", "Tat", "Ohta", "Pamintuan", "Seki", "Kok", "Okimoto", "Que", "Saiki", "Venkatesan",
                   "Pervez", "Dalisay", "Ip", "Chun", "Tsan", "Stamaria", "Kuroda", "Choudhury", "Rathod", "Sampat",
                   "Jilani", "Bhola", "Sotto", "Brillantes", "Vachhani", "Zia", "Parikh", "Fujiwara",
                   "Saldanha", "Andrada", "Tin", "Chaudhary", "Dana", "Chui", "Shukla", "Chaudry", "Kaul",
                   "Yam", "Suda", "Tsuji", "Sze", "Kazmi", "Dhindsa", "Elahi", "Leota", "Soth", "Singhal", "Iwamoto",
                   "Cunanan", "Nishikawa", "Ny", "Bukhari", "Sethi", "Bose", "Insixiengmay", "Muramoto", "Huot",
                   "Kojima", "Caparas", "Yoshikawa", "Kurup", "Khamvongsa", "Gala", "Yuen", "Ge", "Thakar", "Raju",
                   "Aujla", "Sadiq", "Kyi", "Ilano", "Kumar", "Fukunaga", "Nawaz", "Te", "Pabla", "Sajjad", "Gupte",
                   "Nakayama", "Visitacion", "Pi", "Sa", "Okuda", "Yabut", "Ji", "Baral", "Fontanilla", "Kim", "Jim",
                   "Gang", "Yuan", "Ines", "Miu", "Lala", "Quon", "Madan", "Bang", "Balaji", "Hashim", "Ryoo", "Da",
                   "Keo", "Heer", "Viswanathan", "Agcaoili", "Jee", "Myung", "Ghuman", "Vijay", "Rigor", "Sastry",
                   "Shah", "Mall", "Santaana", "Saiyed", "Fujikawa", "Nguyen", "Ali", "Pannu", "Dionisio", "Calma",
                   "Cayabyab", "Koizumi", "Ng", "Niu", "Luu", "Zang", "Lien", "Bumanglag", "Sugiyama", "Aspiras",
                   "Miao", "Dino", "Buenviaje", "Umeda", "Parekh", "Misa", "Moy", "Cua", "Manglicmot", "Dixit", "Kido",
                   "Trinh", "Sheu", "Prasad", "Patil", "Soe", "Kissoon", "Phimmasone", "Sang", "Hong", "Manalili",
                   "Dhillon", "Uyehara", "Chari", "Dhesi", "Deperalta", "Alviar", "Auyeung", "Dulay", "Ravishankar",
                   "Han", "Tao", "Hinh", "Takara", "Hsing", "Masud", "Mehmood", "Mittal", "Vemuri", "Dungca", "Mei",
                   "Terrado", "Chuang", "Jalil", "Regala", "Mani", "Khandelwal", "Lachica", "Zhan", "Yo", "Lansang",
                   "Arca", "Lalwani", "Tecson", "Kaw", "Shariff", "Sagar", "Raut", "Nakasone", "Kuang", "Deb", "Trang",
                   "Yamashiro", "Sese", "Sunga", "Zubair", "Fujioka", "Hu", "Kabir", "Xian", "Teodoro", "Balan",
                   "Otsuka", "Buenaflor", "Brun", "Teng", "Su", "Jasti", "Dang", "Ayson", "Samala", "Miyasato",
                   "Sai", "Agha", "Capili", "Rong", "Maharjan", "Ninh", "Balakrishnan", "Hundal", "Ing", "Selvaraj",
                   "Wang", "Capati", "Sundaresan", "Bou", "Koy", "Tsai", "Topacio", "Ea", "Abueg", "Nagasawa",
                   "Jaiswal", "Garg", "Hyon", "Adachi", "Naik", "Chea", "Sakurai", "Dar", "Manickam", "Nadkarni",
                   "Vaid", "Raman", "Rami", "Yamauchi", "Niazi", "Singla", "Ka", "Abaya", "Kuan", "Mody", "Verzosa",
                   "Bokhari", "Khatiwada", "Cheung", "Choksi", "Setiawan", "Ly", "Ta", "Mochizuki", "Leang", "Leong",
                   "Yang", "Pang", "Siv", "Brar", "Saefong", "Sidhu", "Oommen", "Naseer", "Parungao", "Nakao",
                   "Sabharwal", "Panchal", "Shahzad", "Fujita", "Qu", "Baxi", "Domingo", "Chadha", "Sarkar", "Vijayan",
                   "Quitugua", "Fifita", "Javaid", "Shaik", "Kawai", "Radhakrishnan", "Panlilio", "Khin", "Chaudhuri",
                   "Kitagawa", "Mou", "Kukreja", "Doo", "Lodhi", "Marzan", "Soun", "Darjee", "Varughese", "Baek",
                   "Asato", "Landicho", "Lian", "Bharadwaj", "Rehman", "Fnu", "Kye", "Tso", "Poudel", "Ragasa",
                   "Kausar", "Raina", "Andaya", "Cabanilla", "Dave", "Sio", "Macalino", "Degracia", "Chanda", "Inamdar",
                   "Luk", "Vemula", "Pheng", "Bhandari", "Horiuchi", "Supnet", "Lavarias", "Hai", "Pasion", "Yeon",
                   "Tanabe", "Van", "Vaidyanathan", "Thieu", "Asad", "Kohli", "Faustino", "Jafri", "Tuy", "Ramani",
                   "Swamy", "Giri", "Parvin", "Shin", "Santhanam", "Hau", "Yi", "Mangat", "Ning", "Moo", "Di",
                   "Soliman", "Kashif", "Byun", "Kin", "Ryu", "Mansuri", "Liaw", "Upadhyaya", "Suresh", "Kwan", "Gip",
                   "Arya", "Zong", "Vangala", "Escano", "Ramroop", "Wu", "Oyama", "Gaddam", "Rhee", "Atluri", "Mondal",
                   "Kudo", "Yiu", "Mo", "Saha", "Aslam", "Tsao", "Ganesan", "Rajesh", "Okumura", "Liao", "Parajuli",
                   "Dhar", "Lardizabal", "Bak", "Salman", "Gan", "Hy", "Uyeno", "Khawaja", "Abellera", "Ramdass",
                   "Iwata", "Wahab", "Koo", "Tsuchiya", "Finau", "Dawood", "Nigam", "Dey", "Ramnarine", "Nagaraj",
                   "Dwivedi", "Darji", "Chowdhry", "Kolli", "Villamor", "Basdeo", "Chan", "Kem", "Mehrotra", "Asif",
                   "Sayson", "Coloma", "Tom", "Afridi", "Mughal", "Alluri", "Okazaki", "Sanagustin", "Akter", "Htwe",
                   "Trivedi", "Lum", "Fiesta", "Balingit", "Venkatachalam", "Sabado", "Loh", "Mazumder", "Dumlao",
                   "Lad", "Rin", "Magno", "Samra", "Gopal", "Gandhi", "Rizvi", "Pin", "Nadeem", "Devilla", "Narra",
                   "Khiev", "Suan", "Nandi", "Rasool", "Sangha", "Sam", "Budhu", "Solanki", "Hoang", "Estacio",
                   "Saechao", "Murugan", "Devi", "Paras", "Viado", "Rajput", "Nishida", "Ra", "Hun", "Quang", "Baik",
                   "Venkataraman", "Gunawan", "Raghunathan", "Khun", "Sahota", "Nie", "Khuc", "Dholakia", "Tak",
                   "Irani", "Em", "Widjaja", "Heo", "Ros", "Swaminathan", "Bagchi", "Saetern", "Adriano", "Reh",
                   "Malhi", "Goya", "Bhuiyan", "Arciaga", "Uppal", "Tajima", "Sharma", "Kong", "Hoque", "Prajapati",
                   "Antony", "Agbayani", "Salahuddin", "Kagawa", "Mey", "Murtaza", "Maglalang", "Eun", "Hak", "Viray",
                   "Chay", "Masood", "Yambao", "Manalang", "Manaois", "Villaluz", "Pokhrel", "Uy", "Vuong", "Srinivas",
                   "Delmundo", "Dung", "Albano", "Tummala", "Aguinaldo", "Jeung", "Aurelio", "Joshi", "Singh", "Rath",
                   "Inaba", "Kadam", "Tokunaga", "Pyon", "Altaf", "Kaushal", "Xue", "Palaniappan", "Heng",
                   "Bhattacharyya", "Braganza", "Khang", "Kadiyala", "Abadilla", "Goswami", "Tan", "Galang", "Khuong",
                   "Chak", "Sananikone", "Bhaskar", "Awasthi", "Jue", "Varghese", "Majid", "Phong", "Khurana", "Oh",
                   "Tong", "Taufa", "Yamane", "Li", "Ahmad", "Chavan", "Moorthy", "Krishnan", "Nagata", "Gao", "Nair",
                   "Sabir", "Khokhar", "Vakil", "Talwar", "Eh", "Kurian", "Parmar", "Mahmud", "Ichikawa", "Nisar",
                   "Cuaresma", "Modi", "Bay", "Lahiri", "Imamura", "Shi", "Don", "Tominaga", "Azim", "Pak", "Kaushik",
                   "Guinto", "So", "Kwon", "Mon", "Lac", "Sandiego", "Yano", "Nimmagadda", "Thakore", "Hahm", "Lukose",
                   "Pon", "Giang", "Bahadur", "Jiao", "Shen", "Nham", "Floresca", "Ramnath", "Soeun", "Un", "Nakahara",
                   "Bhatt", "Doshi", "Fu", "Dayao", "Yoshino", "Inoue", "Lagmay", "Hegde", "Lai", "Heu", "Thu", "Ghai",
                   "Xie", "Maheshwari", "Lao", "Dorjee", "Virk", "Luan", "Bajwa", "Mathew", "Varma", "Sarker", "Nasir",
                   "Lin", "Sivakumar", "Athwal", "Zeng", "Delrosario", "Jung", "Gulati", "Ramakrishnan", "Nou",
                   "Thammavong", "Marwaha", "Hira", "Nagamine", "Kono", "Zuo", "Kue", "Hue", "Pepito", "Keung",
                   "Jayaram", "Miura", "Izumi", "Ang", "Uehara", "Hironaka", "Sou", "Sridhar", "Kan", "Guha", "Shareef",
                   "Eng", "Dubey", "Vy", "Seo", "Bhardwaj", "Jing", "Sethuraman", "Ayub", "Sun", "Ilagan", "Pae",
                   "Gautam", "Younus", "Kaur", "Chalasani", "Qui", "Mung", "Makino", "Nan", "Gajjar", "Tsoi", "Talluri",
                   "Hou", "Rastogi", "Gu", "Wahid", "Chauhan", "Loc", "Konda", "Fukushima", "Yom", "Multani", "Vong",
                   "Akther", "Lwin", "Nop", "Fei", "Mallick", "Palanisamy", "Macaspac", "Ara", "Okano", "Apostol",
                   "Dalal", "Soung", "Bhagat", "Fronda", "Peng", "Ton", "Um", "Chou", "Hadi", "Sha", "Gopalan",
                   "Narain", "Kuruvilla", "Manandhar", "Doi", "Kubota", "Rane", "Nong", "Liang", "Sajid", "Tzeng",
                   "Jahan", "Chey", "Kamran", "Raval", "Miyata", "Garcha", "Mammen", "Demesa", "Dea", "Keomany", "Jia",
                   "Sao", "Sunkara", "Florendo", "Arai", "Yong", "Koga", "Taing", "Dimaano", "Ahuja", "Rawat",
                   "Khurshid", "Nam", "Sur", "Xiong", "Shroff", "Sibayan", "Marinas", "Qin", "Nuon", "Ullah", "Mandava",
                   "Ojha", "Lor", "Pangilinan", "Shan", "Gopalakrishnan", "Bindra", "Whang", "Ling", "Alo",
                   "Lach", "Senthil", "Uemura", "Dai", "Mangubat", "Waheed", "Alegado", "Mohanty", "Contractor", "Chum",
                   "Kassam", "Sen", "Tamang", "Kitamura", "Sar", "Nagao", "Mach", "Cao", "Grewal", "Tio", "Belen",
                   "Chhin", "Akiyama", "Sok", "Naveed", "Hasan", "Kamat", "Yadav", "Oishi", "Toh", "Nocon", "Piao",
                   "Parameswaran", "Zhong", "Cui", "Shimada", "Gurung", "Kyaw", "Hari", "Dou", "Paguio", "Sana", "Ying",
                   "Hamasaki", "Luong", "Lising", "Mehra", "Nazareno", "Layug", "Woo", "Oum", "Babauta", "Banga",
                   "Rauf", "Arain", "Carandang", "Banerjee", "Oshima", "Lee", "Atwal", "Shue", "Bui", "Dieu", "Duan",
                   "Deguia", "Takai", "Oei", "Baccam", "Murai", "Pawar", "Choi", "Tien", "Gokhale", "Lovan", "Shon",
                   "Jayakumar", "Lat", "Mukhtar", "Upadhyay", "Hang", "Gaerlan", "Hsu", "Aman", "Sek", "Datta", "Awan",
                   "Razvi", "Saephanh", "Usman", "Kamath", "Chatha", "Anjum", "Paracha", "Chiem", "Khim",
                   "Krishnaswamy", "Akhter", "Thiara", "Ung", "Seid", "Pham", "Agarwal", "Sieng", "Deasis", "Morikawa",
                   "Truong", "Jariwala", "Dee", "Kano", "Doung", "Sood", "Madriaga", "Huynh", "Dhawan", "Bibi",
                   "Kawasaki", "Saravanan", "Sarma", "Cong", "Papa", "Noorani", "Baskaran", "Ranjan", "Gohil",
                   "Chandrasekaran", "Thor", "Agrawal", "Matsunaga", "Iwasaki", "Fonua", "Pua", "Lall", "Lacson",
                   "Verghese", "Kelkar", "Abella", "Dhakal", "Pathak", "Zaheer", "Tian", "Sugihara", "Bandaru",
                   "Mahadeo", "Dah", "Hafiz", "Fatima", "Trias", "Nambiar", "Manabat", "Uchiyama", "Hirai", "Bien",
                   "Taw", "Pan", "Dasgupta", "Bakshi", "Kawaguchi", "Geng", "Madhavan", "Sangalang", "Sahu", "Vitug",
                   "Miyake", "Yogi", "Sekhon", "Suen", "Susanto", "Samad", "Dan", "Dosanjh", "Chakravarty",
                   "Sonoda", "Ty", "Gaw", "Samaroo", "Taguchi", "Manda", "Chopra", "Ouk", "Liwag", "Pe", "Tsering",
                   "Salonga", "Punzalan", "Chung", "Asghar", "Kulkarni", "Fukuhara", "Subramani", "Umali", "Majmudar",
                   "Bal", "Hameed", "Nakama", "Sumida", "Casino", "Sin", "Yamazaki", "Zaveri", "Khera", "Engineer",
                   "Arif", "Thiagarajan", "Malla", "Madayag", "Gim", "Gunda", "Ohashi", "Cabreros", "Sein",
                   "Srinivasan", "Cham", "Fukumoto", "Gul", "Ooi", "Guanzon", "Goll", "Sah", "Kimoto", "Paek", "Mak",
                   "Alam", "Naidoo", "Toves", "Beg", "Shiau", "Prom", "Jivani", "Tupou", "Phang", "Ro", "Arumugam",
                   "Tsukamoto", "Tangonan", "Poblete", "Parvez", "Kalsi", "Kuriakose", "Gilani", "Menor", "Wadhwa",
                   "Tran", "Pant", "Joo", "Shiu", "Hsia", "Tra", "Yamamoto", "Begum", "Durrant", "Gin", "Meng", "Zaw",
                   "Majeed", "Jun", "Sheth", "Chanthavong", "Chowdhary", "Rajani", "Hussain", "Javed", "Shek",
                   "Manansala", "Gade", "Dhami", "Kharel", "Saxena", "Imam", "Neang", "Deocampo", "Bastola",
                   "Walia", "Ding", "Roeun", "Aulakh", "Rahaman", "Meh", "Morioka", "Kurihara", "Tse", "Po",
                   "Govindarajan", "Bian", "Pradhan", "Thaker", "Kota", "Tsang", "Reddy", "Cayanan", "Faisal",
                   "Santoso", "Leu", "Wong", "Joson", "Khaira", "Tha", "Mahtani", "Jeon", "Bacani", "Choudhary", "Ye",
                   "Phanthavong", "Samonte", "Hussaini", "Bhandal", "Bhimani", "Shimamoto", "Cachola", "Khatri", "Chu",
                   "Pajarillo", "Nozaki", "Suon", "Ky", "Siharath", "Bhattacharya", "Tuazon", "Naqvi", "Liwanag",
                   "Sato", "Chae", "Chia", "Nagar", "Oshita", "Mohiuddin", "Chandran", "Sayarath", "Barretto", "Or",
                   "Tau", "Kawahara", "Cheema", "Rao", "Zhen", "Thong", "Bains", "Sohal", "Karthik", "Rampersaud",
                   "Chhor", "Poon", "Bamba", "Kau", "Bai", "Ghimire", "Chandy", "Lamba", "Ahn", "Nag", "Khwaja", "Che",
                   "Ho", "Debnath", "Tun", "Wo", "Nagai", "Matsubara", "Qiu", "Pen", "Hirayama", "Kinoshita", "Deo",
                   "Shimoda", "Takeda", "Tsay", "Vaz", "Khanam", "Onishi", "Yau", "Lue", "Brahmbhatt", "Mao",
                   "Cadiente", "Bala", "Satish", "Pich", "Tep", "Furukawa", "Pacis", "Baby", "Aryal", "Kodama", "Oza",
                   "Shakoor", "Kathuria", "Diep", "Lok", "Mirchandani", "Barroga", "Batac", "Choudry", "Chhun",
                   "Tu", "Xu", "Tashiro", "Subba", "Tokuda", "Dao", "Rajaram", "Sheng", "Kumagai", "Chheng", "Dharia",
                   "Xing", "Banh", "Seng", "Ishihara", "Vijayakumar", "Gohel", "Takayama", "Mathai", "Jagannathan",
                   "Sayeed", "Tandon", "Muraoka", "Shibuya", "Paragas", "Kanda", "Lim", "Murali", "Nahar", "Bhattarai",
                   "Saini", "Esguerra", "Yasuda", "Zacharias", "Banzon", "Zhu", "Hsueh", "Mohsin", "Chau", "Ninan",
                   "Rafanan", "Ahmed", "Ramanathan", "Rajendran", "Bondoc", "Manohar", "Tsui", "Trieu", "Bartolome",
                   "Abid", "Choo", "Kai", "Jao", "Takata", "Jonnalagadda", "Qazi", "Yarlagadda", "Somani",
                   "Bhattacharjee", "Dahal", "Saeteurn", "Yoo", "Yousuf", "Srivastava", "Chidambaram", "Juneja",
                   "Vallabhaneni", "Rimando", "Shakya", "Chandrasekhar", "Yuson", "Mansoor", "Doh", "Mang", "Deol",
                   "Datu", "Mahesh", "Troung", "Imtiaz", "Eapen", "Jhaveri", "Canlas", "Pei", "Ha", "Baba", "Mumtaz",
                   "Choung", "Deshpande", "Takagi", "Vo", "Padmanabhan", "Pyun", "Tram", "Shinde", "Shaheen", "Soni",
                   "Phi", "Gatchalian", "Pau", "Mun", "Araneta", "Nazir", "Bari", "Umar", "Huh", "Ranganathan",
                   "Hlaing", "Hyder", "Sheen", "Ganesh", "Yoshihara", "Balagot", "Sakata", "Calimlim", "Iyer", "Anand",
                   "Tae", "Hayat", "Cheng", "Hattori", "Roxas", "Cen", "Chhay", "Sundaram", "Sem", "Advani", "Magat",
                   "Srikanth", "Vien", "Rani", "Amar", "Dayrit", "Naeem", "Zafar", "Takashima", "Hew", "Nguy",
                   "Lomibao", "Sano", "Sit", "Venkateswaran", "Kolla", "Ishibashi", "Krishnamurthy", "Dhaliwal", "Mua",
                   "Leano", "Thota", "Sodhi", "Diao", "Srey", "Dogra", "Sallee", "Dua", "Dutt", "Sawhney", "Tseng",
                   "Lau", "Kataoka", "Hyun", "Bali", "Singson", "Shao", "Hoshino", "Maredia", "Ahamed", "Seong",
                   "Miyasaki", "Au", "Dacanay", "Eom", "Teh", "Querubin", "Zapanta", "Tim", "Dong", "Tiongson", "Eang",
                   "Maranan", "Chohan", "Bee", "Fung", "Nicdao", "Memon", "Luangrath", "Muralidharan", "Cheon", "Vi",
                   "Cherian", "Rizwan", "Ishida", "Dimalanta", "Vu", "Waseem", "Murata", "Zaidi", "Majumdar", "Kuo",
                   "Parthasarathy", "Higuchi", "Chow", "Pillay", "Ueda", "Nanda", "Khong", "Huo", "Ju", "Vang", "Sagun",
                   "Deen", "Hasnain", "Mu", "Azhar", "Khem", "Husain", "Vyas", "Kahlon", "Duong", "Gui", "Vinluan",
                   "Raza", "Syed", "Narula", "Pasha", "Sundara", "Zaman", "Chowdhury", "Hata", "Ahsan", "Vij", "Ko",
                   "Khatun", "Chin", "Raja", "Arakawa", "Ozawa", "Rabanal", "Sundar", "Thein", "Tayag",
                   "Krishnamoorthy", "Tripathy", "Rathi", "Bhavsar", "Shrestha", "Bhat", "Gogineni", "Krishnakumar",
                   "Shrivastava", "Som", "Bhakta", "Acob", "Suleman", "Golla", "Tabassum", "Pandya", "Sabio",
                   "Marasigan", "Paruchuri", "Patel", "Vora", "Jain", "Nhem", "Rodrigo", "Yan", "Baig", "Bajaj", "Wen",
                   "Cacal", "Phu", "Murtha", "Shieh", "Tagawa", "Sia", "Vea", "Matsushita", "Basu", "Azam", "Jo",
                   "Hayashida", "Fabro", "Resurreccion", "Lacsamana", "Sum", "Chakrabarti", "Chhan", "Yoshimura",
                   "Huie", "Yadao", "Mukherjee", "Pai", "Tahir", "Pande", "Koike", "Mishra", "Rupani", "Hirota", "Kung",
                   "Sohn", "Nagra", "Feng", "Imai", "Sung", "Minami", "Chew", "Mia", "Haque", "Respicio", "Pung",
                   "Prak", "Venkatraman", "Maruyama", "Tay", "Dutta", "Trac", "Siddique", "Yeung", "Malladi", "Babar",
                   "Kubo", "Wadhwani", "Baluyot", "Naz", "Zachariah", "Tanimoto", "Svay", "Sami", "San", "Fukui",
                   "Bhargava", "Arora", "Komatsu", "Dhanoa", "Canete", "Patankar", "Lacap", "Prabhakar", "Katragadda",
                   "Boado", "Ravichandran", "Camba", "Chieng", "Uchida", "Manibusan", "Tsung", "Nghiem", "Venkatesh",
                   "Cheong", "Jocson", "Janjua", "Luo", "Johal", "Antolin", "Alli", "Tamanaha", "Xin", "Xuan", "Cing",
                   "Tiet", "Phuong", "Munar", "Kawano", "Lugtu", "Ramamurthy", "Sanghavi", "Calica", "Quach",
                   "Ramachandran", "Staana", "Kumari", "Persaud", "Aye", "Sibal", "Bandyopadhyay", "Cu", "Sukhu",
                   "Surapaneni", "Ahluwalia", "Bu", "Perveen", "Eum", "Shyu", "Lu", "Liv", "Khoo", "Hsi", "Verma",
                   "Nakajima", "Nang", "Tieu", "Joh", "Zhuo", "Mikami", "Misra", "Khoja", "Jamal", "Pandian", "Virani",
                   "Karki", "Lem", "Dau", "Raghavan", "Nabi", "Yee", "Okawa", "Myint", "Kalia", "Pha",
                   "Deguzman", "Munir"]
}

inter_racial_names = {
    "last_names": ["Tinker", "Pal", "Sultan", "Kamaka", "Lal", "Inouye", "Azizi", "Shaikh", "Oda", "Popal", "Sablan",
                   "Harjo", "Saleem", "Akbar", "Ahuna", "Ishii", "Hodson", "Aoki", "Ishikawa", "Khalil", "Khalid",
                   "Chee", "Kam", "Shih", "Ono", "Nitta", "Gouveia", "Khanna", "Dizon", "Lui", "Mirza", "Mori",
                   "Suzuki", "Desilva", "Butt", "Loo", "Murakami", "Turney", "Hasegawa", "Higashi", "Cordeiro",
                   "Taitano", "Baptista", "Abbasi", "Anwar", "Raj", "Gong", "Rapoza", "Issa", "Ikeda", "Neves",
                   "Billiot", "Maeda", "Habib", "Pascua", "Fujii", "Coelho", "Aziz", "Mahmoud", "Wan", "Endo", "Aguon",
                   "Cambra", "Moniz", "Matsuda", "Ting", "Mohammadi", "Hosseini", "Texeira", "Kakar", "Saeed", "Nazari",
                   "Abdul", "Decosta", "Chai", "Barakat", "Goo", "Yamashita", "Scanlan", "Nobriga", "Tamura",
                   "Morimoto", "Hashimi", "Chaudhry", "Kimura", "Mohan", "Karimi", "Hom", "Honda", "Ansari", "Perreira",
                   "Choy", "Haider", "Kawakami", "Ming", "Quan", "Kawamura", "Shim", "Tung", "Iqbal", "Leeper", "Aki",
                   "Yen", "Shimizu", "Hamidi", "Mahabir", "Matsumoto", "Nishimura", "Mansour", "Mohammad", "Tiger",
                   "Sultani", "Xavier", "Hamid", "Nakagawa", "Chock", "Dsouza", "Mau", "Viernes", "Sing", "Abe",
                   "Yim", "Corpuz", "Azimi", "Mendonca", "Hakim", "Sakamoto", "Apo", "Mahmood", "Akiona", "Lyn",
                   "Takeuchi", "Kato", "Chandra", "Sison", "Wardak", "Hanohano", "Mossman", "Miyamoto", "Sasaki",
                   "Devera", "Kobayashi", "Delima", "Ogata", "Hirata", "Ogawa", "Manalo", "Rahimi", "Hamada", "Ancheta",
                   "Yousif", "Yamasaki", "Ku", "Min", "Ota", "Jardine", "Hashimoto", "Sannicolas", "Ram", "Amini",
                   "Toma", "Nakamoto", "Jaber", "Higa", "Noori", "Seto", "Nomura", "Baldridge", "Youssef", "Ito",
                   "Prakash", "Akana", "Morita", "Miyashiro", "Hsieh", "Persad", "Rampersad", "Nakata", "Uddin",
                   "Habibi", "Akbari", "Abdallah", "Leonguerrero", "Furtado", "Ramkissoon", "Fujimoto", "Qureshi",
                   "Yoshida", "Rahim", "Akina", "Sadeghi", "Ornellas", "Kamai", "Kaneshiro", "Kealoha", "Toy",
                   "Taniguchi", "Gragg", "Hosein", "Sayed", "Degroat", "Zamani", "Yamada", "Hamdan", "Masuda", "Thach",
                   "Ahmadi", "Abdulla", "Narayan", "Sylva", "Arakaki", "Rahmani", "Maharaj", "Yeh", "Suleiman",
                   "Mclellan", "Botelho", "Awad", "Takahashi", "Demello", "Okada", "Chilton", "Saad", "Okamoto",
                   "Kawamoto", "Mah", "Sharifi", "Kao", "Fukuda", "Kalama", "Bhatti", "Afshar", "Hazard", "Khoury",
                   "Akau", "Uyeda", "Hara", "Hee", "Nakano", "Yip", "Abbas", "Tehrani", "Pangelinan", "Rai", "Salehi",
                   "Nasser", "Sakai", "Nishimoto", "Vandunk", "Hayashi", "Hakimi", "Yap", "Amiri", "Shimabukuro",
                   "Cravens", "Paiva", "Kapoor", "Nakashima", "Okamura", "Watanabe", "Chand", "Safi", "Hashemi", "Tai",
                   "Siu", "Harada", "Baksh", "Oshiro", "Yamaguchi", "Mayle"]}

religion_wise_names = {
    "Muslim": [
        "Adyan",
        "Kasib",
        "Sadiqah ",
        "Samit",
        "Husam",
        "Abdul Qadir",
        "Gulfam",
        "Rashdan",
        " Rasheeda ",
        "Mulayl",
        " Hussein",
        "Sayfiyy",
        "Faheem",
        "Jawharah ",
        "Sageda ",
        "Nusayr",
        "Nisha ",
        "Iqra ",
        "Marnia ",
        " Ubaydah",
        "Nazim",
        "Ziram ",
        "Sahibah ",
        "Najm al Din",
        "Majdy",
        "Mahrus",
        "Nimr",
        "Talib",
        "Shuhda ",
        "Mubin",
        "Nasih",
        "Sakinah",
        "Jameelah ",
        "Rubadah ",
        " Ala al din",
        "Khidr",
        "Adl",
        "Norhan ",
        " Rufaydah ",
        "Sahrish ",
        "Abdul Mueed",
        "Shabeeh",
        "Isaf ",
        " Sayf",
        "Amatullah ",
        "Nisrin ",
        "Fazzilet ",
        "Nazirah ",
        "Bakht ",
        "Taqwa",
        "Abdul Noor",
        "Shahnoor ",
        "Fadwah ",
        "Ali",
        "Mohid",
        "Mikhail",
        "Abdus Sami",
        "Salam",
        "Muazah ",
        "Abdul Samad",
        "Alzubra ",
        "Waseem",
        " Lulwa ",
        "Abdul-Malik",
        "Mahir",
        "Abdul Jabbar",
        "Shabaan",
        "Rafah ",
        " Khayriyyah",
        "Fahimah ",
        "Muqatadir",
        "Rafeek",
        "Furayah ",
        "Wahibah ",
        "Zaigham",
        "Abdus Sattar",
        "Amin",
        "Rabi",
        "Sumlina ",
        "Hanifa ",
        "Kishwar",
        " Intisaar ",
        "Azlan",
        "Ibtihal ",
        "Muneerah ",
        " Fareeq",
        "Aqil",
        "Azra ",
        "Aman ",
        "Murshidah ",
        "Zulekha ",
        "Shuaib",
        "Jasim",
        "Zulfiqar",
        "Nuri",
        "Abdul Aliyy",
        "Fadilah ",
        "Ambreen ",
        "Ruhi",
        "Karimah ",
        "Suheb",
        "Ayah",
        "Abdul-Ghafur",
        "Thamer",
        "Mariyah ",
        "Abdul-Jabbar",
        "Mandhur",
        "Abdul-Barr",
        "Mashhur",
        "Muhsin",
        "Mundhir",
        "Saib",
        " Jumaana ",
        "Aasim",
        "Abdul-Mueid",
        "Robeel",
        "Parveen ",
        "Naveen ",
        "Jabalah",
        "Mukarram",
        "Anwaar",
        "Shumaylah ",
        "Dhiya",
        "Sad al Din",
        "Istakhri",
        "Aryisha ",
        "Faizah",
        "Sameenah ",
        "Sahmir",
        "Armaan",
        "Khirash",
        "Fayruz ",
        "Abdul-Waajid",
        "Aludra ",
        "Nashmia ",
        "Lamya",
        "Aabirah ",
        "Qudamah",
        "Zumzum ",
        "Humayl",
        "Umayr",
        "Inam",
        "Barkat",
        "Rahiq ",
        "Tanweer ",
        "Abdul-Muqtadir",
        "Sumara ",
        "Mahirah ",
        "Kaseem",
        "Habis",
        "Sultanah ",
        "Ahzab",
        "Tulayhah ",
        "Jazib",
        " Taalah ",
        "Hibah ",
        "Shaheer",
        "Husain",
        " Yaseen",
        "Muruj ",
        "Makki",
        " Anaan ",
        "Abdul Wahhab",
        "Banafsha ",
        "Tazmeen ",
        "Zaynah",
        " Raneem ",
        "Taymullah",
        "Muneer",
        "Zahra ",
        "Hayaat",
        "Mahdi",
        "Azizah ",
        " Hasna",
        "Hakim",
        "Azka ",
        "Nadirah ",
        " Nawwaf",
        "Gulzar",
        "Rubaba ",
        "Munkadir",
        "Dunya ",
        "Adbul-Qawi",
        "Usaimah",
        "Saleemah ",
        "Burhan",
        "Aasimah ",
        " Nasser",
        "Zaytoon ",
        "Wajeeh",
        "Aftab",
        "Limazah",
        "Wadiah ",
        "Asbat",
        "Tarannum",
        "Chaman ",
        "Iffah ",
        "Balqis ",
        "Wahbiyah ",
        "Rayyan",
        "Wifaq ",
        "Maheen",
        "Baqir",
        "Wafa",
        " Farraj",
        " Khadeeja ",
        "Abdul-Haseeb",
        "Munqad",
        "Quadir",
        "Ayman",
        "Zaeem",
        "Ilias",
        "Mujab",
        " Nudhar ",
        "Saima ",
        "Shumaila ",
        "Dakhil",
        "Wahidah ",
        "Kardawiyah ",
        "Jamal al Din",
        "Aidh",
        "Gul-e-Rana ",
        " Faiza ",
        "Mufid",
        "Abdul Badee",
        " Ghayth",
        "Hooman",
        "Mawiyah",
        "Abdul Waali",
        "Mariam",
        "Maridah ",
        "Samiyah",
        "Arwa ",
        "Abeer ",
        "Hadeeqah ",
        "Nur-ul-Qiblatayn",
        "Hibba ",
        "Shabah",
        " Nur ",
        " Waseem",
        "Kamilah ",
        "Sameeha ",
        "Bakr",
        "Soraiya ",
        "Naim",
        "Uhud ",
        "Noman",
        "Mirsab",
        "Mujahid",
        "Thauban",
        "Shillan ",
        "Najjar",
        " Hasna ",
        "Summar ",
        "Nabil",
        "Mubeenah ",
        "Urooj",
        " Hikmat ",
        "Mehjabeen ",
        "Fadi",
        "Jun ",
        "Mohsin",
        "Athil",
        "Ghaziyah ",
        "Amirah ",
        " Shafeeq",
        "Marghub",
        "Nageenah ",
        "Khulayd",
        "Jabr",
        "Izz",
        "Khatib",
        "Majd",
        "Mika",
        "Lamya ",
        "Tariqah ",
        "Nasirah ",
        " Nashat",
        "Risay",
        "Fajaruddin",
        "Hanai",
        "Haneef",
        "Shabbeer",
        "Abeedah ",
        "Ishfaq ",
        "Juma",
        "Lutf",
        "Amreen ",
        "Nasifah ",
        "Bilqis",
        "Zayba ",
        "Basel",
        "Zaytoonah ",
        "Zaahirah ",
        "Hashim",
        "Mummar",
        "Senait ",
        "Ismat ",
        "Fanan ",
        " Safiya ",
        "Qindeel ",
        "Hanfa ",
        "Sultaan",
        "Hayud ",
        " Taahira ",
        "Bahia ",
        " Manaal ",
        "Hadiyah",
        "Shahnaaz ",
        "Sumra ",
        "Iskandar",
        "Farqad ",
        "Wafiyah ",
        " Shareefa",
        "Ammar",
        "Nimah ",
        "Reem ",
        " Khairiya ",
        "Fusaylah ",
        "Waddah",
        "Kadar",
        "Intizar",
        "Anisa ",
        "Faria ",
        "Naina ",
        "Junnut ",
        "Samira ",
        "Wardah",
        "Manzoor",
        "Ruqayyah",
        "Naira ",
        "Safuh",
        "Mulham",
        "Zahid",
        "Murtada",
        "Zuti",
        " Najaah ",
        "Salsabil",
        "Mays",
        "Tahseenah ",
        "Mutahharah ",
        "Mardhiah ",
        "Nisa ",
        "Sahirah ",
        "Areeb",
        "Abdul Mujeeb",
        " Aida ",
        " Najeeba ",
        " Manaar ",
        "Qameer ",
        "Rijja ",
        "Hamidah ",
        "Zaynah ",
        "Jahdari",
        "Amrah ",
        "Mihran",
        "Yamha ",
        "Nasra ",
        "Faridah ",
        "Tahir",
        "Haniyyah",
        "Almir",
        "Najm",
        "Arissa ",
        "Zumurruda ",
        "Nawwar ",
        "Qutb",
        "Ali ",
        "Sulafah ",
        "Karam ",
        "Qani",
        "Munahid",
        "Shafiq",
        "Mehndi ",
        "Muslimah ",
        "Shakir",
        "Ghazanfar",
        "Haniya ",
        "Nimat",
        "Hibatullah ",
        "Ajer",
        "Nafi",
        "Isa ",
        "Shahrazad ",
        "Ibrahim",
        "Shamsheer",
        "Zuhur ",
        "Nawlah ",
        "Abzari",
        "Adeem",
        " Irfan",
        "Wazeera ",
        "Ghaniyah ",
        " Rayyaa ",
        "Jada ",
        "Numan",
        "Jasrah ",
        "Samihah",
        "Abdush Shahid",
        "Nizam",
        "Aroosa ",
        "Shakeelah ",
        "Subhaan ",
        " Fawza ",
        "Awatif ",
        "Shaheenah ",
        "Muniba ",
        "Sakina ",
        "Alim",
        "Faheemah ",
        "Yasmin ",
        "Zunairah ",
        "Rahat",
        "Lublubah ",
        " Mohammed",
        "Abdul Rahim",
        "Abdul-Hakeem",
        "Tabalah ",
        "Taqiy",
        "Nura ",
        "Tasneem ",
        "Jamila ",
        "Hunaidah",
        "Abdul Qawi",
        "Kanza ",
        "Iqbal",
        "Mahdiya ",
        "Luluah",
        "Saila ",
        "Nabigh",
        "Hujjat",
        "Aminah",
        "Salah al Din",
        "Haifa ",
        "Simra ",
        "Karida ",
        "Badia ",
        " Shaymaa ",
        "Qirat ",
        "Nashirah ",
        "Iba ",
        " Ruqayya ",
        "Zahra",
        "Abdul Kareem",
        " Iffat ",
        "Abdul Wali",
        "Malik",
        "Thalabah",
        "Imam",
        "Mikaeel",
        "Naba ",
        " Raawiya ",
        "Yunus",
        "Mehr ",
        "Wagma ",
        "Safwah",
        "Anbar ",
        "Mawaddah ",
        "Ruhee ",
        "Abdul Haseeb",
        "Jabrayah ",
        "Athazaz",
        "Sabiha ",
        "Shairyaar",
        "Thawab ",
        "Zulfa ",
        "Salman",
        "Aliyah ",
        "Mateen",
        "Khazanah ",
        " Thanaa ",
        "Shamailah ",
        "Aleena ",
        "Seema",
        "Ashalina ",
        "Hirah ",
        "Humaira ",
        "Zaid",
        "Sukainah",
        "Zubdah ",
        "Maysa ",
        "Tanwir",
        "Rizwan",
        "Fatik",
        "Ghufayrah ",
        "Asim",
        "Faiz",
        "Abdul Qahhar",
        "Muafa",
        "Jalilah ",
        "Jafar",
        "Fir ",
        "Kaltham ",
        "Ishaq",
        "Zahir",
        "Nawrah ",
        "Masarrah ",
        "Abdul Muti",
        "Qabalah ",
        "Ghareebah ",
        "Nasmi",
        "Mishall ",
        "Sammar ",
        "Asiya ",
        "Abdul Tawwab",
        "Aymen ",
        " Ziyad",
        " Atiya ",
        "Sairah",
        " Kameel",
        "Sabrina ",
        "Shama ",
        "Mustaeenah ",
        "Rahila ",
        "Sabahat",
        "Sakhr",
        "Qubilah ",
        "Saleh",
        "Aatirah ",
        "Liba ",
        "Hayat ",
        "Mutawalli",
        " Junayd",
        "Shahbaz",
        "Shahida ",
        "Madaniyah ",
        " Rida",
        " Badriya ",
        "Udaysah ",
        "Fasahat",
        "Deema ",
        "Lulu ",
        "Salsaal",
        "Nazmin ",
        "Sadan",
        " Jaleel",
        "Naushad",
        "Ziya ",
        "Ithaar",
        "Aneesa ",
        "Zenia ",
        "Abdul Adl",
        "Mustahsan",
        "Mustafa",
        "Sameen ",
        "Raquib",
        "Ajmal",
        "Hawa",
        "Raid",
        "Hameeda ",
        "Hurya ",
        "Kaheesha ",
        "Adeelah ",
        "Razia ",
        "Pervaiz",
        " Joozher",
        " Atifa ",
        " Saleem",
        "Mulhim",
        "Zafar",
        "Rafay",
        "Kamran",
        "Zaeemah ",
        "Hibbah ",
        "Mutasim",
        "Sabeen ",
        "Ghanim",
        "Khitam ",
        "Ehsan",
        "Abdul Hafiz",
        "Mazhar",
        " Raja ",
        "Mubid",
        "Faiq",
        "Liban",
        "Koila ",
        " Sherrifah ",
        "Walladah ",
        "Basir",
        "Talhah",
        "Abdul Baqi",
        "Ghayda ",
        "Amah ",
        "Shuja",
        "Shakila ",
        "Tamim",
        "Rafid",
        "Samaira ",
        "Sarwat ",
        "Hashmat",
        "Nur al Din",
        " Safwat",
        "Saaqib",
        " Leila ",
        " Muneera ",
        "Rifaat ",
        "Muzhir",
        "Shamsa ",
        "Tahirah",
        "Meher ",
        "Saadat",
        "Hawazin ",
        "Shajarah ",
        "Sabina ",
        "Tihami",
        "Faiqa ",
        "Hamzah",
        "Taslim",
        "Hijrah ",
        "Layla",
        "Muizz",
        "Tahoor",
        "Abia ",
        "Nashida ",
        "Thabitah ",
        "Yusuf",
        "Rahma ",
        "Mubassirah ",
        " Ayeh ",
        " Yusraa ",
        "Izz al Din",
        " Kareem",
        "Zarrah ",
        " Lubayd",
        "Qasid",
        " Usaym",
        "Meymona ",
        "Rafiah ",
        "Yaqeen",
        "Lanika ",
        "Afifah ",
        "Juwan ",
        "Ruwaid",
        "Subhan",
        "Eimaan ",
        "Mehtab",
        "Khalil",
        "Dina ",
        " Zubayr",
        "Ahsan",
        "Birrah ",
        "Fozia ",
        "Shellah ",
        "Mubarakah ",
        " Faysal",
        " Hakeem",
        "Sami",
        "Fellah ",
        "Museeb",
        "Saji",
        " Suhayb",
        "Akifah ",
        "Linah",
        "Rushd",
        "Abdul Wahid",
        " Labeeb",
        "Mayyasah ",
        "Safa ",
        "Shabina ",
        "Siddra ",
        "Abdul Ghafoor",
        "Ghalibah ",
        "Ma as-sama ",
        "Talha",
        "Qais",
        "Ghumaysa ",
        "Tawhid",
        "Tuqa",
        "Maimun",
        "Aribah ",
        "Nafis",
        "Rasin",
        "Shehr bano ",
        "Wakeel",
        "Mushir",
        " Nadwa ",
        "Nabiha ",
        "Abdul Jabaar",
        "Parvez",
        "Zulfaqar",
        "Sunya ",
        "Nahal ",
        "Futun ",
        "Ziyad",
        " Shuayb",
        "Anniyah ",
        "Shahirah ",
        "Waqas",
        "Masoomah ",
        "Shareen ",
        "Matloob",
        "Qatadah",
        "Haydar",
        "Eiliyah ",
        "Hazar ",
        "Hayah ",
        "Eshal ",
        "Damurah",
        "Amira ",
        "Atiya ",
        "Eiman ",
        "Sabah ",
        "Nusaybah ",
        "Muntasir",
        "Haifa",
        "Shuhrah ",
        " Zaafirah ",
        " Sahla ",
        "Shawaiz",
        "Suad ",
        "Tulayb",
        "Khuzama ",
        " Zayn",
        "Tawbah ",
        "Fahmi",
        " Fatima ",
        "Aafreeda ",
        "Ihsan",
        "Hira ",
        " Amineh",
        "Tumadur ",
        "Abdul-Majeed",
        "Heba ",
        "Hannah ",
        "Aymaan",
        "Ijlal ",
        "Daliyah ",
        "Tabassum ",
        "Mufallah",
        "Taibah ",
        "Faseeh",
        "Abida ",
        "Nuzhah ",
        " Tubaa ",
        " Wadhaa ",
        "Kas ",
        "Nasimah ",
        "Masroor",
        "Minha ",
        " Juwayn",
        "Muddaththir",
        "Halwani",
        "Tanveer",
        "Yazid",
        "Reeha ",
        " Ghaydaa ",
        "Unaysah ",
        "Zeena ",
        "Gulshan",
        "Reyah ",
        "Hallaj",
        "Mahaz",
        "Muzzammil",
        "Najibah ",
        "Nuhaid",
        "Muhjah",
        "Mushfiq",
        "Rizqin ",
        "Ruwaidah",
        " Azzam",
        "Aani Fatimah Khatoon ",
        " Usamah",
        "Nawaz",
        "Ayaat ",
        "Nizzar",
        "Rajaa",
        "Amirah",
        "Nibal",
        "Fakeehah ",
        "Tawfiq",
        "Aafreen ",
        "Sauda",
        "Sadaf ",
        "Khalis",
        "Youssef",
        "Izzah (Izzat) ",
        "Sakinah ",
        "Wafiqah ",
        "Aziman ",
        "Leilah ",
        " Nabeela ",
        "Tufayl",
        "Dawlat Khatoon ",
        "Abdul-Haleem",
        "Sakhawat",
        "Mansur",
        "Qadr ",
        "Rukayat ",
        " Suhaymah ",
        "Bahirah",
        "Aswad",
        "Zarifah ",
        "Ilm ",
        "Muammar",
        "Aya ",
        "Maysarah ",
        "Gazala ",
        " Usaymah ",
        "Nuha ",
        "Noshaba ",
        "Fairuzah ",
        " Nojood ",
        "Muyassar",
        "Aqilah ",
        "Zynah ",
        "Ghawth",
        "Akhdan",
        "Dhakwan",
        "Shahla ",
        "Taima",
        "Mihyar",
        "Raheel",
        "Fatimah ",
        "Halimah ",
        "Rasul",
        "Azeeza ",
        "Daania ",
        " Haneefa ",
        "Namyla ",
        "Mashel ",
        "Taqiyy",
        "Faseehah ",
        "Shafeeqah ",
        "Waqqas",
        "Farha ",
        "Raghad or Raghda ",
        "Subhi",
        "Naifah ",
        "Abdul-Ghani",
        "Nabih",
        "Fatinah ",
        "Neelofer ",
        "Marwah ",
        "Humaydah ",
        "Reda",
        "Nejat ",
        "Shakib",
        "Nabeelah ",
        "Fahad",
        "Ghitbah ",
        "Fakhri",
        "Shumaysah ",
        "Darakhshaan ",
        "Sonia ",
        "Hamal",
        "Ridha",
        "Deen",
        "Amaar",
        "Thubaytah ",
        "Abdul Mubdi",
        "Samra ",
        "Hussein",
        "Thumamah",
        "Tamara ",
        "Jumanah",
        "Rafan",
        "Fakih",
        " Nuwayrah ",
        "Rais",
        "Fareeha ",
        "Azim",
        "Tamir",
        "Nigar ",
        " Zayn ",
        " Noori",
        "Shimah ",
        "Akbar",
        "Shujana ",
        "Zulaym",
        "Nazindah ",
        "Shaila ",
        "Shamilah ",
        "Wali",
        "Ghazi",
        "Id",
        "Shamas",
        "Siddiq",
        "Duaa ",
        "Imani ",
        "Juthamah",
        "Abdul Latif",
        "Rakin",
        "Ilham ",
        " Jala ",
        "Khayriyah",
        "Yaseen",
        "Qurratul Ayn ",
        "Zilal ",
        "Abdul Muhaymin",
        "Salsabil ",
        "Nafiah ",
        "Uzair",
        "Yafi",
        "Jumaymah ",
        "Adab",
        "Muqaddas",
        "Fawzan",
        "Obaid",
        "Siwar",
        " Haala ",
        "Rihab",
        "Taha",
        "Farheen ",
        "Nurah",
        "Salah",
        "Nabilah ",
        " Ahmed",
        "Farhan",
        "Sayf",
        "Munib",
        "Ghanem",
        "Baha",
        "Hadil ",
        "Hamdan",
        " Riyadh",
        "Nawar ",
        "Hamnah ",
        "Imtiaz",
        "Lubna ",
        "Sadiq",
        "Abu Bakr",
        "Zahraa ",
        "Qutayyah ",
        "Asar",
        "Himayat",
        "Hidayah ",
        "Shabeehah ",
        "Raihana ",
        "Latifah",
        "Talibah ",
        "Mahbub",
        " Ayoob",
        "Hashir",
        "Buhjah ",
        "Bariah",
        "Manahil ",
        "Ayra ",
        "Asma ",
        "Radiyah",
        "Hujaymah ",
        "Walihah ",
        "Abdul-Mujeeb",
        "Kardal",
        "Kadeen",
        "Shariq",
        "Attiq",
        "Mouna ",
        "Zainab ",
        "Jian ",
        "Nuaym",
        "Tarub ",
        "Dameer",
        " Afeef",
        "Munawar ",
        "Warda ",
        "Tali",
        "Sidra ",
        "Usman",
        "Abdul Lateef",
        " Ameena ",
        "Luja ",
        "Nadeem",
        " Nabeeha ",
        "Sahlah ",
        "Anisah",
        "Aishah ",
        " Maymun",
        "Abdul-Lateef",
        "Angbin ",
        "Makhtoonah ",
        "Abdur Rashid",
        "Hiba ",
        "Suhayb",
        "Fareedah ",
        "Farihah",
        "Jammana ",
        "Muznah ",
        "Dafiyah ",
        "Shasmeen ",
        "Raseem",
        "Suhaim",
        "Manar ",
        " Nadeeda ",
        "Dayyan",
        "Rubaa ",
        "Shakeel",
        "Abdul Musawwir",
        "Samia ",
        "Samina ",
        "Thuml ",
        "Tufaylah ",
        "Khidash",
        "Shafqat",
        "Faruq",
        "Qurban",
        " Nazaaha ",
        "Adilah",
        " Atif",
        "Salma ",
        "Surur",
        "Jahdami",
        "Safiy",
        "Kulthum ",
        "Farwah",
        "Abbudin",
        "Jahan Aara ",
        "Aariz",
        "Jennah ",
        "Rumeha ",
        "Shafiulla",
        "Furat ",
        "Aahil",
        "Tayyibah ",
        "Abdul Muiz",
        "Zaheen ",
        "Izzah ",
        "Lubanah ",
        "Shahd ",
        "Barzah ",
        "Aban",
        " Abdel",
        "Uwaisah",
        "Ubayd",
        "Abdul Ghafur",
        "Khudrah ",
        "Nasif",
        "Barirah ",
        "Nina ",
        "Kabirah ",
        "Afnan ",
        "Sumayya",
        "Jasmina ",
        "Momina ",
        " Ali",
        "Maira ",
        "Nijad",
        "Mussaret ",
        "Makarim",
        "Amina ",
        " Taym Allah",
        "Zunnoon",
        "Nazar",
        " Kalil",
        " Hunaydah ",
        "Yar",
        "Diya al Din",
        "Numair",
        "Summaya ",
        "Lashirah ",
        "Zia ",
        "Nadyne ",
        "Adiba ",
        "Haseen",
        "Masahir ",
        "Rania ",
        "Raameen ",
        "Nasir al Din",
        "Mahveen ",
        "Kifayat",
        "Leena ",
        "Mutawassit",
        "Sumaira",
        "Abdul Matin",
        "Faiza ",
        "Nawel ",
        "Utaybah ",
        "Abdul-Qaiyoum",
        "Anasah",
        "Shariqah ",
        " Fareeha ",
        "Jahdamah ",
        "Maisarah ",
        "Najih",
        "Muhafiz",
        "Fadwa ",
        "Rumailah",
        "Laila ",
        "Masabeeh ",
        "Nahid",
        "Nisreen ",
        "Islam",
        "Huda ",
        "Abdus-Shaheed",
        " Nazeeh",
        "Mamun",
        "Ayah ",
        "Zahwah ",
        "Safeer",
        "Shamamah ",
        "Minhaj",
        "Wasfiyah ",
        "Fouad",
        "Vardah ",
        "Murtaad",
        " Sibaal ",
        "Nailah",
        "Mujazziz",
        "Femida ",
        "Faraj",
        "Nashwan",
        "Farihah ",
        "Aybak",
        "Asimah",
        "Zuhayr",
        "Hunaydah ",
        " Adnan",
        "Mamduh",
        "Ziad",
        "Ain ",
        "Fadiyah ",
        "Mumin",
        "Shamima ",
        "Fadl",
        "Reza",
        "Muflih",
        "Zainab",
        "Raha ",
        "Hamidah",
        "Hurmat",
        "Adeena ",
        " Awad",
        "Ramih",
        " Basheera ",
        "Yusra ",
        "Naji",
        "Tahani ",
        "Nasim",
        "Abdul Maajid",
        "Asmat ",
        "Wala",
        "Rashid",
        " Imran",
        "Dunyana ",
        "Hudun ",
        "Wadid",
        "Rabeea ",
        "Liyaqat",
        "Salamat",
        "Rowel",
        "Waqar",
        "Alleyah ",
        "Abidin",
        "Ajeebah ",
        "Yaghnam",
        "Naimah",
        "Thawab",
        "Nilofer ",
        "Jabir",
        "Anwar",
        "Sayhan",
        "Alishba ",
        "Khalisah ",
        "Ashfaq",
        "Ashaz",
        "Nazir",
        "Adawi",
        "Haleef",
        "Safiyya ",
        "Abdul Jawwad",
        "Qareeb",
        "Mahbeer",
        "Salamah",
        "Jahan Khatoon ",
        "Muzakkir",
        "Bahriyah al-Aabidah ",
        "Mahabbah ",
        " Sihaam ",
        " Rafa ",
        "Abdul Baasit",
        "Athar",
        "Ermina ",
        "Abdul Hameed",
        " Zaky",
        "Zeba ",
        "Murdiyyah ",
        "Khulud",
        "Shafath ",
        "Ramiz",
        "Afia ",
        "Kawkab ",
        "Sameh ",
        "Safiy-Allah",
        "Fattah",
        "Afizah ",
        "Bisar ",
        "Dalal ",
        "Maida ",
        "Abdus-Salaam",
        "Faqeeh",
        " Zuzer",
        "Najla ",
        "Barir",
        " Ameen",
        "Bariah ",
        " Mona ",
        " Tharaa ",
        "Romeesa ",
        "Rabitah ",
        "Saira ",
        "Syed",
        "Mawara ",
        " Aadab ",
        "Samiah ",
        "Falisha ",
        "Bakhtawar ",
        "Raees",
        "Tayyab",
        "Naqeebah ",
        "Shimaz ",
        "Sabih",
        "Fiddah ",
        "Kunza ",
        "Hidayat",
        "Widad ",
        "Muyassar ",
        "Ghazwan",
        "Sadad",
        "Zerina ",
        "Baha al Din",
        "Abdul Nafi",
        "Anjum ",
        "Hayed ",
        "Ghiyath",
        "Mujeeb",
        "Jahaan ",
        "Diqrah ",
        "Manhalah ",
        "Nishat ",
        "Hababah ",
        "Munsif",
        "Munirah",
        "Farah ",
        "Hawshab",
        "Walif",
        "Mehvesh ",
        "Nashita Energetic",
        "Nasrin ",
        "Khallad",
        "Ashika ",
        "Safwah ",
        "Yasmin",
        "Sabiqah ",
        "Abdul-Mutaalee",
        "Aalee",
        "Bakri",
        " Hilel",
        "Azeem",
        "Basinah ",
        "Kaysah ",
        "Najeeb",
        "Maysun ",
        "Firdaus ",
        "Harith",
        "Manzar",
        "Urfee",
        "Saniyah ",
        "Fareed",
        "Muawwiz",
        "Imtiyaz",
        "Nawaf",
        "Zonira ",
        "Mustaeen",
        "Umaynah ",
        "Diyari",
        "Siham ",
        "Rafiq",
        "Fuseelah ",
        "Hajrah ",
        "Kanzah ",
        "Musaddiq",
        "Zafeerah ",
        "Faaz",
        "Luban ",
        "Madani",
        "Suad",
        "Amal",
        "Shadab",
        "Bahar ",
        "Aniq",
        "Maysa",
        "Ajlah",
        "Najidah ",
        "Dildar",
        "Afroze ",
        " Ruwaydah ",
        "Nahidah",
        "Tanzeela ",
        "Abdul Ghafaar",
        "Jahm",
        "Naveed",
        "Saeed",
        "Ateefa ",
        "Hasinah ",
        "Lamis",
        "Sukaynah ",
        "Tisha ",
        "Aaban",
        "Malih",
        "Budail",
        "Shaheen",
        "Ghazawan",
        "Hakem",
        "Sheza ",
        "Feroz",
        "Sahir",
        "Sohaib",
        "Fahima ",
        "Sayyidah ",
        "ziyada ",
        "Abdul Muhyi",
        " Dhuha ",
        "Khazin",
        "Musheer",
        "Arsalaan",
        "Khadeeja ",
        "Shuruq ",
        "Habbab",
        "Azad",
        "Ruyah ",
        "Muhair",
        "Johara ",
        "Shaheerah ",
        "Kasam",
        "Moemen",
        "Asna ",
        " Uwaysah ",
        "Jiyad",
        "Rami",
        "Nashit",
        "Juhainah",
        "Ghunwah or Ghunyah ",
        "Naazneen ",
        "Munisah ",
        "Mudar",
        "Wisam",
        "Sifet",
        "Mehriban ",
        "Jinan ",
        "Nashah",
        "Shudun ",
        "Shawqi",
        "Thawban",
        "Farafisa",
        "Mysha ",
        " Zaina ",
        "Areej ",
        "Aaleyah ",
        " Saamiya ",
        "Tahiyah ",
        "Sahib",
        "Sarwari ",
        "Kathirah ",
        "karawan ",
        "Sarah ",
        "Thara ",
        "Abdul Muqaddim",
        "Fayha ",
        " Hafsa ",
        "Safwana ",
        " Yasmeen ",
        "Mamdouh",
        "Nabighah",
        "Masudah",
        "Abdul Baseer",
        "Hayam",
        " Tareef",
        "Iram ",
        "Hibat Allah ",
        "Mahasin ",
        "Aminah ",
        "Tasnim ",
        "Shahana ",
        "Safia ",
        "Rasheed",
        "Kamaliyah ",
        "Suraiya ",
        "Mudabbir",
        "Yusayrah ",
        "Zulaykha ",
        "Kaashif",
        "Shuayb",
        "Saffar",
        "Manfoosah ",
        "Mehnaz ",
        "Wasim",
        "Najah",
        "Rasheedah ",
        "Yumna ",
        "Fariha ",
        "Mahek ",
        "Shaistah ",
        "Faseelah ",
        "Qasif",
        "Saida ",
        "Makkiyah ",
        "Muallim",
        "Ambereen ",
        "Umair",
        "Waajidah ",
        "Sumrah",
        "Foziah ",
        " Hanifa",
        "Makhtooma ",
        "Suwaybit",
        "Usama",
        "Aimen ",
        "Dabir",
        "Hameem",
        "Badriyah",
        " Aroob ",
        "Sameya ",
        "Shadha ",
        "Naeema ",
        " Alhusayn",
        "Hayyan",
        "Raahil",
        "Abdul-Ghaffar",
        "Tawseef",
        "Zubair",
        " Afraa ",
        "Shiyam ",
        "Junayd",
        "Hafsah",
        "Isha ",
        "Thana",
        "Rabee",
        "Utbah",
        "Aabidah ",
        "Azraa ",
        "Komal ",
        "Kuhaylah ",
        "Juman ",
        "Yusur ",
        "Fawzi",
        "Abdul-Baasit",
        "Mikayeel",
        "Ateeqah ",
        "Nudbah ",
        "Cala ",
        "Sabburah ",
        "Abdus Samad",
        " Sumayyah ",
        "Musaykah ",
        "Mushtaq",
        "Tayyib",
        "Thana ",
        "Abdul Waliy",
        "Abdul-Wahhab",
        "Fatin or Fatinah ",
        " Raniya ",
        "Abdul-Baari",
        "Akhtar",
        "Iffah",
        "Hasibah ",
        "Falah",
        "Jahfar",
        "Tabish",
        "Amna ",
        "Qiyyama ",
        "Mourad",
        "Aaeedah ",
        "Fikri",
        "Sajjad",
        "Abdul Bari",
        "Mina ",
        "Nagheen ",
        "Fakhr",
        " Sameeha ",
        "Abdul Maalik",
        "Hooria ",
        "Hareem ",
        "Fayd",
        " Nazeera ",
        "Manab ",
        "Ramzia ",
        "Bisma ",
        "Haniyah ",
        "Mukarram ",
        " Leena ",
        "Iqrit",
        "Bayan ",
        "Thuwaibah",
        "Umamah ",
        "Sofia ",
        "Suhaib",
        "Talat",
        "Humd",
        "Khalilah ",
        "Alina ",
        "Lubaid",
        "Nubaid",
        "Anan",
        "Jaraah",
        "Nibras",
        "Abdus-Samad",
        "Tamadur ",
        "Shanaz ",
        "Radwa",
        " Warqaa ",
        " Ghaada ",
        "Zuhayra ",
        "Fawwaz",
        "Nazmi",
        "Jaun",
        "Aziz",
        "Abdul Mumin",
        "Erum ",
        "Ikram ",
        "Manha ",
        "Hud",
        "Abdul Salam",
        "Abdul Muqtadir",
        "Shakurah ",
        "Asiya",
        "Mehwish ",
        "Rubina ",
        "Noreen ",
        " Naila ",
        "Ziyan ",
        " Kareema ",
        "Seemeen ",
        "Khalid",
        "Arya ",
        "Fikriyah ",
        "Ikrimah",
        "Abdul Rafi",
        "Nazahah ",
        "Rawdah",
        "Naib",
        "Wajihah ",
        "Alaia ",
        "Latifa ",
        "Naraiman ",
        "Halimah",
        "Asbah ",
        "Abdul Qudoos",
        "Ulfah ",
        "Abul-Hassan",
        "Watheq",
        "Shahrukh",
        "Maizah ",
        "Zafirah ",
        "Rukanah",
        "Zarar",
        "Khidrah ",
        "Nadirah",
        "Sahlah",
        "Intaj",
        "Barrah ",
        "Halah ",
        "Shurooq ",
        "Ahd ",
        "Mukhlis",
        "Ataubaq",
        "Ghauth",
        "Iyaas",
        "Abdul-Nur",
        "Basil",
        "Muzaffar",
        "Sulayk",
        "Tasneen",
        "Taysir",
        "Ubadah",
        "Mayeda ",
        "Abdul Batin",
        "Hubaab",
        "Haleem",
        "Naqi",
        " Badia ",
        "Mahjabeen ",
        "Huzayl",
        "Jalal al Din",
        "Samaa ",
        "Mustakim",
        " Seif",
        "Hadiyyah ",
        "Zara ",
        "Abdul-Quddus",
        "Lujain",
        "Ashaath",
        "Ranya ",
        "Abdul-Hafeedh",
        "Adli",
        "Sad",
        " Muhanned",
        " Hana ",
        " Huwaydah ",
        "Sakhrah",
        "Soraya ",
        "Lu Luah ",
        "Hamamah ",
        "Huzaifah",
        " Amal",
        "Maha ",
        "Kanz ",
        "Amber ",
        "Ruqayya ",
        "Abdul Razzaq",
        "Hana",
        "Ramin",
        "Nasim ",
        " Sameera ",
        " Joozhar",
        "Faraza ",
        "Saburah",
        "Marjanah ",
        "Shamal",
        "Bahiyyah ",
        "Nihad ",
        "Nabilah",
        "Sheyla ",
        "Saadiya ",
        "Shihab",
        "Siraj",
        "Urwah",
        "Sawwaf",
        "Ibtihaj ",
        "Muskan ",
        "Raidah",
        "Anwara ",
        "Muayyad",
        "Ummayyah ",
        "Musaid",
        "Saful Islam",
        "Rayn",
        "Rehana ",
        "Mahfuzah ",
        "Fakeeh",
        "Wakil",
        " Masouda ",
        "Jari",
        "Shumayl",
        "Aaidah ",
        "Haziqah ",
        "Khayaam",
        "Amam",
        "Samih",
        "Muneeb",
        "Inaya ",
        "Masrur",
        "Fariah ",
        "Jadwa ",
        "Muqbalah ",
        "Qabeel",
        "Kuwaysah ",
        " Khaldoon",
        " Khaled",
        "Ashmath",
        " Adil",
        "Jarood",
        "Muadh",
        "Tobias",
        " Reema ",
        "Urshia ",
        "Aadil",
        "Hilmi",
        "Aasif",
        " Fahad",
        "Fateen",
        "Diya",
        " Areej ",
        "Abdul-Dhahir",
        "Fakhir",
        "Huriyah",
        "Safiyyah",
        "Tharwat",
        "Marwa ",
        "Adeeb",
        "Mounira ",
        " Budayl",
        "Dani",
        "Yasmina ",
        "Wasay",
        "Rahilah ",
        "Zehna ",
        "Maymun",
        "Aatif",
        "Thaqib",
        "Maliha ",
        "Hilal",
        "Qaniah ",
        "Ain alsaba ",
        "Reyhana ",
        "Shayma ",
        " Noorah ",
        "Huma ",
        "Mubaraq",
        "Nazli ",
        "Zoufishan ",
        "Zebadiyah",
        "Haroon",
        "Shezan ",
        "Safi",
        "Basheera ",
        "Sayyar",
        "Shamil",
        "Midhaa ",
        "Muawiyah",
        "Saheim",
        "Qaraah ",
        "Raifah ",
        "Qaymayriyah ",
        "Shakirah ",
        "Aatiqah ",
        "Faisal",
        "Batul",
        " Ghusoon ",
        "Tazeem",
        "Rauf",
        "Isma ",
        "Khatera ",
        "Adeela ",
        "Budur ",
        "Sultan",
        "Mimar",
        " Udayl",
        "Zakwan",
        "Uday",
        "Rasha ",
        "Habibah ",
        "Waheed",
        "Jawahir ",
        "Humair",
        "Shatha ",
        "Tara ",
        "Zarmina ",
        "Nadra ",
        "Nusrah ",
        "Miyaz",
        "Muttee",
        "Abdus Salaam",
        " Bahiya",
        "Abdul Mannan",
        "Mujibur",
        "Affan",
        "Eman ",
        "Baahir",
        "Yusr",
        "Jaiyana ",
        "Kharqa ",
        "Monera ",
        "Aashif",
        "Ghali",
        "Basimah",
        "Najihah ",
        "Abdul-Qaadir",
        "Muntaha ",
        "Naimah ",
        "Nazeerah ",
        "Mansoor",
        "Farhat ",
        "Madhat ",
        "Shaaf",
        "Nyla ",
        "Banujah ",
        "Labeeb",
        "Safun ",
        "Wareesha ",
        "Taheem",
        "Yaqoot",
        " Haleema ",
        "Najeed",
        "Mariya ",
        "Mounir",
        "Mahbubah ",
        "Laqeet",
        "Rashad",
        "Sabriyah ",
        "Shihab al Din",
        "Nashat",
        "Ramia ",
        "Muqtasid",
        "Rukhsar ",
        " Mais ",
        "Badr al Din",
        "Sharafat",
        "Tamam",
        "Nayyirah ",
        "Barr",
        "Abdul Baith",
        "Awwab",
        "Ahmad",
        "Iyad",
        " Aneesa ",
        "Arjumand ",
        "Shah",
        "Abdul Fattah",
        "Jul",
        "Nasihah ",
        "Hamdi",
        "Abdul Sabur",
        "Bushr",
        "Izdihar ",
        "Khairi",
        "Qadeer",
        "Jehan ",
        "Leila ",
        "Izdihar",
        "Nafisah ",
        "Zuharah ",
        "Kausar ",
        "Asadel",
        " Azim",
        "Asilah ",
        "Faeq",
        "Areebah ",
        "Liyana ",
        "Najair",
        "Jud ",
        "Dema ",
        "Talah",
        "Haytham",
        "Zubaidah ",
        " Kadir",
        " Aziza",
        "Shalimar ",
        "Tabinda ",
        "Uthman",
        "Rafah",
        "Safeerah ",
        "Abdul Munim",
        "Iqraam",
        "Hasna ",
        "Nashema ",
        "Samirah ",
        "Rayhanah ",
        "Bashirah ",
        "Rumaithah",
        "Hafs",
        "Abdul Rahman",
        "Bisharah ",
        "Banan ",
        "Bandar",
        "Lahiah",
        "Ghaliyah",
        "Jumaynah ",
        "Anah ",
        " Maysoon ",
        "Nazirah",
        "Nimat ",
        " Baseema ",
        "Maymunah ",
        "Misba ",
        "Suhail",
        "Musnah ",
        "Malika ",
        "Ahad",
        "Afif",
        " Zinat ",
        "Zarrar",
        "Badri",
        "Rafa",
        "Shamila ",
        "Athmah ",
        "Sharmeen ",
        "Shajeeah ",
        "Sharifah ",
        "Ibthaj ",
        "Qamar ",
        "Firas",
        "Faraz",
        "Humam",
        "Batal",
        "Wafiza ",
        "Abdul Hakeem",
        "Abdul-Jaleel",
        "Kaysan",
        "Tameem",
        "Shazmah ",
        "Mustajab",
        "Hikmah",
        "Shallal",
        "Rahim",
        "Tahsin",
        "Nudrat ",
        "Jana ",
        "Shahada ",
        "Samrah ",
        "Zuha",
        "Taban",
        "Kashish ",
        "Jalal",
        "Rahaf ",
        "Aaqib",
        "Sadeem",
        "Qabool ",
        "Sumanah ",
        "Arzo ",
        "Hindah ",
        "Rumana ",
        "Hafsah ",
        "Fara ",
        "Sahil",
        "Anmar ",
        "Riyasat",
        "Khasib",
        "Ayan ",
        "Nabihah",
        "Sarwath ",
        "Kasim",
        "Muttaqi",
        "Aasia ",
        " Makaarim ",
        "Shahnaz ",
        "Nimra ",
        "Abdul-Warith",
        "Thoraya ",
        "Adeeba ",
        "Midhah ",
        "Aashir",
        "Babar",
        "Jessenia ",
        "Zairah ",
        "Abdul Muizz",
        "Nunah ",
        "Saffanah ",
        "Mursal",
        "Kazi",
        "Abdur-Raheem",
        "Dabbah",
        "Mamoon",
        "Gamal",
        "Jamal",
        "Abdul Hasib",
        "Ghazalah ",
        "Hudad",
        "Numa ",
        "Mishaal",
        " Mahmoud",
        "Safiy al Din",
        "Fakhra ",
        "Rehemat ",
        "Murad",
        "Jasmir",
        "Layyah ",
        "Shazia ",
        "Nusrat ",
        "Talal",
        " Nazeeha ",
        "Rubiya ",
        "Musn ",
        "Fatin",
        "Wahhab",
        "Sayyid",
        "Madiha ",
        "Muqbil",
        "Minal ",
        "Hamood",
        "Ghadah",
        "Feiyaz ",
        " Husayn",
        "Ruwayfi",
        "Hadeel ",
        "Dujanah ",
        "Ubah ",
        " Ammar",
        "Mueen",
        "Usamah",
        "Zuhera ",
        "Zaib ",
        "Abdul-Aalee",
        "Huzayfah",
        "Imthithal ",
        "Samah ",
        "Inan ",
        "Juwairiyah",
        "Irfan",
        "Khansa ",
        "Sumaiyah",
        "Farizah ",
        "Nadim",
        "Ghayda",
        "Nazuk ",
        " Yumna ",
        "Azfer",
        "Amelia ",
        "Akilah ",
        "Azzah ",
        "Nur al Huda ",
        "Adifaah ",
        "Firdaws",
        "Nahida ",
        "Iftikhar ",
        "Raniyah",
        "Rafee",
        "Muizza ",
        "Isa",
        "Annam ",
        "Suhailah",
        "Faizaan",
        "Abdul Rashid",
        "Misbah",
        "Gulab",
        " Sabeeh",
        "Maimoona",
        "Rameesha ",
        "Hamim",
        "Aamira ",
        "Sawsan ",
        "Zakiyah ",
        "Aqeel",
        "Mehboob",
        "Jariyah",
        "Mujtaba",
        "Musa",
        "Ablah ",
        "Arman",
        "Basem",
        "Aiza ",
        "Adila ",
        "Nelofar ",
        "Jaseena ",
        "Nasha ",
        " Thurayya ",
        "Fawad",
        "Rajab",
        "Nashitah ",
        "Suha ",
        "Ilan",
        "Mona ",
        "Abdul Muzanni",
        "Jumaana ",
        "Nasheelah ",
        "Masud",
        "Moazzam",
        "Laiq",
        "Rihana ",
        "Zorah ",
        "Shazeb",
        "Shairah ",
        "Munawwar ",
        "Shiya ",
        "Unays",
        "Anum ",
        "Shaqeeq",
        "Tariq",
        "Abdul Azeez",
        "Najah ",
        "Ayham",
        "Ramzi",
        "Saaliha ",
        "Majdi",
        "Afham",
        " Rumaythah ",
        "Naseer",
        "Qamayr ",
        "Dilawar",
        "Abisali",
        "Shadi",
        "Zakar",
        "Salifah ",
        " Mishal",
        "Abqurah ",
        "Baha ",
        "Hur ",
        "Almas ",
        "Zeeshan",
        " Samaah ",
        "Ghassan",
        "Sadeed",
        "Wazir",
        "Ghufran ",
        "Adel",
        "Masoud",
        "Mohga ",
        "Agharr",
        " Atika ",
        " Rudaynah ",
        "Shukri",
        "Layali ",
        "Mahum ",
        "Zaroon",
        "Qadi",
        "Eshan",
        "Rasool",
        "Mehvish ",
        "Azab",
        "Malayeka ",
        "Hudhafah",
        "Arif",
        "Munaf",
        "Zuhair",
        "Itidal ",
        "Thurayya ",
        "Farhah ",
        "Ata al Rahman",
        "Taqiyah ",
        "Nasir",
        "Nidda ",
        "Iftikar ",
        " Taqwaa ",
        "Farooq",
        "Jala",
        "Abdul Hamid",
        "Subhiyah ",
        "Ada ",
        "Hajar ",
        "Sundus ",
        " Anwaar ",
        "Inayah",
        "Rahil",
        "Alman",
        "Muhriz",
        "Dhakiy",
        "Hadeeqa ",
        "Fawzah",
        "Khair al Din",
        "Anisah ",
        "Asbagh",
        "Qarasafahl ",
        " Naima ",
        "Hadad",
        "Wildan",
        "Itimad ",
        "Adeeva ",
        "Abdul Qahaar",
        "Naseerah ",
        "Nadimah ",
        "Dhakir",
        "Qutaylah ",
        "Arub",
        "Wahuj ",
        "Musab",
        "Heela ",
        "Umaiza ",
        "Noor Jehan ",
        "Salaahddinn",
        " Jumuah",
        "Falaq ",
        "Sadah ",
        "Azzah",
        "Kashifah ",
        "Abdul Muid",
        "Jal",
        "Saba ",
        "Fath",
        "Imtihal ",
        "Thaminah ",
        "Raheemah ",
        "Nur Firdaus",
        "Wadi",
        "Mashoodah ",
        " Ridha",
        "Naweed ",
        "Nailah ",
        "Abdul Muhyee",
        "Shayaan",
        "Sofian",
        "Yumn ",
        "Inaam",
        "Asheeyana ",
        "Shahlah ",
        "Dinar",
        "Buhaysah ",
        " Ismat ",
        "Yazan",
        "Abdullah",
        "Issar",
        " Hayat ",
        "Lutfiyah ",
        " Ragheb",
        "Iyaad",
        "Nasira ",
        "Warqa",
        "Ahnaf",
        "Anas",
        "Nada ",
        "Samarah ",
        "Sahm",
        "Hazimah ",
        " Wisaal ",
        "Waqaar",
        "Shahin",
        "Abdul Mutaal",
        " Hayfa ",
        " Baha",
        "Abdur-Rauf",
        "Shahzaib",
        "Rahmah ",
        "Ranim",
        "Dawoud",
        "Muqadaas ",
        "Shams al Din",
        "Mubashir",
        "Bareerah ",
        "Mawsil",
        "Rasmi",
        "Nesrin ",
        "Mazin",
        "Gharam ",
        "Shaharyar",
        "Nayyab ",
        "Asra ",
        " Yusuf",
        " Kasim",
        "Sagheer",
        "Fadl Allah",
        "Wajid",
        " Muhayr",
        "Naadir",
        " Ubaab ",
        "Tahira ",
        "Abbud",
        "Emran",
        "Sehrish ",
        " Asim",
        "Luay",
        "Imaad",
        "Hubba ",
        "Abdul Raheem",
        "Azraqi",
        "Kifah ",
        "Udail",
        "Basaaria ",
        "Abdul Hannan",
        "Zakariyya",
        "Sharaheel",
        " Huriyyah",
        "Muhibbah ",
        "Marid",
        "Hadi",
        "Luqman",
        "Jamilah ",
        "Shihaam ",
        "Halima ",
        "Mirah ",
        "Riyad",
        "Lubabah",
        "Lana ",
        "Naflah ",
        "Arzu ",
        "Rand ",
        "Suraya ",
        "Thufailah ",
        " Majida ",
        "Abdul Qaadir",
        "Akeem",
        "Tamkeen",
        "Arij ",
        "Najibah",
        "Sajidah ",
        "Waseefah ",
        "Aighar ",
        "Suhair",
        "Zubayr",
        "Samiyah ",
        "Baasim",
        "Yuhannis",
        "Aziz ",
        "Judamah ",
        "Abrash",
        " Hudhayfah",
        "Nissa ",
        "Sarra ",
        "Muazzaz ",
        "Hanbal",
        "Zohra ",
        "Abdul Muhaimin",
        "Muhibb",
        "Amala ",
        "Munjid",
        "Sumayrah ",
        "Nuraz",
        "Hayfa ",
        "Afaf ",
        "Ayyash",
        "Shamoodah ",
        "Rawhiyah ",
        "Ramlah ",
        "Iqtidar",
        "Rabiyah ",
        "Furozh",
        "Kahil",
        "Fareess ",
        "Abdul Alim",
        "Najya ",
        "Turhan",
        " Saabira ",
        "Jahmyyllah ",
        "Zinah",
        "Azzam",
        "Naqid",
        "Ghazal ",
        "Zakirah ",
        "Maysan ",
        "Aabish ",
        "Zaheerah ",
        "Abid",
        "Mishael ",
        "Zayd",
        "Shahidah ",
        " Juhaynah ",
        "Alia ",
        "Mahrosh ",
        "Abdul-Muizz",
        "Wajih",
        "Mashhud",
        "Tahseen",
        "Owais",
        "Fateenah",
        "Jaza ",
        "Samirah",
        "Hammad",
        "Sakeenah ",
        "Sadaqat",
        "Sawa",
        "Musharraf",
        "Motasim",
        "Yara ",
        "Mufeed",
        "Zulfah ",
        "Jasim.",
        "Sabirah",
        "Jabeen ",
        " Adeela ",
        "Abdul Khaliq",
        "Bassam",
        "Faizah ",
        "Ikram",
        "Asif",
        "Jawl ",
        "Kawakib ",
        "Sughra ",
        "Khatoon ",
        "Rushdi",
        "Umm Kulthum ",
        "Shahzad",
        "Fariza ",
        "Ghusoon ",
        "Lamah ",
        "Qudsiyah ",
        " Wafaa ",
        " Yasser",
        "Jahiz",
        "Naseem",
        "Tajammal",
        "Badiyah ",
        "Badra ",
        "Layth",
        "Shiraz",
        "Shehla ",
        "Zaara ",
        "Jummal",
        "Daneen ",
        " Inayat ",
        "Lut",
        "Ghazzal",
        "Sheila ",
        "Wardah ",
        "Rabah",
        "Rabbani",
        "Abdul-Qahhar",
        "Hafiz",
        "Bayhas",
        "Afeerah ",
        "Javier",
        "Khubayb",
        "Basim",
        "Daniyah ",
        " Qais",
        "Zohair",
        " Nabeel",
        "Sinan",
        "Abdul Rabb",
        "Usayd",
        "Hawwa ",
        "Mahdiyah ",
        "Mustaqeem",
        "Ezzah ",
        "Hanifah",
        "Ihtisham",
        "Sabeeyah ",
        "Ablah",
        "Neelam ",
        "Tahiyat ",
        "Rasil",
        "Sarina ",
        " Umair",
        "Munazzah ",
        " Nibaal ",
        "Yasirah ",
        "Arsal",
        "Zamil",
        "Mumtaz",
        "Marzuq",
        "Shayan",
        "Kashif",
        "Ayana ",
        "Samman",
        "Mersiha ",
        "Samar ",
        "Mustaneer",
        "Khayriyyah ",
        " Widaad ",
        "Boulos",
        "Darwish",
        " Reem ",
        "Samir",
        "Zaman",
        "Lina ",
        "Shafiah ",
        "Bulhut",
        "Shifa ",
        "Muminah ",
        "Mujaddid",
        "Salar",
        "Khateeb",
        "Shareekah ",
        "Wafeeqah ",
        "Rafal ",
        "Abdul Ghaffar",
        " Fuad",
        "Qaim",
        "Hala ",
        "Summayyah ",
        "Jabbar",
        "Jilan ",
        "Wakalat",
        "Zayb ",
        "Dawud",
        "Lamiah ",
        "Adawiyah ",
        "Samiun ",
        "Sorfina ",
        "Mastura ",
        "Shahid",
        " Katib",
        "Sawdah ",
        "Muharrem",
        "Zoeya ",
        "Mukhlisah ",
        "Khusbakht ",
        "Mobeen",
        " Salsabeel ",
        "Aaeesha ",
        "Abir ",
        "Mahbasah ",
        "Maqboolah ",
        "Jawdah",
        "Sahab",
        "Afeef",
        "Subhah ",
        " Wisaam ",
        "Nabhan",
        "Zahirah ",
        "Jamil",
        "Kaleemah ",
        "Naureen ",
        "Shazad",
        "Manar",
        "Kazim",
        "Reham ",
        "Abdul Mubdee",
        "Kiswar ",
        "Abdul Qayyum",
        "Sulaiman",
        " Gamali",
        "Adara ",
        "Huda",
        " Suhaym",
        "Marzuqah ",
        "Mustatab",
        "Nighat ",
        "Buhayyah ",
        "Jarir",
        "Humayrah ",
        "Binish ",
        "Jalil",
        "Abdul Jalil",
        "Tanisha ",
        "Ashraf",
        "Kamal",
        "Abdur-Rahman",
        "Shurahbeel",
        " Buhaisah ",
        "Nazeefah ",
        "Shuraym",
        "Rehan",
        "Yushua",
        "Amjad ",
        "Hamra ",
        "Firoz",
        "Mansurah ",
        "Omar",
        "Husn ",
        "Nafeesa ",
        "Barika ",
        "Ward",
        "Latifah ",
        "Amana ",
        "Hurrah",
        "Minaal ",
        "Motaz",
        "Intisar",
        "Wasimah ",
        "Imad",
        "Sheraz",
        "Wasif",
        "Izzat",
        "Razan",
        "Afsheen ",
        "Anbarin ",
        "Andalib ",
        " Hooda ",
        "Saidah ",
        "Usaim",
        "Muhannad",
        "Zehra ",
        "Faris",
        "Awn",
        "Batrisyia ",
        "Zaynab ",
        "Amid",
        "Riaz",
        "Mawahib ",
        "Rameez",
        "Saud",
        "Yasar",
        " Yoonus",
        "Hessa ",
        " Rabeea ",
        "Nathifa ",
        "Saqib",
        "Anjam",
        "Rahmaa ",
        "Ashwaq ",
        " Fareed",
        " Wordah ",
        "Sumaytah ",
        "Inayah ",
        "Abal ",
        "Khayrah ",
        "Rahman",
        "Baysan ",
        "Raghid",
        "Alraaz ",
        "Hashid",
        "Amra ",
        "Mubarak",
        "Murtaza",
        "Roshini ",
        "Dawlah",
        "Kaiser",
        " Zuhayr",
        "Fathiyah ",
        "Azraq",
        "Laaibah ",
        "Rawhah ",
        "Baligh",
        "Wid ",
        "Sadun",
        "Aalim",
        "Nadhir",
        "Fatin ",
        "Shafaat",
        "Habibah",
        "Shukriyah ",
        "Swiyyah ",
        "Abdul Hadi",
        "Shazana ",
        "Zubaydah ",
        "Fariq",
        "Ana ",
        "Dahab ",
        "Ala al Din",
        "Fatimah",
        "Shajee",
        "Shafee",
        "Ahlam ",
        "Reshma ",
        "Yusra",
        "Aws",
        "Basimah ",
        "Madihah ",
        "Maruf",
        "Rafidah ",
        "Abdur-Razzaq",
        "Nawal ",
        "Kadeer",
        "Butrus",
        "Hanan ",
        "Aydin",
        "Nihal ",
        "Salihah ",
        "Shurafa ",
        "Fawziyah ",
        "Tuba",
        " Zuhaa ",
        "Abdul-Kareem",
        "Ammaar",
        "Janan ",
        "Saif",
        "Ammarah ",
        "Lutfi",
        "Hasib",
        "Siham",
        "Abdul Raafi",
        "Abdul Warith",
        "Aneeq",
        "Ehan",
        "Basbas ",
        "Abbas",
        "Baraah ",
        "Abdul Rauf",
        " Hayaam ",
        "Khaleel",
        "Daliya ",
        "Yaminah ",
        "Hidiyah ",
        " Asiyah ",
        "Ahdia ",
        "Walidah ",
        "Fazal",
        "Khayri",
        "Muwaffaq",
        "Aamirah",
        "Nuaim",
        "Fathiya ",
        "Juhaym",
        "Yumnah",
        "Ilyas",
        "Shahadat",
        "Intisar ",
        " Naeema ",
        "Makin",
        "Lablab",
        " Hooriya ",
        "Shaybah",
        "Sadiah ",
        "Latif",
        "Wahib",
        "Mutazah ",
        "Raya ",
        "Sumnah ",
        "Narmin ",
        " Sumayra ",
        "Tibah ",
        "Mubassir",
        " Asima ",
        "Imtithal ",
        "Raif",
        "Abdul-Baaqi",
        "Zoharin ",
        "Abdul Hafeez",
        "Mahad",
        "Faeezah ",
        "Khuraymah",
        "Rafi",
        "Ata Allah",
        "Safiyy",
        "Bashirah",
        " Inaam ",
        "Shuaa",
        "Sairish ",
        "Khaleed",
        "Arub ",
        "Tammam",
        "Nora ",
        "Mawiyah ",
        " Rafat ",
        "Abdur Razzaq",
        " Murtadi",
        "Husniya ",
        " Houd",
        "Sairah ",
        "Mehrish ",
        "Bilal",
        "Shabnam ",
        "Shiza ",
        "Naairah ",
        "Abdul Muntaqim",
        "Abdul Karim",
        "Jawdan",
        "Shayla ",
        "Hiyam ",
        "Minnah ",
        "Atikah",
        "Tasheen ",
        "Zareena ",
        "Maysarah",
        "Hayder",
        "Adham",
        "Aalia ",
        " Maymunah ",
        "Abdul-Hameed",
        "Maram",
        "Saood",
        "Fatim ",
        "Shareek",
        "Habiba ",
        "Al-Adur al-Karimah ",
        "Abdus-Shakur",
        "Barraq",
        "Fuad",
        "Hoor ",
        "Navil ",
        "Amara ",
        "Nur",
        "Shabab",
        "Aaqilah ",
        "Ghania ",
        " Tuqaa ",
        "Rudainah",
        "Akhfash",
        "Aqeil",
        "Mutayyib",
        "Qadim",
        "Alya ",
        "Nuzhat ",
        "Badi",
        "Ashar",
        "Ghizlan ",
        "Hadiyah ",
        "Mumayyaz ",
        "Shehryaar",
        "Baseema ",
        "Asma",
        " Asma",
        "Fudayl ",
        "Maryum ",
        " Hameeda ",
        "Mufidah",
        "Sabr ",
        "Miftah",
        "Sharmeela ",
        "Faridah",
        "Subbiha ",
        "Ishtiyaq",
        "Zayan",
        "Raji",
        "Hosaam",
        " Baheera ",
        "Buhthah ",
        "Hami",
        "Mehreen ",
        " Lubaaba ",
        "Firdowsa ",
        "Aaqil",
        "Horia ",
        " Muhja ",
        " Farooq",
        " Adila",
        "Anida ",
        "Amany ",
        "Mahfuz",
        "Jibril",
        "Rida ",
        "Taybah ",
        "Arfa ",
        " Radhiya ",
        "Aisha ",
        "Saimah ",
        "Adil",
        "Mutahhir",
        "Muhsinah ",
        "Khadijah ",
        "Afzal",
        "Suwaydah ",
        "Tahera ",
        "Ubab",
        "Zartaj ",
        "Abdul Ali",
        "Balqees ",
        "Maram ",
        "Rizwana ",
        "Hajjah ",
        "Shihad",
        "Ilhan ",
        "Azmat",
        "Nabila ",
        "Abdul-Wadood",
        "Humayun",
        "Asghar",
        "Saad",
        " Suhayl",
        "Jehaan ",
        " Wafeeq",
        "Almahdi",
        "Inas ",
        "Juzar",
        " Sameer",
        " Haadiya ",
        "Hooriya ",
        "Selina ",
        "Umaymah ",
        "Musaddiqah ",
        " Khayri",
        "Jawna ",
        "Nurjenna ",
        "Najid",
        "Arham",
        "Shanum ",
        "Sanjeedah ",
        "Layan ",
        "Aatikah ",
        "Mubashirah ",
        "Ghutayf",
        "Ishraq ",
        "Ruksha ",
        "Wasil",
        "Muzaynah ",
        "Husni",
        "Simah ",
        "Shafaq ",
        "Abdul-Khaliq",
        "Jasmin ",
        "Zubi ",
        "Abd Al-Ala",
        "Ajradah ",
        "Abdul Muhsin",
        "Daleela ",
        "Karim",
        "Hadee",
        "Najam",
        "Hamd",
        "Rashad ",
        "Bahir",
        "Ridwan",
        "Gohar",
        "Osama",
        "Fadilah",
        "Huwaidah",
        " Waleed",
        "Radeyah ",
        "Dhakirah ",
        "Natasha ",
        "Qareebah ",
        "Isar ",
        "Shehroze",
        "Fadila ",
        " Mawiya ",
        "Nashwa ",
        "Aza",
        " Raaida ",
        "Salikah ",
        "Istabraq ",
        "Nawwal ",
        " Nazeem",
        "Najiyah ",
        "Souhayla ",
        "Sehr ",
        "Aamir",
        "Naushaba ",
        "Khayyat",
        "Abdul Mujib",
        "Shadmani ",
        "Narjis ",
        "Quadriyyah ",
        "Lamisah ",
        "Shahina ",
        "Marwan",
        "Lajlaj",
        "Ghuzayyah ",
        "Hanin ",
        "Doaa ",
        "Medina ",
        "Fajr ",
        "Suhaymah ",
        "Suhayr ",
        "Faiqah ",
        "Abyan",
        "Taim Allah",
        "Majidah",
        "Saibah ",
        "Masun",
        "Farrukh",
        "Saaleha ",
        "Sawlat",
        "Laith",
        "Zayaan ",
        "Nazih",
        "Aamaal ",
        "Zumurrud ",
        "Wijdan ",
        "Rabar",
        "Wasifah ",
        "Nazimah ",
        "Basilah ",
        "Qailah ",
        "Naseef",
        "Ameer",
        "Badi al Zaman",
        "Sabuhi ",
        "Anis",
        " Sireen ",
        "Wakeelah ",
        " Jabr",
        "Arij",
        "Hannad",
        " Ikraam ",
        "Sameer",
        "Reema ",
        "Hani",
        "Nurah ",
        "Abdul Malik",
        "Atifah",
        "Abaan",
        " Aliyyah",
        "Hasnah",
        "Nidaa ",
        "Sarrinah ",
        "Nuriyah ",
        "Nazakat",
        "Hudhaifah",
        "Abdul Mateen",
        "Zahidah ",
        "Hutun ",
        "Atia ",
        "Nyasia ",
        "Arsh",
        "Sabeeh",
        "Shahzor",
        "Wafi",
        "Muna",
        " Lateefa ",
        "Abdul Nasser",
        "Barakah",
        "Ahwas",
        "Ithar ",
        "Hena ",
        "Pakeezah ",
        "Baber",
        "Arisha ",
        " Ameer",
        "Shaista ",
        "Elma ",
        "Rabiah",
        "Sabur",
        "Hubayshah ",
        "Rizq",
        "Jihan ",
        "Abeera ",
        "Ruaa ",
        "Nadia ",
        "Asifa ",
        "Sadiyah ",
        "Shad",
        "Qusay",
        "Asriyah ",
        "Abidah",
        "Malikah ",
        "Jeelan",
        "Jubair",
        "Fathima ",
        "Shamshad",
        "Tharya ",
        "Irem ",
        "Fadil",
        "Muhyi al Din",
        "Raja",
        "Yawar",
        "Fakhriyah ",
        "Deeba ",
        "Ilham",
        " Maysaa ",
        "Sanam ",
        "Maya ",
        "Nudar",
        "Mayyadah ",
        "Safoorah ",
        "Atif",
        "Ghaith",
        " Salih",
        "Nazihah",
        "Adan",
        "Tajudinn",
        " Batool ",
        "Sabirah ",
        "Sadit",
        "Sharif",
        "Istilah ",
        "Mahjub",
        "Abdul Haqq",
        "Akif",
        " Musheera ",
        "Bashshar",
        "Behzad",
        "Khursheed",
        "Abdul Mani",
        "Shamsideen",
        "Muhtadi",
        "Thamar",
        "Fakihah ",
        "Husna ",
        "Kanwal ",
        "Noor-Al-Haya ",
        "Fawz ",
        "Hujayrah ",
        "Nazeer",
        "Waiz",
        "Dunia ",
        "Sabihah ",
        "Aiman",
        "Antarah",
        "Dhul Fiqar",
        "Wahban",
        "Haikal",
        " Abeer ",
        " Fakhry",
        "Ghunayn",
        " Main",
        "Amr",
        "Ban ",
        "Raeesah ",
        "Hamid",
        "Mukhtar",
        "Alhena ",
        "Farkhandah ",
        "Jannah ",
        "Ayshah ",
        "Aram ",
        "Abdul Basir",
        "Muslim",
        "Suheera ",
        "Raidah ",
        "Chandni ",
        "Nazeef",
        "Farhanah ",
        "Thuwaybah ",
        "Najaf ",
        "Halah",
        "Noorali",
        "Mufiah ",
        "Shadhiyah ",
        "Khulaybah ",
        "Anees",
        " Maraam ",
        "Ferran",
        "Maisah",
        "Aseed",
        "Mualla",
        "Siyana ",
        "Sanaubar ",
        "Sulayman",
        " Najeeb",
        "Dean",
        "Fida ",
        "Sayid",
        " Firdoos ",
        "Shibli",
        "Mada ",
        "Nasmah ",
        "Samah",
        "Malak ",
        "Shaukat",
        "Sharaf",
        "Samawah ",
        "Iraj ",
        "Zahrah ",
        "Khafid",
        "Abdul Shakur",
        "Sahl",
        "Asima ",
        "Aamanee ",
        " Azza ",
        "Adam",
        "Tahirah ",
        "Ateeb",
        "Aijaz",
        "Yakootah ",
        "Shamim",
        "Khulus",
        "Bashair ",
        "Nithar",
        "Yaqub",
        "Firyal ",
        " Sukaynah ",
        "Nazneen ",
        "Suhayl",
        "Kalila ",
        "Wafiq",
        "Adiy",
        "Nain ",
        " Murtadhy",
        "Rafeeqah ",
        "Ujala ",
        "Abdul-Mumin",
        "Inayat",
        " Haniya ",
        "Muin",
        "Ibtisam ",
        " Ilhaam ",
        "Iyas",
        "Nishaaj",
        "Sahar ",
        "Zariya ",
        "Zakir",
        "Hatib",
        "Salif",
        "Zafir",
        " Isam",
        "Yusri",
        "Rua ",
        "Atyaf ",
        "Nuryn ",
        "Hamas",
        "Atifa ",
        "Maria ",
        "Afraz",
        "Sufyan",
        "Abdur-Rasheed",
        "Maysoon ",
        "Cantara ",
        "Saadah",
        "Sara ",
        "Najwa ",
        "Masood",
        "Reja ",
        "Aidah ",
        " Nadeem",
        "Sagheerah ",
        "Zufar",
        "Diyanah ",
        "Romana ",
        "Basmah",
        "Darim",
        "Qays",
        "Fahd",
        "Umnia ",
        "Zakariya",
        "Masumah ",
        "Qismah ",
        "Falih",
        "Hujayyah",
        "Intessar ",
        " Fawziya",
        "Rufaidah",
        "Khalifah",
        "Uqbah",
        "Aila ",
        "Afaaq",
        "Muhanna",
        " Sulayman",
        " Buthayna ",
        "Yaman",
        "Kaamil",
        "Dirar",
        "Jaan",
        "Nayif",
        "Bashir",
        "Anaum ",
        "Haddad",
        "Thayer",
        "Muhdee",
        "Adnan",
        "Khayr",
        "Aakifah ",
        "Fudail",
        "Khulud ",
        "Jibran",
        "Takiyah ",
        "Yafiah ",
        "Hajjaj",
        "Bashaar",
        "Abda ",
        "Ibtihaj",
        "Nusaibah",
        "Wahab",
        "Sharmin ",
        "Isra ",
        " Baraka ",
        "Aduz Zahir",
        "Jawhar",
        "Suwayd",
        "Kanval ",
        "Raghidah ",
        "Saffiya ",
        "Amjad",
        "Suud",
        "Naseemah ",
        " Sawdah ",
        "Munzir",
        "Abdul Sattar",
        "Natiq",
        "Rakhshan",
        "Abu al Khayr",
        "Durar ",
        "Wajdi",
        " Abida ",
        "Abir",
        "Badriyah ",
        "Sajid",
        "Nabeeha ",
        "Raghibah ",
        "Rajiyah ",
        "Muhib",
        "Munis",
        "Farid",
        "Maisah ",
        "Shahed ",
        "Amaya ",
        "Zoha ",
        "Jalees",
        "Zuhrah ",
        "Aishah",
        "Faakhir",
        "Umniyah ",
        "Sudi ",
        "Nusrah",
        "Abdul Qadeer",
        "Razeen",
        "Taymur",
        "Uzayr",
        "Afsa ",
        "Azizah",
        " Badriyyah",
        "Yasir",
        "Fathi",
        " Razaan ",
        "Yasna ",
        "Ruqaya ",
        "Ikhlas ",
        "Lunah ",
        "Haajar ",
        "Mahreen ",
        "Nasib",
        "Rana ",
        "Hafthah ",
        "Nazahah",
        "Zawiya ",
        "Raitah ",
        "Hawadah ",
        "Zaim",
        "Umar",
        "Aarifah ",
        "Bahijah ",
        "Salimah ",
        "Nasheed ",
        "Nagina ",
        "Zoya ",
        "Rayya",
        "Silah",
        "Abdur-Raqeeb",
        "Shams ",
        "Sarim",
        "Aala ",
        "Sarosh",
        "Ajib",
        "Aroob ",
        "Varisha ",
        "Fakhirah ",
        "Nuhaa ",
        "Muhammad",
        "Khayriyah ",
        "Ihab",
        "Muna ",
        " Zahraa ",
        "Abdul-Aleem",
        "Abdul Jaleel",
        "Nasri",
        "Qasim",
        "Quraybah ",
        " Maryam ",
        "Tehzeeb ",
        "Siraj al Din",
        "Muhab",
        "Jabirah ",
        " Ruwayd",
        "Adeel",
        "Abdul Wasi",
        "Rayna ",
        " Asmaa ",
        "Wasilah ",
        "Afsana ",
        "Munira ",
        "Kaneez ",
        " Khaleel",
        "Wajahat",
        "Hatim",
        "Aimal ",
        "Farida ",
        "Abdul Hakim",
        "Maahnoor ",
        "Mateenah ",
        " Rawdha ",
        "Shadha",
        "Hafizah ",
        " Fareeda ",
        "Zalfa ",
        "Durriyah ",
        "Azaan",
        "Radi",
        "Abdul Muqsit",
        "Abdus Subbooh",
        "Burayd",
        "Naaz ",
        "Shamis ",
        "Munerah ",
        "Hijab ",
        "Daghfal",
        "Amaan",
        "Najib",
        "Mahja",
        "Shafia ",
        "Abdul",
        "Nibras ",
        "Mehek ",
        "El-Amin",
        "Athir",
        "Fauzia ",
        "Mahwish ",
        "Nazish ",
        "Muballigh",
        "Raima ",
        "Nargis ",
        "Hurayth",
        "Sawad",
        "Rushd ",
        "Abdul Mughni",
        "Nooh",
        "Nidal",
        " Shareef",
        "Fahmida ",
        "Adn ",
        "Samiya ",
        "Buthaynah ",
        "Rohaan ",
        "Nasuh",
        "Abdul Khabir",
        "Shahir",
        "Mad",
        "Aneeqa ",
        "Nahlah",
        "Rukhsana ",
        "Afya ",
        "Mahnoor ",
        "Aneezah ",
        "Khuwaylah ",
        "Ubaidah",
        "Waliy Allah",
        "Nuwwarrah ",
        "Mehrunisa ",
        "Umarah",
        "Ilifat",
        "Kawthar ",
        " Nusaybah ",
        "Akleema ",
        "Kalbi",
        "Mufti",
        "Maqil",
        "Azhar",
        "Jahangir",
        "Saadia ",
        "Nafisah",
        "Zameer",
        "Nimah",
        "Ayser",
        "Subaha ",
        "Abdul-Majid",
        " Juwayriyah ",
        " Thuwaybah ",
        "Falak ",
        "Aidah",
        "Misha ",
        "Ashim",
        "Salim",
        "Wadha",
        " Fahada ",
        "Sarfaraz",
        " Bilqees ",
        "Sunbul ",
        "Nasreen ",
        "Husniyah ",
        " Jameel",
        "Wahhaj",
        "Uthal",
        "Shazfa ",
        "Sirin",
        "Rawahah",
        "Abdul-Mughni",
        "Sadid",
        "Kaliq",
        "Mueez",
        "Waail",
        "Aadila ",
        "Akram",
        "Abdul Halim",
        "Walid",
        "Raghad ",
        "Kadshah ",
        "Afiyah ",
        "Tuba ",
        "Hesam",
        "Fahdah",
        "Rifaah",
        "Amani ",
        "Sharifah",
        "Alhasan",
        "Ghusun",
        "Hammam",
        "Niyaf ",
        "Amsah ",
        "Suhaimah",
        "Shams-Ul-Haq",
        "Labib",
        "Wafiqah",
        "Abdul Haq",
        "Basoos ",
        " Moosa",
        "Saeedah ",
        "Qaseem",
        "Chanda ",
        "Hifza ",
        "Isir ",
        "Alika ",
        "Muslih",
        "Raghib",
        "Hayam ",
        "Madihah",
        "Majidah ",
        "Nuwairah",
        "Murshid",
        "Sadad ",
        "Hassan",
        "Aresha ",
        "Mumina ",
        "Noureen ",
        "Salsal",
        "Khushtar",
        " Zayd",
        "Altaf ",
        "Itab ",
        "Ratib",
        "Shadiyah ",
        "Hukaymah ",
        " Suraa ",
        "Fatihah ",
        "Zaida ",
        "Akia ",
        "Shabib.",
        "Rubi ",
        "Dahma ",
        "Hakimah ",
        "Maher",
        "Bunanah ",
        "Lubabah ",
        "Dawid",
        "Busrah ",
        "Hajib",
        "Nawfal",
        "Rabab ",
        "Thaman",
        " Sanaa ",
        " Sakeena ",
        "Karam",
        "Hussain",
        "Rajih",
        "Asad",
        "Abdul Majeed",
        "Arshaq",
        "Aslam",
        "Shaqeeqah ",
        " Yazeed",
        "Abdul Ahad",
        "Sati",
        "Sarwar",
        "Sheenaz ",
        "Lubab ",
        "Alhusain",
        "Umayyah",
        " Naheeda ",
        "Maysun",
        "Rabit",
        "Jaul",
        "Ula ",
        " Fateen",
        "Kulthum",
        "Tazkia ",
        "Haroun",
        "Faizan",
        " Bassam",
        "Juwain",
        "Nusayb",
        "Raza",
        "Ashadieeyah ",
        "Raiqah ",
        "Salaam",
        "Abdul Afuw",
        "Sundas ",
        "Abdus-Sabour",
        "Mashkoor",
        "Rafia ",
        "Taghrid ",
        "Seif",
        "Bishr",
        " Eisa",
        "Abdul Hakam",
        "Abdul Muqeet",
        "Amer",
        " Qutaibah",
        "Aroush ",
        "Munif",
        "Hafa ",
        "Khawlah ",
        "Nevaeh ",
        "Khuzamah ",
        "Iman ",
        "Insha ",
        "Fujai",
        "Razaanah ",
        "Shadan ",
        "Saja ",
        "Rayhan",
        "Buhaysah",
        "Maysam ",
        "Subayah ",
        "Qabilah ",
        "Shamsia ",
        "Abasah ",
        "Ubaydullah",
        "Abdul-Hadi",
        "Wiam ",
        "Ghannam",
        "Israail",
        "Thashin ",
        "Ramadan",
        " Mamduh",
        "Tahawwur",
        "Zain",
        "Abra ",
        "Siddiqah ",
        "Hasan",
        "Qanit",
        "Abdul Naseer",
        "Daamin",
        " Mayyada ",
        "Abdul Kabir",
        " Nimaat ",
        "Omera ",
        " Mufeeda ",
        "Abdul Basit",
        " Azhaar ",
        "Abdul-Haqq",
        "Mutazz",
        "Dhuka ",
        "Qutaybah",
        "Nurdeen",
        "Absi",
        "Aamil",
        "Wabisa ",
        "Mahvish ",
        "Murjanah ",
        "Hanash",
        "Arfan",
        "Zahabiya ",
        "Abdus Sabur",
        "Ifra ",
        "Imad al Din",
        "Razin",
        "Ziaud",
        "Amtullah ",
        "Janan",
        "Zarqa ",
        "Burdah ",
        "Balsam ",
        " Yusef",
        "Umm Kalthum",
        "Salih",
        "Aleemah ",
        "Akhlaq",
        "Henna",
        " Khuzaymah",
        "Rawiah",
        "Shafana ",
        "Nabihah ",
        "Labibah ",
        "Hamdhy",
        "Taseen",
        " Shadhaa ",
        "Sanika ",
        "Rawah ",
        "Asmara ",
        " Fadheela ",
        "Naqeeb",
        "Sarish ",
        "Sikandar",
        "Ghalib",
        "Heyam ",
        "Rukan ",
        " Buthainah",
        "Bahira ",
        "Saleem",
        "Raihan",
        "Nija ",
        "Senada ",
        "Zanubiya ",
        "Rona ",
        "Uwayam",
        "Yasmine ",
        "Saif al Din",
        "Shuneal",
        "Jahanzeb",
        "Dizhwar",
        "Uhban",
        "Thuraiya",
        "Niyaz",
        "Sanari ",
        "Thaqaf",
        " Nooh",
        " Alia",
        "Zamrud ",
        "Qaysar ",
        "Raheesh",
        "Sarmad",
        "Aaliyah ",
        "Mahibah ",
        "Sfiyah ",
        "Ijli",
        "Awa ",
        "Sabaa ",
        " Issam",
        "Shan",
        "Shawq ",
        "Anika ",
        "Kurayb",
        "Shehzadi ",
        "Aafiya",
        "Tharwah ",
        "Abdul Wadud",
        "Fayyad",
        " Lina",
        "Abdul Muhsi",
        "Maab ",
        "Fadeelah ",
        "Durrah ",
        "Ala",
        "Ramziyah ",
        "May ",
        "Abdul Baari",
        "Fatih",
        "Abeerah ",
        "Hamdiyah ",
        "Nahid ",
        "Sobia ",
        "Afreen ",
        "Uzma ",
        "Shayma",
        "Majid",
        "Naman",
        "Bushra ",
        "Riffat ",
        "Zameena ",
        "Bashar",
        "Jumah",
        "Wurud ",
        "Alima ",
        "Thabit",
        "Shanika ",
        "Suda ",
        "Tajammul",
        "Isad ",
        "Nakhat ",
        "Bazam",
        " Alia ",
        "Wisal",
        "Abrar ",
        "Dhakiyah ",
        "Wail",
        "Lazim ",
        "Kehkashan ",
        "Hayrah ",
        "Manal ",
        "Lamees ",
        "Kaukab ",
        "Jemimah ",
        "Najmah ",
        "Miqdad",
        "Nadir",
        "Sanawbar",
        "Asrar ",
        "Saqr",
        " Janaan ",
        "Inam ",
        " Nafeesa ",
        "Abdul Aleem",
        "Hazim",
        "Simrah ",
        "Ghasaan",
        " Hawwa ",
        "Altair",
        "Faryat ",
        "Hafid",
        "Ihtiram",
        "Nail",
        "Shagufta",
        "Sitarah ",
        "Tafida ",
        " Ayishah ",
        "Bahiya ",
        "Zaina ",
        "Nayab",
        "Faqirah ",
        " Khairy",
        "Buqayrah ",
        "Zafirah",
        "Ayesha ",
        "Ramsha ",
        "Intikhab",
        "Maaz",
        "Saqer",
        "Majd al Din",
        "Tanim",
        " Aisha",
        "Firdous ",
        " Jubayr",
        "Shua ",
        "Rafiqah ",
        "Munisa ",
        "Mounia ",
        "Nilofar ",
        "Zaid ",
        "Roshan",
        "Muhtashim",
        "Farasat",
        "Fakhr al Din",
        "Sirah ",
        "Jahida ",
        "Qadriyyah ",
        "Ismail",
        "Muti",
        " Bahiyaa ",
        "Humera ",
        "Waseemah ",
        "Neha ",
        "Ihtsham",
        "Abdul Wakil",
        "Muta",
        "Abdul Sami",
        "Zaki",
        "Abdul Zahir",
        " Bahiyy al Din",
        "Miskeen",
        "Abdus Shafi",
        "Hajna ",
        "Idhar ",
        "Ghazalan",
        "Khalidah",
        "Nasiha ",
        "Sumaiya ",
        "Nijah ",
        "Mashal",
        "Basharat",
        "Imran",
        "Mabad",
        "Masarrat",
        "Nadiyah ",
        "Makhdoom",
        "Malmal ",
        "Faysal",
        " Wafeeqa ",
        "Tawfeeq",
        "Sibal",
        "Abdul Barr",
        "Mushirah",
        "Abdus-Sameei",
        "Zahara ",
        "Rahimah ",
        "Saim",
        "Judi ",
        "Sadoof ",
        "Dilshad Khatoon ",
        "Husam al Din",
        "Bahij",
        "Laraib ",
        "Aalam",
        " Kadin",
        "Abdul Shahid",
        "Safiyyah ",
        "Yalqoot ",
        "Fahyim",
        "Shadeed",
        "Ubayy",
        "Abdul Nur",
        "Farhana ",
        "Nabijah ",
        "Warsan ",
        "Shabb",
        "Layla ",
        "Ghulam",
        "Ishrat",
        "Daanish",
        "Aladdin",
        "Abdul-Adheem",
        "Namir",
        "Shurayh",
        "Fakhtah ",
        "Aaminah ",
        "Rima",
        "Sura",
        "Khaleeq",
        " Amala ",
        "Nuwwar ",
        "Saiqa ",
        "Abdul Quddus",
        "Lujaina ",
        "Binesh ",
        "Haris",
        "Afeefa ",
        "Mahneerah ",
        "Izaan",
        "Kharijah",
        "Shehzaad",
        "Mekka",
        "Mahmud",
        "Thara",
        "Zohura ",
        "Yathrib",
        "Mustafeed",
        "Nafasat",
        " Bahira",
        "Lama ",
        "Taj",
        "Saihah ",
        "Qaylah ",
        "Shafiqah ",
        "Itaf ",
        "Nouf ",
        " Kedar",
        " Rumaylah ",
        "Kinza",
        "Ayyub",
        "Haji",
        "Jamilah",
        "Ruqayyah ",
        "Altaf",
        "Nizar",
        "Sanaullah",
        "Saafir",
        "Yasin",
        " Tayma ",
        "Yasmeenah ",
        "Aqeelah ",
        "Nujud",
        "Simak",
        "Nadr",
        "Sair",
        "Waliy al Din",
        "Safwan",
        " Madeeha ",
        "Abdul Awwal",
        "Rawh",
        "Mufakkir",
        "Ata",
        "Junah ",
        "Suhaylah ",
        "Mohaddisa ",
        "Aazim",
        "Amro",
        " Suhaylah ",
        "Umm-e-kulsum ",
        "Salimah",
        "Qutuz",
        "Nuaymah ",
        " Radhwaa ",
        "Sameea ",
        "Amilah ",
        "Abdul Raqib",
        "Bilqis ",
        "Hubab ",
        "Juhanah ",
        "Tasawwar",
        "Farees",
        "Tawoos",
        "Madeeha ",
        "Afshan ",
        "Artah",
        "Ulfat",
        "Murtadaa",
        " Ibtihaaj ",
        "Randa ",
        "Rayya ",
        " Thamir",
        "Aleeza ",
        "Khoury",
        "Qasoomah ",
        "Muhajir",
        "Nosheen ",
        "Zarif",
        "Sabir",
        "Jenna ",
        "Nausheen ",
        "Nasrullah ",
        "Dua ",
        "Somaya ",
        "Atiq",
        "Wajd ",
        "Ghadir ",
        "Anan ",
        " Naif",
        "Umran",
        "Athilah ",
        "Alma ",
        "Yarah ",
        "Tazim ",
        "Farzana ",
        "Shaheem",
        "Kafeel",
        "Daria ",
        "Ibadah ",
        "Mishel ",
        "Nasr",
        "Khush Bakht",
        "Binyamin ",
        "Iffat ",
        "Rabiya ",
        "Rihab ",
        " Nahla ",
        "Ahmar",
        " Aliyy",
        "Hawra ",
        "Ghayoor",
        "Rija ",
        "Raashid",
        " Saleema ",
        "Tarif",
        "Durdanah ",
        "Najat ",
        " Ablaa ",
        "Sumbul ",
        "Waliyah ",
        " Fazia ",
        "Humra ",
        "Salmaa ",
        "Sab",
        "Ijaz ",
        "Shareef",
        "Nelam ",
        " Suhayr ",
        "Marghoob",
        "Daniyal",
        "Jahanara ",
        "Shafi",
        "Danish",
        "Zareenah ",
        "Ambar ",
        "Abthi",
        " Nuhayd",
        "Aliyah",
        "Haniah ",
        "Raonar",
        " Imad",
        "Fayek",
        "Abdus",
        "Shameemah ",
        "Haaziq",
        "Karif",
        " Suoud",
        "Riham ",
        " Aziz",
        "Huthayfa",
        "Khalil al Allah",
        " Izdihaar ",
        " Khalida ",
        "Khunays",
        "Tasadduq",
        "Zaighum",
        "Adab ",
        "Shireen ",
        "Afifa ",
        " Ataa",
        "Alimah ",
        "Neeshad ",
        "Rasmiyah ",
        "Sabri",
        "Sana ",
        "Abdul Aalee",
        "Daud",
        "Yameen",
        "Shadin",
        "Rim",
        "Kyda ",
        "Khalam",
        " Sabeer",
        "Muheet",
        "Rimsha ",
        "Javairea ",
        " Lamees ",
        "Junaid",
        "Salik",
        "Aini ",
        "Az-zahra ",
        "Nabeel",
        " Abd al",
        " Kaseeb",
        "Dimah ",
        "Zeenat ",
        "Nuh",
        "Awad",
        "Nahla ",
        "Naeemah ",
        "Subuhi ",
        "Hisham",
        "Haider",
        "Rafif ",
        "Juwariyah ",
        "Hayah",
        "Namar ",
        "Abdul Wajid",
        "Shameem",
        "Mayyadah",
        "Marah ",
        " Nadira ",
        "Hibbaan",
        "Munir",
        "Aarif",
        "Zaheer",
        "Eliza ",
        "Ameenah ",
        "Sidrah ",
        "Shoaib",
        "Aatifa ",
        "Fawziyyah",
        "Tameez",
        "Shahnawaz",
        "Waleed",
        "Sharique",
        "Badiah",
        "Fiza ",
        "Ayat ",
        "Zameelah ",
        "Arshad",
        "Jundub",
        " Lamya ",
        "Amal ",
        "Musad",
        "Azadeh ",
        "Izma ",
        "Hurairah",
        " Isa",
        "Tameemah ",
        "Mughith",
        "Salwa ",
        " Baraaa ",
        "Aamilah ",
        "Maleehah ",
        "Khalaf",
        "Lubena ",
        " Maisa ",
        "Rashidah",
        "Wad ",
        "Mistah",
        "Sufia ",
        "Beena ",
        "Yahya",
        "Amir",
        "Hulyah ",
        "Shafin",
        " Aamal",
        "Ruhina ",
        "Buthaynah",
        "Khadijah",
        "Mohammed",
        "Safeenah",
        "Taj al Din",
        "Halim",
        "Sohail",
        "Afrah ",
        "Miskeenah ",
        "Batinah ",
        "Shukrah ",
        "Idris",
        " Abla",
        " Nabih",
        " Humayrah ",
        "Feerozah ",
        " Khulood ",
        "Hazirah ",
        "Shabana ",
        "Mikail",
        " Omar",
        "Haboos ",
        "Akhas",
        " Kareef",
        "Arbaaz",
        " Basma ",
        "Wahb",
        "Suraqah",
        "Falaknaz ",
        "Mehrnaz ",
        "Abdul Badi",
        "Abdul Nasir",
        "Kajji",
        "Ara ",
        "Masum",
        "Tooba",
        "Malakah ",
        "Khaldun",
        "Abyad",
        " Lujayn ",
        "Jad Allah",
        "Mahd",
        " Zaynab ",
        "Abdul Haleem",
        "Shahzaadee ",
        " Muneer",
        "Shaban",
        "Wahid",
        "Qadriyah ",
        "Rashida ",
        "Sarfraz",
        "Sana",
        "Erina ",
        "Hind ",
        "Yusriyah ",
        " Walaa ",
        "Anam ",
        "Fayzan",
        "Khuzaimah",
        "Nida ",
        "Abrad",
        "Maali ",
        "Ubaid",
        " Kulthoom ",
        "Adib",
        "Rumaisa ",
        "Fayaaz",
        "Muthanna",
        "Humza",
        "Ismah",
        "Mubin ",
        "Noor",
        "Khadim",
        "Duha",
        "Abdul Ghani",
        "Kamil",
        "Naheed ",
        "Razan ",
        "Naeem",
        "Ajwa ",
        "Insaf ",
        "Mayameen ",
        "Badr",
        "Ghaliyah ",
        " Ameera ",
        "Ghaneemah ",
        "Aniya",
        "Nadidah",
        "Qisaf ",
        "Aqsa ",
        "Jareer",
        "Naseeka ",
        "Keyaan",
        "Quddusiyyah ",
        "Shamel",
        "Hanif",
        "Afra ",
        "Nazia ",
        "Busr ",
        "Afra",
        "Aara ",
        "Safaa ",
        "Hamza",
        "Wasna ",
        "Seerat ",
        "Saiful Azman",
        "Yelda ",
        "Humairah",
        "Rabia ",
        "Tamanna",
        "Jawad",
        " Benyamin",
        "Jihad",
        "Ghadah ",
        " Dawud",
        " Azeeza ",
        "Muntazir",
        "Mufaddal",
        "Umayrah ",
        " Mufeed",
        "Awf",
        " Nuaym",
        "Bahiyah",
        "Sariyah",
        "Taimur",
        "Aalimah ",
        "Sarab",
        "Batool ",
        "Widad",
        "Aanisah ",
        "Azeemah ",
        " Jameela ",
        "Kulus ",
        "Manal",
        "Maladh ",
        "Zinah ",
        "Abdul Azim",
        "Basmah ",
        "Khalidah ",
        "Rani",
        "Isam",
        "Zuhoor",
        "Asalah ",
        "Laiba ",
        "Athir ",
        "Karimah",
        "Abdul Majid",
        "Rahmat",
        "Habib",
        " Habeeba ",
        "Murabbi",
        "Miraj",
        "Nadwah",
        "Surayj",
        "Asil ",
        "Abdul Hayy",
        "Khurram",
        "Fida",
        "Jawa ",
        "Akil",
        "Jad",
        " Harun",
        "Zuehb",
        "Mussah ",
        "Atiyah",
        "Najdah ",
        " Nusrat",
        "Yamamah ",
        "Zinneerah ",
        "Kaleem",
        "Ameera ",
        "Firdaws ",
        "Kateb",
        " Souad ",
        "Nahleejah ",
        "Rayann ",
        "Wisal ",
        " Ghaaliya ",
        "Wahabah ",
        "Abdul Aziz"
    ],

    "Hindu": ["Neni", "Shiva", "Kumkum", "Pramjot", "Annu", "Leela", "Golu", "Sarvesh", "Rukmani", "Nandu", "Rajeev",
              "Sabhana", "Harishankar", "Usha", "Araddhna", "Badri", "Jang", "Rajneesh", "Jeenat", "Mohan", "Divaraj",
              "Durgash", "Sakshi", "Kushal", "Himani", "Saveta", "Shabanagudiya", "Durgesh", "Mumtazbabi", "Rustam",
              "Yognder", "Anshul", "Rijakpal", "Anjali", "Tarjan", "Soni", "Ankush", "Riya", "Shalu", "Yash", "Pooran",
              "Kunalkannu", "Lalideepa", "Rajuchhotu", "Baksi", "Jasoda", "Birju", "Karinakavita", "Purnima", "Sharat",
              "Sana", "Ranu", "Naresh", "Naveen", "Vinod", "Rijul", "Piyush", "Nabav", "Nirmal", "Karishma", "Rashab",
              "Surjeet", "Ishika", "Avdhesh", "Rama", "Dipti", "Minakxi", "Andhav", "Padma", "Hemant", "Bhanu", "Mamta",
              "Sahiba", "Ramdin", "Mira", "Dharam", "Chander", "Ashu", "Radheyshyam", "Akshit", "Pancham", "Sabbo",
              "Indra", "Sarita", "Shivam", "Tavinder", "Chahat", "Apsana", "Kamla", "Rekhai", "Bhola", "Ramsem",
              "Ramkishan", "Mudrika", "Shardanand", "Vimla", "Grace", "Aashiya", "Vikashmungeri", "Harprasad",
              "Sidharath", "Silender", "Brijmohan", "Shehnaz", "Nirmla", "Shubham", "Sahil", "Rohit", "Sevakpitambar",
              "Rajveer", "Anu", "Chain", "Anshu", "Jamrujaha", "Sonali", "Molu", "Subhash", "Pinkooguddu", "Mudsay",
              "Mahabir", "Devraj", "Priya", "Ghansyam", "Harsh", "Neelam", "Abhijeet", "Bodh", "Suman",
              "Sudha", "Jag", "Tina", "Vidhi", "Kangana", "Kritikakittu", "Rishi", "Rashid", "Satish", "Lakshya",
              "Akhilesh", "Parerna", "Beeru", "Narender", "Tarif", "Aamod", "Rajenderkaku", "Radha", "Nadim", "Chaya",
              "Kishan", "Kranti", "Neha", "Huma", "Samaiali", "Devender", "Henkhochon", "Amil", "Chirag", "Akash",
              "Madhu", "Aanamika", "Parth", "Sobit", "Lakshman", "Gutam", "Punit", "Aditya", "Jai", "Jaipal",
              "Laxmikant", "Sarain", "Champa", "Hina", "Shankar", "Basnti", "Brij", "Manoj", "Bhatri", "Nimla", "Sunny",
              "Gautam", "Sikandar", "Savan", "Benjir", "Sambhu", "Manju", "Nagina", "Raghubir", "Harpal", "Imamudeen",
              "Sazi", "Manishmukesh", "Khushbu", "Anjalibabli", "Ankita", "Govind", "Leelawati", "Rosy", "Parminder",
              "Dilip", "Sujen", "Shrishti", "Mala", "Pinki", "Shabanm", "Kausal", "Khokan", "Nitu", "Harish", "Dev",
              "Ketan", "Chumki", "Rakesh", "Aryan", "Roshni", "Vimal", "Khusboo", "Jay", "Amar", "Nikita", "Deeya",
              "Rajni", "Aarti", "Kiran", "Seemasimran", "Shelender", "Kailash", "Yashoda", "Dinesh", "Maya", "Tarun",
              "Sweety", "Pritam", "Bir", "Doly", "Subin", "Nekki", "Deepti", "Mamuni", "Bimlesh", "Krishan", "Sunaina",
              "Keshar", "Vibhuti", "Tikku", "Bhagwati", "Deep", "Shallu", "Jorj", "Nidhi", "Madhuanita", "Devinder",
              "Vansu", "Susila", "Gourav", "Varsa", "Damanjeet", "Sanny", "Payal", "Dharmbir", "Gappu", "Chottu",
              "Vakil", "Pushpendra", "Montu", "Ravinderbacchi", "Babli", "Mohabbat", "Soniya", "Rajkumar", "Chhotelal",
              "Preety", "Abhinav", "Rani", "Sahar", "Pardeep", "Shakti", "Sahin", "Abhishekh", "Subham", "Murli",
              "Anubhav", "Rupesh", "Deva", "Kripya", "Mayank", "Aasishkumar", "Kinya", "Sumitra", "Khimanand", "Tejvir",
              "Radheshyam", "Bhag", "Jagdish", "Priynka", "Vikram", "Ikramuddin", "Bigan", "Mahender", "Pramod",
              "Laxmi", "Durga", "Chand", "Sajan", "Mehraj", "Virender", "Tarachandpappu", "Amardeep", "Sona", "Lal",
              "Ranveer", "Phoolwatiphoolo", "Alok", "Devki", "Ankit", "Sarad", "Rajia", "Manpreet", "Ramanrancho",
              "Haider", "Ayush", "Saneha", "Partibha", "Gulnanj", "Guman", "Shankarlalsukharam", "Jony", "Sukhdev",
              "Kanhaiya", "Mazida", "Pandit", "Veer", "Sachin", "Juneb", "Rohan", "Meghana", "Sohni", "Kavita",
              "Murari", "Satyadev", "Gurdeep", "Rajbir", "Komal", "Vicky", "Nanagram", "Aasto", "Azad", "Lakhan",
              "Punam", "Bharkah", "Ranita", "Vikas", "Minakchi", "Bishun", "Brahamprakashmeer", "Pintu", "Neetu",
              "Pavitra", "Neeraj", "Kulli", "Seema", "Laxman", "Sanjeev", "Supriyal", "Vijay", "Arun", "Bhushan",
              "Harneet", "Laxmikumari", "Tripti", "Vikash", "Avinash", "Omparkash", "Ranjeeta", "Janesh", "Subodh",
              "Sheetal", "Adersen", "Shanti", "Himanshiroshani", "Anil", "Sashi", "Surendra", "Jankisoni", "Sagar",
              "Parwati", "Somdath", "Kusuma", "Santlalgolu", "Krishnamanisha", "Chandni", "Parul", "Satnosh",
              "Mohithimanshu", "Banwari", "Yameen", "Sushma", "Minakshi", "Mukul", "Chetanya", "Uma", "Sameer",
              "Malkeet", "Noojo", "Sukhbir", "Sohnal", "Prem", "Sarbjeetronak", "Kamlesh", "Lilu", "Madan", "Deepu",
              "Ajit", "Mahesh", "Dilawar", "Kunal", "Roshan", "Bharat", "Pradeep", "Midda", "Parvesh", "Mahavir", "Son",
              "Balraj", "Archana", "Mubarik", "Uday", "Muntiyaj", "Shilpa", "Jatinsonu", "Ruksana", "Kajol", "Krisana",
              "Arti", "Vipin", "Hare", "Anjli", "Chama", "Hemlata", "Reshma", "Vibha", "Niranjan", "Omprkash",
              "Sangeeta", "Parniti", "Dharmshila", "Nithyanandham", "Diksha", "Muskan", "Roshani", "Abhishek", "Ravish",
              "Mantu", "Pulkit", "Raghunandan", "Vandana", "Asharam", "Arindra", "Ranjita", "Priyansi", "Chanderpal",
              "Gyatri", "Hari", "Surender", "Rishu", "Praful", "Renu", "Aakanksha", "Reema", "Chotti", "Priyanandani",
              "Niraj", "Udham", "Krishna", "Chhabi", "Chetan", "Anupama", "Koshal", "Dheerajmontu", "Sony", "Reena",
              "Shiwani", "Mushir", "Om", "Kanika", "Souravsumit", "Vude", "Spana", "Naveena", "Rimmi", "Doodhnath",
              "Milap", "Pallavi", "Najar", "Tapas", "Monika", "Gayatri", "Phoolmani", "Rekhaboby", "Bittu", "Neeru",
              "Narayan", "Ridhima", "Radhika", "Chandan", "Harbirsingh", "Himanshu", "Sandhya", "Sareen", "Anju",
              "Paramjeet", "Amrit", "Parmod", "Kanta", "Asha", "Ramkaran", "Raju", "Gudya", "Disha", "Ramjan",
              "Liyakat", "Virjiniya", "Buity", "Charu", "Mangla", "Saurabh", "Shiv", "Suraj", "Ashshwer", "Yogesh",
              "Arsh", "Sapna", "Janki", "Amit", "Vinit", "Pramood", "Hoor", "Masoom", "Khushi", "Vandnakrishma",
              "Prince", "Pappy", "Madam", "Swati", "Chango", "Khusbhu", "Savita", "Bhupender", "Yogita", "Bharti",
              "Vashudev", "Ajay", "Goldy", "Madhuri", "Harender", "Anuradha", "Atul", "Samir", "Gopal", "Menadevi",
              "Sonu", "Anuj", "Sorabh", "Saraswati", "Hardeephunny", "Sarojini", "Armaansuvalin", "Kanti", "Sardar",
              "Bilke", "Gyan", "Gulshan", "Rubby", "Shayra", "Vipulander", "Ramesh", "Karan", "Pooja", "Rimpy",
              "Palaksimran", "Babalu", "Bimla", "Girishi", "Manojkumar", "Pankaj", "Inderpal", "Sitara", "Rubbi",
              "Avinsh", "Lala", "Shishram", "Lavtar", "Puran", "Rajender", "Sushant", "Megha", "Tekchand", "Jaya",
              "Devi", "Monu", "Nandkishore", "Badshya", "Hari", "Anand", "Phirdos", "Chhotu", "Neelu", "Nasimareshma",
              "Santosh", "Sohan", "Charan", "Mangat", "Inderjeet", "Kiswar", "Iswar", "Mercy", "Nahar", "Varsha",
              "Rahina", "Preeti", "Khushboo", "Ishtkar", "Lalan", "Shasi", "Kamal", "Gayatrirani", "Munna",
              "Ankushshera", "Kummamta", "Dollyrekha", "Sparsh", "Sangeet", "Deepak", "Mohammad", "Sheru", "Lalita",
              "Noor", "Isha", "Shivani", "Parbhat", "Versha", "Nagma", "Jockyipai", "Rajkumari", "Geeta",
              "Pappumahender", "Nilam", "Divya", "Manisha", "Shenaz", "Jassi", "Deelip", "Jeeya", "Arjun", "Ajayajju",
              "Rashika", "Maansingh", "Rajiv", "Akhil", "Vishvash", "Sabnam", "Vipol", "Rinku", "Vishalmoni", "Babita",
              "Sunita", "Shyama", "Shekher", "Poonam", "Jyoti", "Somender", "Renurinki", "Ramwati", "Ilema", "Satender",
              "Arunvicky", "Sanjit", "Kartikkaku", "Satyenderkalu", "Sureshtinku", "Nisha", "Rubina", "Momin", "Ranbir",
              "Manish", "Varun", "Kamli", "Fitrat", "Kanchan", "Mukhtyar", "Arvind", "Shashikajal", "Krishka", "Ram",
              "Dipendra", "Bulbuldevi", "Rajan", "Ashishaashu", "Suresh", "Rangeeta", "Kanheya", "Khushbu",
              "Ahsaminjuhi", "Gajender", "Rinukanwr", "Neelima", "Meenu", "Rahul", "Ranjana", "Birjesh", "Nandni",
              "Rakhi", "Tammanne", "Satpal", "Bhavesh", "Vipiv", "Sanjay", "Khadak", "Jitender", "Vinay", "Sivani",
              "Akansha", "Heena", "Matuldevi", "Saanu", "Heenazamil", "Roshini", "Abhi", "Jaswant", "Shikha",
              "Shashank", "Anupam", "Abhay", "Parnav", "Manorma", "Arman", "Raja", "Lalit", "Tara", "Samreen", "Meena",
              "Anita", "Tapsam", "Yuvraj", "Uttam", "Ramvati", "Bhawana", "Nitin", "Nootan", "Jyoty", "Resham",
              "Sarojani", "Subhdra", "Mohit", "Puneet", "Ravindra", "Aruna", "Anoop", "Sawan", "Palak", "Manjeet",
              "Bindiya", "Kaushaliya", "Sunali", "Gulafsa", "Alka", "Gaurav", "Sumit", "Laxami", "Ravi", "Dharmender",
              "Khuma", "Sugantisonali", "Ritu", "Kripal", "Priti", "Ziyabul", "Ekta", "Nanhu", "Gunjan", "Puja",
              "Aakash", "Firakat", "Durganand", "Tausin", "Naval", "Rita", "Gorav", "Ruby", "Dimpal", "Preetam", "Rada",
              "Mansi", "Sugodh", "Ashutoshdeepak", "Shukla", "Mayur", "Namarta", "Pawan", "Nand", "Sita", "Inder",
              "Kureja", "Kamre", "Saroj", "Babloo", "Bhrat", "Munni", "Raj", "Sarthak", "Sefalisweta", "Sumnesh",
              "Gytrigarg", "Hemani", "Vishal", "Archna", "Narbada", "Ramvilash", "Dhansinghpuri", "Deepali",
              "Badrunisha", "Abhimanyu", "Mannimanish", "Dheeraj", "Meera", "Pavan", "Kamni", "Chanchal", "Shyam",
              "Lokesh", "Phulkana", "Vandhna", "Amarjeet", "Munender", "Rekha", "Babansuresh", "Ramsurat", "Rampati",
              "Astha", "Dhanwantidevi", "Fooljhnah", "Nikhleshwar", "Priyanka", "Aman", "Mohini", "Lakhi", "Gul",
              "Sitaram", "Rubi", "Kiranvina", "Sonia", "Tamsa", "Rima", "Prakul", "Raman", "Vivek", "Santna", "Sone",
              "Ishant", "Sagartakla", "Kali", "Deepika", "Priyaki", "Hukum", "Bobby", "Jeta", "Pushpa", "Som",
              "Chandesh", "Nikhil", "Bablu", "Akshay", "Karunakar", "Axat", "Ashok", "Garima", "Tanuja", "Ranju",
              "Guddi", "Gungun", "Milan", "Sunil", "Rajmani", "Kirti", "Akkash", "Prema", "Shana", "Nanku", "Nanak",
              "Patikmonu", "Harman", "Munbura", "Gurmit", "Shathi", "Sama", "Himanshi", "Barjraj", "Kalyani", "Kabir",
              "Sandhaya", "Nayana", "Ratikant", "Ruchi", "Nishachinu", "Poornima", "Dalip", "Birender", "Sunaki",
              "Sandeep", "Ravinder", "Parash", "Simran", "Nainshi", "Aashik", "Angreg", "Mannu", "Prateek", "Himansi",
              "Kalawati", "Kumari", "Biwa", "Gurdarshan", "Hemraj", "Kuldeep", "Yashika", "Savita,", "Guddu",
              "Raghuveer", "Deepa", "Sunder", "Ritik", "Moti", "Ishwar", "Batloon", "Jitendra", "Mukesh", "Amarapal",
              "Kajal", "Rishab", "Ravirinkku", "Ashsish", "Ramaiya", "Rinki", "Rajesh", "Ombir", "Rupa", "Sneha",
              "Kusum", "Subhadra", "Ashish", "Shabana", "Munnaravi", "Shakshi", "Sonam", "Vaishali", "Reeta",
              "Subhamvikash", "Sanavvar", "Chotelal", "Bhanwar", "Kesnata"],

    "Buddhist": ["Abhaya", "Achara", "Adhiarja", "Adika", "Agung", "Altansarnai", "Altantsetseg", "Amanthi",
                 "Amitaruci", "Ananada", "Anantacaritra", "Anantamati", "Anantavikrama", "Angkasa", "Anh", "Anong",
                 "Anuman", "Anzan", "Aom", "Arban", "Arkar", "Asahi", "Ashwaghosh", "Asnee", "Atid", "Aung",
                 "Avalokitesvara", "Aye", "Bagaskoro", "Bagus", "Baharupa", "Bahuksana", "Baika", "Bakti", "Balavrata",
                 "Bankei", "Banyu", "Banzan", "Bao", "Basho", "Bassui", "Bat Erdene", "Bataar", "Batbayar", "Batjargal",
                 "Batsaikhan", "Batuhan", "Batukhan", "Batzorig", "Bayarmaa", "Beam", "Bensen", "Bhadanta",
                 "Bhadrapala", "Bhismasvaraja", "Bi", "Boddhidharma", "Bodhi", "Bodhidharma", "Bolin", "Bolormaa",
                 "Boon-Mee", "Boon-Nam", "Boonsri", "Brahmadhvaja", "Brahmajetas", "Brhadsphalas", "Bu", "Buddha",
                 "Buddhacaksus", "Buddhamitra", "Buddhanandi", "Budh", "Budhasuta", "Budi", "Bupposo", "Busarakham",
                 "Butsugen", "Butsuju", "Buu", "Cahya", "Caihong", "Cais", "Cakrasmavara", "Candavira", "Candragarbha",
                 "Candrakirti", "Candrasurya", "Canh", "Cao", "Cetan", "Chaghatai", "Chai Son", "Chaisai", "Chaiya",
                 "Chakan", "Chalerm", "Chalermchai", "Chaloem", "Champo", "Chandaka", "Channarong", "Charanpreet",
                 "Charini", "Chenda", "Chenghiz", "Chesa", "Chewa", "Chiko", "Chime", "Chimeg", "Chingis", "Chinshu",
                 "Chinua", "Chit", "Choden", "Chodren", "Chomden", "Chorei", "Chosui", "Chozen", "Chuanchen", "Chugai",
                 "Chuluun", "Chuluunbold", "Chuong", "Cudabhiksuni", "Cuong", "Da Shin", "Dachen", "Daibai", "Daiden",
                 "Daido", "Daiji", "Daikaku", "Daikan", "Daiko", "Dainin", "Daishin", "Daivika", "Dampa", "Danan",
                 "Danasura", "Danyasarathi", "Dasbala", "Dashin", "Dawa", "Dayakurca", "Decha", "Dechen", "Dedan",
                 "Denkatsu", "Denpa", "Denpo", "Devasrigarbha", "Devatideva", "Dhanayus", "Dhanibuddha", "Dhanuraja",
                 "Dharmadhara", "Dharmadhatu", "Dharmakara", "Dhiman", "Dhitika", "Diki", "Dipankara", "Divijata",
                 "Dohna", "Dojin", "Dokai", "Dolkar", "Doryu", "Doyu", "Drdahana", "Drdhahanus", "Drtaka", "Druk",
                 "Druki", "Duangkamol", "Duanphen", "Dundhabisvara", "Durdharsakumara", "Dzhambul", "Eido", "Eila",
                 "Eindra", "Ekai Jinko", "Ekaijinko", "Enkhjargal", "Enkhtuya", "Enmei", "Erden", "Erdenechimeg",
                 "Erhi", "Eshin", "Etsudo", "Fa", "Fai", "Feng", "Fu", "Fuji", "Fumihiro", "Fumiko", "Gan", "Ganbaatar",
                 "Ganbold", "Ganendra", "Gang", "Gansukh", "Gantulga", "Ganzorig", "Garma", "Gawa", "Genghis", "Genji",
                 "Genjin", "Genjo", "Genkai", "Genkaku", "Genkei", "Genki", "Genko", "Genno", "Gensho", "Gerel",
                 "Getsuren", "Gewa", "Goldeheve", "Gomin", "Gunaketu", "Gurtej", "Gurtek", "Hakaku", "Hakue",
                 "Hanumanta", "Hanumanth", "Harsula", "Hayma", "Haymar", "Heljo", "Hella", "Hema", "Hiten", "Hla",
                 "Hlaing", "Hodo", "Hopkins", "Hopkinson", "Hosho", "Htay", "Htet", "Htin", "Htun", "Htut", "Htway",
                 "Indazita", "Indivar", "Indrajalin", "Inzali", "Issan", "Itsuki", "Jahlee", "Jahleel", "Jampa",
                 "Jayasurya", "Jayathi", "Jiao-long", "Jie", "Jiho", "Jikai", "Jimmyl", "Jimuta", "Jin", "Jiyu",
                 "Jochi", "Justeene", "Justen", "Kamnan", "Kan", "Kannika", "Kanok", "Kanokwan", "Kanshin", "Karambir",
                 "Karamia", "Karawek", "Karma", "Karnchana", "Kasemchai", "Keisho", "Kesang", "Khemkhaeng", "Khenbish",
                 "Khin", "Khine", "Khongordzol", "Khulan", "Khun Mae", "Khunbish", "Kittibun", "Kittichat", "Kla",
                 "Klaew Kla", "Kob Sook", "Kobutsu", "Koge", "Kohsoom", "Koju", "Kokan", "Kokoro", "Kongkea", "Kraisee",
                 "Kriang Krai", "Kulap", "Kumbikhanna", "Kwang", "Kyaw", "Kyi", "Kyine", "Kywe", "Lamon", "Lawan",
                 "Leakhena", "Lek", "Lhamu", "Li Jie", "Li Jing", "Li Jun", "Li Na", "Li Wei", "Li Xiu", "Liu Wei",
                 "Lkhagvas\u00fcren", "Loday", "Longwei", "Lwin", "Madee", "Malee", "Malivalaya", "Manjusri", "Marlar",
                 "Maung", "Mayuree", "Medekhgui", "Mee Noi", "Mima", "Minato", "Mongolekhorniiugluu", "Monkh Erdene",
                 "Monkhbat", "Munish", "Munkhtsetseg", "Muunokhoi", "Myaing", "Myat", "Myia", "Myine", "Myint",
                 "Myitzu", "Myo", "Naing", "Nandar", "Narangerel", "Narantsetseg", "Natcha", "Nekhii", "Nilar", "Nima",
                 "Nin", "Nugai", "Nyan", "Nyein", "Nyunt", "Och", "Od", "Odgerel", "Odtsetseg", "Odval", "Ogtbish",
                 "Ohma", "Ohnmar", "Oktai", "Opame", "Orochi", "Otgonbayar", "Oyunchimeg", "Oyuunchimeg", "Padmayani",
                 "Paitoon", "Pakpao", "Pali", "Pasang", "Patakin", "Pema", "Pemala", "Penden", "Pensri", "Phaibun",
                 "Phairoh", "Phassakorn", "Phawta", "Phichit", "Phitsamai", "Phone", "Phueng", "Phurba", "Phyu",
                 "Pimchan", "Ploy", "Pururavas", "Qacha", "Qara", "Rinzen", "Ritthirong", "Rochana", "Saengdao",
                 "Sakda", "Sakyamuni", "Samorn", "San", "Sandar", "Sandeepe", "Sandeepen", "Sangmu", "Sankalpa",
                 "Sanoh", "Sarangerel", "Sarantsatsral", "Sarasija", "Sarnai", "Shakyasinha", "Shein", "Shenden",
                 "Shway", "Siddhartha", "Sirichai", "Sirikit", "Siriporn", "Socheata", "Soe", "Somchair", "Sonam",
                 "Soo", "Sook", "Sopa", "Sophea", "Sopheak", "Sou", "Sovann", "Sovannah", "Sovay", "Sreyleak", "Sud",
                 "Suda", "Sukhbataar", "Sunako", "Sunstra", "Suong", "Susu", "Syaoran", "Taban", "Tadaaki", "Tae",
                 "Taichi", "Taiga", "Taiki", "Taji", "Taka", "Takahiro", "Takai", "Takako", "Takara", "Takarra",
                 "Takashi", "Takato", "Takaya", "Takeo", "Taki", "Taku", "Takuma", "Tanawat", "Tarkhan", "Taru",
                 "Tasanee", "Tashi", "Tathagat", "Tathagata", "Tatharaj", "Teesta", "Temujin", "Tenpa", "Tenzin",
                 "Tenzin; Tenzing", "Tenzing", "Terbish", "Thagyamin", "Tham", "Thandar", "Thang", "Thanh", "Thant",
                 "Thao", "Thaung", "Thawda", "Thawka", "Theavy", "Thein", "Theingi", "Therein", "Thet", "Thida",
                 "Thien", "Thiha", "Thiri", "Tho", "Thuan", "Thuc", "Thuong", "Thura", "Thuta", "Thuy", "Thuya",
                 "Thuyet", "Thuza", "Thuzar", "Ti", "Tida", "Tien", "Tika", "Tin", "Tohru", "Tomiche",
                 "Tomiichi", "Tomo", "Tomoe", "Tomohiro", "Tomoko", "Tomorbaatar", "Tomoya", "Tong", "Tonica", "Tora",
                 "Toru", "Toshiko", "Toshiro", "Trieu", "Trigya", "Tsetseg", "Tsetsegmaa", "Tsolmon", "Tsubame",
                 "Tsubasa", "Tsukiya", "Tsumugi", "Tsuru", "Tu", "Tun", "Turgen", "Tuya", "Tuyen", "Tuyet", "Tylanni",
                 "Ulagan", "Upagupta", "Uranchimeg", "Uttiya", "Uuliinyagaantsetseg", "Vipaschit", "Wang Fang",
                 "Wang Jing", "Wang lei", "Wang Li", "Wang Wei", "Wang Xiu", "Wang Yong", "Wendywee", "Wunna", "Yadana",
                 "Yadanar", "Yamato", "Yangchen", "Yangkyi", "Yarzar", "Yaza", "Yeshe", "Yonten", "Youta", "Yul", "Yun",
                 "Yuu", "Yuuma", "Yuuto", "Yuzana", "Zachoeje", "Zar", "Zarni", "Zaw", "Zenji", "Zeya", "Zeyar",
                 "Zhang Li", "Zhang Min", "Zhang Wei", "Zhang Xiu", "Zhang Yong", "A-wut", "Abhaya", "Adhiarja",
                 "Adika", "Agung", "Amitaruci", "Ananada", "Anantacaritra", "Anantamati", "Anantavikrama", "Anh",
                 "Anuman", "Anurak", "Anzan", "Arban", "Arkar", "Asahi", "Ashwaghosh", "Asnee", "Aung",
                 "Avalokitesvara", "Aye", "Bagaskoro", "Bagus", "Baharupa", "Bahuksana", "Baika", "Bakti", "Balavrata",
                 "Bankei", "Banko", "Banyu", "Banzan", "Bao", "Basho", "Bassui", "Bat Erdene", "Bataar", "Batjargal",
                 "Batsaikhan", "Batuhan", "Batukhan", "Batzorig", "Bensen", "Bhadanta", "Bhadrapala", "Bhismasvaraja",
                 "Bhuddisrigarbha", "Boddhidharma", "Bodhidharma", "Bolin", "Boon-Mee", "Boon-Nam", "Brahmadhvaja",
                 "Brahmajetas", "Brhadsphalas", "Bu", "Buddhacaksus", "Buddhamitra", "Buddhanandi", "Budh", "Budhasuta",
                 "Budhh", "Budi", "Bupposo", "Butsugen", "Butsuju", "Buu", "Cahya", "Cais", "Cakrasmavara", "Candavira",
                 "Candragarbha", "Candrakirti", "Candrasurya", "Canh", "Chaghatai", "Chai Son", "Chaisai", "Chaiya",
                 "Chakan", "Chalerm", "Chalermchai", "Chaloem", "Champo", "Chandaka", "Channarong", "Charanpreet",
                 "Chenghiz", "Chiko", "Chimon", "Chingis", "Chinshu", "Chinua", "Chorei", "Chosui", "Chozen",
                 "Chuanchen", "Chugai", "Chuluun", "Chuluunbold", "Chuong", "Cuong", "Da Shin", "Dachen", "Daeshim",
                 "Daibai", "Daiden", "Daido", "Daiji", "Daikaku", "Daikan", "Daiko", "Dainin", "Daishin", "Dampa",
                 "Danan", "Danasura", "Danyasarathi", "Dasbala", "Dashin", "Dayakurca", "Decha", "Dechen", "Dedan",
                 "Denkatsu", "Denpa", "Denpo", "Devasrigarbha", "Devatideva", "Dhanayus", "Dhanibuddha", "Dhanuraja",
                 "Dharmadhara", "Dharmakara", "Dhiman", "Dhitika", "Dipankara", "Divijata", "Dojin", "Dokai", "Doryu",
                 "Doyu", "Drdahana", "Drdhahanus", "Drtaka", "Druki", "Dundhabisvara", "Durdharsakumara", "Dzhambul",
                 "Eido", "Ekai Jinko", "Ekaijinko", "Erden", "Eshin", "Etsudo", "Fa", "Fai", "Feng", "Fu", "Fumihiro",
                 "Gan", "Ganbaatar", "Ganbold", "Ganendra", "Gang", "Gansukh", "Gantulga", "Ganzorig", "Genghis",
                 "Genjin", "Genjo", "Genkaku", "Genkei", "Genki", "Genko", "Genno", "Genpo", "Gensho", "Getsuren",
                 "Gomin", "Gunaketu", "Gurtej", "Gurtek", "Hakaku", "Hakue", "Hanumanta", "Hanumanth", "Harsula",
                 "Hemlal", "Hiten", "Hlaing", "Hodo", "Hopkins", "Hopkinson", "Hosho", "Htay", "Htet", "Htin", "Htun",
                 "Htut", "Htway", "Indazita", "Indivar", "Indrajalin", "Issan", "Itsuki", "Jahlee", "Jahleel",
                 "Jayasurya", "Jiao-long", "Jiho", "Jikai", "Jimmyl", "Jimuta", "Jin", "Jiyu", "Jochi", "Justen",
                 "Kamnan", "Kan", "Kanshin", "Karambir", "Kasemchai", "Keisho", "Khemkhaeng", "Khenbish", "Khin",
                 "Khine", "Khunbish", "Kittichat", "Kla", "Klaew Kla", "Kob Sook", "Kobutsu", "Koge", "Koju", "Kokan",
                 "Koshing", "Kraisee", "Kriang Krai", "Kumbikhanna", "Kywe", "Lamon", "Lek", "Li Jie", "Li Jun",
                 "Li Qiang", "Li Wei", "Lkhagvas\u00fcren", "Loday", "Longwei", "Lwin", "Maung", "Mee Noi", "Minato",
                 "Mongkut", "Mongolekhorniiugluu", "Monkh Erdene", "Monkhbat", "Munish", "Muunokhoi", "Myaing", "Myat",
                 "Myint", "Myo", "Naimanzuunnadintsetseg", "Naing", "Nugai", "Nyan", "Nyein", "Nyunt", "Och", "Od",
                 "Odgerel", "Ogtbish", "Ohnmar", "Oktai", "Orochi", "Otgonbayar", "Padmayani", "Paitoon", "Partha",
                 "Pasang", "Patakin", "Phassakorn", "Phichit", "Phyu", "Pururavas", "Qara", "Ritthirong", "Sakda",
                 "Sakyamuni", "Sandeepe", "Sandeepen", "Sangmu", "Sankalpa", "Sarasija", "Shakyasinha", "Shein",
                 "Shway", "Siddhartha", "Sirichai", "Soe", "Somchair", "Sopheak", "Sou", "Sovay", "Sud", "Sukhbataar",
                 "Susu", "Syaoran", "Taban", "Tadaaki", "Tadashi", "Tae", "Taichi", "Taiga", "Taiki", "Taji",
                 "Takahiro", "Takai", "Takashi", "Takato", "Takaya", "Takeo", "Takuma", "Tanawat", "Tarkhan", "Taru",
                 "Tashi", "Tathagat", "Tathagata", "Tatharaj", "Teesta", "Temujin", "Tenpa", "Tenzin", "Tenzing",
                 "Terbish", "Thagyamin", "Thant", "Thaung", "Thein", "Therein", "Thien", "Thiha", "Thuan", "Thuc",
                 "Thuong", "Thura", "Thuta", "Thuy", "Thuya", "Thuyet", "Thuza", "Tin", "Tohru", "Tokyo", "Tomiche",
                 "Tomiichi", "Tomohiro", "Tomorbaatar", "Tomoya", "Toru", "Toshiro", "Trieu", "Trigya", "Tsukiya", "Tu",
                 "Tun", "Turgen", "Twan", "Ulagan", "Upagupta", "Uttiya", "Vipaschit", "Wang lei", "Wang Wei",
                 "Wang Yong", "Wunna", "Xanadu", "Yamato", "Yarzar", "Yaza", "Yeshe", "Yonten", "Youta", "Yul", "Yuu",
                 "Yuuma", "Yuuto", "Zachoeje", "Zaw", "Zenji", "Zeya", "Zeyar", "Zhang Wei", "Zhang Yong"],

    "Jain": ["Aadinath", "Aagam", "Aakash", "Aalok", "Aanat", "Aanay", "Aatman", "Abhay", "Abhay Kumar", "Abhay Prasad",
             "Abhayendra", "Abhi", "Abhijeet", "Abhinandan", "Abhishek", "Adinath", "Ajatshatru", "Ajey", "Ajit",
             "Ajit Kumar", "Ajit Prasad", "Ajitnath", "Akalank", "Akash", "Akshat", "Akshay", "Alok", "Amar", "Amogh",
             "Amoghvarsh", "Amrish", "Amritchandra", "Amrutchandra", "Anant", "Anant Kumar", "Anant Prasad",
             "Anantnath", "Anish", "Ankesh", "Ankit", "Ankur", "Anuj", "Anup", "Archit", "Arhadas", "Arhant", "Arhat",
             "Arhnath", "Arihant", "Arinjay", "Arish", "Atik", "Atish", "Atith", "Ativeer", "Bahubali", "Balbhadra",
             "Baldev", "Bhaarat", "Bhadrabahu", "Bhadresh", "Bhamandal", "Bharam", "Bharat", "Bharat Kumar",
             "Bharateshwar", "Bharatraj", "Bhargav", "Bhartendu", "Bhartesh", "Bhaskar", "Bhaumik", "Bhautik",
             "Bhavesh", "Bhavin", "Bhumi", "Bhupal", "Bhuvanedra Kumar", "Bhuvanendra", "Bhuvanesh", "Bimbisar",
             "Bindusar", "Bramha", "Bramhendra", "Brijesh", "Chaitan", "Chakrawarti", "Chakrvarti", "Chamundrai",
             "Chandragupta", "Chandrakant", "Chandranath", "Chandraprabhu", "Chetak", "Chetan", "Chintan", "Chirag",
             "Chirayu", "Chitrang", "Dakshesh", "Darsh", "Darshan", "Darshil", "Darshit", "Deshbhushan", "Devang",
             "Devendra", "Devendra Kumar", "Devesh", "Dhanesh", "Dhanpal", "Dharin", "Dharm", "Dharmanath",
             "Dharmendra", "Dharmesh", "Dharmin", "Dharnendra", "Dharsen", "Dhaval", "Dhimant", "Dhiram", "Dhiren",
             "Dhvanish", "Digant", "Dipesh", "Dirgh", "Divyesh", "Falgun", "Fenil", "Gajkumar", "Gandhar", "Gaurang",
             "Gitesh", "Gomtesh", "Goutam", "Gunesh", "Gyanendra", "Hardik", "Harikesh", "Harsh", "Harshit", "Heer",
             "Hemchandra", "Hemendra", "Hetul", "Ilesh", "Indrabhuti", "Jainam", "Jainesh", "Jaipal", "Jay", "Jaypal",
             "Jeet", "Jigar", "Jignesh", "Jineshwar", "Jiten", "Jitesh", "Jugal", "Kalyan", "Karan", "Kaustubh",
             "Krupesh", "Krutarth", "Kulbhushan", "Kulin", "Kumarpal", "Kunthinath", "Kunthu", "Kunthunath",
             "Kunthusagar", "Lalit", "Litesh", "Mahavir", "Mallesh", "Mallinath", "Manav", "Mandar", "Mangal",
             "Manthan", "Maulik", "Mihir", "Milind", "Mitul", "Mokshit", "Mrugesh", "Mrunal", "Munindra",
             "Munindra Kumar", "Munisuvrat", "Nabhi", "Nabhikumar", "Nabhinandan", "Nabhiraj", "Nabhiray", "Nagendra",
             "Nagkumar", "Nakesh", "Namikumar", "Naminath", "Nandivardhan", "Nemdas", "Nemendra", "Nemi", "Nemichand",
             "Nemichandra", "Nemidas", "Nemikumar", "Neminath", "Nemish", "Nemnath", "Nihir", "Niket", "Nikhil",
             "Nilesh", "Nimesh", "Nirav", "Nirbhay", "Nirmal", "Nirmal Kumar", "Nirmal Prasad", "Nishal", "Nishant",
             "Nishith", "Nitesh", "Padmakumar", "Padmanath", "Padmaprabhu", "Padmaraj", "Pallav", "Parag", "Paras",
             "Paraskumar", "Parshwa", "Parshwakumar", "Parshwanath", "Pathik", "Piyush", "Prabhav", "Pradumna",
             "Pradyot", "Pragnesh", "Prajesh", "Pranav", "Pranay", "Pranjal", "Prasenjit", "Prashant", "Pratham",
             "Pratik", "Pritesh", "Purav", "Rachit", "Rahi", "Raj", "Rajendra", "Rajkumar", "Rakshit", "Rashesh",
             "Ratesh", "Ratnakar", "Ratnesh", "Ravi", "Ravindra", "Riddhesh", "Rishabhdev", "Rishabhkumar",
             "Rishabhnath", "Rishabhraj", "Ritesh", "Ritul", "Romit", "Ronak", "Rupin", "Sagar", "Saket", "Sakshat",
             "Samant", "Samantbhadra", "Samarth", "Sambhav", "Sambhavnath", "Samkit", "Sammed", "Samprati", "Samvar",
             "Samyak", "Sanket", "Sanyat", "Saran", "Sarvesh", "Sashank", "Saurabh", "Shantikumar", "Shantilal",
             "Shantinath", "Shantiprasad", "Shatichandra", "Sheetalnath", "Sheetalprasad", "Shrenik", "Shreyans",
             "Shreyansnath", "Shreyas", "Shripal", "Siddhant", "Siddharth", "Sidhesh", "Sitanshu", "Smit", "Subahu",
             "Subham", "Suchit", "Sudarshan", "Sudesh", "Sudharma", "Suhash", "Sujash", "Aarya", "Aaushi", "Aditi",
             "Akshya", "Alpa", "Aneri", "Angi", "Angira", "Anisha", "Anjana", "Ankita", "Anshita", "Anuja", "Arati",
             "Archa", "Arpita", "Arti", "Avani", "Bela", "Bhakti", "Bharati", "Bhavana", "Bhavika", "Bhavisha",
             "Bhranti", "Bina", "Binal", "Binita", "Bramhi", "Bramhila", "Chaitali", "Chakreshwari", "Champa",
             "Champa Kumari", "Champapuri", "Chandana", "Chandanbala", "Charmi", "Chelana", "Chetana", "Chhaya",
             "Chiti", "Darsana", "Darshana", "Darshika", "Daya", "Deshna", "Devanshi", "Devi", "Dhara", "Dharini",
             "Dhisha", "Dhruti", "Dhvani", "Diksha", "Dipti", "Dishita", "Divya", "Divyaprabha", "Drishti", "Falguni",
             "Foram", "Gargi", "Garima", "Gatha", "Gautami", "Gira", "Harsha", "Hema", "Hemali", "Hemanshi", "Indrani",
             "Jahanvi", "Jalpa", "Jayana", "Jigisha", "Jinali", "Jinisha", "Jwala", "Jwalamalini", "Kajal", "Kalika",
             "Keya", "Khusali", "Khyati", "Komal", "Krupali", "Kruti", "Kshama", "Kushmandini", "Labdhi", "Lajja",
             "Madhvi", "Maitri", "Mallika", "Mangala", "Manishi", "Manshi", "Margi", "Marudevi", "Meghal", "Miti",
             "Moksha", "Monal", "Mruga", "Mukti", "Nainshi", "Nami", "Namrata", "Nandita", "Nikita", "Nimisha",
             "Nirmala", "Nishita", "Nitali", "Nitya", "Padmaja", "Padmavati", "Padmini", "Pava", "Pawapuri", "Pooja",
             "Prabha", "Prabhavati", "Pradnya", "Pragya", "Pratima", "Pratishta", "Puja", "Purti", "Rajal", "Rajalmati",
             "Rajimati", "Rajmati", "Rajul", "Rajulmati", "Rajvi", "Rakhi", "Ramya", "Ratnali", "Riddhi", "Rima",
             "Ritvi", "Riya", "Ruchira", "Rushita", "Sadhana", "Sadhna", "Sakshi", "Samali", "Samata", "Samhita",
             "Sandhya", "Sanmati", "Sapana", "Saraswati", "Sashi", "Satya", "Saumya", "Shaila", "Shaili", "Shailja",
             "Shantala", "Shanti", "Sheetal", "Shena", "Shila", "Shilpa", "Shital", "Shivani", "Shraddha", "Shrina",
             "Shruti", "Shubhali", "Shyama", "Siddhi", "Sonal", "Sonali", "Sreya", "Srusti", "Stuti", "Sumangala",
             "Sumati", "Sundari", "Suprabha", "Surali", "Sushali", "Suta", "Svati", "Tamanna", "Tapasya", "Tejal",
             "Toral", "Trishala", "Trishla", "Trushna", "Trushti", "Tulika", "Tulya", "Udita", "Ullupi", "Umangi",
             "Unnati", "Urja", "Urmil", "Urmila", "Urvi", "Ushma", "Vaidehi", "Vaishali", "Vallabhi", "Vama", "Vandana",
             "Vapra", "Vatsha", "Vibha", "Vibhuti", "Vidhi", "Vidya", "Vinaya", "Vipra", "Virani", "Vishali", "Vruddhi",
             "Vrunda", "Vrushti", "Vrutti", "Yama", "Yashashvi", "Yesha", "Zankhana", "Zarna", "Zeel"],

    "Christian": ["THOMAS", "JAMES", "JACK", "DANIEL", "MATTHEW", "RYAN", "JOSHUA", "LUKE", "SAMUEL", "JORDAN", "ADAM",
                  "MICHAEL", "ALEXANDER", "CHRISTOPHER", "BENJAMIN", "JOSEPH", "LIAM", "JAKE", "WILLIAM", "ANDREW",
                  "GEORGE", "LEWIS", "OLIVER", "DAVID", "ROBERT", "JAMIE", "NATHAN", "CONNOR", "JONATHAN", "HARRY",
                  "CALLUM", "AARON", "ASHLEY", "BRADLEY", "JACOB", "KIERAN", "SCOTT", "SAM", "JOHN", "BEN", "MOHAMMED",
                  "NICHOLAS", "KYLE", "CHARLES", "MARK", "SEAN", "EDWARD", "STEPHEN", "RICHARD", "ALEX", "PETER",
                  "DOMINIC", "JOE", "REECE", "LEE", "RHYS", "STEVEN", "ANTHONY", "CHARLIE", "PAUL", "CRAIG", "JASON",
                  "DALE", "ROSS", "CAMERON", "LOUIS", "DEAN", "CONOR", "SHANE", "ELLIOT", "PATRICK", "MAX", "SHAUN",
                  "HENRY", "SIMON", "TIMOTHY", "MITCHELL", "BILLY", "PHILIP", "JOEL", "JOSH", "MARCUS", "DYLAN", "CARL",
                  "ELLIOTT", "BRANDON", "MARTIN", "TOBY", "STUART", "GARETH", "DANNY", "CHRISTIAN", "TOM", "DECLAN",
                  "KARL", "MOHAMMAD", "MATHEW", "JAY", "OWEN", "DARREN", "RICKY", "TONY", "BARRY", "LEON", "TERRY",
                  "GREGORY", "BRIAN", "KEITH", "ANTONY", "JUSTIN", "MARTYN", "LEIGH", "ABDUL", "DAMIEN", "STEWART",
                  "ROBIN", "IAIN", "GAVIN", "TREVOR", "GLEN", "RAYMOND", "MALCOLM", "GARRY", "BRETT", "KENNETH",
                  "ROGER", "GLENN", "TERENCE", "DEREK", "IAN", "KEVIN", "GARY", "ALAN", "NEIL", "NIGEL", "COLIN",
                  "GRAHAM", "ADRIAN", "WAYNE", "JEREMY", "RUSSELL", "JEFFREY", "CLIVE", "PHILLIP", "JULIAN", "GEOFFREY",
                  "ROY", "VINCENT", "GORDON", "DUNCAN", "LESLIE", "RONALD", "FRANCIS", "GRAEME", "GUY",
                  "ERIC", "ALLAN", "GERARD", "GERALD", "HOWARD", "DENNIS", "BRUCE", "DONALD", "BERNARD", "FRANK",
                  "NORMAN", "FREDERICK", "ARTHUR", "LEONARD", "LAWRENCE", "BRYAN", "CLIFFORD", "STANLEY", "VICTOR",
                  "HUGH", "MOHAMED", "ALBERT", "MAURICE", "DENIS", "RODNEY", "BARRIE", "REGINALD", "ERNEST", "ALFRED",
                  "HAROLD", "MELVYN", "WALTER", "EDWIN", "RALPH", "IVAN", "CYRIL", "SIDNEY", "ROYSTON", "HERBERT",
                  "DERRICK", "NEVILLE", "IVOR", "DESMOND", "WILFRED", "SYDNEY", "CECIL", "NOEL", "FRED", "ARNOLD",
                  "ALEC", "REBECCA", "LAUREN", "JESSICA", "CHARLOTTE", "HANNAH", "SOPHIE", "AMY", "EMILY", "LAURA",
                  "EMMA", "CHLOE", "SARAH", "LUCY", "KATIE", "BETHANY", "JADE", "MEGAN", "ALICE", "RACHEL", "SAMANTHA",
                  "DANIELLE", "HOLLY", "ABIGAIL", "OLIVIA", "STEPHANIE", "ELIZABETH", "VICTORIA", "NATASHA", "GEORGIA",
                  "ZOE", "NATALIE", "ELEANOR", "SHANNON", "PAIGE", "GEORGINA", "GEMMA", "NICOLE", "CHELSEA", "KIRSTY",
                  "ALEXANDRA", "MELISSA", "JENNIFER", "HAYLEY", "LOUISE", "KATHERINE", "JODIE", "GRACE", "ANNA",
                  "MOLLY", "AMBER", "JASMINE", "KAYLEIGH", "KELLY", "HARRIET", "ASHLEIGH", "CATHERINE", "LEAH",
                  "NICOLA", "FRANCESCA", "NAOMI", "KATE", "ABBIE", "CLAIRE", "LEANNE", "RACHAEL", "ROSIE", "AIMEE",
                  "ELLIE", "SIAN", "KIMBERLEY", "LYDIA", "HOLLIE", "STACEY", "BETHAN", "AMELIA", "BETH", "KATHRYN",
                  "HEATHER", "LISA", "HELEN", "ELLA", "ROBYN", "CHANTELLE", "ELLEN", "DAISY", "DEMI", "COURTNEY",
                  "GABRIELLE", "YASMIN", "LILY", "RHIANNON", "MARIA", "KERRY", "IMOGEN", "REBEKAH", "JORDAN", "JOANNA",
                  "CAITLIN", "JEMMA", "TONI", "MICHELLE", "JOANNE", "DONNA", "CLARE", "JENNA", "CAROLINE", "AMANDA",
                  "KAREN", "ALISON", "SARA", "CARLY", "RUTH", "FIONA", "ANGELA", "SUZANNE", "KATY", "MARIE", "CHERYL",
                  "MELANIE", "SALLY", "JULIE", "CHARLENE", "TRACEY", "DEBORAH", "LINDSEY", "LINDSAY", "SUSAN", "JANE",
                  "KIM", "CARLA", "CHRISTINE", "DAWN", "TANYA", "JENNY", "ANDREA", "LYNDSEY", "JACQUELINE", "LYNSEY",
                  "MARY", "SHARON", "TRACY", "PAULA", "WENDY", "LORRAINE", "TINA", "ANNE", "JULIA", "GILLIAN",
                  "VANESSA", "ANN", "JAYNE", "DIANE", "SANDRA", "TERESA", "LINDA", "ELAINE", "NICHOLA", "CAROL",
                  "HEIDI", "PATRICIA", "BEVERLEY", "DENISE", "TARA", "CLAIR", "SONIA", "DEBBIE", "LESLEY", "ANITA",
                  "DEBRA", "JANET", "MARGARET", "MANDY", "PAULINE", "LYNN", "YVONNE", "JUDITH", "PAMELA", "CAROLE",
                  "BARBARA", "GAIL", "LYNNE", "JANICE", "JILL", "KATHLEEN", "SHIRLEY", "ANNETTE", "CAROLYN", "VALERIE",
                  "JEANETTE", "KAY", "MAXINE", "FRANCES", "THERESA", "LYNDA", "MAUREEN", "ROSEMARY", "MICHELE",
                  "SHEILA", "JEAN", "MARION", "JOAN", "MARILYN", "MARIAN", "BRENDA", "EILEEN", "HILARY",
                  "SYLVIA", "IRENE", "DOROTHY", "JOSEPHINE", "JOYCE", "HAZEL", "RITA", "GERALDINE", "DIANA",
                  "CHRISTINA", "PENELOPE", "JOY", "DOREEN", "GLYNIS", "VERONICA", "AUDREY", "BERYL", "NORMA", "GLORIA",
                  "MARJORIE", "CYNTHIA", "MAVIS", "MARLENE", "BETTY", "EVELYN", "IRIS", "VERA", "BRIDGET", "LILIAN",
                  "MONICA", "GLENYS", "VIVIENNE", "DAPHNE", "PHYLLIS", "GWENDOLINE", "DORIS", "MURIEL"],

    "Sikh": ["Abhaijeet", "Amanjit", "Amanpreet", "Amardeep", "Anantjeet", "Anokh", "Arinajeet", "Arman", "Arunvir",
             "Aryan", "Ashreet", "Avaneet", "Baljeet", "Balmeet", "Balpreet", "Bhavdeep", "Bhavmeet", "Birpal",
             "Bishanpal", "Bishmeet", "Bismeet", "Brahmjot", "Brahmpal", "Brahmvir", "Chanderjit", "Chanderpreet",
             "Charanpal", "Charnjit", "Chattarpal", "Daler", "Daljeet", "Dhanjeet", "Dhanwant", "Dharam", "Dilbaag",
             "Dilmeet", "Divyajot", "Fateh", "Gagan", "Guneet", "Gurdas", "Gurman", "Hans", "Harbir", "Harcharanjit",
             "Hardayal", "Hardeep", "Hargun", "Harjeet", "Harman", "Harnek", "Harprit", "Ikhtiar", "Imrat",
             "Inderpreet", "Indivar", "Indrajit", "Ishapreet", "Isharjeet", "Ishjeet", "Ishmeet", "Ishpal", "Ishwar",
             "Ishwinder", "Isminder", "Jaghr", "Jagjeet", "Janeesh", "Japneet", "Jasjeev", "Jasmanvir", "Jasveer",
             "Jaswant", "Jeet", "Jivan", "Jugraj", "Kanwal", "Karanvir", "Kavneet", "Khushjeet", "Khushpreet",
             "Khushwant", "Kiranjit", "Kirpal", "Kuldeep", "Lamjot", "Lavanya", "Livtar", "Lokpreet", "Lovejeet",
             "Lovepreet", "Madhupreet", "Mahajeet", "Mahipal", "Mandeep", "Maneet", "Manpreet", "Manraj", "Mohanpal",
             "Mohinder", "Naampreet", "Naindeep", "Naitarpal", "Narveer", "Navnihal", "Navpreet", "Navraj",
             "Neelamjeet", "Ojas", "Ompreet", "Onkarjit", "Onkarpreet", "Paramjeet", "Paramvir", "Pargatjeet", "Prajit",
             "Praneet", "Rajvir", "Ranjit", "Ranvir", "Raviraj", "Sajiv", "Samarjeet", "Sarjeet", "Sartaj", "Shamsher",
             "Tandeep", "Tanmeet", "Taranvir", "Tarunpal", "Tejdeep", "Tejpal", "Uchitjeet", "Upjeet", "Urveer",
             "Uttam", "Vajrajit", "Veer", "Vishwpal", "Yamajit", "Yashveer", "Yudhjeet", "Yuvraj", "Aamodini",
             "Anureet", "Armani", "Armin", "Asreet", "Avneet", "Eshnaa", "Eveneet", "Garima", "Gunjeet", "Gurjeet",
             "Gurupreet", "Heera", "Hema", "Hir", "Japleen", "Jasjeet", "Jasmeen", "Jasmeet", "Jasmit", "Jaspreet",
             "Jhalak", "Julie", "Karunya", "Kashmira", "Lavanya", "Luvleen", "Maheshwari", "Manreet", "Manveer",
             "Meher", "Mridula", "Noor", "Prageet", "Prajna", "Preet", "Raveena", "Ridhima", "Rubani", "Sadhika",
             "Savreen", "Shana", "Simrat", "Simrita", "Sunaina", "Surina", "Sushmeet", "Tripta", "Vasundhara", "Vidhya",
             "Yasmine"],

    "Parsi": ["Abadan", "Adel", "Anosh", "Arshan", "Azman", "Azadafroz", "Bakhtayar", "Bastavar", "Baman", "Darashah",
              "Delafruz", "Delawar", "Dinyar", "Farhad", "Farrokh", "Farzan", "Homyar", "Hormazd", "Ishvat",
              "Jahanshah", "Jehangir", "Kaizaad", "Khubyar", "Khufiruz", "Meheryar", "Meherzad", "Nawazish", "Navroz",
              "Parwez", "Peroz", "Ramin", "Rustam", "Sarafraz", "Shaharzaad", "Suroyazat", "Taronish", "Varaz",
              "Yazdyar", "Zirak", "Zubin", "Afareen", "Aanahita", "Arnavaz", "Arzoo", "Bahar", "Bakhtawar", "Behroz",
              "Benaifer", "Cheherazad", "Delnaz", "Delnavaz", "Dinaz", "Farnaaza", "Fehroza", "Gulrukh", "Gulshirin",
              "Hufriya", "Jahanray", "Khursheed", "Khushnavaz", "Laleh", "Lilya", "Mahbanoo", "Mahrukh", "Meher",
              "Nauheed", "Navaz", "Parinaaz", "Parizaad", "Rukhsaar", "Roshanak", "Sanobar", "Shahnaz", "Shehernavaz",
              "Shereen", "Tanaz", "Tehmina", "Vahbeez", "Yazdin", "Zarin"]

}

# Dicts of respective gender pronouns
female_pronouns = {'subjective_pronouns': ['she'], 'objective_pronouns': ['her'], 'reflexive_pronouns': ['herself'],
                   'possessive_pronouns': ['her', 'hers']}
male_pronouns = {'subjective_pronouns': ['he'], 'objective_pronouns': ['him'], 'reflexive_pronouns': ['himself'],
                 'possessive_pronouns': ['his']}
neutral_pronouns = {'subjective_pronouns': ['per', 'they', 've', 'xe', 'ze', 'zie', 'ey', 'tey'],
                    'objective_pronouns': ['them', 'ver', 'xem', 'hir', 'em', 'ter'],
                    'reflexive_pronouns': ['themself', 'themselves', 'eirself', 'perself', 'verself', 'hirself',
                                           'xemself', 'emself', 'terself'],
                    'possessive_pronouns': ['their', 'theirs', 'pers', 'vis', 'xyr', 'hirs', 'xyrs', 'eir', 'eirs',
                                            'tem', 'ters']}

# add country economic dict
country_economic_dict = {
    "High-income": ["Aruba", "Andorra", "U.A.E", "U.S.", "U.K.", "UK", "England", "Antigua and Barbuda", "Australia",
                    "Austria", "Belgium", "Bahrain", "Bahamas", "Bermuda", "Barbados", "Brunei Darussalam",
                    "Canada", "Switzerland", "Channel Islands", "Chile", "Curacao", "Curaçao", "Cayman Islands", "Cyprus",
                    "Czech Republic", "Germany", "Denmark", "Spain", "Estonia", "Finland", "France", "Faroe Islands",
                    "United Kingdom", "Gibraltar", "Greece", "Greenland", "Guam", "Hong Kong", "Croatia",
                    "Hungary", "Isle of Man", "Ireland", "Iceland", "United Arab Emirates", "UAE", "Israel", "Italy",
                    "Japan", "St. Kitts and Nevis", "South Korea", "Kuwait", "Liechtenstein", "Lithuania", "Luxembourg",
                    "Latvia", "Macao", "St. Martin", "Monaco", "Malta",
                    "Northern Mariana Islands", "New Caledonia", "Netherlands", "Norway", "Nauru", "New Zealand",
                    "Oman", "Panama", "Poland", "Puerto Rico", "Portugal", "French Polynesia", "Qatar", "Romania",
                    "Saudi Arabia", "Singapore", "San Marino", "Slovak Republic", "Slovenia", "Sweden",
                    "Sint Maarten", "Seychelles", "Turks and Caicos Islands", "Trinidad and Tobago",
                    "Taiwan", "Uruguay", "United States", "British Virgin Islands", "Virgin Islands"],
    "Low-income": ["Afghanistan", "Burundi", "Burkina Faso", "Central African Republic", "Congo", "Eritrea",
                   "Ethiopia", "Guinea", "Gambia", "Guinea-Bissau", "Liberia", "Madagascar", "Mali", "Mozambique",
                   "Mtoalawi", "Niger", "North Korea", "Rwanda", "Sudan", "Sierra Leone", "Somalia",
                   "South Sudan", "Syria", "Chad", "Togo", "Uganda", "Yemen", "Zambia"],
    "Lower-middle-income": ["Angola", "Benin", "Bangladesh", "Bolivia", "Bhutan", "Côte d'Ivoire", "Ivory Coast", "Cameroon",
                            "Congo", "Comoros", "Cabo Verde", "Djibouti", "Algeria", "Egypt",
                            "Micronesia", "Ghana", "Honduras", "Haiti", "Indonesia", "India",
                            "Iran", "Kenya", "Kyrgyz Republic", "Cambodia", "Kiribati", "Lao",
                            "Lebanon", "Sri Lanka", "Lesotho", "Morocco", "Myanmar", "Mongolia", "Mauritania",
                            "Nigeria", "Nicaragua", "Nepal", "Pakistan", "Philippines", "Papua New Guinea",
                            "West Bank and Gaza", "Senegal", "Solomon Islands", "El Salvador",
                            "Saint Thomas and Prince", "São Tomé and Príncipe", "Eswatini", "Tajikistan", "Timor-Leste",
                            "Tunisia", "Tanzania", "Ukraine", "Uzbekistan", "Vietnam", "Vanuatu", "Samoa", "Zimbabwe"],
    "Upper-middle-income": ["Albania", "Argentina", "Armenia", "American Samoa", "Azerbaijan", "Bulgaria",
                            "Bosnia and Herzegovina", "Belarus", "Belize", "Brazil", "Botswana", "China", "Colombia",
                            "Costa Rica", "Cuba", "Dominica", "Dominican Republic", "Ecuador", "Fiji", "Gabon",
                            "Georgia", "Equatorial Guinea", "Grenada", "Guatemala", "Guyana", "Iraq", "Jamaica",
                            "Jordan", "Kazakhstan", "Libya", "St. Lucia", "Moldova", "Maldives", "Mexico",
                            "Marshall Islands", "North Macedonia", "Montenegro", "Mauritius", "Malaysia", "Namibia",
                            "Peru", "Palau", "Paraguay", "Russian Federation", "Serbia", "Suriname", "Thailand",
                            "Turkmenistan", "Tonga", "Turkey", "Türkiye", "Tuvalu", "St. Vincent and the Grenadines",
                            "Kosovo", "South Africa"]}


def get_substitution_names(values_list: List[List[str]]) -> List[str]:
    """ Helper function to get list of substitution names

    Args:
         values_list (List[List[str]]):
            list of substitution lists.

    Returns:
         List[str]:
            List of substitution names
    """
    substitution_names = []
    for lst in values_list:
        substitution_names.extend(lst)

    return substitution_names


def create_terminology(ner_data: pd.DataFrame) -> Dict[str, List[str]]:
    """Iterate over the DataFrame to create terminology from the predictions. IOB format converted to the IO.

    Args:
        ner_data: Pandas DataFrame that has 2 column, 'text' as string and 'label' as list of labels

    Returns:
        Dictionary of entities and corresponding list of words.
    """
    terminology = {}

    chunk = list()
    ent_type = None
    for i, row in ner_data.iterrows():

        sent_labels = row.label
        for token_indx, label in enumerate(sent_labels):

            if label.startswith('B'):

                if chunk:
                    if terminology.get(ent_type, None):
                        terminology[ent_type].append(" ".join(chunk))
                    else:
                        terminology[ent_type] = [" ".join(chunk)]

                sent_tokens = row.text.split(' ')
                chunk = [sent_tokens[token_indx]]
                ent_type = label[2:]

            elif label.startswith('I'):

                sent_tokens = row.text.split(' ')
                chunk.append(sent_tokens[token_indx])

            else:

                if chunk:
                    if terminology.get(ent_type, None):
                        terminology[ent_type].append(" ".join(chunk))
                    else:
                        terminology[ent_type] = [" ".join(chunk)]

                chunk = None
                ent_type = None

    return terminology


default_label_representation = {'O': 0, 'LOC': 0, 'PER': 0, 'MISC': 0, 'ORG': 0}
default_ehtnicity_representation = {'black': 0, 'asian': 0, 'white': 0, 'native_american': 0, 'hispanic': 0,
                                    'inter_racial': 0}
default_religion_representation = {'muslim': 0, 'hindu': 0, 'sikh': 0, 'christian': 0, 'jain': 0, 'buddhist': 0,
                                   'parsi': 0}
default_economic_country_representation = {'high_income': 0, 'low_income': 0, 'lower_middle_income': 0,
                                           'upper_middle_income': 0}


def get_label_representation_dict(data: List[Sample]) -> Dict[str, int]:
    """
    Args:
        data (List[Sample]): The input data to be evaluated for representation test.

    Returns:
        dict: a dictionary containing label representation information.
    """

    label_representation = defaultdict(int)

    for sample in data:
        for prediction in sample.expected_results.predictions:
            if isinstance(prediction, SequenceLabel):
                label_representation[prediction.label] += 1
            elif isinstance(prediction, NERPrediction):
                if prediction.entity == 'O':
                    label_representation[prediction.entity] += 1
                elif prediction.entity in ['B-LOC', 'I-LOC', 'B-PER', 'I-PER', 'B-MISC', 'I-MISC', 'B-ORG', 'I-ORG']:
                    label_representation[prediction.entity.split("-")[1]] += 1

    return label_representation


def check_name(word: str, name_lists: List[List[str]]) -> bool:
    """
    Checks if a word is in a list of list of strings

    Args:
        word (str):
            string to look for
        name_lists (List[List[str]]):
            list of lists of potential candidates
    """
    return any(word.lower() in [name.lower() for name in name_list] for name_list in name_lists)


def get_country_economic_representation_dict(data: List[Sample]) -> Dict[str, int]:
    """
    Args:
       data (List[Sample]): The input data to be evaluated for representation test.

    Returns:
       Dict[str, int]: a dictionary containing country economic representation information.
    """

    country_economic_representation = {"high_income": 0, "low_income": 0, "lower_middle_income": 0,
                                       "upper_middle_income": 0}
    
    income_mapping = {
    "High-income": "high_income",
    "Lower-middle-income": "low_income",
    "Low-income": "low_income",
    "Upper-middle-income": "upper_middle_income"
    }

    for sample in data:
        if isinstance(sample.expected_results, NEROutput):
            words = [x.span.word.lower() for x in sample.expected_results.predictions]  
        elif isinstance(sample.expected_results, SequenceClassificationOutput):
            words = set(sample.original.replace('.', '').lower().split())
        elif sample.task =='question-answering':
            if "perturbed_context" in sample.__annotations__:  
                words = set(sample.original_context.replace('.', '').lower().split())
            else:
                words = set(sample.original_question.replace('.', '').lower().split())
        elif sample.task =='summarization':
             words = set(sample.original.replace('.', '').lower().split())

        for income, countries in country_economic_dict.items():
            for country in countries:
                country_words = set(country.lower().split()) 
                if country_words.issubset(words):    
                    country_economic_representation[income_mapping[income]] += 1

    return country_economic_representation


def get_religion_name_representation_dict(data: List[Sample]) -> Dict[str, int]:
    """
    Args:
        data (List[Sample]): The input data to be evaluated for representation test.

    Returns:
        Dict[str, int]: a dictionary containing religion representation information.
    """

    religion_representation = {'muslim': 0, 'hindu': 0, 'sikh': 0, 'christian': 0, 'jain': 0, 'buddhist': 0, 'parsi': 0}
    religions = ['Muslim', 'Hindu', 'Sikh', 'Parsi', 'Christian', 'Buddhist', 'Jain']

    for sample in data:
        if isinstance(sample.expected_results, NEROutput):
            words = [x.span.word for x in sample.expected_results.predictions]
        elif isinstance(sample.expected_results, SequenceClassificationOutput):
            words = sample.original.split()
        elif sample.task =='question-answering':
            if "perturbed_context" in sample.__annotations__:  
                words = sample.original_context.split()
            else:
                words = sample.original_question.split()   
        elif sample.task =='summarization':
            words = sample.original.split()
            
        for i in words:
            for religion in religions:
                if check_name(i, [religion_wise_names[religion]]):
                    religion_representation[religion.lower()] += 1

    return religion_representation


def get_ethnicity_representation_dict(data: List[Sample]) -> Dict[str, int]:
    """
    Args:
        data (List[Sample]): The input data to be evaluated for representation test.

    Returns:
        Dict[str, int]: a dictionary containing ethnicity representation information.
    """
    ethnicity_representation = {"black": 0, "asian": 0, "white": 0, "native_american": 0, "hispanic": 0,
                                "inter_racial": 0}

    for sample in data:
        if isinstance(sample.expected_results, NEROutput):
            words = [x.span.word for x in sample.expected_results.predictions]
        elif isinstance(sample.expected_results, SequenceClassificationOutput):
            words = sample.original.split()
        elif sample.task =='question-answering':
            if "perturbed_context" in sample.__annotations__:  
                words = sample.original_context.split()
            else:
                words = sample.original_question.split()   
        elif sample.task =='summarization':
            words = sample.original.split()
            
        for i in words:
            if check_name(i, [white_names['first_names'], white_names['last_names']]):
                ethnicity_representation["white"] += 1
            if check_name(i, [black_names['first_names'], black_names['last_names']]):
                ethnicity_representation["black"] += 1
            if check_name(i, [hispanic_names['first_names'], hispanic_names['last_names']]):
                ethnicity_representation["hispanic"] += 1
            if check_name(i, [asian_names['first_names'], asian_names['last_names']]):
                ethnicity_representation["asian"] += 1
            if check_name(i, [inter_racial_names['last_names']]):
                ethnicity_representation["inter_racial"] += 1
            if check_name(i, [native_american_names['last_names']]):
                ethnicity_representation["native_american"] += 1

    return ethnicity_representation


def get_entity_representation_proportions(entity_representation):
    """
    Args:
       entity_representation (dict): a dictionary containing representation information.

    Returns:
       dict: a dictionary with proportions of each entity.
    """

    total_entities = sum(entity_representation.values())
    entity_representation_proportion = {}
    for k, v in entity_representation.items():
        if total_entities == 0:
            entity_representation_proportion[k] = 0
        else:
            entity_representation_proportion[k] = v / total_entities

    return entity_representation_proportion

default_user_prompt = {
    "boolq": "I've provided a question and context. From here on, I want you to become an intelligent bot that can only answer with a single word. The words you are capable of saying are True and False. If you think the answer to the question is True, then say 'True'. If it is False, then say 'False'. Do not say anything else other than that.",
    "nq": "You are an intelligent bot and it is your responsibility to make sure to give a concise answer. Answer:",
    "xsum": "You are an intelligent Context summarizer. Please read the following context carefully. After understanding its content, create a concise summary, capturing the essential themes and key details. Please ensure that the summary does not end abruptly and remains within the max_tokens word limit."
}

qa_prompt_template ="""
You are a distinguished professor known for your expertise in meticulously grading students' answers to questions. Your extensive knowledge and experience make you the go-to authority in your field.
You have been entrusted with the evaluation of the following question:
{query}
Presented below is the indisputably correct answer:
{answer}
Your responsibility is to thoroughly scrutinize the predicted answer provided by a student:
{result}
Remember, your response should consist of a single word only. You have two choices: "CORRECT" or "INCORRECT".
When you are convinced that the answer is absolutely accurate, respond with "CORRECT". In the event that it is unequivocally incorrect, respond with "INCORRECT". It is essential that you strictly adhere to this guideline.
Employ a meticulous, step-by-step approach to meticulously appraise the answer's factual integrity.
Furthermore, you are expected to evaluate the degree of similarity between the correct answer and the predicted answer, quantifying how closely they align.
Your comprehensive assessment will play a crucial role in determining the student's performance.
"""

ocr_typo_dict =    {'tle': 'the', 
                    'Tle': 'The', 
                    'tlie': 'the', 
                    'Tlie': 'The',
                    'tbe': 'the', 
                    'Tbe': 'The', 
                    'tbis': 'this', 
                    'Tbis': 'This', 
                    'iito': 'into',
                    'tbe' : 'the','0ffer' : 'offer',
                    '0ffice' : 'office',
                    '0fficer' : 'officer',
                    '0fficial' : 'official',
                    '0ften' : 'often',
                    '0nce' : 'once',
                    '0nly' : 'only',
                    '0pen' : 'open',
                    '0peration' : 'operation',
                    '0rder' : 'order',
                    '0rganization' : 'organization',
                    '0ther' : 'other',
                    '0thers' : 'others',
                    '0ver' : 'over',
                    '0wner' : 'owner',
                    '1and' : 'land',
                    '1anguage' : 'language',
                    '1arge' : 'large',
                    '1ast' : 'last',
                    '1ate' : 'late',
                    '1ater' : 'later',
                    '1dea' : 'idea',
                    '1dentify' : 'identify',
                    '1ead' : 'lead',
                    '1earn' : 'learn',
                    '1east' : 'least',
                    '1eave' : 'leave',
                    '1eft' : 'left',
                    '1egal' : 'legal',
                    '1ess' : 'less',
                    '1etter' : 'letter',
                    '1evel' : 'level',
                    '1ife' : 'life',
                    '1ight' : 'light',
                    '1ike' : 'like',
                    '1ikely' : 'likely',
                    '1ine' : 'line',
                    '1ist' : 'list',
                    '1itt1e' : 'little',
                    '1ittle' : 'little',
                    '1ive' : 'live',
                    '1mage' : 'image',
                    '1mpact' : 'impact',
                    '1mportant' : 'important',
                    '1mprove' : 'improve',
                    '1nclud1ng' : 'including',
                    '1ncluding' : 'including',
                    '1ncrease' : 'increase',
                    '1ndeed' : 'indeed',
                    '1ndividual' : 'individual',
                    '1ndustry' : 'industry',
                    '1nformat1on' : 'information',
                    '1nformation' : 'information',
                    '1nside' : 'inside',
                    '1nst1tut1on' : 'institution',
                    '1nstead' : 'instead',
                    '1nstitution' : 'institution',
                    '1nterest' : 'interest',
                    '1nteresting' : 'interesting',
                    '1nternational' : 'international',
                    '1nterview' : 'interview',
                    '1nto' : 'into',
                    '1nvestment' : 'investment',
                    '1ong' : 'long',
                    '1ook' : 'look',
                    '1ose' : 'lose',
                    '1oss' : 'loss',
                    '1ove' : 'love',
                    '1ssue' : 'issue',
                    '1tem' : 'item',
                    '1tself' : 'itself',
                    'a1most' : 'almost',
                    'a1one' : 'alone',
                    'a1ready' : 'already',
                    'a1so' : 'also',
                    'a1though' : 'although',
                    'a1ways' : 'always',
                    'aUeady' : 'already',
                    'aUhough' : 'although',
                    'aUo' : 'also',
                    'aUso' : 'also',
                    'aUvays' : 'always',
                    'a[)pear' : 'appear',
                    'a\vay' : 'away',
                    'a])pear' : 'appear',
                    'a])ply' : 'apply',
                    'a])proach' : 'approach',
                    'a^d' : 'and',
                    'a^great' : 'great',
                    'a^nd' : 'and',
                    'a^ny' : 'any',
                    'a^rt' : 'art',
                    'a^vay' : 'away',
                    'aavay' : 'away',
                    'ab0ut' : 'about',
                    'ab0ve' : 'above',
                    'ab1e' : 'able',
                    'ab6ut' : 'about',
                    'ab6ve' : 'above',
                    'abUity' : 'ability',
                    'abead' : 'ahead',
                    'abi1ity' : 'ability',
                    'abiUty' : 'ability',
                    'abihty' : 'ability',
                    'abilitv' : 'ability',
                    'ablc' : 'able',
                    'abont' : 'about',
                    'aboui' : 'about',
                    'abov^e' : 'above',
                    'abovc' : 'above',
                    'ac^t' : 'act',
                    'acc0rding' : 'according',
                    'acc0unt' : 'account',
                    'acc6unt' : 'account',
                    'acce])t' : 'accept',
                    'accej)t' : 'accept',
                    'accoiding' : 'according',
                    'accord1ng' : 'according',
                    'accordiug' : 'according',
                    'accouut' : 'account',
                    'aclion' : 'action',
                    'aclivity' : 'activity',
                    'aclually' : 'actually',
                    'acrofs' : 'across',
                    'acrols' : 'across',
                    'act1on' : 'action',
                    'act1vity' : 'activity',
                    'acti0n' : 'action',
                    'acti6n' : 'action',
                    'actiou' : 'action',
                    'activitv' : 'activity',
                    'actlon' : 'action',
                    'actuaUy' : 'actually',
                    'actuallv' : 'actually',
                    'actuauy' : 'actually',
                    'addrcfs' : 'address',
                    'addrcss' : 'address',
                    'addref' : 'address',
                    'addrefs' : 'address',
                    'addrels' : 'address',
                    'adion' : 'action',
                    'adivity' : 'activity',
                    'adlion' : 'action',
                    'adlivity' : 'activity',
                    'adlually' : 'actually',
                    'adm1n1stration' : 'administration',
                    'adm1nistration' : 'administration',
                    'adm1t' : 'admit',
                    'admin1stration' : 'administration',
                    'adminiflration' : 'administration',
                    'adminiftration' : 'administration',
                    'adminiltration' : 'administration',
                    'administrat1on' : 'administration',
                    'administrati0n' : 'administration',
                    'adtion' : 'action',
                    'adtivity' : 'activity',
                    'adtually' : 'actually',
                    'adually' : 'actually',
                    'affcft' : 'affect',
                    'affecl' : 'affect',
                    'affed' : 'affect',
                    'affedl' : 'affect',
                    'affedt' : 'affect',
                    'affeft' : 'affect',
                    'affume' : 'assume',
                    'afk' : 'ask',
                    'aflect' : 'affect',
                    'afler' : 'after',
                    'aflumc' : 'assume',
                    'aflume' : 'assume',
                    'afsume' : 'assume',
                    'aftcr' : 'after',
                    'aftei' : 'after',
                    'aftion' : 'action',
                    'aftivity' : 'activity',
                    'aftually' : 'actually',
                    'ag^ain' : 'again',
                    'ag^ainst' : 'against',
                    'ag^e' : 'age',
                    'againfi' : 'against',
                    'againfl' : 'against',
                    'againft' : 'against',
                    'againit' : 'against',
                    'againjl' : 'against',
                    'againlt' : 'against',
                    'againsi' : 'against',
                    'againsl' : 'against',
                    'againſi' : 'against',
                    'againſl' : 'against',
                    'againﬁ' : 'against',
                    'agaiu' : 'again',
                    'agaiust' : 'against',
                    'agaln' : 'again',
                    'agalnst' : 'against',
                    'agamst' : 'against',
                    'agcncy' : 'agency',
                    'agcnt' : 'agent',
                    'agencv' : 'agency',
                    'agrce' : 'agree',
                    'agrcement' : 'agreement',
                    'agrec' : 'agree',
                    'agrecment' : 'agreement',
                    'agreemcnt' : 'agreement',
                    'ahcad' : 'ahead',
                    'ahility' : 'ability',
                    'ahle' : 'able',
                    'ahone' : 'alone',
                    'ahout' : 'about',
                    'ahove' : 'above',
                    'ahready' : 'already',
                    'ahso' : 'also',
                    'aivay' : 'away',
                    'aj)pear' : 'appear',
                    'aj)ply' : 'apply',
                    'aj)proach' : 'approach',
                    'al6ne' : 'alone',
                    'al6ng' : 'along',
                    'al\vays' : 'always',
                    'alffo' : 'also',
                    'alfo' : 'also',
                    'alivays' : 'always',
                    'alloAv' : 'allow',
                    'allo\v' : 'allow',
                    'alloiv' : 'allow',
                    'alm6st' : 'almost',
                    'almofl' : 'almost',
                    'almoft' : 'almost',
                    'almolt' : 'almost',
                    'almos' : 'almost',
                    'almoſl' : 'almost',
                    'alon6' : 'alone',
                    'alonc' : 'alone',
                    'aloue' : 'alone',
                    'aloug' : 'along',
                    'alrcadv' : 'already',
                    'alrcady' : 'already',
                    'alreadv' : 'already',
                    'als0' : 'also',
                    'als6' : 'also',
                    'altbougb' : 'although',
                    'altbough' : 'although',
                    'althongh' : 'although',
                    'althougb' : 'although',
                    'althougli' : 'although',
                    'altliough' : 'although',
                    'alv/ays' : 'always',
                    'alvays' : 'always',
                    'alwavs' : 'always',
                    'alwayf' : 'always',
                    'alſb' : 'also',
                    'am0ng' : 'among',
                    'am6ng' : 'among',
                    'amoug' : 'among',
                    'amouut' : 'amount',
                    'an0ther' : 'another',
                    'an1mal' : 'animal',
                    'an6ther' : 'another',
                    'an^d' : 'and',
                    'an^y' : 'any',
                    'analvsis' : 'analysis',
                    'analyfis' : 'analysis',
                    'analylis' : 'analysis',
                    'analys1s' : 'analysis',
                    'anfiver' : 'answer',
                    'anfv/er' : 'answer',
                    'anfwcr' : 'answer',
                    'anfwer' : 'answer',
                    'animaU' : 'animal',
                    'animah' : 'animal',
                    'anlmal' : 'animal',
                    'anlwer' : 'answer',
                    'anoiher' : 'another',
                    'anotber' : 'another',
                    'anothcr' : 'another',
                    'anothei' : 'another',
                    'anotlier' : 'another',
                    'ansAver' : 'answer',
                    'ans\ver' : 'answer',
                    'ansv/er' : 'answer',
                    'ansver' : 'answer',
                    'answcr' : 'answer',
                    'answei' : 'answer',
                    'anthor' : 'author',
                    'anthority' : 'authority',
                    'anvone' : 'anyone',
                    'anvthing' : 'anything',
                    'anytbing' : 'anything',
                    'anyth1ng' : 'anything',
                    'anytliing' : 'anything',
                    'ap[)ear' : 'appear',
                    'ap])ear' : 'appear',
                    'ap])ly' : 'apply',
                    'apj)ear' : 'appear',
                    'apj)ly' : 'apply',
                    'appcar' : 'appear',
                    'applv' : 'apply',
                    'approacb' : 'approach',
                    'ap|)ear' : 'appear',
                    'ar0und' : 'around',
                    'arguc' : 'argue',
                    'arouud' : 'around',
                    'arr1ve' : 'arrive',
                    'arriire' : 'arrive',
                    'arriv6' : 'arrive',
                    'arrivc' : 'arrive',
                    'art1cle' : 'article',
                    'articlc' : 'article',
                    'artifl' : 'artist',
                    'artift' : 'artist',
                    'artilt' : 'artist',
                    'artiﬁ' : 'artist',
                    'assumc' : 'assume',
                    'attcntion' : 'attention',
                    'attent1on' : 'attention',
                    'attorncy' : 'attorney',
                    'attornev' : 'attorney',
                    'aud1ence' : 'audience',
                    'audicnce' : 'audience',
                    'auother' : 'another',
                    'auswer' : 'answer',
                    'autbor' : 'author',
                    'autboritg' : 'authority',
                    'autbority' : 'authority',
                    'auth0r' : 'author',
                    'auth0rity' : 'authority',
                    'authoi' : 'author',
                    'authoiity' : 'authority',
                    'author1ty' : 'authority',
                    'authoritv' : 'authority',
                    'autlior' : 'author',
                    'autliority' : 'authority',
                    'av/ay' : 'away',
                    'av^ay' : 'away',
                    'avaUable' : 'available',
                    'availahle' : 'available',
                    'avall' : 'wall',
                    'avater' : 'water',
                    'avell' : 'well',
                    'avest' : 'west',
                    'avhat' : 'what',
                    'avhen' : 'when',
                    'avhich' : 'which',
                    'avhite' : 'white',
                    'avho' : 'who',
                    'avill' : 'will',
                    'avith' : 'with',
                    'avork' : 'work',
                    'awav' : 'away',
                    'a|)pear' : 'appear',
                    'a£lually' : 'actually',
                    'a£tually' : 'actually',
                    'aﬁer' : 'after',
                    'aﬁne' : 'fine',
                    'b00k' : 'book',
                    'b0ard' : 'board',
                    'b0dy' : 'body',
                    'b0ok' : 'book',
                    'b0th' : 'both',
                    'b1ack' : 'black',
                    'b1ll' : 'bill',
                    'b1ood' : 'blood',
                    'b1ue' : 'blue',
                    'b6dy' : 'body',
                    'b6ok' : 'book',
                    'b^ar' : 'bar',
                    'b^it' : 'bit',
                    'b^ut' : 'but',
                    'babv' : 'baby',
                    'bafe' : 'base',
                    'bahy' : 'baby',
                    'bair' : 'hair',
                    'balf' : 'half',
                    'bappen' : 'happen',
                    'bappy' : 'happy',
                    'bas6' : 'base',
                    'baöir' : 'hair',
                    'bcat' : 'beat',
                    'bcautiful' : 'beautiful',
                    'bccaufc' : 'because',
                    'bccaufe' : 'because',
                    'bccausc' : 'because',
                    'bcforc' : 'before',
                    'bcfore' : 'before',
                    'bcft' : 'best',
                    'bcgin' : 'begin',
                    'bchavior' : 'behavior',
                    'bchind' : 'behind',
                    'bclieve' : 'believe',
                    'bclween' : 'between',
                    'bcnefit' : 'benefit',
                    'bcst' : 'best',
                    'bctAveen' : 'between',
                    'bctiveen' : 'between',
                    'bcttcr' : 'better',
                    'bctter' : 'better',
                    'bctwcen' : 'between',
                    'bctwecn' : 'between',
                    'bctween' : 'between',
                    'bcvond' : 'beyond',
                    'bcyond' : 'beyond',
                    'be/art' : 'heart',
                    'be1ieve' : 'believe',
                    'beUeve' : 'believe',
                    'bealth' : 'health',
                    'beantiful' : 'beautiful',
                    'beart' : 'heart',
                    'beaut1ful' : 'beautiful',
                    'beautifiU' : 'beautiful',
                    'beautifu1' : 'beautiful',
                    'beautifuU' : 'beautiful',
                    'beavy' : 'heavy',
                    'bebind' : 'behind',
                    'bec6me' : 'become',
                    'becanse' : 'because',
                    'becaufc' : 'because',
                    'becaufe' : 'because',
                    'becauie' : 'because',
                    'becaule' : 'because',
                    'becausc' : 'because',
                    'becomc' : 'become',
                    'bef0re' : 'before',
                    'bef6re' : 'before',
                    'befoie' : 'before',
                    'befor6' : 'before',
                    'beforc' : 'before',
                    'beft' : 'best',
                    'beg1n' : 'begin',
                    'beg^in' : 'begin',
                    'beheve' : 'believe',
                    'beiore' : 'before',
                    'bel1eve' : 'believe',
                    'belAveen' : 'between',
                    'belicve' : 'believe',
                    'belieie' : 'believe',
                    'believ^e' : 'believe',
                    'believc' : 'believe',
                    'beliind' : 'behind',
                    'belore' : 'before',
                    'belp' : 'help',
                    'belter' : 'better',
                    'bencfit' : 'benefit',
                    'benef1t' : 'benefit',
                    'beneflt' : 'benefit',
                    'beneﬁ' : 'benefit',
                    'berfelf' : 'herself',
                    'berself' : 'herself',
                    'betAvcen' : 'between',
                    'betAvecn' : 'between',
                    'betAveeu' : 'between',
                    'bet\veen' : 'between',
                    'bet^veen' : 'between',
                    'betaveen' : 'between',
                    'betivcen' : 'between',
                    'betivecn' : 'between',
                    'betiveen' : 'between',
                    'bettcr' : 'better',
                    'bettei' : 'better',
                    'bettveen' : 'between',
                    'betv/een' : 'between',
                    'betv^een' : 'between',
                    'betveen' : 'between',
                    'betveeu' : 'between',
                    'betwccn' : 'between',
                    'betwcen' : 'between',
                    'betwecn' : 'between',
                    'betweeu' : 'between',
                    'betzveen' : 'between',
                    'beueve' : 'believe',
                    'bevond' : 'beyond',
                    'beyoud' : 'beyond',
                    'beſi' : 'best',
                    'beſl' : 'best',
                    'beſore' : 'before',
                    'bftter' : 'better',
                    'bftween' : 'between',
                    'biU' : 'bill',
                    'biftory' : 'history',
                    'bigh' : 'high',
                    'biiU' : 'bill',
                    'bil1' : 'bill',
                    'bimfelf' : 'himself',
                    'bimjelf' : 'himself',
                    'bimsclf' : 'himself',
                    'bimself' : 'himself',
                    'bistory' : 'history',
                    'biu' : 'bill',
                    'blll' : 'bill',
                    'bluc' : 'blue',
                    'bnilding' : 'building',
                    'bodv' : 'body',
                    'bofpital' : 'hospital',
                    'boru' : 'born',
                    'bospital' : 'hospital',
                    'botb' : 'both',
                    'botl' : 'both',
                    'botli' : 'both',
                    'bowever' : 'however',
                    'br1ng' : 'bring',
                    'brcak' : 'break',
                    'briug' : 'bring',
                    'brlng' : 'bring',
                    'brmg' : 'bring',
                    'brotber' : 'brother',
                    'brothcr' : 'brother',
                    'brothei' : 'brother',
                    'brotlier' : 'brother',
                    'bu1ld1ng' : 'building',
                    'bufband' : 'husband',
                    'buffinefs' : 'business',
                    'buffines' : 'business',
                    'buffiness' : 'business',
                    'bufincfs' : 'business',
                    'bufinef' : 'business',
                    'bufinefs' : 'business',
                    'bufines' : 'business',
                    'bufiness' : 'business',
                    'bufmefs' : 'business',
                    'buge' : 'huge',
                    'bui1ding' : 'building',
                    'buihiing' : 'building',
                    'build1ng' : 'building',
                    'bujband' : 'husband',
                    'bulinels' : 'business',
                    'buliness' : 'business',
                    'buman' : 'human',
                    'bundred' : 'hundred',
                    'busband' : 'husband',
                    'busincss' : 'business',
                    'businefs' : 'business',
                    'businels' : 'business',
                    'busmess' : 'business',
                    'buﬁnefs' : 'business',
                    'buﬁneſs' : 'business',
                    'bymself' : 'himself',
                    'c0llege' : 'college',
                    'c0me' : 'come',
                    'c0mmercial' : 'commercial',
                    'c0mpany' : 'company',
                    'c0nditi0n' : 'condition',
                    'c0st' : 'cost',
                    'c0uld' : 'could',
                    'c0untry' : 'country',
                    'c0urse' : 'course',
                    'c0urt' : 'court',
                    'c1ass' : 'class',
                    'c1ear' : 'clear',
                    'c1ose' : 'close',
                    'c1ty' : 'city',
                    'c1vil' : 'civil',
                    'c6me' : 'come',
                    'c6mmon' : 'common',
                    'c6st' : 'cost',
                    'c6uld' : 'could',
                    'c6untry' : 'country',
                    'c6urse' : 'course',
                    'c6urt' : 'court',
                    'c^an' : 'can',
                    'caU' : 'call',
                    'ca[)ital' : 'capital',
                    'ca])ital' : 'capital',
                    'cach' : 'each',
                    'cai)ital' : 'capital',
                    'caie' : 'care',
                    'caj)ital' : 'capital',
                    'cam])aign' : 'campaign',
                    'cami)aign' : 'campaign',
                    'cand1date' : 'candidate',
                    'cap1tal' : 'capital',
                    'capita1' : 'capital',
                    'carecr' : 'career',
                    'carrv' : 'carry',
                    'cas6' : 'case',
                    'catcb' : 'catch',
                    'caufc' : 'cause',
                    'caufe' : 'cause',
                    'cauie' : 'cause',
                    'caule' : 'cause',
                    'caus6' : 'cause',
                    'causc' : 'cause',
                    'ca|)ital' : 'capital',
                    'cbair' : 'chair',
                    'cbance' : 'chance',
                    'cbange' : 'change',
                    'cbaracter' : 'character',
                    'cbarafter' : 'character',
                    'cbarge' : 'charge',
                    'cbeck' : 'check',
                    'cbild' : 'child',
                    'cboice' : 'choice',
                    'cboofe' : 'choose',
                    'cboose' : 'choose',
                    'cburcb' : 'church',
                    'cburch' : 'church',
                    'cburcli' : 'church',
                    'ccll' : 'cell',
                    'ccnter' : 'center',
                    'ccntral' : 'central',
                    'ccnturv' : 'century',
                    'ccntury' : 'century',
                    'cconomv' : 'economy',
                    'cconomy' : 'economy',
                    'ccrtain' : 'certain',
                    'ccrtainlv' : 'certainly',
                    'ccrtainly' : 'certainly',
                    'cdge' : 'edge',
                    'cducation' : 'education',
                    'ceUor' : 'color',
                    'ceitain' : 'certain',
                    'centcr' : 'center',
                    'centnry' : 'century',
                    'centra1' : 'central',
                    'centuiy' : 'century',
                    'centurv' : 'century',
                    'certain1y' : 'certainly',
                    'certainlv' : 'certainly',
                    'certaiu' : 'certain',
                    'certaiuly' : 'certainly',
                    'certaln' : 'certain',
                    'certamly' : 'certainly',
                    'cffcct' : 'effect',
                    'cffecl' : 'effect',
                    'cffect' : 'effect',
                    'cffeft' : 'effect',
                    'cffort' : 'effort',
                    'cfpccially' : 'especially',
                    'cfpecially' : 'especially',
                    'cftablifh' : 'establish',
                    'ch1ld' : 'child',
                    'chaUenge' : 'challenge',
                    'chancc' : 'chance',
                    'chang6' : 'change',
                    'changc' : 'change',
                    'characlcr' : 'character',
                    'characler' : 'character',
                    'charactcr' : 'character',
                    'charactei' : 'character',
                    'charader' : 'character',
                    'charadler' : 'character',
                    'charadter' : 'character',
                    'charaftcr' : 'character',
                    'charafter' : 'character',
                    'chara£ler' : 'character',
                    'chara£ter' : 'character',
                    'charaﬁter' : 'character',
                    'charg6' : 'charge',
                    'chargc' : 'charge',
                    'chauenge' : 'challenge',
                    'chi1d' : 'child',
                    'chlld' : 'child',
                    'chnrch' : 'church',
                    'choicc' : 'choice',
                    'choofc' : 'choose',
                    'choofe' : 'choose',
                    'choole' : 'choose',
                    'choosc' : 'choose',
                    'chuich' : 'church',
                    'churcb' : 'church',
                    'churcli' : 'church',
                    'chureh' : 'church',
                    'cight' : 'eight',
                    'ciiy' : 'city',
                    'citizcn' : 'citizen',
                    'citv' : 'city',
                    'civ1l' : 'civil',
                    'civi1' : 'civil',
                    'civiU' : 'civil',
                    'claff' : 'class',
                    'clafs' : 'class',
                    'clals' : 'class',
                    'clasf' : 'class',
                    'clcar' : 'clear',
                    'clcarlv' : 'clearly',
                    'clcarly' : 'clearly',
                    'clcction' : 'election',
                    'cleai' : 'clear',
                    'clearlv' : 'clearly',
                    'clection' : 'election',
                    'cliair' : 'chair',
                    'cliange' : 'change',
                    'cliaracter' : 'character',
                    'cliarge' : 'charge',
                    'cliild' : 'child',
                    'cliurcb' : 'church',
                    'cliurch' : 'church',
                    'cliurcli' : 'church',
                    'clofe' : 'close',
                    'closc' : 'close',
                    'clse' : 'else',
                    'clty' : 'city',
                    'clvil' : 'civil',
                    'cnergv' : 'energy',
                    'cnergy' : 'energy',
                    'cnjoy' : 'enjoy',
                    'cnough' : 'enough',
                    'cnter' : 'enter',
                    'cntire' : 'entire',
                    'co11ege' : 'college',
                    'co1d' : 'cold',
                    'coUection' : 'collection',
                    'coUedge' : 'college',
                    'coUedion' : 'collection',
                    'coUedlion' : 'collection',
                    'coUeftion' : 'collection',
                    'coUega' : 'college',
                    'coUege' : 'college',
                    'coUoq' : 'color',
                    'coacb' : 'coach',
                    'coft' : 'cost',
                    'cohor' : 'color',
                    'coiUd' : 'could',
                    'col1ege' : 'college',
                    'collcgc' : 'college',
                    'collcge' : 'college',
                    'colleclion' : 'collection',
                    'collect1on' : 'collection',
                    'colledion' : 'collection',
                    'colledtion' : 'collection',
                    'colleftion' : 'collection',
                    'collegc' : 'college',
                    'com[)any' : 'company',
                    'com])any' : 'company',
                    'comc' : 'come',
                    'comi)any' : 'company',
                    'comj)any' : 'company',
                    'comm6n' : 'common',
                    'commcrcial' : 'commercial',
                    'commerc1al' : 'commercial',
                    'commercia1' : 'commercial',
                    'commou' : 'common',
                    'communitv' : 'community',
                    'companv' : 'company',
                    'compar6' : 'compare',
                    'comparc' : 'compare',
                    'compauy' : 'company',
                    'com|)any' : 'company',
                    'conccrn' : 'concern',
                    'cond1t1on' : 'condition',
                    'cond1tion' : 'condition',
                    'condit1on' : 'condition',
                    'confcrence' : 'conference',
                    'confercnce' : 'conference',
                    'conferencc' : 'conference',
                    'confumer' : 'consumer',
                    'conilder' : 'consider',
                    'conld' : 'could',
                    'conlider' : 'consider',
                    'conrse' : 'course',
                    'conrt' : 'court',
                    'cons1der' : 'consider',
                    'considcr' : 'consider',
                    'cont1nue' : 'continue',
                    'continuc' : 'continue',
                    'contro1' : 'control',
                    'cosl' : 'cost',
                    'cou1d' : 'could',
                    'couection' : 'collection',
                    'couege' : 'college',
                    'couise' : 'course',
                    'couit' : 'court',
                    'countiy' : 'country',
                    'countrv' : 'country',
                    'courfc' : 'course',
                    'courfe' : 'course',
                    'courie' : 'course',
                    'courle' : 'course',
                    'coursc' : 'course',
                    'couutry' : 'country',
                    'covcr' : 'cover',
                    'crcate' : 'create',
                    'creatc' : 'create',
                    'crimc' : 'crime',
                    'cspecially' : 'especially',
                    'cstablish' : 'establish',
                    'cuftomer' : 'customer',
                    'culturc' : 'culture',
                    'currcnt' : 'current',
                    'cven' : 'even',
                    'cvening' : 'evening',
                    'cvent' : 'event',
                    'cver' : 'ever',
                    'cvery' : 'every',
                    'cverything' : 'everything',
                    'cvidence' : 'evidence',
                    'cxactly' : 'exactly',
                    'cxample' : 'example',
                    'cxist' : 'exist',
                    'cxpect' : 'expect',
                    'cxpedt' : 'expect',
                    'cxpeft' : 'expect',
                    'cxperience' : 'experience',
                    'cxplain' : 'explain',
                    'd1fference' : 'difference',
                    'd1fferent' : 'different',
                    'd1fficult' : 'difficult',
                    'd1nner' : 'dinner',
                    'd1rection' : 'direction',
                    'd1scover' : 'discover',
                    'd1scussion' : 'discussion',
                    'd6cision' : 'decision',
                    'd6fense' : 'defense',
                    'd6or' : 'door',
                    'd6tail' : 'detail',
                    'd6termin6' : 'determine',
                    'd6termine' : 'determine',
                    'd6wn' : 'down',
                    'd^veloppement' : 'development',
                    'daik' : 'dark',
                    'danghter' : 'daughter',
                    'daugbter' : 'daughter',
                    'daughtcr' : 'daughter',
                    'daugliter' : 'daughter',
                    'dcad' : 'dead',
                    'dcal' : 'deal',
                    'dcath' : 'death',
                    'dccifion' : 'decision',
                    'dccision' : 'decision',
                    'dcep' : 'deep',
                    'dcfcribe' : 'describe',
                    'dcfign' : 'design',
                    'dcgrce' : 'degree',
                    'dcmocratic' : 'democratic',
                    'dcsign' : 'design',
                    'dctail' : 'detail',
                    'dctermine' : 'determine',
                    'dea1' : 'deal',
                    'deaU' : 'deal',
                    'dea^h' : 'deal',
                    'deaih' : 'death',
                    'dealh' : 'death',
                    'deatb' : 'death',
                    'deatli' : 'death',
                    'debatc' : 'debate',
                    'dec1sion' : 'decision',
                    'decid6' : 'decide',
                    'decifion' : 'decision',
                    'decilion' : 'decision',
                    'deciﬁon' : 'decision',
                    'decp' : 'deep',
                    'defcribc' : 'describe',
                    'defcribe' : 'describe',
                    'defcrihe' : 'describe',
                    'defenfe' : 'defense',
                    'deffenfe' : 'defense',
                    'defign' : 'design',
                    'defpite' : 'despite',
                    'degrcc' : 'degree',
                    'degrce' : 'degree',
                    'degrec' : 'degree',
                    'dehate' : 'debate',
                    'delcribe' : 'describe',
                    'delign' : 'design',
                    'des1gn' : 'design',
                    'descr1be' : 'describe',
                    'describc' : 'describe',
                    'descrihe' : 'describe',
                    'deserihe' : 'describe',
                    'detai1' : 'detail',
                    'detcrmine' : 'determine',
                    'determ1ne' : 'determine',
                    'determin6' : 'determine',
                    'determinc' : 'determine',
                    'devclopment' : 'development',
                    'develo])ment' : 'development',
                    'develoi)ment' : 'development',
                    'develoj)ment' : 'development',
                    'developmcnt' : 'development',
                    'deáh' : 'deal',
                    'deﬁgn' : 'design',
                    'dhection' : 'election',
                    'difcafc' : 'disease',
                    'difcafe' : 'disease',
                    'difcovcr' : 'discover',
                    'difcover' : 'discover',
                    'difcuffion' : 'discussion',
                    'difcuflion' : 'discussion',
                    'difcufs' : 'discuss',
                    'difcussion' : 'discussion',
                    'difeafc' : 'disease',
                    'difeafe' : 'disease',
                    'difease' : 'disease',
                    'diff1cult' : 'difficult',
                    'diff^erent' : 'different',
                    'diffcrcnt' : 'different',
                    'diffcrence' : 'difference',
                    'diffcrent' : 'different',
                    'differcnce' : 'difference',
                    'differcnt' : 'different',
                    'differencc' : 'difference',
                    'difficuU' : 'difficult',
                    'difficuUy' : 'difficult',
                    'difficuhy' : 'difficult',
                    'difflcult' : 'difficult',
                    'diflerence' : 'difference',
                    'diflerent' : 'different',
                    'diflicult' : 'difficult',
                    'difſerent' : 'different',
                    'dilcover' : 'discover',
                    'dillerent' : 'different',
                    'dilﬁcult' : 'difficult',
                    'dinncr' : 'dinner',
                    'direclion' : 'direction',
                    'direclor' : 'director',
                    'direct1on' : 'direction',
                    'directi0n' : 'direction',
                    'diredion' : 'direction',
                    'diredlion' : 'direction',
                    'diredor' : 'director',
                    'diredtion' : 'direction',
                    'direftion' : 'direction',
                    'direftor' : 'director',
                    'dire£lion' : 'direction',
                    'dire£tion' : 'direction',
                    'direﬁtion' : 'direction',
                    'discasc' : 'disease',
                    'discase' : 'disease',
                    'discovcr' : 'discover',
                    'discuffion' : 'discussion',
                    'discufsion' : 'discussion',
                    'discuss1on' : 'discussion',
                    'diseafe' : 'disease',
                    'diseasc' : 'disease',
                    'ditﬁcult' : 'difficult',
                    'diſferent' : 'different',
                    'diſiicult' : 'difficult',
                    'diſſerence' : 'difference',
                    'diſſerent' : 'different',
                    'diﬁcrent' : 'different',
                    'diﬁferent' : 'different',
                    'dlfferent' : 'different',
                    'dming' : 'during',
                    'dnring' : 'during',
                    'doAvii' : 'down',
                    'do\vn' : 'down',
                    'do^vn' : 'down',
                    'doavn' : 'down',
                    'doclor' : 'doctor',
                    'dodlor' : 'doctor',
                    'dodor' : 'doctor',
                    'dodtor' : 'doctor',
                    'doftor' : 'doctor',
                    'doivn' : 'down',
                    'dooi' : 'door',
                    'dov/n' : 'down',
                    'dov^n' : 'down',
                    'dovn' : 'down',
                    'dowu' : 'down',
                    'draAv' : 'draw',
                    'dra\v' : 'draw',
                    'dra^v' : 'draw',
                    'draiv' : 'draw',
                    'drcam' : 'dream',
                    'drivc' : 'drive',
                    'duiing' : 'during',
                    'dur1ng' : 'during',
                    'duriug' : 'during',
                    'durlng' : 'during',
                    'durmg' : 'during',
                    'e1ection' : 'election',
                    'e1ght' : 'eight',
                    'e1ther' : 'either',
                    'eVei' : 'even',
                    'e\eiy' : 'every',
                    'e^at' : 'eat',
                    'e^nd' : 'end',
                    'e^very' : 'every',
                    'eacb' : 'each',
                    'eacli' : 'each',
                    'eaft' : 'east',
                    'eafy' : 'easy',
                    'eaily' : 'early',
                    'eait' : 'east',
                    'ear1y' : 'early',
                    'earh' : 'each',
                    'earlv' : 'early',
                    'easUy' : 'early',
                    'easv' : 'easy',
                    'eaſl' : 'east',
                    'ebaracter' : 'character',
                    'ec0n0my' : 'economy',
                    'econom1c' : 'economic',
                    'economv' : 'economy',
                    'edgc' : 'edge',
                    'educat1on' : 'education',
                    'educati0n' : 'education',
                    'educati6n' : 'education',
                    'eff^ect' : 'effect',
                    'effccl' : 'effect',
                    'effcft' : 'effect',
                    'effecl' : 'effect',
                    'effed' : 'effect',
                    'effedl' : 'effect',
                    'effedt' : 'effect',
                    'effeft' : 'effect',
                    'eflablifh' : 'establish',
                    'eflablifli' : 'establish',
                    'eflect' : 'effect',
                    'efpccially' : 'especially',
                    'efpeciaUy' : 'especially',
                    'efpecially' : 'especially',
                    'efpeciauy' : 'especially',
                    'eftabhfh' : 'establish',
                    'eftablifb' : 'establish',
                    'eftablifh' : 'establish',
                    'eftablifli' : 'establish',
                    'eftabliih' : 'establish',
                    'eftablijh' : 'establish',
                    'eftablim' : 'establish',
                    'eftablish' : 'establish',
                    'ei^en' : 'even',
                    'eien' : 'even',
                    'eient' : 'event',
                    'eiery' : 'every',
                    'eig^ht' : 'eight',
                    'eigbt' : 'eight',
                    'eiglit' : 'eight',
                    'eilher' : 'either',
                    'eitber' : 'either',
                    'eithcr' : 'either',
                    'eithei' : 'either',
                    'eitlier' : 'either',
                    'ei»en' : 'even',
                    'eleclion' : 'election',
                    'elect1on' : 'election',
                    'electlon' : 'election',
                    'eledion' : 'election',
                    'eledlion' : 'election',
                    'eledtion' : 'election',
                    'eleftion' : 'election',
                    'ele£lion' : 'election',
                    'elght' : 'eight',
                    'elpecially' : 'especially',
                    'els6' : 'else',
                    'elsc' : 'else',
                    'eltablilh' : 'establish',
                    'elther' : 'either',
                    'employec' : 'employee',
                    'en6ugh' : 'enough',
                    'encrgv' : 'energy',
                    'encrgy' : 'energy',
                    'energv' : 'energy',
                    'enjov' : 'enjoy',
                    'enongh' : 'enough',
                    'enoug^h' : 'enough',
                    'enougb' : 'enough',
                    'enougli' : 'enough',
                    'ent1re' : 'entire',
                    'entcr' : 'enter',
                    'entei' : 'enter',
                    'entirc' : 'entire',
                    'eould' : 'could',
                    'es[)ecially' : 'especially',
                    'es])ecially' : 'especially',
                    'esi)ecially' : 'especially',
                    'esj)ecially' : 'especially',
                    'espccially' : 'especially',
                    'espec1ally' : 'especially',
                    'especiaUy' : 'especially',
                    'especiahy' : 'especially',
                    'especiallv' : 'especially',
                    'especiauy' : 'especially',
                    'especlally' : 'especially',
                    'estab1ish' : 'establish',
                    'estabUsh' : 'establish',
                    'estabhsh' : 'establish',
                    'establ1sh' : 'establish',
                    'establifh' : 'establish',
                    'establilh' : 'establish',
                    'establisb' : 'establish',
                    'estahiish' : 'establish',
                    'estahlish' : 'establish',
                    'es|)ecially' : 'especially',
                    'euough' : 'enough',
                    'ev1dence' : 'evidence',
                    'ev6n' : 'even',
                    'ev^en' : 'even',
                    'ev^ening' : 'evening',
                    'ev^ent' : 'event',
                    'ev^er' : 'ever',
                    'ev^ery' : 'every',
                    'evcn' : 'even',
                    'evcnt' : 'event',
                    'evcr' : 'ever',
                    'evcry' : 'every',
                    'evcrything' : 'everything',
                    'eveiy' : 'every',
                    'even1ng' : 'evening',
                    'evenmg' : 'evening',
                    'everv' : 'every',
                    'evervbody' : 'everybody',
                    'evervone' : 'everyone',
                    'evervthing' : 'everything',
                    'everybodv' : 'everybody',
                    'everyhody' : 'everybody',
                    'everytbing' : 'everything',
                    'eveu' : 'even',
                    'evidcnce' : 'evidence',
                    'evidencc' : 'evidence',
                    'evldence' : 'evidence',
                    'ex1st' : 'exist',
                    'ex[)erience' : 'experience',
                    'ex])erience' : 'experience',
                    'ex])lain' : 'explain',
                    'exacUy' : 'exactly',
                    'exaclly' : 'exactly',
                    'exactlv' : 'exactly',
                    'exadlly' : 'exactly',
                    'exadly' : 'exactly',
                    'exadtly' : 'exactly',
                    'exaftly' : 'exactly',
                    'exam[)le' : 'example',
                    'exam])le' : 'example',
                    'exami)le' : 'example',
                    'examj)le' : 'example',
                    'examp1e' : 'example',
                    'examplc' : 'example',
                    'exa£lly' : 'exactly',
                    'exa£tly' : 'exactly',
                    'execut1ve' : 'executive',
                    'exi)ect' : 'expect',
                    'exi)erience' : 'experience',
                    'exi)lain' : 'explain',
                    'exifl' : 'exist',
                    'exift' : 'exist',
                    'exilt' : 'exist',
                    'exj)ect' : 'expect',
                    'exj)erience' : 'experience',
                    'exj)lain' : 'explain',
                    'exp6rience' : 'experience',
                    'expcft' : 'expect',
                    'expcrience' : 'experience',
                    'expecl' : 'expect',
                    'exped' : 'expect',
                    'expedl' : 'expect',
                    'expedt' : 'expect',
                    'expeft' : 'expect',
                    'exper1ence' : 'experience',
                    'expericnce' : 'experience',
                    'experiencc' : 'experience',
                    'ex|)erience' : 'experience',
                    'eſfect' : 'effect',
                    'eſlabliſh' : 'establish',
                    'eﬁfect' : 'effect',
                    'f)lace' : 'place',
                    'f/W' : 'few',
                    'f0rce' : 'force',
                    'f0reign' : 'foreign',
                    'f0rm' : 'form',
                    'f0ur' : 'four',
                    'f1eld' : 'field',
                    'f1ght' : 'fight',
                    'f1gure' : 'figure',
                    'f1ll' : 'fill',
                    'f1lm' : 'film',
                    'f1milar' : 'similar',
                    'f1nal' : 'final',
                    'f1nally' : 'finally',
                    'f1nancial' : 'financial',
                    'f1nd' : 'find',
                    'f1ne' : 'fine',
                    'f1nger' : 'finger',
                    'f1nish' : 'finish',
                    'f1re' : 'fire',
                    'f1rm' : 'firm',
                    'f1rst' : 'first',
                    'f1sh' : 'fish',
                    'f1tuation' : 'situation',
                    'f1ve' : 'five',
                    'f6rce' : 'force',
                    'f6rm' : 'form',
                    'f6ur' : 'four',
                    'fUy' : 'fly',
                    'f^all' : 'fall',
                    'f^ar' : 'far',
                    'f^ill' : 'fill',
                    'f^ive' : 'five',
                    'f^ood' : 'food',
                    'f^or' : 'for',
                    'f^r' : 'for',
                    'f^rom' : 'from',
                    'f^und' : 'fund',
                    'faUh' : 'fall',
                    'fac6' : 'face',
                    'facc' : 'face',
                    'facl' : 'fact',
                    'faclor' : 'factor',
                    'fadl' : 'fact',
                    'fador' : 'factor',
                    'fadt' : 'fact',
                    'fadtor' : 'factor',
                    'fafe' : 'safe',
                    'fafl' : 'fast',
                    'faft' : 'fast',
                    'faftor' : 'factor',
                    'fai1' : 'fail',
                    'faiU' : 'fail',
                    'faih' : 'fail',
                    'fal1' : 'fall',
                    'fam1ly' : 'family',
                    'famUy' : 'family',
                    'fami1y' : 'family',
                    'familv' : 'family',
                    'fatber' : 'father',
                    'fathcr' : 'father',
                    'fathei' : 'father',
                    'fatlier' : 'father',
                    'fave' : 'save',
                    'faye' : 'say',
                    'fbort' : 'short',
                    'fbould' : 'should',
                    'fcafon' : 'season',
                    'fcbool' : 'school',
                    'fccling' : 'feeling',
                    'fccond' : 'second',
                    'fcction' : 'section',
                    'fccurity' : 'security',
                    'fcderal' : 'federal',
                    'fcel' : 'feel',
                    'fceling' : 'feeling',
                    'fcem' : 'seem',
                    'fcene' : 'scene',
                    'fchool' : 'school',
                    'fcicnce' : 'science',
                    'fciencc' : 'science',
                    'fcience' : 'science',
                    'fcore' : 'score',
                    'fcrious' : 'serious',
                    'fcrvicc' : 'service',
                    'fcrvice' : 'service',
                    'fcvcral' : 'several',
                    'fcveral' : 'several',
                    'feAv' : 'few',
                    'fea' : 'sea',
                    'feafon' : 'season',
                    'feai' : 'fear',
                    'feason' : 'season',
                    'fecl' : 'feel',
                    'fecling' : 'feeling',
                    'feclion' : 'section',
                    'fecond' : 'second',
                    'fection' : 'section',
                    'fecurity' : 'security',
                    'federa1' : 'federal',
                    'fedion' : 'section',
                    'fedlion' : 'section',
                    'fedtion' : 'section',
                    'fee1' : 'feel',
                    'feeU' : 'feel',
                    'feeUng' : 'feeling',
                    'feeh' : 'feel',
                    'feehng' : 'feeling',
                    'feek' : 'seek',
                    'feel1ng' : 'feeling',
                    'feem' : 'seem',
                    'feeung' : 'feeling',
                    'feftion' : 'section',
                    'feiv' : 'few',
                    'fenfe' : 'sense',
                    'fenior' : 'senior',
                    'fense' : 'sense',
                    'ferics' : 'series',
                    'feries' : 'series',
                    'feriouf' : 'serious',
                    'ferious' : 'serious',
                    'ferve' : 'serve',
                    'fervicc' : 'service',
                    'fervice' : 'service',
                    'fevcral' : 'several',
                    'feven' : 'seven',
                    'feveral' : 'several',
                    'fex' : 'sex',
                    'fexual' : 'sexual',
                    'fe£tion' : 'section',
                    'ffave' : 'save',
                    'ffea' : 'sea',
                    'ffhe' : 'she',
                    'ffite' : 'site',
                    'ffom' : 'from',
                    'ffome' : 'some',
                    'fhake' : 'shake',
                    'fhare' : 'share',
                    'fhe' : 'she',
                    'fhoot' : 'shoot',
                    'fhort' : 'short',
                    'fhot' : 'shot',
                    'fhould' : 'should',
                    'fhoulder' : 'shoulder',
                    'fhow' : 'show',
                    'fi1m' : 'film',
                    'fiU' : 'fill',
                    'fiate' : 'state',
                    'ficld' : 'field',
                    'fie1d' : 'field',
                    'fifh' : 'fish',
                    'fifler' : 'sister',
                    'fifli' : 'fish',
                    'fifter' : 'sister',
                    'figbt' : 'fight',
                    'figlit' : 'fight',
                    'fign' : 'sign',
                    'fignificant' : 'significant',
                    'figur6' : 'figure',
                    'figurc' : 'figure',
                    'fiift' : 'first',
                    'fiih' : 'fish',
                    'fijb' : 'fish',
                    'fil1' : 'fill',
                    'filh' : 'fish',
                    'fimilar' : 'similar',
                    'fimplc' : 'simple',
                    'fimple' : 'simple',
                    'fimply' : 'simply',
                    'fin1sh' : 'finish',
                    'fina1' : 'final',
                    'finaU' : 'final',
                    'finaUy' : 'finally',
                    'finallv' : 'finally',
                    'financia1' : 'financial',
                    'finauy' : 'finally',
                    'finc' : 'fine',
                    'fincc' : 'since',
                    'fince' : 'since',
                    'fing' : 'sing',
                    'fingcr' : 'finger',
                    'finglc' : 'single',
                    'fingle' : 'single',
                    'finifh' : 'finish',
                    'finifli' : 'finish',
                    'finiih' : 'finish',
                    'finijh' : 'finish',
                    'finilh' : 'finish',
                    'finim' : 'finish',
                    'firc' : 'fire',
                    'firfi' : 'first',
                    'firfl' : 'first',
                    'firft' : 'first',
                    'firit' : 'first',
                    'firlt' : 'first',
                    'firsi' : 'first',
                    'fisb' : 'fish',
                    'fisli' : 'fish',
                    'fister' : 'sister',
                    'fite' : 'site',
                    'fituation' : 'situation',
                    'fiud' : 'find',
                    'fiv^e' : 'five',
                    'fivc' : 'five',
                    'fize' : 'size',
                    'fkill' : 'skill',
                    'fkin' : 'skin',
                    'fl^y' : 'fly',
                    'flaff' : 'staff',
                    'flage' : 'stage',
                    'fland' : 'stand',
                    'flandard' : 'standard',
                    'flart' : 'start',
                    'flatement' : 'statement',
                    'flation' : 'station',
                    'fleld' : 'field',
                    'flght' : 'fight',
                    'flgure' : 'figure',
                    'fliarc' : 'share',
                    'fliare' : 'share',
                    'flill' : 'still',
                    'fliort' : 'short',
                    'fliot' : 'shot',
                    'fliould' : 'should',
                    'flioulder' : 'shoulder',
                    'fliow' : 'show',
                    'flll' : 'fill',
                    'flnaUy' : 'finally',
                    'flnal' : 'final',
                    'flnally' : 'finally',
                    'flnancial' : 'financial',
                    'flnd' : 'find',
                    'flne' : 'fine',
                    'flnger' : 'finger',
                    'flnish' : 'finish',
                    'flre' : 'fire',
                    'flreet' : 'street',
                    'flrm' : 'firm',
                    'flrong' : 'strong',
                    'flrst' : 'first',
                    'flructure' : 'structure',
                    'flrufture' : 'structure',
                    'flsh' : 'fish',
                    'fludent' : 'student',
                    'fludy' : 'study',
                    'flyle' : 'style',
                    'fmal' : 'final',
                    'fmall' : 'small',
                    'fmally' : 'finally',
                    'fmgle' : 'single',
                    'fmile' : 'smile',
                    'fnll' : 'full',
                    'foUov' : 'follow',
                    'foUow' : 'follow',
                    'focial' : 'social',
                    'focicty' : 'society',
                    'focietv' : 'society',
                    'fociety' : 'society',
                    'focul' : 'focus',
                    'foice' : 'force',
                    'foim' : 'form',
                    'foldicr' : 'soldier',
                    'foldier' : 'soldier',
                    'folloAv' : 'follow',
                    'follo\v' : 'follow',
                    'folloiv' : 'follow',
                    'follov' : 'follow',
                    'fomcthing' : 'something',
                    'fomctimcs' : 'sometimes',
                    'fomctimes' : 'sometimes',
                    'fome' : 'some',
                    'fomebody' : 'somebody',
                    'fometbing' : 'something',
                    'fomething' : 'something',
                    'fometimcs' : 'sometimes',
                    'fometimes' : 'sometimes',
                    'fong' : 'song',
                    'foon' : 'soon',
                    'forAvard' : 'forward',
                    'for\vard' : 'forward',
                    'for^vard' : 'forward',
                    'forc6' : 'force',
                    'forcc' : 'force',
                    'forcign' : 'foreign',
                    'foreigu' : 'foreign',
                    'forgct' : 'forget',
                    'forivard' : 'forward',
                    'formcr' : 'former',
                    'formei' : 'former',
                    'forv/ard' : 'forward',
                    'forvard' : 'forward',
                    'fouow' : 'follow',
                    'fourcc' : 'source',
                    'fource' : 'source',
                    'foutb' : 'south',
                    'fouth' : 'south',
                    'fouthcrn' : 'southern',
                    'fouthern' : 'southern',
                    'fpace' : 'space',
                    'fpccial' : 'special',
                    'fpccific' : 'specific',
                    'fpcech' : 'speech',
                    'fpeak' : 'speak',
                    'fpecch' : 'speech',
                    'fpecial' : 'special',
                    'fpecific' : 'specific',
                    'fpecilic' : 'specific',
                    'fpeecb' : 'speech',
                    'fpeech' : 'speech',
                    'fpend' : 'spend',
                    'fport' : 'sport',
                    'fpring' : 'spring',
                    'fr0m' : 'from',
                    'fr0nt' : 'front',
                    'fr1end' : 'friend',
                    'fr6m' : 'from',
                    'fr^om' : 'from',
                    'frec' : 'free',
                    'fricnd' : 'friend',
                    'frieud' : 'friend',
                    'frlend' : 'friend',
                    'froni' : 'front',
                    'frout' : 'front',
                    'ftaff' : 'staff',
                    'ftafl' : 'staff',
                    'ftage' : 'stage',
                    'ftand' : 'stand',
                    'ftandard' : 'standard',
                    'ftar' : 'star',
                    'ftart' : 'start',
                    'ftatcment' : 'statement',
                    'ftate' : 'state',
                    'ftatement' : 'statement',
                    'ftation' : 'station',
                    'ftay' : 'stay',
                    'ftep' : 'step',
                    'ftiil' : 'still',
                    'ftill' : 'still',
                    'ftock' : 'stock',
                    'ftop' : 'stop',
                    'ftore' : 'store',
                    'ftory' : 'story',
                    'ftrcet' : 'street',
                    'ftrect' : 'street',
                    'ftreet' : 'street',
                    'ftrong' : 'strong',
                    'ftruclure' : 'structure',
                    'ftructurc' : 'structure',
                    'ftructure' : 'structure',
                    'ftrudlure' : 'structure',
                    'ftrudture' : 'structure',
                    'ftrudure' : 'structure',
                    'ftrufture' : 'structure',
                    'ftudent' : 'student',
                    'ftudy' : 'study',
                    'ftuff' : 'stuff',
                    'ftyle' : 'style',
                    'fuU' : 'full',
                    'fuUj' : 'full',
                    'fuUv' : 'full',
                    'fubjcct' : 'subject',
                    'fubjecT' : 'subject',
                    'fubjecft' : 'subject',
                    'fubjecl' : 'subject',
                    'fubject' : 'subject',
                    'fubjed' : 'subject',
                    'fubjedl' : 'subject',
                    'fubjedt' : 'subject',
                    'fubjeft' : 'subject',
                    'fubje£b' : 'subject',
                    'fubje£l' : 'subject',
                    'fubje£r' : 'subject',
                    'fubje£t' : 'subject',
                    'fucceff' : 'success',
                    'fuccefs' : 'success',
                    'fuccefsful' : 'successful',
                    'fuccess' : 'success',
                    'fuch' : 'such',
                    'fuddcnly' : 'suddenly',
                    'fuddenly' : 'suddenly',
                    'fuffcr' : 'suffer',
                    'fuffer' : 'suffer',
                    'fuggcft' : 'suggest',
                    'fuggefl' : 'suggest',
                    'fuggeft' : 'suggest',
                    'fuggest' : 'suggest',
                    'fuhject' : 'subject',
                    'ful1' : 'full',
                    'fummcr' : 'summer',
                    'fummer' : 'summer',
                    'fupport' : 'support',
                    'fure' : 'sure',
                    'furfacc' : 'surface',
                    'furface' : 'surface',
                    'futurc' : 'future',
                    'futuræ' : 'future',
                    'fvftem' : 'system',
                    'fyflem' : 'system',
                    'fyftcm' : 'system',
                    'fyftem' : 'system',
                    'fystem' : 'system',
                    'g00d' : 'good',
                    'g0od' : 'good',
                    'g0vernment' : 'government',
                    'g1ve' : 'give',
                    'g6n6ral' : 'general',
                    'g6neral' : 'general',
                    'g6od' : 'good',
                    'g6vernment' : 'government',
                    'g^as' : 'gas',
                    'g^eneral' : 'general',
                    'g^et' : 'get',
                    'g^ive' : 'give',
                    'g^ood' : 'good',
                    'g^overnment' : 'government',
                    'g^reat' : 'great',
                    'g^reen' : 'green',
                    'g^round' : 'ground',
                    'gaf' : 'gas',
                    'gamc' : 'game',
                    'gardcn' : 'garden',
                    'gcncral' : 'general',
                    'gcneral' : 'general',
                    'gcneration' : 'generation',
                    'ge^t' : 'get',
                    'gen6ral' : 'general',
                    'gencral' : 'general',
                    'gencration' : 'generation',
                    'geneial' : 'general',
                    'genera1' : 'general',
                    'generaU' : 'general',
                    'generah' : 'general',
                    'geueral' : 'general',
                    'ghass' : 'glass',
                    'gieat' : 'great',
                    'ginaUy' : 'finally',
                    'giound' : 'ground',
                    'gir1' : 'girl',
                    'girU' : 'girl',
                    'girh' : 'girl',
                    'giv6' : 'give',
                    'giv^e' : 'give',
                    'givc' : 'give',
                    'giæ' : 'give',
                    'glaff' : 'glass',
                    'glafs' : 'glass',
                    'glals' : 'glass',
                    'glrl' : 'girl',
                    'goa1' : 'goal',
                    'goaU' : 'goal',
                    'goah' : 'goal',
                    'gouerniment' : 'government',
                    'gov^ernment' : 'government',
                    'govcrnmcnt' : 'government',
                    'govcrnment' : 'government',
                    'governmcnt' : 'government',
                    'governmeut' : 'government',
                    'gr0und' : 'ground',
                    'gr6und' : 'ground',
                    'gr^eat' : 'great',
                    'grcat' : 'great',
                    'grcen' : 'green',
                    'greai' : 'great',
                    'grecn' : 'green',
                    'greeu' : 'green',
                    'groAv' : 'grow',
                    'groAvth' : 'growth',
                    'gro\v' : 'grow',
                    'gro\vth' : 'growth',
                    'gro^v' : 'grow',
                    'gro^vth' : 'growth',
                    'groiv' : 'grow',
                    'groivth' : 'growth',
                    'grouud' : 'ground',
                    'grov' : 'grow',
                    'grov/th' : 'growth',
                    'growtb' : 'growth',
                    'growtli' : 'growth',
                    'gucss' : 'guess',
                    'guef' : 'guess',
                    'guefs' : 'guess',
                    'guels' : 'guess',
                    'guesf' : 'guess',
                    'h0me' : 'home',
                    'h0use' : 'house',
                    'h1gh' : 'high',
                    'h1mself' : 'himself',
                    'h1story' : 'history',
                    'h6pe' : 'hope',
                    'h6re' : 'here',
                    'h6tel' : 'hotel',
                    'h6wever' : 'however',
                    'h^ard' : 'hard',
                    'h^ave' : 'have',
                    'h^er' : 'her',
                    'h^is' : 'his',
                    'h^it' : 'hit',
                    'h^r' : 'her',
                    'ha1f' : 'half',
                    'ha1r' : 'hair',
                    'ha[)py' : 'happy',
                    'ha\^ng' : 'hang',
                    'ha])pen' : 'happen',
                    'ha])py' : 'happy',
                    'ha^^ng' : 'hang',
                    'ha^ang' : 'hang',
                    'ha^e' : 'have',
                    'ha^ng' : 'hang',
                    'ha^nng' : 'hang',
                    'ha^ve' : 'have',
                    'haby' : 'baby',
                    'hahf' : 'half',
                    'haj)pen' : 'happen',
                    'haj)py' : 'happy',
                    'halr' : 'hair',
                    'hap[)y' : 'happy',
                    'hap])en' : 'happen',
                    'hap])y' : 'happy',
                    'hapj)en' : 'happen',
                    'hapj)y' : 'happy',
                    'happcn' : 'happen',
                    'happv' : 'happy',
                    'hap|)y' : 'happy',
                    'hav6' : 'have',
                    'hav^e' : 'have',
                    'havc' : 'have',
                    'ha|)py' : 'happy',
                    'hcad' : 'head',
                    'hcalth' : 'health',
                    'hcar' : 'hear',
                    'hcart' : 'heart',
                    'hcat' : 'heat',
                    'hcautiful' : 'beautiful',
                    'hcavy' : 'heavy',
                    'hccause' : 'because',
                    'hclp' : 'help',
                    'hcre' : 'here',
                    'hcrfclf' : 'herself',
                    'hcrfelf' : 'herself',
                    'hctween' : 'between',
                    'he1p' : 'help',
                    'heUeve' : 'believe',
                    'he^ad' : 'head',
                    'he^r' : 'her',
                    'hea1th' : 'health',
                    'heai' : 'hear',
                    'heait' : 'heart',
                    'heaiy' : 'heavy',
                    'healtb' : 'health',
                    'healtli' : 'health',
                    'heantiful' : 'beautiful',
                    'heaotiful' : 'beautiful',
                    'heauliful' : 'beautiful',
                    'heautifiil' : 'beautiful',
                    'heautifnl' : 'beautiful',
                    'heautifol' : 'beautiful',
                    'heautiful' : 'beautiful',
                    'heautifull' : 'beautiful',
                    'heav^y' : 'heavy',
                    'hecaiise' : 'because',
                    'hecaufe' : 'because',
                    'hecausc' : 'because',
                    'hecause' : 'because',
                    'hecome' : 'become',
                    'hefore' : 'before',
                    'hegin' : 'begin',
                    'hehavior' : 'behavior',
                    'hehind' : 'behind',
                    'heie' : 'here',
                    'helicve' : 'believe',
                    'helievc' : 'believe',
                    'helieve' : 'believe',
                    'hencfit' : 'benefit',
                    'henefit' : 'benefit',
                    'herc' : 'here',
                    'herfclf' : 'herself',
                    'herfelf' : 'herself',
                    'herfell' : 'herself',
                    'herlelf' : 'herself',
                    'hersclf' : 'herself',
                    'herseU' : 'herself',
                    'herſelſ' : 'herself',
                    'hetiveen' : 'between',
                    'hetwcen' : 'between',
                    'hetwecn' : 'between',
                    'hetweeii' : 'between',
                    'hetween' : 'between',
                    'heyond' : 'beyond',
                    'hfe' : 'life',
                    'hght' : 'light',
                    'hi^s' : 'his',
                    'hi^t' : 'hit',
                    'hieten' : 'listen',
                    'hif' : 'his',
                    'hife' : 'life',
                    'hifee' : 'life',
                    'hiffe' : 'life',
                    'hiflory' : 'history',
                    'hiftorv' : 'history',
                    'hiftory' : 'history',
                    'hig^h' : 'high',
                    'higb' : 'high',
                    'higli' : 'high',
                    'hiife' : 'life',
                    'hiiild' : 'build',
                    'hiiilding' : 'building',
                    'hiisiness' : 'business',
                    'hiiten' : 'listen',
                    'hiitory' : 'history',
                    'hikke' : 'like',
                    'hiltory' : 'history',
                    'him^self' : 'himself',
                    'himfclf' : 'himself',
                    'himfeif' : 'himself',
                    'himfelf' : 'himself',
                    'himfelff' : 'himself',
                    'himfell' : 'himself',
                    'himielf' : 'himself',
                    'himlelf' : 'himself',
                    'himne' : 'line',
                    'himsclf' : 'himself',
                    'himse1f' : 'himself',
                    'himseU' : 'himself',
                    'himseli' : 'himself',
                    'himten' : 'listen',
                    'himſelſ' : 'himself',
                    'hin^e' : 'line',
                    'hinguage' : 'language',
                    'hin|e' : 'line',
                    'hismen' : 'listen',
                    'hispen' : 'listen',
                    'hist0ry' : 'history',
                    'histan' : 'listen',
                    'histin' : 'listen',
                    'histoiy' : 'history',
                    'historv' : 'history',
                    'histun' : 'listen',
                    'hiszen' : 'listen',
                    'hitely' : 'likely',
                    'hiſiory' : 'history',
                    'hiſlory' : 'history',
                    'hiﬁory' : 'history',
                    'hkely' : 'likely',
                    'hlack' : 'black',
                    'hlgh' : 'high',
                    'hlmself' : 'himself',
                    'hlood' : 'blood',
                    'hlstory' : 'history',
                    'hlue' : 'blue',
                    'hmne' : 'line',
                    'hnilding' : 'building',
                    'hnman' : 'human',
                    'hnndred' : 'hundred',
                    'hnoivledge' : 'knowledge',
                    'hnsband' : 'husband',
                    'hnsiness' : 'business',
                    'hnttle' : 'little',
                    'ho1d' : 'hold',
                    'hoAv' : 'how',
                    'hoAvcver' : 'however',
                    'hoAvevcr' : 'however',
                    'ho\vever' : 'however',
                    'ho^t' : 'hot',
                    'ho^vever' : 'however',
                    'ho^w' : 'how',
                    'hoavever' : 'however',
                    'hody' : 'body',
                    'hofpital' : 'hospital',
                    'hohd' : 'hold',
                    'hoiv' : 'how',
                    'hoivever' : 'however',
                    'hoj)e' : 'hope',
                    'holpital' : 'hospital',
                    'homc' : 'home',
                    'honr' : 'hour',
                    'hopc' : 'hope',
                    'hos[)ital' : 'hospital',
                    'hos])ital' : 'hospital',
                    'hosi)ital' : 'hospital',
                    'hosj)ital' : 'hospital',
                    'hosp1tal' : 'hospital',
                    'hospita1' : 'hospital',
                    'hospitaU' : 'hospital',
                    'hotcl' : 'hotel',
                    'hote1' : 'hotel',
                    'hoteh' : 'hotel',
                    'hoth' : 'both',
                    'houfc' : 'house',
                    'houfe' : 'house',
                    'houffe' : 'house',
                    'houie' : 'house',
                    'housc' : 'house',
                    'hov/ever' : 'however',
                    'hov^^ever' : 'however',
                    'hov^ever' : 'however',
                    'hovever' : 'however',
                    'howcvcr' : 'however',
                    'howcver' : 'however',
                    'howeier' : 'however',
                    'howev^er' : 'however',
                    'howevcr' : 'however',
                    'howevei' : 'however',
                    'hreak' : 'break',
                    'hring' : 'bring',
                    'hrothcr' : 'brother',
                    'hrother' : 'brother',
                    'hsten' : 'listen',
                    'httle' : 'little',
                    'hudget' : 'budget',
                    'hufband' : 'husband',
                    'hufhand' : 'husband',
                    'hufinefs' : 'business',
                    'huiband' : 'husband',
                    'huild' : 'build',
                    'huilding' : 'building',
                    'huildiug' : 'building',
                    'hujhand' : 'husband',
                    'hulband' : 'husband',
                    'humau' : 'human',
                    'hundrcd' : 'hundred',
                    'hushand' : 'husband',
                    'husincss' : 'business',
                    'husinefs' : 'business',
                    'husines' : 'business',
                    'husiness' : 'business',
                    'husiuess' : 'business',
                    'huudred' : 'hundred',
                    'huſhand' : 'husband',
                    'hösten' : 'listen',
                    'i)Oor' : 'poor',
                    'i)Osition' : 'position',
                    'i)Ut' : 'put',
                    'i)ainting' : 'painting',
                    'i)aper' : 'paper',
                    'i)articular' : 'particular',
                    'i)articularly' : 'particularly',
                    'i)artner' : 'partner',
                    'i)arty' : 'party',
                    'i)atient' : 'patient',
                    'i)ay' : 'pay',
                    'i)eace' : 'peace',
                    'i)en' : 'open',
                    'i)eople' : 'people',
                    'i)er' : 'per',
                    'i)erform' : 'perform',
                    'i)erformance' : 'performance',
                    'i)erhaps' : 'perhaps',
                    'i)eriod' : 'period',
                    'i)erson' : 'person',
                    'i)ersonal' : 'personal',
                    'i)hysical' : 'physical',
                    'i)icture' : 'picture',
                    'i)lace' : 'place',
                    'i)lan' : 'plan',
                    'i)oint' : 'point',
                    'i)olice' : 'police',
                    'i)olicy' : 'policy',
                    'i)olitical' : 'political',
                    'i)olitics' : 'politics',
                    'i)oor' : 'poor',
                    'i)opular' : 'popular',
                    'i)opulation' : 'population',
                    'i)osition' : 'position',
                    'i)ossible' : 'possible',
                    'i)ractice' : 'practice',
                    'i)repare' : 'prepare',
                    'i)rescnt' : 'present',
                    'i)resent' : 'present',
                    'i)reseut' : 'present',
                    'i)resident' : 'president',
                    'i)ressure' : 'pressure',
                    'i)retty' : 'pretty',
                    'i)revent' : 'prevent',
                    'i)rice' : 'price',
                    'i)rivate' : 'private',
                    'i)robably' : 'probably',
                    'i)rocess' : 'process',
                    'i)roduce' : 'produce',
                    'i)roduct' : 'product',
                    'i)roduction' : 'production',
                    'i)roperty' : 'property',
                    'i)rotect' : 'protect',
                    'i)rove' : 'prove',
                    'i)rovide' : 'provide',
                    'i)ublic' : 'public',
                    'i)urpose' : 'purpose',
                    'i)ut' : 'put',
                    'iSee' : 'see',
                    'iVote' : 'vote',
                    'i^n' : 'in',
                    'i^t' : 'it',
                    'i^ts' : 'its',
                    'iave' : 'save',
                    'idca' : 'idea',
                    'identifv' : 'identify',
                    'ieveral' : 'several',
                    'iffue' : 'issue',
                    'iflue' : 'issue',
                    'ifsue' : 'issue',
                    'ifue' : 'issue',
                    'ihan' : 'than',
                    'ihare' : 'share',
                    'ihat' : 'that',
                    'iheir' : 'their',
                    'ihem' : 'them',
                    'ihese' : 'these',
                    'ihey' : 'they',
                    'ihing' : 'thing',
                    'ihink' : 'think',
                    'ihird' : 'third',
                    'ihort' : 'short',
                    'ihose' : 'those',
                    'ihot' : 'shot',
                    'ihough' : 'though',
                    'ihould' : 'should',
                    'ihrough' : 'through',
                    'ihus' : 'thus',
                    'ii])on' : 'upon',
                    'iield' : 'field',
                    'iii)on' : 'upon',
                    'iince' : 'since',
                    'iirft' : 'first',
                    'iirst' : 'first',
                    'ikill' : 'skill',
                    'iliould' : 'should',
                    'ilsue' : 'issue',
                    'iltuation' : 'situation',
                    'im[)ortant' : 'important',
                    'im])ortant' : 'important',
                    'imagc' : 'image',
                    'imaginc' : 'imagine',
                    'imall' : 'small',
                    'imi)ortant' : 'important',
                    'imi)rove' : 'improve',
                    'imj)ortant' : 'important',
                    'imp0rtant' : 'important',
                    'imp6rtant' : 'important',
                    'impacl' : 'impact',
                    'improvc' : 'improve',
                    'im|)ortant' : 'important',
                    'in^to' : 'into',
                    'inc1uding' : 'including',
                    'inclnding' : 'including',
                    'includ1ng' : 'including',
                    'includc' : 'include',
                    'incrcafc' : 'increase',
                    'incrcafe' : 'increase',
                    'incrcase' : 'increase',
                    'increafc' : 'increase',
                    'increafe' : 'increase',
                    'increale' : 'increase',
                    'increasc' : 'increase',
                    'ind1vidual' : 'individual',
                    'indced' : 'indeed',
                    'indecd' : 'indeed',
                    'indicatc' : 'indicate',
                    'individua1' : 'individual',
                    'induflry' : 'industry',
                    'induftry' : 'industry',
                    'indultry' : 'industry',
                    'industrv' : 'industry',
                    'induſlry' : 'industry',
                    'inf0rmati0n' : 'information',
                    'infidc' : 'inside',
                    'infide' : 'inside',
                    'inflcad' : 'instead',
                    'inflead' : 'instead',
                    'informat1on' : 'information',
                    'inftcad' : 'instead',
                    'inftead' : 'instead',
                    'inftitution' : 'institution',
                    'inlide' : 'inside',
                    'inlo' : 'into',
                    'inltead' : 'instead',
                    'inltitution' : 'institution',
                    'insistment' : 'investment',
                    'inst1tut1on' : 'institution',
                    'inst1tution' : 'institution',
                    'instcad' : 'instead',
                    'institut1on' : 'institution',
                    'instituti0n' : 'institution',
                    'int0' : 'into',
                    'int6' : 'into',
                    'intcrcft' : 'interest',
                    'intcrcst' : 'interest',
                    'intcreft' : 'interest',
                    'intcrefting' : 'interesting',
                    'intcrest' : 'interest',
                    'intcresting' : 'interesting',
                    'intercfl' : 'interest',
                    'intercft' : 'interest',
                    'intercfting' : 'interesting',
                    'intercst' : 'interest',
                    'intercsting' : 'interesting',
                    'interefl' : 'interest',
                    'interefling' : 'interesting',
                    'intereft' : 'interest',
                    'interefting' : 'interesting',
                    'interelt' : 'interest',
                    'interelting' : 'interesting',
                    'interest1ng' : 'interesting',
                    'intereſl' : 'interest',
                    'internationa1' : 'international',
                    'intervicw' : 'interview',
                    'interviev' : 'interview',
                    'inveftment' : 'investment',
                    'inﬁde' : 'inside',
                    'ioice' : 'voice',
                    'iome' : 'some',
                    'iong' : 'song',
                    'iove' : 'love',
                    'ipeak' : 'speak',
                    'iriend' : 'friend',
                    'irue' : 'true',
                    'isfue' : 'issue',
                    'islue' : 'issue',
                    'issne' : 'issue',
                    'issuc' : 'issue',
                    'it^s' : 'its',
                    'itand' : 'stand',
                    'itcm' : 'item',
                    'itf' : 'its',
                    'itfclf' : 'itself',
                    'itfelf' : 'itself',
                    'itfell' : 'itself',
                    'itff' : 'its',
                    'itill' : 'still',
                    'itlelf' : 'itself',
                    'itrong' : 'strong',
                    'itsclf' : 'itself',
                    'itse1f' : 'itself',
                    'itsell' : 'itself',
                    'itſelſ' : 'itself',
                    'iudeed' : 'indeed',
                    'iure' : 'sure',
                    'iuterest' : 'interest',
                    'iuto' : 'into',
                    'ivait' : 'wait',
                    'ivalk' : 'walk',
                    'ivall' : 'wall',
                    'ivatch' : 'watch',
                    'ivater' : 'water',
                    'ivear' : 'wear',
                    'iveek' : 'week',
                    'iveight' : 'weight',
                    'ivell' : 'well',
                    'ivestern' : 'western',
                    'ivhat' : 'what',
                    'ivhatever' : 'whatever',
                    'ivhen' : 'when',
                    'ivhether' : 'whether',
                    'ivhich' : 'which',
                    'ivhile' : 'while',
                    'ivhite' : 'white',
                    'ivho' : 'who',
                    'ivhofe' : 'whose',
                    'ivhole' : 'whole',
                    'ivhom' : 'whom',
                    'ivhose' : 'whose',
                    'ivhy' : 'why',
                    'ivife' : 'wife',
                    'ivilhout' : 'without',
                    'ivill' : 'will',
                    'ivind' : 'wind',
                    'ivindow' : 'window',
                    'ivish' : 'wish',
                    'ivitbout' : 'without',
                    'ivith' : 'with',
                    'ivithin' : 'within',
                    'ivithoiit' : 'without',
                    'ivithont' : 'without',
                    'ivithout' : 'without',
                    'ivitliout' : 'without',
                    'ivliere' : 'where',
                    'ivliich' : 'which',
                    'ivliite' : 'white',
                    'ivliole' : 'whole',
                    'ivoman' : 'woman',
                    'ivonder' : 'wonder',
                    'ivord' : 'word',
                    'ivork' : 'work',
                    'ivorld' : 'world',
                    'ivould' : 'would',
                    'ivrite' : 'write',
                    'ivriter' : 'writer',
                    'ivrong' : 'wrong',
                    'j)0ssible' : 'possible',
                    'j)0wer' : 'power',
                    'j)Oor' : 'poor',
                    'j)Osition' : 'position',
                    'j)Ositive' : 'positive',
                    'j)Ossible' : 'possible',
                    'j)Ower' : 'power',
                    'j)age' : 'page',
                    'j)ainting' : 'painting',
                    'j)arent' : 'parent',
                    'j)art' : 'part',
                    'j)articular' : 'particular',
                    'j)articularly' : 'particularly',
                    'j)artner' : 'partner',
                    'j)arty' : 'party',
                    'j)ass' : 'pass',
                    'j)ast' : 'past',
                    'j)atient' : 'patient',
                    'j)attern' : 'pattern',
                    'j)cace' : 'peace',
                    'j)cople' : 'people',
                    'j)crhaps' : 'perhaps',
                    'j)criod' : 'period',
                    'j)crson' : 'person',
                    'j)eace' : 'peace',
                    'j)en' : 'open',
                    'j)eo])le' : 'people',
                    'j)eoi)le' : 'people',
                    'j)eoj)le' : 'people',
                    'j)eopIe' : 'people',
                    'j)eoplc' : 'people',
                    'j)eople' : 'people',
                    'j)erform' : 'perform',
                    'j)erformance' : 'performance',
                    'j)erhaps' : 'perhaps',
                    'j)eriod' : 'period',
                    'j)erliaps' : 'perhaps',
                    'j)erson' : 'person',
                    'j)ersonal' : 'personal',
                    'j)hysical' : 'physical',
                    'j)ick' : 'pick',
                    'j)icture' : 'picture',
                    'j)iece' : 'piece',
                    'j)lacc' : 'place',
                    'j)lace' : 'place',
                    'j)lan' : 'plan',
                    'j)lant' : 'plant',
                    'j)lay' : 'play',
                    'j)nblic' : 'public',
                    'j)nrpose' : 'purpose',
                    'j)olice' : 'police',
                    'j)olicy' : 'policy',
                    'j)olitical' : 'political',
                    'j)olitics' : 'politics',
                    'j)oor' : 'poor',
                    'j)opular' : 'popular',
                    'j)opulation' : 'population',
                    'j)osition' : 'position',
                    'j)ositive' : 'positive',
                    'j)ossible' : 'possible',
                    'j)owcr' : 'power',
                    'j)ower' : 'power',
                    'j)ractice' : 'practice',
                    'j)rcsent' : 'present',
                    'j)repare' : 'prepare',
                    'j)rescnt' : 'present',
                    'j)resent' : 'present',
                    'j)reseut' : 'present',
                    'j)resident' : 'president',
                    'j)ressure' : 'pressure',
                    'j)retty' : 'pretty',
                    'j)revent' : 'prevent',
                    'j)rice' : 'price',
                    'j)rivate' : 'private',
                    'j)robably' : 'probably',
                    'j)roblem' : 'problem',
                    'j)rocess' : 'process',
                    'j)roduce' : 'produce',
                    'j)roduct' : 'product',
                    'j)roduction' : 'production',
                    'j)rofessional' : 'professional',
                    'j)rofessor' : 'professor',
                    'j)roj)erty' : 'property',
                    'j)roject' : 'project',
                    'j)ropcrty' : 'property',
                    'j)roperty' : 'property',
                    'j)rotect' : 'protect',
                    'j)rove' : 'prove',
                    'j)rovide' : 'provide',
                    'j)ublic' : 'public',
                    'j)uhlic' : 'public',
                    'j)ul)lic' : 'public',
                    'j)ull' : 'pull',
                    'j)urpose' : 'purpose',
                    'j)ush' : 'push',
                    'j0in' : 'join',
                    'jLTHOUGH' : 'although',
                    'jPUBLIC' : 'public',
                    'j^that' : 'that',
                    'j^uhlic' : 'public',
                    'j^ust' : 'just',
                    'jbort' : 'short',
                    'jbot' : 'shot',
                    'jbould' : 'should',
                    'jhake' : 'shake',
                    'jhare' : 'share',
                    'jhoot' : 'shoot',
                    'jhort' : 'short',
                    'jhot' : 'shot',
                    'jhould' : 'should',
                    'jhow' : 'show',
                    'jufl' : 'just',
                    'juft' : 'just',
                    'jult' : 'just',
                    'jus^t' : 'just',
                    'jusi' : 'just',
                    'juſi' : 'just',
                    'juſl' : 'just',
                    'jvhether' : 'whether',
                    'jvithout' : 'without',
                    'jx)litical' : 'political',
                    'jx)sition' : 'position',
                    'jx)ssible' : 'possible',
                    'k1ll' : 'kill',
                    'k1tchen' : 'kitchen',
                    'kcep' : 'keep',
                    'kecp' : 'keep',
                    'kiUi' : 'kill',
                    'kil1' : 'kill',
                    'kin^d' : 'kind',
                    'kitcben' : 'kitchen',
                    'kiud' : 'kind',
                    'klll' : 'kill',
                    'klnd' : 'kind',
                    'kltchen' : 'kitchen',
                    'knavledge' : 'knowledge',
                    'knmvledge' : 'knowledge',
                    'knoAv' : 'know',
                    'knoAvlcdge' : 'knowledge',
                    'knoAvledgc' : 'knowledge',
                    'knoAvledge' : 'knowledge',
                    'kno\v' : 'know',
                    'kno\vledge' : 'knowledge',
                    'kno^v' : 'know',
                    'kno^vledge' : 'knowledge',
                    'knoavledge' : 'knowledge',
                    'knoiv' : 'know',
                    'knoivlcdge' : 'knowledge',
                    'knoivledgc' : 'knowledge',
                    'knoivledge' : 'knowledge',
                    'knorvledge' : 'knowledge',
                    'knosvledge' : 'knowledge',
                    'knotvledge' : 'knowledge',
                    'knov/ledge' : 'knowledge',
                    'knov^ledge' : 'knowledge',
                    'knovdedge' : 'knowledge',
                    'knovi^ledge' : 'knowledge',
                    'knoviledge' : 'knowledge',
                    'knovjledge' : 'knowledge',
                    'knovledge' : 'knowledge',
                    'knovrledge' : 'knowledge',
                    'knovv^ledge' : 'knowledge',
                    'knovvledge' : 'knowledge',
                    'knovyledge' : 'knowledge',
                    'know1edge' : 'knowledge',
                    'knowUdge' : 'knowledge',
                    'knowlcdge' : 'knowledge',
                    'knowledg^e' : 'knowledge',
                    'knowledgc' : 'knowledge',
                    'knoxvledge' : 'knowledge',
                    'knozvledge' : 'knowledge',
                    'kno»v' : 'know',
                    'kter^m' : 'term',
                    'kuoAvledge' : 'knowledge',
                    'kuow' : 'know',
                    'l)arty' : 'party',
                    'l)eople' : 'people',
                    'l)eriod' : 'period',
                    'l)lay' : 'play',
                    'l)oor' : 'poor',
                    'l)osition' : 'position',
                    'l)resent' : 'present',
                    'l)rivate' : 'private',
                    'l)roperty' : 'property',
                    'l)ublic' : 'public',
                    'l)urpose' : 'purpose',
                    'l0cal' : 'local',
                    'l0ng' : 'long',
                    'l0ss' : 'loss',
                    'l0ve' : 'love',
                    'l1fe' : 'life',
                    'l1ght' : 'light',
                    'l1ke' : 'like',
                    'l1kely' : 'likely',
                    'l1ne' : 'line',
                    'l1st' : 'list',
                    'l1ttle' : 'little',
                    'l1ve' : 'live',
                    'l6ft' : 'left',
                    'l6ng' : 'long',
                    'l6ss' : 'less',
                    'l6ve' : 'love',
                    'lOv' : 'low',
                    'l^and' : 'land',
                    'l^ast' : 'last',
                    'l^ate' : 'late',
                    'l^aw' : 'law',
                    'l^ay' : 'lay',
                    'l^eg' : 'leg',
                    'l^et' : 'let',
                    'l^etter' : 'letter',
                    'l^ie' : 'lie',
                    'l^ife' : 'life',
                    'l^ike' : 'like',
                    'l^ine' : 'line',
                    'l^ive' : 'live',
                    'l^ong' : 'long',
                    'l^ook' : 'look',
                    'l^ot' : 'lot',
                    'l^ove' : 'love',
                    'l^ow' : 'low',
                    'la3t' : 'last',
                    'la8t' : 'last',
                    'laAv' : 'law',
                    'laAvyer' : 'lawyer',
                    'la\vyer' : 'lawyer',
                    'la^vyer' : 'lawyer',
                    'lafe' : 'safe',
                    'lafft' : 'last',
                    'laft' : 'last',
                    'laige' : 'large',
                    'laiv' : 'law',
                    'laivyer' : 'lawyer',
                    'lale' : 'late',
                    'lamily' : 'family',
                    'lan3' : 'land',
                    'langh' : 'laugh',
                    'langnage' : 'language',
                    'languagc' : 'language',
                    'lar9e' : 'large',
                    'larg^e' : 'large',
                    'largc' : 'large',
                    'latc' : 'late',
                    'latcr' : 'later',
                    'latei' : 'later',
                    'laugb' : 'laugh',
                    'laugli' : 'laugh',
                    'lawjer' : 'lawyer',
                    'lawver' : 'lawyer',
                    'laſi' : 'last',
                    'laſl' : 'last',
                    'lcad' : 'lead',
                    'lcader' : 'leader',
                    'lcaft' : 'least',
                    'lcarn' : 'learn',
                    'lcast' : 'least',
                    'lcave' : 'leave',
                    'lcene' : 'scene',
                    'lcft' : 'left',
                    'lchool' : 'school',
                    'lcience' : 'science',
                    'lcss' : 'less',
                    'lcttcr' : 'letter',
                    'lctter' : 'letter',
                    'lcvel' : 'level',
                    'ldentify' : 'identify',
                    'le9al' : 'legal',
                    'leadcr' : 'leader',
                    'leafl' : 'least',
                    'leaft' : 'least',
                    'leait' : 'least',
                    'lealt' : 'least',
                    'learu' : 'learn',
                    'leason' : 'season',
                    'leav^e' : 'leave',
                    'leavc' : 'leave',
                    'leaye' : 'leave',
                    'leaſl' : 'least',
                    'lecond' : 'second',
                    'lecurity' : 'security',
                    'leff' : 'less',
                    'leffs' : 'less',
                    'lefl' : 'left',
                    'lefs' : 'less',
                    'lega1' : 'legal',
                    'legai' : 'legal',
                    'lell' : 'tell',
                    'lenior' : 'senior',
                    'lerious' : 'serious',
                    'lerve' : 'serve',
                    'lervice' : 'service',
                    'les3' : 'less',
                    'les8' : 'less',
                    'lesf' : 'less',
                    'lettcr' : 'letter',
                    'lettei' : 'letter',
                    'levcl' : 'level',
                    'leve1' : 'level',
                    'levei' : 'level',
                    'leveral' : 'several',
                    'leyel' : 'level',
                    'leﬁ' : 'left',
                    'lftter' : 'letter',
                    'lhake' : 'shake',
                    'lhan' : 'than',
                    'lhare' : 'share',
                    'lhat' : 'that',
                    'lheir' : 'their',
                    'lhem' : 'them',
                    'lhey' : 'they',
                    'lhoot' : 'shoot',
                    'lhort' : 'short',
                    'lhot' : 'shot',
                    'lhould' : 'should',
                    'lhoulder' : 'shoulder',
                    'lhow' : 'show',
                    'li3t' : 'list',
                    'li8t' : 'list',
                    'liaVe' : 'have',
                    'lia\e' : 'leave',
                    'liair' : 'hair',
                    'lialf' : 'half',
                    'liand' : 'hand',
                    'liang' : 'hang',
                    'liappen' : 'happen',
                    'liappy' : 'happy',
                    'liav' : 'have',
                    'liave' : 'have',
                    'liead' : 'head',
                    'liealth' : 'health',
                    'liear' : 'hear',
                    'lieart' : 'heart',
                    'lieat' : 'heat',
                    'lieavy' : 'heavy',
                    'lielp' : 'help',
                    'liere' : 'here',
                    'lierself' : 'herself',
                    'lifc' : 'life',
                    'liflen' : 'listen',
                    'liftcn' : 'listen',
                    'liften' : 'listen',
                    'lig^ht' : 'light',
                    'ligbt' : 'light',
                    'ligiit' : 'light',
                    'liglit' : 'light',
                    'lignificant' : 'significant',
                    'liiftory' : 'history',
                    'liigh' : 'high',
                    'liim' : 'him',
                    'liimfelf' : 'himself',
                    'liimsclf' : 'himself',
                    'liimself' : 'himself',
                    'liis' : 'his',
                    'liistorv' : 'history',
                    'liistory' : 'history',
                    'likc' : 'like',
                    'likclv' : 'likely',
                    'likcly' : 'likely',
                    'likeiy' : 'likely',
                    'likelj' : 'likely',
                    'likelv' : 'likely',
                    'lilten' : 'listen',
                    'liltle' : 'little',
                    'limilar' : 'similar',
                    'limple' : 'simple',
                    'limself' : 'himself',
                    'lin3' : 'line',
                    'linal' : 'final',
                    'lince' : 'since',
                    'lingle' : 'single',
                    'liold' : 'hold',
                    'liome' : 'home',
                    'liope' : 'hope',
                    'liospital' : 'hospital',
                    'liotel' : 'hotel',
                    'lioufe' : 'house',
                    'liour' : 'hour',
                    'liouse' : 'house',
                    'liowever' : 'however',
                    'lirft' : 'first',
                    'lirst' : 'first',
                    'listcn' : 'listen',
                    'litt1e' : 'little',
                    'littic' : 'little',
                    'littie' : 'little',
                    'littlc' : 'little',
                    'lituation' : 'situation',
                    'liuge' : 'huge',
                    'liuman' : 'human',
                    'liundred' : 'hundred',
                    'liusband' : 'husband',
                    'liv^e' : 'live',
                    'livc' : 'live',
                    'liye' : 'live',
                    'llght' : 'light',
                    'llttie' : 'little',
                    'lmage' : 'image',
                    'lmall' : 'small',
                    'lmile' : 'smile',
                    'lmpact' : 'impact',
                    'lmportant' : 'important',
                    'lmprove' : 'improve',
                    'lncluding' : 'including',
                    'lncludlng' : 'including',
                    'lncrease' : 'increase',
                    'lndeed' : 'indeed',
                    'lndividual' : 'individual',
                    'lndustry' : 'industry',
                    'lnformation' : 'information',
                    'lnformatlon' : 'information',
                    'lnstead' : 'instead',
                    'lnstitution' : 'institution',
                    'lnterest' : 'interest',
                    'lnteresting' : 'interesting',
                    'lntereſt' : 'interest',
                    'lntereﬅ' : 'interest',
                    'lnternational' : 'international',
                    'lnto' : 'into',
                    'lnvestment' : 'investment',
                    'loAv' : 'low',
                    'loca1' : 'local',
                    'locai' : 'local',
                    'locial' : 'social',
                    'lociety' : 'society',
                    'loeal' : 'local',
                    'lofe' : 'lose',
                    'loff' : 'loss',
                    'loffe' : 'lose',
                    'loffs' : 'loss',
                    'lofs' : 'loss',
                    'loie' : 'lose',
                    'loiv' : 'low',
                    'loldier' : 'soldier',
                    'lomething' : 'something',
                    'lometimes' : 'sometimes',
                    'lon8' : 'long',
                    'lon9' : 'long',
                    'lorce' : 'force',
                    'los3' : 'loss',
                    'losf' : 'loss',
                    'loug' : 'long',
                    'lource' : 'source',
                    'louthern' : 'southern',
                    'lov^e' : 'love',
                    'lovc' : 'love',
                    'lpace' : 'space',
                    'lpeak' : 'speak',
                    'lpecial' : 'special',
                    'lpeech' : 'speech',
                    'lport' : 'sport',
                    'lpring' : 'spring',
                    'lrom' : 'from',
                    'lssue' : 'issue',
                    'ltage' : 'stage',
                    'ltand' : 'stand',
                    'ltate' : 'state',
                    'ltay' : 'stay',
                    'ltep' : 'step',
                    'ltil' : 'still',
                    'ltill' : 'still',
                    'ltock' : 'stock',
                    'ltop' : 'stop',
                    'ltrong' : 'strong',
                    'ltself' : 'itself',
                    'ltudy' : 'study',
                    'ltyle' : 'style',
                    'lubject' : 'subject',
                    'luccess' : 'success',
                    'luch' : 'such',
                    'luddenly' : 'suddenly',
                    'luffer' : 'suffer',
                    'lummer' : 'summer',
                    'lupport' : 'support',
                    'lurface' : 'surface',
                    'lystem' : 'system',
                    'm0dern' : 'modern',
                    'm0ney' : 'money',
                    'm0re' : 'more',
                    'm0st' : 'most',
                    'm1ddle' : 'middle',
                    'm1ght' : 'might',
                    'm1l1tary' : 'military',
                    'm1litary' : 'military',
                    'm1llion' : 'million',
                    'm1nute' : 'minute',
                    'm1ss' : 'miss',
                    'm1ss1on' : 'mission',
                    'm1ssion' : 'mission',
                    'm6dical' : 'medical',
                    'm6ment' : 'moment',
                    'm6ney' : 'money',
                    'm6rning' : 'morning',
                    'm6st' : 'most',
                    'm6ther' : 'mother',
                    'mUUon' : 'million',
                    'mUitary' : 'military',
                    'm^ake' : 'make',
                    'm^an' : 'man',
                    'm^any' : 'many',
                    'm^ay' : 'may',
                    'm^dicale' : 'medical',
                    'm^ore' : 'more',
                    'm^ost' : 'most',
                    'm^ust' : 'must',
                    'm^y' : 'my',
                    'macbine' : 'machine',
                    'machinc' : 'machine',
                    'magaz1ne' : 'magazine',
                    'magazinc' : 'magazine',
                    'maj^or' : 'major',
                    'major1ty' : 'majority',
                    'majoritv' : 'majority',
                    'makc' : 'make',
                    'maln' : 'main',
                    'managc' : 'manage',
                    'managcment' : 'management',
                    'managemcnt' : 'management',
                    'manv' : 'many',
                    'markcl' : 'market',
                    'markct' : 'market',
                    'marr1age' : 'marriage',
                    'marriagc' : 'marriage',
                    'marrlage' : 'marriage',
                    'matcrial' : 'material',
                    'mater1al' : 'material',
                    'materia1' : 'material',
                    'materiaU' : 'material',
                    'materiah' : 'material',
                    'mattcr' : 'matter',
                    'mavbe' : 'maybe',
                    'mayhe' : 'maybe',
                    'mcafurc' : 'measure',
                    'mcafure' : 'measure',
                    'mcan' : 'mean',
                    'mcasure' : 'measure',
                    'mccting' : 'meeting',
                    'mcdia' : 'media',
                    'mcdical' : 'medical',
                    'mcet' : 'meet',
                    'mceting' : 'meeting',
                    'mcflage' : 'message',
                    'mclhod' : 'method',
                    'mcmbcr' : 'member',
                    'mcmber' : 'member',
                    'mcmorv' : 'memory',
                    'mcmory' : 'memory',
                    'mcntion' : 'mention',
                    'mcthod' : 'method',
                    'mdeed' : 'indeed',
                    'meafurc' : 'measure',
                    'meafure' : 'measure',
                    'mealure' : 'measure',
                    'measurc' : 'measure',
                    'mect' : 'meet',
                    'mecting' : 'meeting',
                    'med1cal' : 'medical',
                    'medica1' : 'medical',
                    'medla' : 'media',
                    'meet1ng' : 'meeting',
                    'meetmg' : 'meeting',
                    'meffage' : 'message',
                    'meflage' : 'message',
                    'mefsage' : 'message',
                    'membcr' : 'member',
                    'memher' : 'member',
                    'memoiy' : 'memory',
                    'memorv' : 'memory',
                    'ment1on' : 'mention',
                    'mesfage' : 'message',
                    'meslage' : 'message',
                    'messagc' : 'message',
                    'metbod' : 'method',
                    'meth0d' : 'method',
                    'metliod' : 'method',
                    'miUion' : 'million',
                    'miUtary' : 'military',
                    'midd1e' : 'middle',
                    'middlc' : 'middle',
                    'midiUe' : 'middle',
                    'midtUe' : 'middle',
                    'miffion' : 'mission',
                    'miflion' : 'mission',
                    'mifs' : 'miss',
                    'mifsion' : 'mission',
                    'mig^ht' : 'might',
                    'migbt' : 'might',
                    'mighl' : 'might',
                    'miglit' : 'might',
                    'mihtary' : 'military',
                    'mil1ion' : 'million',
                    'mil1tary' : 'military',
                    'militaiy' : 'military',
                    'militarv' : 'military',
                    'minutc' : 'minute',
                    'misf' : 'miss',
                    'mislion' : 'mission',
                    'miss1on' : 'mission',
                    'miud' : 'mind',
                    'miuion' : 'million',
                    'miſlion' : 'mission',
                    'mlddle' : 'middle',
                    'mlght' : 'might',
                    'mlnd' : 'mind',
                    'mlss' : 'miss',
                    'mnsic' : 'music',
                    'modcl' : 'model',
                    'modcrn' : 'modern',
                    'mode1' : 'model',
                    'moft' : 'most',
                    'moie' : 'more',
                    'moit' : 'most',
                    'momcnt' : 'moment',
                    'moncy' : 'money',
                    'monev' : 'money',
                    'montb' : 'month',
                    'montli' : 'month',
                    'mor^e' : 'more',
                    'morc' : 'more',
                    'morn1ng' : 'morning',
                    'morniug' : 'morning',
                    'mornmg' : 'morning',
                    'moruing' : 'morning',
                    'mos^t' : 'most',
                    'motber' : 'mother',
                    'mothcr' : 'mother',
                    'mothei' : 'mother',
                    'motlier' : 'mother',
                    'mouey' : 'money',
                    'moutb' : 'mouth',
                    'moutli' : 'mouth',
                    'movc' : 'move',
                    'movcment' : 'movement',
                    'movemcnt' : 'movement',
                    'moſl' : 'most',
                    'mterest' : 'interest',
                    'muUion' : 'million',
                    'mucb' : 'much',
                    'mucli' : 'much',
                    'mueh' : 'much',
                    'mufft' : 'must',
                    'mufic' : 'music',
                    'muft' : 'must',
                    'mulic' : 'music',
                    'mus1c' : 'music',
                    'mus^t' : 'must',
                    'muslc' : 'music',
                    'muſl' : 'must',
                    'muﬁc' : 'music',
                    'mvfelf' : 'myself',
                    'mvsclf' : 'myself',
                    'mvself' : 'myself',
                    'myfclf' : 'myself',
                    'myfelf' : 'myself',
                    'myfell' : 'myself',
                    'mylelf' : 'myself',
                    'mysclf' : 'myself',
                    'mysell' : 'myself',
                    'myſelſ' : 'myself',
                    'n0rth' : 'north',
                    'n0te' : 'note',
                    'n1ce' : 'nice',
                    'n1ght' : 'night',
                    'n6rth' : 'north',
                    'n6thing' : 'nothing',
                    'n^ew' : 'new',
                    'n^ight' : 'night',
                    'n^o' : 'no',
                    'n^or' : 'nor',
                    'n^ot' : 'not',
                    'nam6' : 'name',
                    'nam^e' : 'name',
                    'namc' : 'name',
                    'nat1on' : 'nation',
                    'nat1onal' : 'national',
                    'nati0n' : 'nation',
                    'nati0nal' : 'national',
                    'nationa1' : 'national',
                    'natlon' : 'nation',
                    'natnral' : 'natural',
                    'natnre' : 'nature',
                    'natuie' : 'nature',
                    'natura1' : 'natural',
                    'naturaU' : 'natural',
                    'naturah' : 'natural',
                    'naturc' : 'nature',
                    'ncAvspaper' : 'newspaper',
                    'ncar' : 'near',
                    'ncarlv' : 'nearly',
                    'ncarly' : 'nearly',
                    'ncceffary' : 'necessary',
                    'ncceflary' : 'necessary',
                    'nccessarv' : 'necessary',
                    'nccessary' : 'necessary',
                    'nced' : 'need',
                    'ncver' : 'never',
                    'ncws' : 'news',
                    'ncwspaper' : 'newspaper',
                    'ncxt' : 'next',
                    'neAv' : 'new',
                    'neAvs' : 'news',
                    'neAvspaper' : 'newspaper',
                    'ne\vs' : 'news',
                    'ne^vs' : 'news',
                    'neai' : 'near',
                    'neaily' : 'nearly',
                    'near1y' : 'nearly',
                    'nearlv' : 'nearly',
                    'neccffary' : 'necessary',
                    'neccflary' : 'necessary',
                    'neccssarv' : 'necessary',
                    'neccssary' : 'necessary',
                    'necd' : 'need',
                    'necefary' : 'necessary',
                    'neceffary' : 'necessary',
                    'necefiary' : 'necessary',
                    'neceflarv' : 'necessary',
                    'neceflary' : 'necessary',
                    'necefsary' : 'necessary',
                    'necellary' : 'necessary',
                    'necelsary' : 'necessary',
                    'necesfary' : 'necessary',
                    'neceslary' : 'necessary',
                    'necessaiy' : 'necessary',
                    'necessarv' : 'necessary',
                    'neceſlary' : 'necessary',
                    'neceﬁary' : 'necessary',
                    'neier' : 'never',
                    'neiv' : 'new',
                    'neivspaper' : 'newspaper',
                    'nev/s' : 'news',
                    'nevS' : 'news',
                    'nev^er' : 'never',
                    'nevcr' : 'never',
                    'nevei' : 'never',
                    'nevs' : 'news',
                    'newf' : 'news',
                    'newfpaper' : 'newspaper',
                    'newl' : 'news',
                    'news])aper' : 'newspaper',
                    'newsi)aper' : 'newspaper',
                    'newsj)aper' : 'newspaper',
                    'newspa])er' : 'newspaper',
                    'newspai)er' : 'newspaper',
                    'newspaj)er' : 'newspaper',
                    'nicc' : 'nice',
                    'nig^ht' : 'night',
                    'nigbt' : 'night',
                    'niglit' : 'night',
                    'niimher' : 'number',
                    'nlce' : 'nice',
                    'nlght' : 'night',
                    'nnder' : 'under',
                    'nntil' : 'until',
                    'noith' : 'north',
                    'noiv' : 'now',
                    'non6' : 'none',
                    'nonc' : 'none',
                    'norlh' : 'north',
                    'nortb' : 'north',
                    'nortli' : 'north',
                    'not1ce' : 'notice',
                    'not6' : 'note',
                    'not^e' : 'note',
                    'notbing' : 'nothing',
                    'notbyng' : 'nothing',
                    'notc' : 'note',
                    'noth1ng' : 'nothing',
                    'nothiug' : 'nothing',
                    'nothlng' : 'nothing',
                    'nothmg' : 'nothing',
                    'noticc' : 'notice',
                    'notlce' : 'notice',
                    'notliing' : 'nothing',
                    'nuinher' : 'number',
                    'numbcr' : 'number',
                    'numbei' : 'number',
                    'numher' : 'number',
                    'nund^er' : 'under',
                    'nvithout' : 'without',
                    'oAvn' : 'own',
                    'oAvner' : 'owner',
                    'oUong' : 'along',
                    'o[)en' : 'open',
                    'o\vner' : 'owner',
                    'o])en' : 'open',
                    'o])portunity' : 'opportunity',
                    'o^il' : 'oil',
                    'o^ne' : 'one',
                    'o^this' : 'this',
                    'o^ur' : 'our',
                    'o^ut' : 'out',
                    'o^ver' : 'over',
                    'o^vner' : 'owner',
                    'o^wn' : 'own',
                    'of)en' : 'open',
                    'of^all' : 'fall',
                    'of^f' : 'off',
                    'of^our' : 'four',
                    'off1ce' : 'office',
                    'off1cer' : 'officer',
                    'off1cial' : 'official',
                    'off^er' : 'offer',
                    'offcr' : 'offer',
                    'offic1al' : 'official',
                    'officc' : 'office',
                    'officcr' : 'officer',
                    'offlce' : 'office',
                    'offlcer' : 'officer',
                    'offlcial' : 'official',
                    'offﬁce' : 'office',
                    'oflen' : 'often',
                    'ofler' : 'offer',
                    'oflice' : 'office',
                    'oflicer' : 'officer',
                    'oflicial' : 'official',
                    'oftcn' : 'often',
                    'ofteu' : 'often',
                    'ofﬁcc' : 'office',
                    'ofﬁccr' : 'officer',
                    'ofﬁee' : 'office',
                    'ofﬁeer' : 'officer',
                    'ofﬁre' : 'office',
                    'ofﬁve' : 'office',
                    'oi)en' : 'open',
                    'oi)eration' : 'operation',
                    'oiU' : 'oil',
                    'oiher' : 'other',
                    'oihers' : 'others',
                    'oiiU' : 'oil',
                    'oiten' : 'often',
                    'oivn' : 'own',
                    'oivner' : 'owner',
                    'oj)en' : 'open',
                    'oj)eration' : 'operation',
                    'oj)portunity' : 'opportunity',
                    'ol)en' : 'open',
                    'olﬁce' : 'office',
                    'olﬁcer' : 'officer',
                    'olﬁcial' : 'official',
                    'on1y' : 'only',
                    'on^ce' : 'once',
                    'on^e' : 'one',
                    'onc6' : 'once',
                    'oncc' : 'once',
                    'onhy' : 'only',
                    'onlv' : 'only',
                    'op6n' : 'open',
                    'op6ration' : 'operation',
                    'op[)ortunity' : 'opportunity',
                    'op])ortunity' : 'opportunity',
                    'opcn' : 'open',
                    'opcration' : 'operation',
                    'operat1on' : 'operation',
                    'opeu' : 'open',
                    'opj)ortunity' : 'opportunity',
                    'opportun1ty' : 'opportunity',
                    'opportunitv' : 'opportunity',
                    'op|)ortunity' : 'opportunity',
                    'ordcr' : 'order',
                    'otber' : 'other',
                    'otbers' : 'others',
                    'otb«r' : 'other',
                    'oth6r' : 'other',
                    'oth^er' : 'other',
                    'othcr' : 'other',
                    'othcrs' : 'others',
                    'othei' : 'other',
                    'otheis' : 'others',
                    'other^s' : 'others',
                    'otherf' : 'others',
                    'otherl' : 'others',
                    'otlier' : 'other',
                    'otliers' : 'others',
                    'otﬁce' : 'office',
                    'otﬁcer' : 'officer',
                    'otﬁcial' : 'official',
                    'ouly' : 'only',
                    'outfidc' : 'outside',
                    'outfide' : 'outside',
                    'outlide' : 'outside',
                    'outﬁde' : 'outside',
                    'ov/ner' : 'owner',
                    'ov6r' : 'over',
                    'ov^er' : 'over',
                    'ovcr' : 'over',
                    'ovei' : 'over',
                    'ovner' : 'owner',
                    'owncr' : 'owner',
                    'o|)en' : 'open',
                    'oſfer' : 'offer',
                    'oſﬁce' : 'office',
                    'oﬁen' : 'often',
                    'oﬁfer' : 'offer',
                    'oﬁﬁcer' : 'officer',
                    'oﬂﬁce' : 'office',
                    'p0int' : 'point',
                    'p0licy' : 'policy',
                    'p0litical' : 'political',
                    'p0pulati0n' : 'population',
                    'p0pulation' : 'population',
                    'p0wer' : 'power',
                    'p1ace' : 'place',
                    'p1ay' : 'play',
                    'p1cture' : 'picture',
                    'p6or' : 'poor',
                    'p6ssible' : 'possible',
                    'p6wer' : 'power',
                    'pOAver' : 'power',
                    'p^er' : 'per',
                    'paff' : 'pass',
                    'pafl' : 'pass',
                    'pafs' : 'pass',
                    'paft' : 'past',
                    'pag6' : 'page',
                    'pagc' : 'page',
                    'pahice' : 'police',
                    'pai)er' : 'paper',
                    'paint1ng' : 'painting',
                    'paity' : 'party',
                    'paiu' : 'pain',
                    'paj)er' : 'paper',
                    'paln' : 'pain',
                    'papcr' : 'paper',
                    'papei' : 'paper',
                    'parcnt' : 'parent',
                    'part1cular' : 'particular',
                    'part1cularly' : 'particularly',
                    'particiUar' : 'particular',
                    'particu1ar' : 'particular',
                    'particuhir' : 'particular',
                    'particuhirly' : 'particularly',
                    'particulai' : 'particular',
                    'particularlv' : 'particularly',
                    'partncr' : 'partner',
                    'partv' : 'party',
                    'pasf' : 'pass',
                    'paticnt' : 'patient',
                    'pbysical' : 'physical',
                    'pcace' : 'peace',
                    'pcoplc' : 'people',
                    'pcople' : 'people',
                    'pcrfon' : 'person',
                    'pcrfonal' : 'personal',
                    'pcrform' : 'perform',
                    'pcrformance' : 'performance',
                    'pcrhaps' : 'perhaps',
                    'pcriod' : 'period',
                    'pcrson' : 'person',
                    'pcrsonal' : 'personal',
                    'peacc' : 'peace',
                    'peciall' : 'special',
                    'peihaps' : 'perhaps',
                    'peiiod' : 'period',
                    'peison' : 'person',
                    'peo2)le' : 'people',
                    'peoi)le' : 'people',
                    'peoj)le' : 'people',
                    'peop1e' : 'people',
                    'peoplc' : 'people',
                    'per10d' : 'period',
                    'per1od' : 'period',
                    'perbaps' : 'perhaps',
                    'perfon' : 'person',
                    'perfonal' : 'personal',
                    'performancc' : 'performance',
                    'perha[)s' : 'perhaps',
                    'perha])S' : 'perhaps',
                    'perha])s' : 'perhaps',
                    'perhai)S' : 'perhaps',
                    'perhai)s' : 'perhaps',
                    'perhaj)S' : 'perhaps',
                    'perhaj)s' : 'perhaps',
                    'perhapf' : 'perhaps',
                    'perha|)s' : 'perhaps',
                    'perliaps' : 'perhaps',
                    'perlonal' : 'personal',
                    'pers0n' : 'person',
                    'pers0nal' : 'personal',
                    'pers6n' : 'person',
                    'persona1' : 'personal',
                    'persou' : 'person',
                    'phace' : 'place',
                    'phvsical' : 'physical',
                    'phyfical' : 'physical',
                    'phylical' : 'physical',
                    'phys1cal' : 'physical',
                    'physica1' : 'physical',
                    'phyﬁcal' : 'physical',
                    'picce' : 'piece',
                    'piclure' : 'picture',
                    'picturc' : 'picture',
                    'pidlure' : 'picture',
                    'pidture' : 'picture',
                    'pidure' : 'picture',
                    'piecc' : 'piece',
                    'piesent' : 'present',
                    'pifture' : 'picture',
                    'piihlic' : 'public',
                    'plac6' : 'place',
                    'placc' : 'place',
                    'plaver' : 'player',
                    'plece' : 'piece',
                    'pnblic' : 'public',
                    'pnrpose' : 'purpose',
                    'po1icy' : 'policy',
                    'po1itical' : 'political',
                    'poAvcr' : 'power',
                    'poUcy' : 'policy',
                    'poUtical' : 'political',
                    'poUtics' : 'politics',
                    'po\ver' : 'power',
                    'po])ulation' : 'population',
                    'po^ver' : 'power',
                    'pof1tion' : 'position',
                    'poffiblc' : 'possible',
                    'poffible' : 'possible',
                    'poffihle' : 'possible',
                    'pofiible' : 'possible',
                    'pofition' : 'position',
                    'pofitivc' : 'positive',
                    'pofitive' : 'positive',
                    'pofliblc' : 'possible',
                    'poflible' : 'possible',
                    'pofsible' : 'possible',
                    'pohce' : 'police',
                    'pohcy' : 'policy',
                    'pohtical' : 'political',
                    'pohtics' : 'politics',
                    'poi)ular' : 'popular',
                    'poi)ulation' : 'population',
                    'poiut' : 'point',
                    'poiver' : 'power',
                    'poj)ular' : 'popular',
                    'poj)ulation' : 'population',
                    'pol1ce' : 'police',
                    'pol1cy' : 'policy',
                    'pol1t1cal' : 'political',
                    'pol1t1cs' : 'politics',
                    'pol1tical' : 'political',
                    'pol1tics' : 'politics',
                    'policc' : 'police',
                    'policv' : 'policy',
                    'polit1cal' : 'political',
                    'polit1cs' : 'politics',
                    'politica1' : 'political',
                    'politiche' : 'political',
                    'polition' : 'position',
                    'politive' : 'positive',
                    'pollible' : 'possible',
                    'polnt' : 'point',
                    'pomt' : 'point',
                    'popiUar' : 'popular',
                    'popu1ation' : 'population',
                    'popuhition' : 'population',
                    'populat1on' : 'population',
                    'pos1tion' : 'position',
                    'pos1tive' : 'positive',
                    'posfible' : 'possible',
                    'posit1on' : 'position',
                    'posit1ve' : 'positive',
                    'positivc' : 'positive',
                    'poslible' : 'possible',
                    'poss1ble' : 'possible',
                    'possib1e' : 'possible',
                    'possiblc' : 'possible',
                    'possihie' : 'possible',
                    'possihle' : 'possible',
                    'pov/er' : 'power',
                    'pov^er' : 'power',
                    'pover' : 'power',
                    'powcr' : 'power',
                    'powei' : 'power',
                    'poſlible' : 'possible',
                    'poﬁible' : 'possible',
                    'poﬁtion' : 'position',
                    'poﬁtive' : 'positive',
                    'pr0blem' : 'problem',
                    'pr0gram' : 'program',
                    'pr0perty' : 'property',
                    'pr1ce' : 'price',
                    'pr1vate' : 'private',
                    'pr6sent' : 'present',
                    'pr6sident' : 'president',
                    'praclice' : 'practice',
                    'pract1ce' : 'practice',
                    'practicc' : 'practice',
                    'pradice' : 'practice',
                    'pradlice' : 'practice',
                    'pradtice' : 'practice',
                    'praftice' : 'practice',
                    'pra£lice' : 'practice',
                    'pra£tice' : 'practice',
                    'prcfcnt' : 'present',
                    'prcfent' : 'present',
                    'prcfident' : 'president',
                    'prcflure' : 'pressure',
                    'prcscnt' : 'present',
                    'prcsent' : 'present',
                    'prcsidcnt' : 'president',
                    'prcsident' : 'president',
                    'prcssure' : 'pressure',
                    'prctty' : 'pretty',
                    'prcvent' : 'prevent',
                    'pref1dent' : 'president',
                    'prefcnt' : 'present',
                    'prefent' : 'present',
                    'preffure' : 'pressure',
                    'prefidcnt' : 'president',
                    'prefident' : 'president',
                    'preflurc' : 'pressure',
                    'preflure' : 'pressure',
                    'prefsure' : 'pressure',
                    'preient' : 'present',
                    'prelent' : 'present',
                    'prelident' : 'president',
                    'prepar6' : 'prepare',
                    'pres1dent' : 'president',
                    'prescnt' : 'present',
                    'preseut' : 'present',
                    'presidcnt' : 'president',
                    'pressurc' : 'pressure',
                    'prettv' : 'pretty',
                    'preﬁdent' : 'president',
                    'pricc' : 'price',
                    'priv^ate' : 'private',
                    'privatc' : 'private',
                    'pro[)erty' : 'property',
                    'pro])erty' : 'property',
                    'probablv' : 'probably',
                    'probahlv' : 'probably',
                    'probahly' : 'probably',
                    'proccfs' : 'process',
                    'proccss' : 'process',
                    'procefs' : 'process',
                    'procels' : 'process',
                    'producc' : 'produce',
                    'producl' : 'product',
                    'produclion' : 'production',
                    'product1on' : 'production',
                    'produd' : 'product',
                    'produdion' : 'production',
                    'produdl' : 'product',
                    'produdt' : 'product',
                    'produdtion' : 'production',
                    'produft' : 'product',
                    'produftion' : 'production',
                    'profcssor' : 'professor',
                    'profeffional' : 'professional',
                    'profeffor' : 'professor',
                    'profeflional' : 'professional',
                    'profeflor' : 'professor',
                    'professiona1' : 'professional',
                    'prohablv' : 'probably',
                    'prohably' : 'probably',
                    'prohahly' : 'probably',
                    'prohlem' : 'problem',
                    'proi)erty' : 'property',
                    'proj)erty' : 'property',
                    'projecl' : 'project',
                    'projed' : 'project',
                    'projedl' : 'project',
                    'projedt' : 'project',
                    'projeft' : 'project',
                    'propcrtv' : 'property',
                    'propcrty' : 'property',
                    'propertv' : 'property',
                    'protecl' : 'protect',
                    'proted' : 'protect',
                    'protedl' : 'protect',
                    'protedt' : 'protect',
                    'prov1de' : 'provide',
                    'provc' : 'prove',
                    'providc' : 'provide',
                    'pro|)erty' : 'property',
                    'proſeſſor' : 'professor',
                    'pub1ic' : 'public',
                    'pubUc' : 'public',
                    'pubhc' : 'public',
                    'publ1c' : 'public',
                    'pufh' : 'push',
                    'pufli' : 'push',
                    'puhlic' : 'public',
                    'puipose' : 'purpose',
                    'pur[)ose' : 'purpose',
                    'pur])ose' : 'purpose',
                    'puri)ose' : 'purpose',
                    'purj)ose' : 'purpose',
                    'purp0se' : 'purpose',
                    'purpofc' : 'purpose',
                    'purpofe' : 'purpose',
                    'purpole' : 'purpose',
                    'purposc' : 'purpose',
                    'pur|)ose' : 'purpose',
                    'pusb' : 'push',
                    'q)on' : 'upon',
                    'q^uality' : 'quality',
                    'q^uestion' : 'question',
                    'q^uickly' : 'quickly',
                    'q^uite' : 'quite',
                    'qiiaUty' : 'quality',
                    'qiiahty' : 'quality',
                    'qnaUty' : 'quality',
                    'qnestion' : 'question',
                    'quUUty' : 'quality',
                    'qua1ity' : 'quality',
                    'quaUte' : 'quality',
                    'quaUty' : 'quality',
                    'quahty' : 'quality',
                    'quaiUity' : 'quality',
                    'qual1ty' : 'quality',
                    'qualitv' : 'quality',
                    'qualiſy' : 'quality',
                    'quanUty' : 'quality',
                    'qucflion' : 'question',
                    'qucftion' : 'question',
                    'qucstion' : 'question',
                    'queflion' : 'question',
                    'queftion' : 'question',
                    'queltion' : 'question',
                    'ques^tion' : 'question',
                    'quest1on' : 'question',
                    'questi0n' : 'question',
                    'questi6n' : 'question',
                    'questiou' : 'question',
                    'questlon' : 'question',
                    'quetlion' : 'question',
                    'queſiion' : 'question',
                    'queſlion' : 'question',
                    'queﬁion' : 'question',
                    'quiUity' : 'quality',
                    'quicUy' : 'quickly',
                    'quickhy' : 'quickly',
                    'quicklv' : 'quickly',
                    'quitc' : 'quite',
                    'quiæ' : 'quite',
                    'qulckly' : 'quickly',
                    'qulte' : 'quite',
                    'qwhiUe' : 'while',
                    'qﬁicial' : 'official',
                    'r/hich' : 'which',
                    'r0ad' : 'road',
                    'r0le' : 'role',
                    'r1ch' : 'rich',
                    'r1ght' : 'right',
                    'r1se' : 'rise',
                    'r6al' : 'real',
                    'r6gion' : 'region',
                    'r6le' : 'role',
                    'r6om' : 'room',
                    'rUBLIC' : 'public',
                    'r^ed' : 'red',
                    'raUways' : 'always',
                    'racc' : 'race',
                    'raife' : 'raise',
                    'raile' : 'raise',
                    'raisc' : 'raise',
                    'ralher' : 'rather',
                    'ralse' : 'raise',
                    'rang6' : 'range',
                    'rangc' : 'range',
                    'ratber' : 'rather',
                    'ratc' : 'rate',
                    'rathcr' : 'rather',
                    'rathei' : 'rather',
                    'ratlier' : 'rather',
                    'rcach' : 'reach',
                    'rcad' : 'read',
                    'rcady' : 'ready',
                    'rcafon' : 'reason',
                    'rcal' : 'real',
                    'rcalitv' : 'reality',
                    'rcality' : 'reality',
                    'rcalize' : 'realize',
                    'rcallv' : 'really',
                    'rcally' : 'really',
                    'rcason' : 'reason',
                    'rcceive' : 'receive',
                    'rccent' : 'recent',
                    'rccently' : 'recently',
                    'rcfource' : 'resource',
                    'rcfult' : 'result',
                    'rcgion' : 'region',
                    'rclationship' : 'relationship',
                    'rcligious' : 'religious',
                    'rclurn' : 'return',
                    'rcmain' : 'remain',
                    'rcmember' : 'remember',
                    'rcmove' : 'remove',
                    'rcport' : 'report',
                    'rcprefent' : 'represent',
                    'rcpresent' : 'represent',
                    'rcst' : 'rest',
                    'rcsult' : 'result',
                    'rcturn' : 'return',
                    'rcveal' : 'reveal',
                    're1ationship' : 'relationship',
                    're1igious' : 'religious',
                    'reUgioun' : 'religious',
                    'reUgious' : 'religious',
                    're[)ort' : 'report',
                    're])ort' : 'report',
                    're])resent' : 'represent',
                    'rea1' : 'real',
                    'reaU' : 'real',
                    'reaUy' : 'really',
                    'reaUze' : 'realize',
                    'reacb' : 'reach',
                    'reacli' : 'reach',
                    'readUy' : 'really',
                    'readv' : 'ready',
                    'reaffon' : 'reason',
                    'reafon' : 'reason',
                    'reah' : 'real',
                    'reahty' : 'reality',
                    'reahze' : 'realize',
                    'real1ty' : 'reality',
                    'realitv' : 'reality',
                    'realizc' : 'realize',
                    'reallv' : 'really',
                    'realon' : 'reason',
                    'reas6n' : 'reason',
                    'reasou' : 'reason',
                    'reccive' : 'receive',
                    'reccnt' : 'recent',
                    'reccntly' : 'recently',
                    'rece1ve' : 'receive',
                    'receiie' : 'receive',
                    'receiv^e' : 'receive',
                    'receivc' : 'receive',
                    'recelve' : 'receive',
                    'recentlv' : 'recently',
                    'recognizc' : 'recognize',
                    'reducc' : 'reduce',
                    'refearch' : 'research',
                    'reffource' : 'resource',
                    'refl' : 'rest',
                    'reflecl' : 'reflect',
                    'refledl' : 'reflect',
                    'refledt' : 'reflect',
                    'refleft' : 'reflect',
                    'refourcc' : 'resource',
                    'refource' : 'resource',
                    'refpond' : 'respond',
                    'refponfe' : 'response',
                    'refponfibility' : 'responsibility',
                    'refult' : 'result',
                    'reg1on' : 'region',
                    'regi6n' : 'region',
                    'rehgious' : 'religious',
                    'rei)resent' : 'represent',
                    'rej)ort' : 'report',
                    'rej)resent' : 'represent',
                    'rel1g1ous' : 'religious',
                    'rel1gious' : 'religious',
                    'relat1onsh1p' : 'relationship',
                    'relat1onship' : 'relationship',
                    'relati0nship' : 'relationship',
                    'relationfhip' : 'relationship',
                    'relationsbip' : 'relationship',
                    'relationsh1p' : 'relationship',
                    'relig1ous' : 'religious',
                    'religi0us' : 'religious',
                    'relt' : 'rest',
                    'relult' : 'result',
                    'remaln' : 'remain',
                    'remam' : 'remain',
                    'remcmber' : 'remember',
                    'remembcr' : 'remember',
                    'rememher' : 'remember',
                    'rep0rt' : 'report',
                    'reponfe' : 'response',
                    'reprcfent' : 'represent',
                    'reprcsent' : 'represent',
                    'reprefcnt' : 'represent',
                    'reprefent' : 'represent',
                    'reprelent' : 'represent',
                    'represcnt' : 'represent',
                    'requirc' : 'require',
                    'requlre' : 'require',
                    'rescarch' : 'research',
                    'researcb' : 'research',
                    'resi)onsibility' : 'responsibility',
                    'responsibUity' : 'responsibility',
                    'responsibiUty' : 'responsibility',
                    'responsibihty' : 'responsibility',
                    'responsibilitv' : 'responsibility',
                    'responsihility' : 'responsibility',
                    'resuUs' : 'result',
                    'retnrn' : 'return',
                    'revcal' : 'reveal',
                    'revea1' : 'reveal',
                    're|)ort' : 'report',
                    'reſi' : 'rest',
                    'reſl' : 'rest',
                    'reſo' : 'rest',
                    'ricb' : 'rich',
                    'ricli' : 'rich',
                    'rifk' : 'risk',
                    'rig^ht' : 'right',
                    'rigbt' : 'right',
                    'righl' : 'right',
                    'riglit' : 'right',
                    'rlch' : 'rich',
                    'rlght' : 'right',
                    'rlse' : 'rise',
                    'rnle' : 'rule',
                    'ro])erty' : 'property',
                    'rolc' : 'role',
                    'ru1e' : 'rule',
                    'rulc' : 'rule',
                    'rvithout' : 'without',
                    's00n' : 'soon',
                    's0cial' : 'social',
                    's0ciety' : 'society',
                    's0me' : 'some',
                    's0on' : 'soon',
                    's0und' : 'sound',
                    's0uth' : 'south',
                    's1de' : 'side',
                    's1milar' : 'similar',
                    's1mply' : 'simply',
                    's1nce' : 'since',
                    's1ng' : 'sing',
                    's1ngle' : 'single',
                    's1ster' : 'sister',
                    's1te' : 'site',
                    's1tuation' : 'situation',
                    's6cial' : 'social',
                    's6metimes' : 'sometimes',
                    's6on' : 'soon',
                    's6uth' : 'south',
                    's^ave' : 'save',
                    's^ay' : 'say',
                    's^ee' : 'see',
                    's^et' : 'set',
                    's^it' : 'sit',
                    's^on' : 'son',
                    'safc' : 'safe',
                    'sam6' : 'same',
                    'samc' : 'same',
                    'savc' : 'save',
                    'sbake' : 'shake',
                    'sbare' : 'share',
                    'sboot' : 'shoot',
                    'sbort' : 'short',
                    'sbot' : 'shot',
                    'sbould' : 'should',
                    'sboulder' : 'shoulder',
                    'sbow' : 'show',
                    'scafon' : 'season',
                    'scason' : 'season',
                    'scclion' : 'section',
                    'sccm' : 'seem',
                    'schoo1' : 'school',
                    'schooU' : 'school',
                    'schooh' : 'school',
                    'scicncc' : 'science',
                    'scicnce' : 'science',
                    'sciencc' : 'science',
                    'sclence' : 'science',
                    'scll' : 'sell',
                    'scnd' : 'send',
                    'scnior' : 'senior',
                    'scnse' : 'sense',
                    'scorc' : 'score',
                    'scrious' : 'serious',
                    'scrve' : 'serve',
                    'scrvicc' : 'service',
                    'scrvice' : 'service',
                    'scvcral' : 'several',
                    'scven' : 'seven',
                    'scveral' : 'several',
                    'seafon' : 'season',
                    'sec0nd' : 'second',
                    'sec6nd' : 'second',
                    'seclion' : 'section',
                    'secm' : 'seem',
                    'secoud' : 'second',
                    'sect10n' : 'section',
                    'sect1on' : 'section',
                    'secti0n' : 'section',
                    'secur1ty' : 'security',
                    'securitv' : 'security',
                    'sedion' : 'section',
                    'sedtion' : 'section',
                    'seftion' : 'section',
                    'sel1' : 'sell',
                    'sen1or' : 'senior',
                    'senfe' : 'sense',
                    'senle' : 'sense',
                    'sens6' : 'sense',
                    'sensc' : 'sense',
                    'ser1es' : 'series',
                    'ser1ous' : 'serious',
                    'serics' : 'series',
                    'serles' : 'series',
                    'serv1ce' : 'service',
                    'serv^e' : 'serve',
                    'servc' : 'serve',
                    'servicc' : 'service',
                    'seud' : 'send',
                    'seuse' : 'sense',
                    'sev^eral' : 'several',
                    'sevcn' : 'seven',
                    'sevcral' : 'several',
                    'seveial' : 'several',
                    'severa1' : 'several',
                    'severaU' : 'several',
                    'sh00t' : 'shoot',
                    'sh0rt' : 'short',
                    'sh0uld' : 'should',
                    'sh6rt' : 'short',
                    'sh6uld' : 'should',
                    'sharc' : 'share',
                    'shoAv' : 'show',
                    'sho\v' : 'show',
                    'shoiUd' : 'should',
                    'shoit' : 'short',
                    'shoiv' : 'show',
                    'shonld' : 'should',
                    'shou1d' : 'should',
                    'shouldcr' : 'shoulder',
                    'shov' : 'show',
                    'si)ecial' : 'special',
                    'si)eech' : 'speech',
                    'siate' : 'state',
                    'sid6' : 'side',
                    'sidc' : 'side',
                    'sifler' : 'sister',
                    'signif1cant' : 'significant',
                    'signiflcant' : 'significant',
                    'sigu' : 'sign',
                    'siihject' : 'subject',
                    'silter' : 'sister',
                    'sim1lar' : 'similar',
                    'simUar' : 'similar',
                    'simi1ar' : 'similar',
                    'simj)le' : 'simple',
                    'simj)ly' : 'simply',
                    'simplc' : 'simple',
                    'simplv' : 'simply',
                    'sincc' : 'since',
                    'sing1e' : 'single',
                    'singlc' : 'single',
                    'sistcr' : 'sister',
                    'situat1on' : 'situation',
                    'siuce' : 'since',
                    'sizc' : 'size',
                    'sj)ace' : 'space',
                    'sj)eak' : 'speak',
                    'sj)ecial' : 'special',
                    'sj)eech' : 'speech',
                    'sj)ring' : 'spring',
                    'sk1ll' : 'skill',
                    'sk1n' : 'skin',
                    'skiU' : 'skill',
                    'skil1' : 'skill',
                    'skiu' : 'skin',
                    'skm' : 'skin',
                    'slde' : 'side',
                    'sliare' : 'share',
                    'slie' : 'she',
                    'slill' : 'still',
                    'sliort' : 'short',
                    'sliot' : 'shot',
                    'sliould' : 'should',
                    'sliow' : 'show',
                    'slnce' : 'since',
                    'slng' : 'sing',
                    'slock' : 'stock',
                    'slory' : 'story',
                    'slte' : 'site',
                    'slze' : 'size',
                    'smaU' : 'small',
                    'smal1' : 'small',
                    'smau' : 'small',
                    'smce' : 'since',
                    'smg' : 'sing',
                    'smgle' : 'single',
                    'snbject' : 'subject',
                    'snch' : 'such',
                    'snre' : 'sure',
                    'soc1al' : 'social',
                    'soc1ety' : 'society',
                    'socia1' : 'social',
                    'socicly' : 'society',
                    'socictv' : 'society',
                    'socicty' : 'society',
                    'societv' : 'society',
                    'socifty' : 'society',
                    'soldicr' : 'soldier',
                    'soldler' : 'soldier',
                    'som6' : 'some',
                    'som^e' : 'some',
                    'somc' : 'some',
                    'somcthing' : 'something',
                    'somctimes' : 'sometimes',
                    'somebodv' : 'somebody',
                    'somehody' : 'somebody',
                    'somet1mes' : 'sometimes',
                    'sometbing' : 'something',
                    'somethmg' : 'something',
                    'sometimcs' : 'sometimes',
                    'sometliing' : 'something',
                    'soug' : 'song',
                    'soulh' : 'south',
                    'sourcc' : 'source',
                    'soutb' : 'south',
                    'soutbern' : 'southern',
                    'southcrn' : 'southern',
                    'soutli' : 'south',
                    'soutliern' : 'southern',
                    'souud' : 'sound',
                    'spacc' : 'space',
                    'spcak' : 'speak',
                    'spccial' : 'special',
                    'spccific' : 'specific',
                    'spcech' : 'speech',
                    'spec1al' : 'special',
                    'spec1f1c' : 'specific',
                    'spec1fic' : 'specific',
                    'specia1' : 'special',
                    'speciaU' : 'special',
                    'specif1c' : 'specific',
                    'speciflc' : 'specific',
                    'speclal' : 'special',
                    'speecb' : 'speech',
                    'speecli' : 'speech',
                    'sriaU' : 'trial',
                    'st0ry' : 'story',
                    'st1ll' : 'still',
                    'st6ry' : 'story',
                    'stIU' : 'still',
                    'stafl' : 'staff',
                    'stagc' : 'stage',
                    'stat1on' : 'station',
                    'statc' : 'state',
                    'statcment' : 'statement',
                    'statemcnt' : 'statement',
                    'staud' : 'stand',
                    'stav' : 'stay',
                    'stcp' : 'step',
                    'stiU' : 'still',
                    'stih' : 'still',
                    'stiu' : 'still',
                    'stlll' : 'still',
                    'stndy' : 'study',
                    'stoiy' : 'story',
                    'storc' : 'store',
                    'storv' : 'story',
                    'str6ng' : 'strong',
                    'strcct' : 'street',
                    'strcet' : 'street',
                    'strect' : 'street',
                    'streft' : 'street',
                    'stroug' : 'strong',
                    'struclure' : 'structure',
                    'structurc' : 'structure',
                    'strudure' : 'structure',
                    'strufture' : 'structure',
                    'studcnt' : 'student',
                    'studv' : 'study',
                    'stvle' : 'style',
                    'sty1e' : 'style',
                    'styU' : 'style',
                    'stylc' : 'style',
                    'subjccl' : 'subject',
                    'subjcft' : 'subject',
                    'subjecl' : 'subject',
                    'subjed' : 'subject',
                    'subjedl' : 'subject',
                    'subjedt' : 'subject',
                    'subjeft' : 'subject',
                    'sucb' : 'such',
                    'succ6ss' : 'success',
                    'succefs' : 'success',
                    'succefsful' : 'successful',
                    'succesf' : 'success',
                    'successfu1' : 'successful',
                    'sucli' : 'such',
                    'suddenlv' : 'suddenly',
                    'sueh' : 'such',
                    'suffcr' : 'suffer',
                    'sufier' : 'suffer',
                    'sufler' : 'suffer',
                    'suggeft' : 'suggest',
                    'suhjcct' : 'subject',
                    'suhject' : 'subject',
                    'suj)port' : 'support',
                    'summcr' : 'summer',
                    'sup[)ort' : 'support',
                    'sup])ort' : 'support',
                    'supj)ort' : 'support',
                    'supp0rt' : 'support',
                    'surc' : 'sure',
                    'surfacc' : 'surface',
                    'suﬁer' : 'suffer',
                    'svithout' : 'without',
                    'svstcm' : 'system',
                    'svstem' : 'system',
                    'syflem' : 'system',
                    'syftcm' : 'system',
                    'syftem' : 'system',
                    'systcm' : 'system',
                    't0tal' : 'total',
                    't1me' : 'time',
                    't6gether' : 'together',
                    't6wn' : 'town',
                    'tOAvard' : 'toward',
                    'tOAvn' : 'town',
                    't^at' : 'that',
                    't^e' : 'the',
                    't^en' : 'ten',
                    't^hat' : 'that',
                    't^he' : 'the',
                    't^hen' : 'then',
                    't^here' : 'there',
                    't^hese' : 'these',
                    't^hey' : 'they',
                    't^his' : 'this',
                    't^ie' : 'the',
                    't^o' : 'to',
                    't^oo' : 'too',
                    't^ree' : 'tree',
                    't^wo' : 'two',
                    'tab1e' : 'table',
                    'tablc' : 'table',
                    'tafk' : 'task',
                    'tahk' : 'talk',
                    'tahle' : 'table',
                    'taik' : 'task',
                    'tak6' : 'take',
                    'takc' : 'take',
                    'tban' : 'than',
                    'tbank' : 'thank',
                    'tbat' : 'that',
                    'tbe' : 'the',
                    'tbefe' : 'these',
                    'tbeir' : 'their',
                    'tbem' : 'them',
                    'tbemfelves' : 'themselves',
                    'tbemselves' : 'themselves',
                    'tben' : 'then',
                    'tbeory' : 'theory',
                    'tbere' : 'there',
                    'tbese' : 'these',
                    'tbey' : 'they',
                    'tbing' : 'thing',
                    'tbink' : 'think',
                    'tbird' : 'third',
                    'tbis' : 'this',
                    'tbofe' : 'those',
                    'tbose' : 'those',
                    'tboufand' : 'thousand',
                    'tbough' : 'though',
                    'tbought' : 'thought',
                    'tbouglit' : 'thought',
                    'tbousand' : 'thousand',
                    'tbreat' : 'threat',
                    'tbree' : 'three',
                    'tbrougbout' : 'throughout',
                    'tbrough' : 'through',
                    'tbroughout' : 'throughout',
                    'tbrougli' : 'through',
                    'tbrow' : 'throw',
                    'tbus' : 'thus',
                    'tb«m' : 'them',
                    'tb«n' : 'then',
                    'tb«y' : 'they',
                    'tcach' : 'teach',
                    'tcacher' : 'teacher',
                    'tcam' : 'team',
                    'tcll' : 'tell',
                    'tcnd' : 'tend',
                    'tcrm' : 'term',
                    'tcst' : 'test',
                    'teU' : 'tell',
                    'teacb' : 'teach',
                    'teacber' : 'teacher',
                    'teachcr' : 'teacher',
                    'teacli' : 'teach',
                    'technologv' : 'technology',
                    'teft' : 'test',
                    'teim' : 'term',
                    'tel1' : 'tell',
                    'tf)e' : 'type',
                    'th0se' : 'those',
                    'th0usand' : 'thousand',
                    'th1ng' : 'thing',
                    'th1nk' : 'think',
                    'th1rd' : 'third',
                    'th1s' : 'this',
                    'th6ir' : 'their',
                    'th6m' : 'them',
                    'th6re' : 'there',
                    'th6ugh' : 'though',
                    'th6ught' : 'thought',
                    'th6y' : 'they',
                    'th^at' : 'that',
                    'th^e' : 'the',
                    'th^ey' : 'they',
                    'th^ir' : 'their',
                    'th^m' : 'them',
                    'th^re' : 'there',
                    'th^t' : 'that',
                    'thcfe' : 'these',
                    'thcir' : 'their',
                    'thcm' : 'them',
                    'thcmfclvcs' : 'themselves',
                    'thcmfclves' : 'themselves',
                    'thcmfelvcs' : 'themselves',
                    'thcmfelves' : 'themselves',
                    'thcmselves' : 'themselves',
                    'thcn' : 'then',
                    'thcorv' : 'theory',
                    'thcory' : 'theory',
                    'thcre' : 'there',
                    'thcse' : 'these',
                    'thcy' : 'they',
                    'the^e' : 'there',
                    'thecause' : 'because',
                    'thefc' : 'these',
                    'thefe' : 'these',
                    'theffe' : 'these',
                    'theie' : 'there',
                    'thele' : 'these',
                    'thelr' : 'their',
                    'themfclvcs' : 'themselves',
                    'themfclves' : 'themselves',
                    'themfelvcs' : 'themselves',
                    'themfelves' : 'themselves',
                    'themielves' : 'themselves',
                    'themlelves' : 'themselves',
                    'themsclves' : 'themselves',
                    'themse1ves' : 'themselves',
                    'themseh^es' : 'themselves',
                    'themselv^es' : 'themselves',
                    'themselvcs' : 'themselves',
                    'themselvef' : 'themselves',
                    'themſelues' : 'themselves',
                    'theoiy' : 'theory',
                    'theorv' : 'theory',
                    'ther6' : 'there',
                    'therc' : 'there',
                    'thes6' : 'these',
                    'thesc' : 'these',
                    'thev' : 'they',
                    'thiee' : 'three',
                    'thif' : 'this',
                    'thiff' : 'this',
                    'thiough' : 'through',
                    'thiug' : 'thing',
                    'thiuk' : 'think',
                    'thlng' : 'thing',
                    'thlnk' : 'think',
                    'thlrd' : 'third',
                    'thls' : 'this',
                    'thmg' : 'thing',
                    'thmk' : 'think',
                    'thofc' : 'those',
                    'thofe' : 'those',
                    'thoie' : 'those',
                    'thongh' : 'though',
                    'thonght' : 'thought',
                    'thonsand' : 'thousand',
                    'thos6' : 'those',
                    'thosc' : 'those',
                    'thoufand' : 'thousand',
                    'thoug^h' : 'though',
                    'thoug^ht' : 'thought',
                    'thougb' : 'though',
                    'thougbt' : 'thought',
                    'thougli' : 'though',
                    'thouglit' : 'thought',
                    'thouland' : 'thousand',
                    'thousaud' : 'thousand',
                    'thr0ugh' : 'through',
                    'thr6ugh' : 'through',
                    'thrcat' : 'threat',
                    'threc' : 'three',
                    'throAv' : 'throw',
                    'throiv' : 'throw',
                    'throngh' : 'through',
                    'throug^h' : 'through',
                    'througb' : 'through',
                    'througbout' : 'throughout',
                    'througli' : 'through',
                    'througliout' : 'throughout',
                    'throv' : 'throw',
                    'thuf' : 'thus',
                    'thul' : 'thus',
                    'th«m' : 'them',
                    'tiiat' : 'that',
                    'tim6' : 'time',
                    'tim^e' : 'time',
                    'timc' : 'time',
                    'tiuth' : 'truth',
                    'tj)e' : 'type',
                    'tl)e' : 'the',
                    'tlian' : 'than',
                    'tliat' : 'that',
                    'tliau' : 'than',
                    'tlic' : 'the',
                    'tlie' : 'the',
                    'tliefe' : 'these',
                    'tlieir' : 'their',
                    'tliem' : 'them',
                    'tliemselves' : 'themselves',
                    'tlien' : 'then',
                    'tliere' : 'there',
                    'tliese' : 'these',
                    'tliey' : 'they',
                    'tliink' : 'think',
                    'tliird' : 'third',
                    'tliis' : 'this',
                    'tlios' : 'those',
                    'tliose' : 'those',
                    'tliougb' : 'though',
                    'tliougbt' : 'thought',
                    'tliough' : 'though',
                    'tliought' : 'thought',
                    'tliougli' : 'though',
                    'tliouglit' : 'thought',
                    'tliousand' : 'thousand',
                    'tliree' : 'three',
                    'tlirougb' : 'through',
                    'tlirough' : 'through',
                    'tliroughout' : 'throughout',
                    'tlirougli' : 'through',
                    'tlirow' : 'throw',
                    'tlius' : 'thus',
                    'tlme' : 'time',
                    'tlus' : 'thus',
                    'tnrn' : 'turn',
                    'toAvard' : 'toward',
                    'toAvn' : 'town',
                    'to\vn' : 'town',
                    'to^vn' : 'town',
                    'todav' : 'today',
                    'togcthcr' : 'together',
                    'togcther' : 'together',
                    'togetber' : 'together',
                    'togethcr' : 'together',
                    'togethei' : 'together',
                    'togetlier' : 'together',
                    'toivard' : 'toward',
                    'toivn' : 'town',
                    'tota1' : 'total',
                    'tougb' : 'tough',
                    'tov/ard' : 'toward',
                    'tov/n' : 'town',
                    'tov^n' : 'town',
                    'tovn' : 'town',
                    'towu' : 'town',
                    'tr1al' : 'trial',
                    'tradc' : 'trade',
                    'train1ng' : 'training',
                    'travaU' : 'travel',
                    'travcl' : 'travel',
                    'trave1' : 'travel',
                    'traveU' : 'travel',
                    'trcat' : 'treat',
                    'trcatment' : 'treatment',
                    'trce' : 'tree',
                    'treatmcnt' : 'treatment',
                    'tria1' : 'trial',
                    'triaU' : 'trial',
                    'triah' : 'trial',
                    'trlal' : 'trial',
                    'trne' : 'true',
                    'trnth' : 'truth',
                    'troublc' : 'trouble',
                    'trouhle' : 'trouble',
                    'trutb' : 'truth',
                    'trutli' : 'truth',
                    'tryaU' : 'trial',
                    'træ' : 'tree',
                    'tt)e' : 'type',
                    'turu' : 'turn',
                    'tv/o' : 'two',
                    'tvO' : 'two',
                    'tvhatever' : 'whatever',
                    'tvhether' : 'whether',
                    'tvithout' : 'without',
                    'tvpe' : 'type',
                    'ty)v' : 'type',
                    'typc' : 'type',
                    'u))on' : 'upon',
                    'u)ay' : 'pay',
                    'u2)on' : 'upon',
                    'u[)on' : 'upon',
                    'u])on' : 'upon',
                    'u^pon' : 'upon',
                    'u^se' : 'use',
                    'uame' : 'name',
                    'uature' : 'nature',
                    'uauaUy' : 'usually',
                    'uccefsful' : 'successful',
                    'uear' : 'near',
                    'ueed' : 'need',
                    'uever' : 'never',
                    'uext' : 'next',
                    'uf)on' : 'upon',
                    'ufe' : 'use',
                    'uffe' : 'use',
                    'ufuaUy' : 'usually',
                    'ufually' : 'usually',
                    'ui)on' : 'upon',
                    'uj)on' : 'upon',
                    'ul)on' : 'upon',
                    'ulually' : 'usually',
                    'un1t' : 'unit',
                    'un^it' : 'unit',
                    'und^er' : 'under',
                    'undcr' : 'under',
                    'undcrftand' : 'understand',
                    'undcrstand' : 'understand',
                    'undei' : 'under',
                    'underfland' : 'understand',
                    'underftand' : 'understand',
                    'underltand' : 'understand',
                    'undertland' : 'understand',
                    'underſiand' : 'understand',
                    'underſland' : 'understand',
                    'underﬁand' : 'understand',
                    'unlt' : 'unit',
                    'unt1l' : 'until',
                    'unti1' : 'until',
                    'untiU' : 'until',
                    'unwiU' : 'until',
                    'up0n' : 'upon',
                    'up6n' : 'upon',
                    'up^on' : 'upon',
                    'urj)ose' : 'purpose',
                    'us^e' : 'use',
                    'usuaUy' : 'usually',
                    'usuallv' : 'usually',
                    'usuauy' : 'usually',
                    'uuder' : 'under',
                    'uutil' : 'until',
                    'ux)on' : 'upon',
                    'u|)on' : 'upon',
                    'v)hat' : 'what',
                    'v)hen' : 'when',
                    'v)hich' : 'which',
                    'v)ith' : 'with',
                    'v/Ith' : 'with',
                    'v/ait' : 'wait',
                    'v/all' : 'wall',
                    'v/ant' : 'want',
                    'v/atch' : 'watch',
                    'v/ay' : 'way',
                    'v/eapon' : 'weapon',
                    'v/ear' : 'wear',
                    'v/eight' : 'weight',
                    'v/ell' : 'well',
                    'v/estern' : 'western',
                    'v/hat' : 'what',
                    'v/hatever' : 'whatever',
                    'v/hcre' : 'where',
                    'v/hen' : 'when',
                    'v/herc' : 'where',
                    'v/here' : 'where',
                    'v/hether' : 'whether',
                    'v/hich' : 'which',
                    'v/hile' : 'while',
                    'v/hite' : 'white',
                    'v/ho' : 'who',
                    'v/hofe' : 'whose',
                    'v/holc' : 'whole',
                    'v/hole' : 'whole',
                    'v/hom' : 'whom',
                    'v/hose' : 'whose',
                    'v/hy' : 'why',
                    'v/ill' : 'will',
                    'v/indow' : 'window',
                    'v/ish' : 'wish',
                    'v/ith' : 'with',
                    'v/ithin' : 'within',
                    'v/ithout' : 'without',
                    'v/itliout' : 'without',
                    'v/liat' : 'what',
                    'v/liere' : 'where',
                    'v/liich' : 'which',
                    'v/liile' : 'while',
                    'v/liole' : 'whole',
                    'v/liom' : 'whom',
                    'v/oman' : 'woman',
                    'v/onder' : 'wonder',
                    'v/ord' : 'word',
                    'v/orld' : 'world',
                    'v/ould' : 'would',
                    'v/rite' : 'write',
                    'v/riter' : 'writer',
                    'v/rong' : 'wrong',
                    'v1ew' : 'view',
                    'v6ice' : 'voice',
                    'v6ry' : 'very',
                    'v6te' : 'vote',
                    'vAy' : 'way',
                    'vHo' : 'who',
                    'vVhether' : 'whether',
                    'vVithout' : 'without',
                    'vWhat' : 'what',
                    'vWhen' : 'when',
                    'vWith' : 'with',
                    'v\^hen' : 'when',
                    'v\^hich' : 'which',
                    'v\^ith' : 'with',
                    'v\^ould' : 'would',
                    'v\hat' : 'what',
                    'v\hen' : 'when',
                    'v\here' : 'where',
                    'v\hich' : 'which',
                    'v\hile' : 'while',
                    'v\hole' : 'whole',
                    'v\hom' : 'whom',
                    'v\ith' : 'with',
                    'v\ithin' : 'within',
                    'v\ithout' : 'without',
                    'v\ould' : 'would',
                    'v^^hat' : 'what',
                    'v^^hen' : 'when',
                    'v^^here' : 'where',
                    'v^^hich' : 'which',
                    'v^^hile' : 'while',
                    'v^^hole' : 'whole',
                    'v^^hom' : 'whom',
                    'v^^hose' : 'whose',
                    'v^^ith' : 'with',
                    'v^^ithout' : 'without',
                    'v^^orld' : 'world',
                    'v^^ould' : 'would',
                    'v^alue' : 'value',
                    'v^ant' : 'want',
                    'v^arious' : 'various',
                    'v^ery' : 'very',
                    'v^hat' : 'what',
                    'v^hatever' : 'whatever',
                    'v^hen' : 'when',
                    'v^here' : 'where',
                    'v^hether' : 'whether',
                    'v^hich' : 'which',
                    'v^hile' : 'while',
                    'v^hite' : 'white',
                    'v^hole' : 'whole',
                    'v^hom' : 'whom',
                    'v^hose' : 'whose',
                    'v^ish' : 'wish',
                    'v^ith' : 'with',
                    'v^ithin' : 'within',
                    'v^ithout' : 'without',
                    'v^oice' : 'voice',
                    'v^oman' : 'woman',
                    'v^ord' : 'word',
                    'v^orld' : 'world',
                    'v^ote' : 'vote',
                    'v^ould' : 'would',
                    'v^rite' : 'write',
                    'va1ue' : 'value',
                    'vaUum' : 'value',
                    'vaiious' : 'various',
                    'valne' : 'value',
                    'valuc' : 'value',
                    'var1ous' : 'various',
                    'vard' : 'yard',
                    'variouf' : 'various',
                    'varioul' : 'various',
                    'varlous' : 'various',
                    'vatch' : 'watch',
                    'vcry' : 'very',
                    'veapon' : 'weapon',
                    'veftern' : 'western',
                    'veight' : 'weight',
                    'veiglit' : 'weight',
                    'veiy' : 'very',
                    'ver^y' : 'very',
                    'verv' : 'very',
                    'vhat' : 'what',
                    'vhatever' : 'whatever',
                    'vhcther' : 'whether',
                    'vhen' : 'when',
                    'vhere' : 'where',
                    'vhethcr' : 'whether',
                    'vhether' : 'whether',
                    'vhich' : 'which',
                    'vhile' : 'while',
                    'vhite' : 'white',
                    'vhofe' : 'whose',
                    'vhole' : 'whole',
                    'vhom' : 'whom',
                    'vhose' : 'whose',
                    'vhy' : 'why',
                    'vi^ithin' : 'within',
                    'vi^ithout' : 'without',
                    'viclim' : 'victim',
                    'vicw' : 'view',
                    'vidim' : 'victim',
                    'vidlim' : 'victim',
                    'vidtim' : 'victim',
                    'vieAv' : 'view',
                    'vie\v' : 'view',
                    'vie^v' : 'view',
                    'vieiv' : 'view',
                    'viev' : 'view',
                    'vifit' : 'visit',
                    'viftim' : 'victim',
                    'viithin' : 'within',
                    'viithout' : 'without',
                    'vilhout' : 'without',
                    'vilit' : 'visit',
                    'vindow' : 'window',
                    'violencc' : 'violence',
                    'vis1t' : 'visit',
                    'vislt' : 'visit',
                    'vitH' : 'with',
                    'vithiii' : 'within',
                    'vithin' : 'within',
                    'vithoiit' : 'without',
                    'vithoul' : 'without',
                    'vithout' : 'without',
                    'vitliin' : 'within',
                    'vitliout' : 'without',
                    'vi«v' : 'view',
                    'viﬁt' : 'visit',
                    'vlew' : 'view',
                    'vliether' : 'whether',
                    'vlile' : 'while',
                    'vlsit' : 'visit',
                    'vniter' : 'writer',
                    'vntiU' : 'until',
                    'voicc' : 'voice',
                    'volce' : 'voice',
                    'voman' : 'woman',
                    'voorld' : 'world',
                    'voould' : 'would',
                    'vord' : 'word',
                    'vorld' : 'world',
                    'vorry' : 'worry',
                    'vorrà' : 'worry',
                    'votc' : 'vote',
                    'vould' : 'would',
                    'voung' : 'young',
                    'vour' : 'your',
                    'voursclf' : 'yourself',
                    'vourself' : 'yourself',
                    'vrhatever' : 'whatever',
                    'vrite' : 'write',
                    'vriter' : 'writer',
                    'vrong' : 'wrong',
                    'vrriter' : 'writer',
                    'vs^ell' : 'sell',
                    'vt^hen' : 'then',
                    'vv^hether' : 'whether',
                    'vv^ithout' : 'without',
                    'vvhether' : 'whether',
                    'vvithout' : 'without',
                    'vyhatever' : 'whatever',
                    'v«ith' : 'with',
                    'v»^hich' : 'which',
                    'v»^ith' : 'with',
                    'v»hat' : 'what',
                    'v»hen' : 'when',
                    'v»hich' : 'which',
                    'v»ith' : 'with',
                    'v»ould' : 'would',
                    'vérite' : 'write',
                    'w0rd' : 'word',
                    'w0rk' : 'work',
                    'w0rld' : 'world',
                    'w0uld' : 'would',
                    'w1de' : 'wide',
                    'w1fe' : 'wife',
                    'w1ll' : 'will',
                    'w1ndow' : 'window',
                    'w1sh' : 'wish',
                    'w1th' : 'with',
                    'w1thin' : 'within',
                    'w1thout' : 'without',
                    'w6man' : 'woman',
                    'w6rd' : 'word',
                    'w6rk' : 'work',
                    'w6rld' : 'world',
                    'w6uld' : 'would',
                    'w^ait' : 'wait',
                    'w^alk' : 'walk',
                    'w^all' : 'wall',
                    'w^ant' : 'want',
                    'w^ar' : 'war',
                    'w^atch' : 'watch',
                    'w^ater' : 'water',
                    'w^ay' : 'way',
                    'w^bich' : 'which',
                    'w^e' : 'we',
                    'w^eapon' : 'weapon',
                    'w^ear' : 'wear',
                    'w^eek' : 'week',
                    'w^eight' : 'weight',
                    'w^ell' : 'well',
                    'w^est' : 'west',
                    'w^estern' : 'western',
                    'w^hat' : 'what',
                    'w^hatever' : 'whatever',
                    'w^hen' : 'when',
                    'w^here' : 'where',
                    'w^hether' : 'whether',
                    'w^hicb' : 'which',
                    'w^hich' : 'which',
                    'w^hile' : 'while',
                    'w^hite' : 'white',
                    'w^ho' : 'who',
                    'w^hole' : 'whole',
                    'w^hom' : 'whom',
                    'w^hose' : 'whose',
                    'w^hy' : 'why',
                    'w^ide' : 'wide',
                    'w^ife' : 'wife',
                    'w^iich' : 'which',
                    'w^ill' : 'will',
                    'w^in' : 'win',
                    'w^ind' : 'wind',
                    'w^indow' : 'window',
                    'w^ish' : 'wish',
                    'w^ith' : 'with',
                    'w^ithin' : 'within',
                    'w^ithout' : 'without',
                    'w^oman' : 'woman',
                    'w^onder' : 'wonder',
                    'w^ord' : 'word',
                    'w^ork' : 'work',
                    'w^orker' : 'worker',
                    'w^orld' : 'world',
                    'w^orry' : 'worry',
                    'w^ould' : 'would',
                    'w^th' : 'with',
                    'waU' : 'wall',
                    'waUi' : 'wall',
                    'wahk' : 'walk',
                    'wal1' : 'wall',
                    'watcb' : 'watch',
                    'watcli' : 'watch',
                    'watcr' : 'water',
                    'watei' : 'water',
                    'wbatever' : 'whatever',
                    'wbere' : 'where',
                    'wbether' : 'whether',
                    'wbetlier' : 'whether',
                    'wbile' : 'while',
                    'wboM' : 'whom',
                    'wbofe' : 'whose',
                    'wbole' : 'whole',
                    'wbose' : 'whose',
                    'wby' : 'why',
                    'wbàt' : 'what',
                    'wcar' : 'wear',
                    'wcek' : 'week',
                    'wcftern' : 'western',
                    'wcight' : 'weight',
                    'wcll' : 'well',
                    'wcstern' : 'western',
                    'we1ght' : 'weight',
                    'weU' : 'well',
                    'weai)on' : 'weapon',
                    'weaj)on' : 'weapon',
                    'wefl' : 'west',
                    'weflern' : 'western',
                    'weftcrn' : 'western',
                    'weftern' : 'western',
                    'weig^ht' : 'weight',
                    'weigbt' : 'weight',
                    'weiglit' : 'weight',
                    'wel1' : 'well',
                    'welght' : 'weight',
                    'weltern' : 'western',
                    'westcrn' : 'western',
                    'westem' : 'western',
                    'weſi' : 'west',
                    'weſiern' : 'western',
                    'weſl' : 'west',
                    'weſlern' : 'western',
                    'whai' : 'what',
                    'whatcver' : 'whatever',
                    'whatev^er' : 'whatever',
                    'whatevcr' : 'whatever',
                    'whcn' : 'when',
                    'whcre' : 'where',
                    'whcthcr' : 'whether',
                    'whcther' : 'whether',
                    'wheie' : 'where',
                    'wher6' : 'where',
                    'wherc' : 'where',
                    'whetber' : 'whether',
                    'whethcr' : 'whether',
                    'whethei' : 'whether',
                    'whetlier' : 'whether',
                    'whi1e' : 'while',
                    'whiUi' : 'while',
                    'whic^h' : 'which',
                    'whicb' : 'which',
                    'whicli' : 'which',
                    'whieh' : 'which',
                    'whilc' : 'while',
                    'whitc' : 'white',
                    'whlch' : 'which',
                    'whlte' : 'white',
                    'who1e' : 'whole',
                    'whoUie' : 'whole',
                    'whoUj' : 'whole',
                    'whoUv' : 'whole',
                    'whofc' : 'whose',
                    'whofe' : 'whose',
                    'whohe' : 'whole',
                    'wholc' : 'whole',
                    'whos^e' : 'whose',
                    'whosc' : 'whose',
                    'wi11' : 'will',
                    'wiU' : 'will',
                    'wiUa' : 'will',
                    'wiUi' : 'will',
                    'widc' : 'wide',
                    'wifc' : 'wife',
                    'wifh' : 'wish',
                    'wifli' : 'wish',
                    'wiihin' : 'within',
                    'wiihout' : 'without',
                    'wiiicli' : 'which',
                    'wijh' : 'wish',
                    'wil1' : 'will',
                    'windoAv' : 'window',
                    'windo\v' : 'window',
                    'windoiv' : 'window',
                    'windov' : 'window',
                    'wisb' : 'wish',
                    'wisli' : 'wish',
                    'wit^h' : 'with',
                    'witb' : 'with',
                    'witbiii' : 'within',
                    'witbin' : 'within',
                    'witboiit' : 'without',
                    'witbout' : 'without',
                    'with0ut' : 'without',
                    'with1n' : 'within',
                    'with6ut' : 'without',
                    'withiu' : 'within',
                    'withln' : 'within',
                    'withont' : 'without',
                    'witli' : 'with',
                    'witliin' : 'within',
                    'witliout' : 'without',
                    'wiud' : 'wind',
                    'wlde' : 'wide',
                    'wlfe' : 'wife',
                    'wliat' : 'what',
                    'wliatever' : 'whatever',
                    'wliere' : 'where',
                    'wlietber' : 'whether',
                    'wliether' : 'whether',
                    'wliich' : 'which',
                    'wliicli' : 'which',
                    'wliile' : 'while',
                    'wliite' : 'white',
                    'wliole' : 'whole',
                    'wliom' : 'whom',
                    'wliose' : 'whose',
                    'wliy' : 'why',
                    'wlll' : 'will',
                    'wlnd' : 'wind',
                    'wlsh' : 'wish',
                    'wlth' : 'with',
                    'wlthin' : 'within',
                    'wlthout' : 'without',
                    'wmd' : 'wind',
                    'woiUd' : 'world',
                    'woid' : 'word',
                    'woild' : 'world',
                    'womau' : 'woman',
                    'wondcr' : 'wonder',
                    'wonld' : 'would',
                    'wor1d' : 'world',
                    'worUI' : 'world',
                    'worUi' : 'world',
                    'wor^d' : 'word',
                    'worrv' : 'worry',
                    'wotUd' : 'world',
                    'wou1d' : 'would',
                    'wouUI' : 'would',
                    'wouUi' : 'would',
                    'wouhd' : 'would',
                    'wovUd' : 'would',
                    'woxUd' : 'world',
                    'wr1te' : 'write',
                    'wr1ter' : 'writer',
                    'writc' : 'write',
                    'writcr' : 'writer',
                    'wrlte' : 'write',
                    'wrlter' : 'writer',
                    'wære' : 'where',
                    'x)Osition' : 'position',
                    'x)Ower' : 'power',
                    'x)aper' : 'paper',
                    'x)art' : 'part',
                    'x)articular' : 'particular',
                    'x)arty' : 'party',
                    'x)ass' : 'pass',
                    'x)atient' : 'patient',
                    'x)ay' : 'pay',
                    'x)eace' : 'peace',
                    'x)eople' : 'people',
                    'x)erhaps' : 'perhaps',
                    'x)eriod' : 'period',
                    'x)erson' : 'person',
                    'x)ersonal' : 'personal',
                    'x)lace' : 'place',
                    'x)lan' : 'plan',
                    'x)litics' : 'politics',
                    'x)oint' : 'point',
                    'x)olitical' : 'political',
                    'x)oor' : 'poor',
                    'x)osition' : 'position',
                    'x)ositive' : 'positive',
                    'x)ossible' : 'possible',
                    'x)ower' : 'power',
                    'x)ractice' : 'practice',
                    'x)resent' : 'present',
                    'x)ressure' : 'pressure',
                    'x)revent' : 'prevent',
                    'x)rice' : 'price',
                    'x)rivate' : 'private',
                    'x)robably' : 'probably',
                    'x)rocess' : 'process',
                    'x)roduce' : 'produce',
                    'x)roduction' : 'production',
                    'x)roperty' : 'property',
                    'x)rove' : 'prove',
                    'x)ublic' : 'public',
                    'x)urpose' : 'purpose',
                    'x)ut' : 'put',
                    'xUthough' : 'although',
                    'xehgious' : 'religious',
                    'xvestern' : 'western',
                    'xvhatever' : 'whatever',
                    'xvhether' : 'whether',
                    'xvithout' : 'without',
                    'y)art' : 'part',
                    'y)arty' : 'party',
                    'y)ay' : 'pay',
                    'y)eople' : 'people',
                    'y)lace' : 'place',
                    'y)resent' : 'present',
                    'y)robably' : 'probably',
                    'y)roperty' : 'property',
                    'y)ublic' : 'public',
                    'y)ut' : 'put',
                    'y/hich' : 'which',
                    'y/hole' : 'whole',
                    'y/hom' : 'whom',
                    'y/ith' : 'with',
                    'y/ithin' : 'within',
                    'y/ithout' : 'without',
                    'y/ould' : 'would',
                    'y0ung' : 'young',
                    'y0ur' : 'your',
                    'y6ung' : 'young',
                    'y6ur' : 'your',
                    'yATURAL' : 'natural',
                    'y^ear' : 'year',
                    'y^es' : 'yes',
                    'y^et' : 'yet',
                    'y^ou' : 'you',
                    'y^oung' : 'young',
                    'y^our' : 'your',
                    'y^same' : 'same',
                    'y^that' : 'that',
                    'y^then' : 'then',
                    'yarioiis' : 'various',
                    'ycar' : 'year',
                    'yef' : 'yes',
                    'yeff' : 'yes',
                    'yourfclf' : 'yourself',
                    'yourfelf' : 'yourself',
                    'yourfelff' : 'yourself',
                    'yourfell' : 'yourself',
                    'yourlelf' : 'yourself',
                    'yoursclf' : 'yourself',
                    'yourseU' : 'yourself',
                    'yourſelſ' : 'yourself',
                    'yvhatever' : 'whatever',
                    'yvhether' : 'whether',
                    'yvithout' : 'without',
                    'zbort' : 'short',
                    'zeien' : 'seven',
                    'zoutb' : 'south',
                    'zthoſe' : 'those',
                    'zvestern' : 'western',
                    'zvhatever' : 'whatever',
                    'zvhether' : 'whether',
                    'zvithout' : 'without',
                    'zſhe' : 'she',
                    'zſhould' : 'should',
                    'zſit' : 'sit'}
abbreviation_dict = {
    "AFG": [
        "afghanistan"
    ],
    "ALA": [
        "aland islands"
    ],
    "ALB": [
        "albania"
    ],
    "DZA": [
        "algeria"
    ],
    "ASM": [
        "american samoa"
    ],
    "AND": [
        "andorra"
    ],
    "AGO": [
        "angola"
    ],
    "AIA": [
        "anguilla"
    ],
    "ATA": [
        "antarctica"
    ],
    "ATG": [
        "antigua and barbuda"
    ],
    "ARG": [
        "argentina"
    ],
    "ARM": [
        "armenia"
    ],
    "ABW": [
        "aruba"
    ],
    "AUS": [
        "australia"
    ],
    "AUT": [
        "austria"
    ],
    "AZE": [
        "azerbaijan"
    ],
    "BHS": [
        "bahamas"
    ],
    "BHR": [
        "bahrain"
    ],
    "BGD": [
        "bangladesh"
    ],
    "BRB": [
        "barbados"
    ],
    "BLR": [
        "belarus"
    ],
    "BEL": [
        "belgium"
    ],
    "BLZ": [
        "belize"
    ],
    "BEN": [
        "benin"
    ],
    "BMU": [
        "bermuda"
    ],
    "BTN": [
        "bhutan"
    ],
    "BOL": [
        "bolivia"
    ],
    "BIH": [
        "bosnia and herzegovina"
    ],
    "BWA": [
        "botswana"
    ],
    "BVT": [
        "bouvet island"
    ],
    "BRA": [
        "brazil"
    ],
    "VGB": [
        "british virgin islands"
    ],
    "IOT": [
        "british indian ocean territory"
    ],
    "BRN": [
        "brunei darussalam"
    ],
    "BGR": [
        "bulgaria"
    ],
    "BFA": [
        "burkina faso"
    ],
    "BDI": [
        "burundi"
    ],
    "KHM": [
        "cambodia"
    ],
    "CMR": [
        "cameroon"
    ],
    "CAN": [
        "canada"
    ],
    "CPV": [
        "cape verde"
    ],
    "CYM": [
        "cayman islands"
    ],
    "CAF": [
        "central african republic"
    ],
    "TCD": [
        "chad"
    ],
    "CHL": [
        "chile"
    ],
    "CHN": [
        "china"
    ],
    "HKG": [
        "hong kong, sar china"
    ],
    "MAC": [
        "macao, sar china"
    ],
    "CXR": [
        "christmas island"
    ],
    "CCK": [
        "cocos (keeling) islands"
    ],
    "COL": [
        "colombia"
    ],
    "COM": [
        "comoros"
    ],
    "COG": [
        "congo (brazzaville)"
    ],
    "COD": [
        "congo, (kinshasa)"
    ],
    "COK": [
        "cook islands"
    ],
    "CRI": [
        "costa rica"
    ],
    "CIV": [
        "côte d'ivoire"
    ],
    "HRV": [
        "croatia"
    ],
    "CUB": [
        "cuba"
    ],
    "CYP": [
        "cyprus"
    ],
    "CZE": [
        "czech republic"
    ],
    "DNK": [
        "denmark"
    ],
    "DJI": [
        "djibouti"
    ],
    "DMA": [
        "dominica"
    ],
    "DOM": [
        "dominican republic"
    ],
    "ECU": [
        "ecuador"
    ],
    "EGY": [
        "egypt"
    ],
    "SLV": [
        "el salvador"
    ],
    "GNQ": [
        "equatorial guinea"
    ],
    "ERI": [
        "eritrea"
    ],
    "EST": [
        "estonia"
    ],
    "ETH": [
        "ethiopia"
    ],
    "FLK": [
        "falkland islands (malvinas)"
    ],
    "FRO": [
        "faroe islands"
    ],
    "FJI": [
        "fiji"
    ],
    "FIN": [
        "finland"
    ],
    "FRA": [
        "france"
    ],
    "GUF": [
        "french guiana"
    ],
    "PYF": [
        "french polynesia"
    ],
    "ATF": [
        "french southern territories"
    ],
    "GAB": [
        "gabon"
    ],
    "GMB": [
        "gambia"
    ],
    "GEO": [
        "georgia"
    ],
    "DEU": [
        "germany"
    ],
    "GHA": [
        "ghana"
    ],
    "GIB": [
        "gibraltar"
    ],
    "GRC": [
        "greece"
    ],
    "GRL": [
        "greenland"
    ],
    "GRD": [
        "grenada"
    ],
    "GLP": [
        "guadeloupe"
    ],
    "GUM": [
        "guam"
    ],
    "GTM": [
        "guatemala"
    ],
    "GGY": [
        "guernsey"
    ],
    "GIN": [
        "guinea"
    ],
    "GNB": [
        "guinea-bissau"
    ],
    "GUY": [
        "guyana"
    ],
    "HTI": [
        "haiti"
    ],
    "HMD": [
        "heard and mcdonald islands"
    ],
    "HND": [
        "honduras"
    ],
    "HUN": [
        "hungary"
    ],
    "ISL": [
        "iceland"
    ],
    "IND": [
        "india"
    ],
    "IDN": [
        "indonesia"
    ],
    "IRQ": [
        "iran"
    ],
    "IRL": [
        "ireland"
    ],
    "IMN": [
        "isle of man"
    ],
    "ISR": [
        "israel"
    ],
    "ITA": [
        "italy"
    ],
    "JAM": [
        "jamaica"
    ],
    "JPN": [
        "japan"
    ],
    "JEY": [
        "jersey"
    ],
    "JOR": [
        "jordan"
    ],
    "KAZ": [
        "kazakhstan"
    ],
    "KEN": [
        "kenya"
    ],
    "KIR": [
        "kiribati"
    ],
    "PRK": [
        "north korea"
    ],
    "KOR": [
        "south korea"
    ],
    "KWT": [
        "kuwait"
    ],
    "KGZ": [
        "kyrgyzstan"
    ],
    "LAO": [
        "lao pdr"
    ],
    "LVA": [
        "latvia"
    ],
    "LBN": [
        "lebanon"
    ],
    "LSO": [
        "lesotho"
    ],
    "LBR": [
        "liberia"
    ],
    "LBY": [
        "libya"
    ],
    "LIE": [
        "liechtenstein"
    ],
    "LTU": [
        "lithuania"
    ],
    "LUX": [
        "luxembourg"
    ],
    "MKD": [
        "macedonia"
    ],
    "MDG": [
        "madagascar"
    ],
    "MWI": [
        "malawi"
    ],
    "MYS": [
        "malaysia"
    ],
    "MDV": [
        "maldives"
    ],
    "MLI": [
        "mali"
    ],
    "MLT": [
        "malta"
    ],
    "MHL": [
        "marshall islands"
    ],
    "MTQ": [
        "martinique"
    ],
    "MRT": [
        "mauritania"
    ],
    "MUS": [
        "mauritius"
    ],
    "MYT": [
        "mayotte"
    ],
    "MEX": [
        "mexico"
    ],
    "FSM": [
        "micronesia"
    ],
    "MDA": [
        "moldova"
    ],
    "MCO": [
        "monaco"
    ],
    "MNG": [
        "mongolia"
    ],
    "MNE": [
        "montenegro"
    ],
    "MSR": [
        "montserrat"
    ],
    "MAR": [
        "morocco"
    ],
    "MOZ": [
        "mozambique"
    ],
    "MMR": [
        "myanmar"
    ],
    "NAM": [
        "namibia"
    ],
    "NRU": [
        "nauru"
    ],
    "NPL": [
        "nepal"
    ],
    "NLD": [
        "netherlands"
    ],
    "ANT": [
        "netherlands antilles"
    ],
    "NCL": [
        "new caledonia"
    ],
    "NZL": [
        "new zealand"
    ],
    "NIC": [
        "nicaragua"
    ],
    "NER": [
        "niger"
    ],
    "NGA": [
        "nigeria"
    ],
    "NIU": [
        "niue"
    ],
    "NFK": [
        "norfolk island"
    ],
    "MNP": [
        "northern mariana islands"
    ],
    "NOR": [
        "norway"
    ],
    "OMN": [
        "oman"
    ],
    "PAK": [
        "pakistan"
    ],
    "PLW": [
        "palau"
    ],
    "PSE": [
        "palestinian territory"
    ],
    "PAN": [
        "panama"
    ],
    "PNG": [
        "papua new guinea"
    ],
    "PRY": [
        "paraguay"
    ],
    "PER": [
        "peru"
    ],
    "PHL": [
        "philippines"
    ],
    "PCN": [
        "pitcairn"
    ],
    "POL": [
        "poland"
    ],
    "PRT": [
        "portugal"
    ],
    "PRI": [
        "puerto rico"
    ],
    "QAT": [
        "qatar"
    ],
    "REU": [
        "reunion"
    ],
    "ROU": [
        "romania"
    ],
    "RUS": [
        "russian federation"
    ],
    "RWA": [
        "rwanda"
    ],
    "BLM": [
        "saint-barthelemy"
    ],
    "SHN": [
        "saint helena"
    ],
    "KNA": [
        "saint kitts and nevis"
    ],
    "LCA": [
        "saint lucia"
    ],
    "MAF": [
        "saint-martin"
    ],
    "SPM": [
        "saint pierre and miquelon"
    ],
    "VCT": [
        "saint vincent and grenadines"
    ],
    "WSM": [
        "samoa"
    ],
    "SMR": [
        "san marino"
    ],
    "STP": [
        "sao tome and principe"
    ],
    "SAU": [
        "saudi arabia"
    ],
    "SEN": [
        "senegal"
    ],
    "SRB": [
        "serbia"
    ],
    "SYC": [
        "seychelles"
    ],
    "SLE": [
        "sierra leone"
    ],
    "SGP": [
        "singapore"
    ],
    "SVK": [
        "slovakia"
    ],
    "SVN": [
        "slovenia"
    ],
    "SLB": [
        "solomon islands"
    ],
    "SOM": [
        "somalia"
    ],
    "ZAF": [
        "south africa"
    ],
    "SGS": [
        "south georgia and the south sandwich islands"
    ],
    "SSD": [
        "south sudan"
    ],
    "ESP": [
        "spain"
    ],
    "LKA": [
        "sri lanka"
    ],
    "SDN": [
        "sudan"
    ],
    "SUR": [
        "suriname"
    ],
    "SJM": [
        "svalbard and jan mayen islands"
    ],
    "SWZ": [
        "swaziland"
    ],
    "SWE": [
        "sweden"
    ],
    "CHE": [
        "switzerland"
    ],
    "SY": [
        "syria"
    ],
    "TWN": [
        "taiwan"
    ],
    "TJK": [
        "tajikistan"
    ],
    "TZA": [
        "tanzania"
    ],
    "THA": [
        "thailand"
    ],
    "TLS": [
        "timor-leste"
    ],
    "TGO": [
        "togo"
    ],
    "TKL": [
        "tokelau"
    ],
    "TON": [
        "tonga"
    ],
    "TTO": [
        "trinidad and tobago"
    ],
    "TUN": [
        "tunisia"
    ],
    "TUR": [
        "turkey"
    ],
    "TKM": [
        "turkmenistan"
    ],
    "TCA": [
        "turks and caicos islands"
    ],
    "TUV": [
        "tuvalu"
    ],
    "UGA": [
        "uganda"
    ],
    "UKR": [
        "ukraine"
    ],
    "ARE": [
        "united arab emirates"
    ],
    "GBR": [
        "united kingdom"
    ],
    "USA": [
        "united states of america"
    ],
    "UMI": [
        "us minor outlying islands"
    ],
    "URY": [
        "uruguay"
    ],
    "UZB": [
        "uzbekistan"
    ],
    "VUT": [
        "vanuatu"
    ],
    "VEN": [
        "venezuela"
    ],
    "VNM": [
        "viet nam"
    ],
    "VIR": [
        "virgin islands"
    ],
    "WLF": [
        "wallis and futuna islands"
    ],
    "ESH": [
        "western sahara"
    ],
    "YEM": [
        "yemen"
    ],
    "ZMB": [
        "zambia"
    ],
    "ZWE": [
        "zimbabwe"
    ],
    "1st": [
        "first"
    ],
    "2nd": [
        "second"
    ],
    "3rd": [
        "third"
    ],
    "4th": [
        "fourth"
    ],
    "5th": [
        "fifth"
    ],
    "6th": [
        "sixth"
    ],
    "7th": [
        "seventh"
    ],
    "8th": [
        "eighth"
    ],
    "9th": [
        "ninth"
    ],
    "10th": [
        "tenth"
    ],
    "Jan.": [
        "january"
    ],
    "Feb.": [
        "february"
    ],
    "Mar.": [
        "march"
    ],
    "Apr.": [
        "april"
    ],
    "Jun.": [
        "june"
    ],
    "Jul.": [
        "july"
    ],
    "Aug.": [
        "august"
    ],
    "Sept.": [
        "september"
    ],
    "Oct.": [
        "october"
    ],
    "Nov.": [
        "november"
    ],
    "Dec.": [
        "december."
    ],
    "Sun.": [
        "sunday"
    ],
    "Mon.": [
        "monday"
    ],
    "Tues.": [
        "tuesday"
    ],
    "Wed.": [
        "wednesday"
    ],
    "Thurs.": [
        "thursday"
    ],
    "Fri.": [
        "friday"
    ],
    "Sat.": [
        "saturday"
    ],
    "hr": [
        "hour"
    ],
    "hrs": [
        "hours"
    ],
    "min": [
        "minute"
    ],
    "mins": [
        "minutes"
    ],
    "AA": [
        "alcoholics anonymous"
    ],
    "B2B": [
        "business-to-business"
    ],
    "B2C": [
        "business-to-consumer"
    ],
    "Cad": [
        "canadian"
    ],
    "WOW": [
        "world of Warcraft"
    ],
    "rofl": [
        "rolling on floor laughing"
    ],
    "stfu": [
        "shut the freak up"
    ],
    "lemeno": [
        "let me know"
    ],
    "Ilu": [
        "i love you"
    ],
    "yolo": [
        "you only live once"
    ],
    "smh": [
        "shaking my head"
    ],
    "lmfao": [
        "laughing my freaking ass off"
    ],
    "nm": [
        "nice meld"
    ],
    "Ikr": [
        "i know, right ?"
    ],
    "ofc": [
        "of course"
    ],
    "#?": [
        "i don't understand what you mean"
    ],
    "Q4U": [
        "i have a question for you"
    ],
    ";s": [
        "gentle warning"
    ],
    "^^": [
        "read message"
    ],
    "<3": [
        "sideways heart"
    ],
    "</3": [
        "broken heart"
    ],
    "<3333": [
        "love"
    ],
    "ateotd": [
        "at the end of the day"
    ],
    ".02": [
        "my two cents worth"
    ],
    "#1tg (,) 2tg": [
        "number of items needed for win"
    ],
    "1up": [
        "extra life"
    ],
    "121": [
        "one-to-one"
    ],
    "l33t": [
        "elite"
    ],
    "1432": [
        "i love you too"
    ],
    "14aa41": [
        "one for all and all for one"
    ],
    "182": [
        "i hate you"
    ],
    "19": [
        "zero hand"
    ],
    "10m": [
        "ten man"
    ],
    "tx": [
        "thanks"
    ],
    "ty": [
        "thank you"
    ],
    "1ce": [
        "Once"
    ],
    "1Dr": [
        "i wonder"
    ],
    "1nam": [
        "one in a million"
    ],
    "2": [
        "to"
    ],
    "20": [
        "location"
    ],
    "2ez": [
        "too easy"
    ],
    "2g2bt": [
        "too good to be true"
    ],
    "2m2h": [
        "too much too handle"
    ],
    "tmth": [
        "too much to handle"
    ],
    "tmi": [
        "too much information"
    ],
    "2mor": [
        "tomorrow"
    ],
    "2nte": [
        "tonight"
    ],
    "4": [
        "for"
    ],
    "411": [
        "information"
    ],
    "Idunno": [
        "i don't know"
    ],
    "lgh": [
        "lets get high"
    ],
    "420": [
        "marijuana"
    ],
    "4ao": [
        "for adults only"
    ],
    "fcol": [
        "for crying out loud"
    ],
    "4eae": [
        "forever and ever"
    ],
    "4eva": [
        "forever"
    ],
    "4nr": [
        "foreigner"
    ],
    "4sale": [
        "for sale"
    ],
    "^5": [
        "high-five"
    ],
    "555": [
        "sobbing crying"
    ],
    "55555": [
        "laughing"
    ],
    "hawt": [
        "attractive"
    ],
    "7k": [
        "sick"
    ],
    "81": [
        "hells angels"
    ],
    "ova": [
        "over"
    ],
    "88": [
        "hugs and kisses"
    ],
    "9": [
        "parent is watching"
    ],
    "*s*": [
        "smile"
    ],
    "*w*": [
        "wink"
    ],
    "a3": [
        "anytime anywhere anyplace"
    ],
    "aa": [
        "ask about"
    ],
    "amof": [
        "as a matter of fact"
    ],
    "aaf": [
        "as a friend"
    ],
    "aak": [
        "alive and kicking"
    ],
    "aamoi": [
        "as a matter of interest"
    ],
    "aap": [
        "always a pleasure"
    ],
    "aar": [
        "at any rate"
    ],
    "aas": [
        "alive and smiling"
    ],
    "aashta": [
        "as always sheldon has the answer"
    ],
    "aatk": [
        "always at the keyboard"
    ],
    "aayf": [
        "as always your friend"
    ],
    "abbr": [
        "abbreviation"
    ],
    "abc": [
        "already been chewed"
    ],
    "abd": [
        "already been done"
    ],
    "abt": [
        "about"
    ],
    "abt2": [
        "about to"
    ],
    "abta": [
        "good-bye"
    ],
    "abu": [
        "all bugged up"
    ],
    "ac": [
        "acceptable content"
    ],
    "acc": [
        "anyone can come"
    ],
    "acd": [
        "alt/control/delete"
    ],
    "acdnt": [
        "accident"
    ],
    "ace": [
        "marijuana cigarette"
    ],
    "ack": [
        "acknowledge"
    ],
    "acpt": [
        "accept"
    ],
    "acqstn": [
        "acquisition"
    ],
    "adad": [
        "another day another dollar"
    ],
    "adbb": [
        "all done bye-bye"
    ],
    "adr": [
        "address"
    ],
    "adih": [
        "another day in hell"
    ],
    "adip": [
        "another day in paradise"
    ],
    "adminr": [
        "administrator"
    ],
    "adn": [
        "any day now"
    ],
    "ae": [
        "area effect"
    ],
    "aeap": [
        "as early as possible"
    ],
    "af": [
        "aggression factor"
    ],
    "afc": [
        "away from computer"
    ],
    "afaiaa": [
        "as far as i am aware"
    ],
    "afaic": [
        "as far as i am concerned"
    ],
    "afaik": [
        "as far as i know"
    ],
    "afaiui": [
        "as far as i understand it"
    ],
    "afap": [
        "as far as possible"
    ],
    "affa": [
        "angels forever forever angels"
    ],
    "afj": [
        "april fool's joke"
    ],
    "afk": [
        "away from keyboard"
    ],
    "afz": [
        "acronym free zone"
    ],
    "afpoe": [
        "a fresh pair of eyes"
    ],
    "agi": [
        "agility"
    ],
    "ah": [
        "at home"
    ],
    "aiamu": [
        "and i am a money's uncle"
    ],
    "aight": [
        "alright"
    ],
    "air": [
        "as i remember"
    ],
    "aisb": [
        "as i said before"
    ],
    "aisi": [
        "as i see it"
    ],
    "aitr": [
        "adult in the room"
    ],
    "aka": [
        "also known as"
    ],
    "alcon": [
        "all concerned"
    ],
    "alol": [
        "actually laughing out loud"
    ],
    "ama": [
        "ask me anything"
    ],
    "amap": [
        "as much as possible"
    ],
    "ambw": [
        "all my best wishes"
    ],
    "aml": [
        "all my love"
    ],
    "amzn": [
        "amazing"
    ],
    "a/n": [
        "author's note"
    ],
    "ao": [
        "anarchy online"
    ],
    "aoc": [
        "available on cell"
    ],
    "aoe": [
        "area of effect"
    ],
    "aom": [
        "age of mythology"
    ],
    "aota": [
        "all of the above"
    ],
    "aoyp": [
        "angel on your pillow"
    ],
    "apac": [
        "all praise and credit"
    ],
    "app": [
        "appreciate"
    ],
    "aqap": [
        "as quiet as possible"
    ],
    "arc": [
        "archive"
    ],
    "are": [
        "acronym rich environment"
    ],
    "arg": [
        "argument"
    ],
    "asig": [
        "and so it goes"
    ],
    "asap": [
        "as soon as possible"
    ],
    "asl": [
        "age/sex/location"
    ],
    "asla": [
        "age/sex/location/availability"
    ],
    "at": [
        "at your terminal"
    ],
    "atb": [
        "all the best"
    ],
    "atm": [
        "at the moment"
    ],
    "atsits": [
        "all the stars in the sky"
    ],
    "atsl": [
        "along the same line"
    ],
    "awc": [
        "after awhile crocodile"
    ],
    "aweso": [
        "awesome"
    ],
    "awol": [
        "absent without leave"
    ],
    "aydy": [
        "are you done yet ?"
    ],
    "aybabtu": [
        "all your base are belong to us"
    ],
    "ayec": [
        "at your earliest convenience"
    ],
    "ayor": [
        "at your own risk"
    ],
    "aysos": [
        "are you stupid or something ?"
    ],
    "ays": [
        "are you stupid ?"
    ],
    "rut": [
        "are you there ?"
    ],
    "aytmtb": [
        "and you're telling me this because"
    ],
    "ayv": [
        "are you vertical ?"
    ],
    "ayw": [
        "as you wish"
    ],
    "azn": [
        "asian"
    ],
    "b": [
        "be"
    ],
    "b&": [
        "banned"
    ],
    "b2w": [
        "back to work"
    ],
    "b8": [
        "bait"
    ],
    "b9": [
        "boss is watching"
    ],
    "boyf": [
        "boyfriend"
    ],
    "b/g": [
        "background"
    ],
    "b4": [
        "before"
    ],
    "bfn": [
        "bye for now"
    ],
    "bag": [
        "busting a gut"
    ],
    "ba": [
        "bad ass"
    ],
    "bae": [
        "baby"
    ],
    "bafo": [
        "best and final offer"
    ],
    "bak": [
        "back at keyboard"
    ],
    "bam": [
        "below average mentality"
    ],
    "bamf": [
        "bad ass mother fucker"
    ],
    "bao": [
        "be aware of"
    ],
    "bas": [
        "big butt smile"
    ],
    "basic": [
        "anything mainstream"
    ],
    "basor": [
        "breathing a sigh of relief"
    ],
    "bau": [
        "business as usual"
    ],
    "bay": [
        "back at ya"
    ],
    "bb": [
        "big brother"
    ],
    "bbc": [
        "big bad challenge"
    ],
    "bbiab": [
        "be back in a bit"
    ],
    "bbiaf": [
        "be back in a few"
    ],
    "bbiam": [
        "be back in a minute"
    ],
    "bbias": [
        "be back in a sec"
    ],
    "bbl": [
        "be back later"
    ],
    "bbn": [
        "bye bye now"
    ],
    "bbq": [
        "barbeque"
    ],
    "bbs": [
        "be back soon"
    ],
    "bbt": [
        "be back tomorrow"
    ],
    "cos": [
        "because"
    ],
    "bc": [
        "be cool"
    ],
    "bcnu": [
        "be seeing you"
    ],
    "bco": [
        "big crush on"
    ],
    "bcoy": [
        "big crush on you"
    ],
    "bd": [
        "big deal"
    ],
    "cakeday": [
        "birthday"
    ],
    "bdn": [
        "big darn number"
    ],
    "beg": [
        "big evil grin"
    ],
    "belf": [
        "blood elf"
    ],
    "bf": [
        "best friend"
    ],
    "bfaw": [
        "best friend at work"
    ],
    "bf2": [
        "battlefield 2"
    ],
    "bff": [
        "best friends forever"
    ],
    "bffl": [
        "best friends for life"
    ],
    "bfflnmw": [
        "best friends for life no matter what"
    ],
    "bfd": [
        "big freaking deal"
    ],
    "bfg": [
        "big freaking grin"
    ],
    "bffn": [
        "best friend for now"
    ],
    "bg": [
        "big grin"
    ],
    "bgwm": [
        "be gentle with me"
    ],
    "bhl8": [
        "be home late"
    ],
    "bib": [
        "boss is back"
    ],
    "bibo": [
        "beer in, beer out"
    ],
    "bic": [
        "butt in chair"
    ],
    "bif": [
        "before i forget"
    ],
    "bih": [
        "burn in hell"
    ],
    "bil": [
        "brother in law"
    ],
    "bio": [
        "bathroom break"
    ],
    "bion": [
        "believe it or not"
    ],
    "bioya": [
        "blow it out your ass"
    ],
    "bioyn": [
        "blow it out your nose"
    ],
    "bis": [
        "best in slot"
    ],
    "bisflatm": [
        "boy, i sure feel like a turquoise monkey !"
    ],
    "bitmt": [
        "but in the meantime"
    ],
    "bl": [
        "belly laugh"
    ],
    "blnt": [
        "better luck next time"
    ],
    "bloke": [
        "man"
    ],
    "bm": [
        "bite me"
    ],
    "bme": [
        "based on my experience"
    ],
    "bm&y": [
        "between me and you"
    ],
    "bob": [
        "back off bitch"
    ],
    "bn": [
        "bad news"
    ],
    "boe": [
        "bind on equip"
    ],
    "bohica": [
        "bend over here it comes again"
    ],
    "bol": [
        "best of luck"
    ],
    "bom": [
        "butt of mine"
    ],
    "bolo": [
        "be on the look out"
    ],
    "booms": [
        "bored out of my skull"
    ],
    "bop": [
        "bind on pickup"
    ],
    "bosmkl": [
        "bending over smacking my knee laughing"
    ],
    "bot": [
        "be on that"
    ],
    "bms": [
        "broke my scale"
    ],
    "bplm": [
        "big person little mind"
    ],
    "brb": [
        "be right back"
    ],
    "br": [
        "best regards"
    ],
    "brbb": [
        "be right back bitch"
    ],
    "brnc": [
        "be right back nature calls"
    ],
    "zzzz": [
        "sleeping"
    ],
    "brh": [
        "be right here"
    ],
    "brt": [
        "be right there"
    ],
    "bsf": [
        "but seriously folks"
    ],
    "bst": [
        "best"
    ],
    "bsod": [
        "blue screen of death"
    ],
    "bsts": [
        "better safe than sorry"
    ],
    "bt": [
        "between technologies"
    ],
    "bta": [
        "but then again"
    ],
    "btdt": [
        "been there done that"
    ],
    "btw": [
        "by the way"
    ],
    "btycl": [
        "bootycall"
    ],
    "bubu": [
        "most beautiful of women"
    ],
    "burn": [
        "used to reference an insult"
    ],
    "buff": [
        "changed and is now stronger"
    ],
    "bwl": [
        "bursting with laughter"
    ],
    "byob": [
        "build your own burger"
    ],
    "byoc": [
        "bring your own computer"
    ],
    "byod": [
        "bring your own device"
    ],
    "byoh": [
        "bat you on the head"
    ],
    "byop": [
        "bring your own paint"
    ],
    "bytm": [
        "better you than me"
    ],
    "c&g": [
        "chuckle & grin"
    ],
    "c4n": [
        "ciao for now"
    ],
    "cad": [
        "control + alt + delete"
    ],
    "cam": [
        "camera"
    ],
    "cb": [
        "crazy bitch"
    ],
    "cd9": [
        "parents are around"
    ],
    "cfs": [
        "care for secret ?"
    ],
    "cfy": [
        "calling for you"
    ],
    "chk": [
        "check"
    ],
    "cico": [
        "coffee in, coffee out"
    ],
    "cid": [
        "consider it done"
    ],
    "clab": [
        "crying like a baby"
    ],
    "cld": [
        "could"
    ],
    "clk": [
        "click"
    ],
    "cm": [
        "call me"
    ],
    "cmap": [
        "cover my ass partner"
    ],
    "cmb": [
        "call me back"
    ],
    "cmgr": [
        "community manager"
    ],
    "cmiiw": [
        "correct me if i'm wrong"
    ],
    "cmon": [
        "come on"
    ],
    "cnp": [
        "continued in next post"
    ],
    "cob": [
        "close of business"
    ],
    "coh": [
        "city of heroes"
    ],
    "c/p": [
        "cross post"
    ],
    "cp": [
        "chat post"
    ],
    "cre8": [
        "create"
    ],
    "crz": [
        "crazy"
    ],
    "craft": [
        "can't remember a freaking thing"
    ],
    "crb": [
        "come right back"
    ],
    "crbt": [
        "crying really big tears"
    ],
    "crit": [
        "critical hit"
    ],
    "crs": [
        "can't remember stuff"
    ],
    "csg": [
        "chuckle, snicker, grin"
    ],
    "csl": [
        "can't stop laughing"
    ],
    "css": [
        "counter-strike source"
    ],
    "ct": [
        "can't talk"
    ],
    "ctc": [
        "care to chat ?"
    ],
    "cthu": [
        "cracking the heck up"
    ],
    "ctn": [
        "can't talk now"
    ],
    "cto": [
        "check this out"
    ],
    "cu": [
        "see you too"
    ],
    "cya": [
        "see you"
    ],
    "cua": [
        "see you around"
    ],
    "syl": [
        "see you later"
    ],
    "cula": [
        "see you later alligator"
    ],
    "cumid": [
        "see you in my dreams"
    ],
    "curlo": [
        "see you around like a donut"
    ],
    "cwd": [
        "comment when done"
    ],
    "cwot": [
        "complete waste of time"
    ],
    "cwyl": [
        "chat with you later"
    ],
    "cx": [
        "correction"
    ],
    "cye": [
        "check your e-mail"
    ],
    "cyep": [
        "close your eyes partner"
    ],
    "cyo": [
        "see you online"
    ],
    "d46?": [
        "down for sex?"
    ],
    "da": [
        "the"
    ],
    "dae": [
        "does anyone else ?"
    ],
    "wtf": [
        "what the fuck ?"
    ],
    "dam": [
        "don't annoy me"
    ],
    "daoc": [
        "dark age of camelot"
    ],
    "dbau": [
        "doing business as usual"
    ],
    "dbeyr": [
        "don't believe everything you read"
    ],
    "dc": [
        "disconnect"
    ],
    "degt": [
        "darling daughter"
    ],
    "dd": [
        "due diligence"
    ],
    "ddg": [
        "drop dead gorgeous"
    ],
    "deez": [
        "nutz"
    ],
    "derp": [
        "silly"
    ],
    "df": [
        "don't even go there"
    ],
    "dfl": [
        "dead freaking last"
    ],
    "dfntly": [
        "definitely"
    ],
    "dga": [
        "don't go anywhere"
    ],
    "dgaf": [
        "don't give a freak"
    ],
    "dgt": [
        "don't go there"
    ],
    "dgtg": [
        "don't go there, girlfriend"
    ],
    "dgyf": [
        "dang, girl you fine"
    ],
    "dh": [
        "dear husband"
    ],
    "dhu": [
        "dinosaur hugs"
    ],
    "diik": [
        "darned if i know"
    ],
    "diku": [
        "do i know you ?"
    ],
    "dilligaf": [
        "do i look like i give a freak ?"
    ],
    "dilligas": [
        "do i look like i give a sugar ?"
    ],
    "dis": [
        "did i say ?"
    ],
    "dityid": [
        "did i tell you i'm distressed ?"
    ],
    "diy": [
        "do it yourself"
    ],
    "dkdc": [
        "don't know, don't care"
    ],
    "dkp": [
        "dragon kill points"
    ],
    "dl": [
        "dead link"
    ],
    "dltbbb": [
        "don't let the bed bugs bite"
    ],
    "dm": [
        "dungeon master"
    ],
    "dmno": [
        "dude man no offense"
    ],
    "dmy": [
        "don't mess yourself"
    ],
    "dn": [
        "down"
    ],
    "Dnc": [
        "i do not understand"
    ],
    "dnr": [
        "dinner"
    ],
    "dnt": [
        "don't"
    ],
    "d00d": [
        "dude"
    ],
    "doe": [
        "daughter of eve"
    ],
    "dorbs": [
        "adorable"
    ],
    "dot": [
        "damage over time"
    ],
    "downvote": [
        "voting negatively on a thread using reddit s voting system"
    ],
    "dps": [
        "damage per second"
    ],
    "dqmot": [
        "don't quote me on this"
    ],
    "dr": [
        "didn't read"
    ],
    "ds": [
        "dear son"
    ],
    "dtr": [
        "define the relationship"
    ],
    "dtrt": [
        "do the right thing"
    ],
    "dts": [
        "don't think so"
    ],
    "dttd": [
        "don't touch that dial"
    ],
    "dupe": [
        "duplicate"
    ],
    "dur": [
        "do you remember ?"
    ],
    "dv8": [
        "deviate"
    ],
    "dw": [
        "dear wife"
    ],
    "dwf": [
        "divorced white female"
    ],
    "dwm": [
        "divorced white male"
    ],
    "dxnry": [
        "dictionary"
    ],
    "dynwutb": [
        "do you know what you are talking about ?"
    ],
    "dyfi": [
        "did you find it ?"
    ],
    "dyfm": [
        "dude, you fascinate me"
    ],
    "dyjhiw": [
        "don't you just hate it when"
    ],
    "dyor": [
        "do your own research"
    ],
    "e": [
        "enemy"
    ],
    "e1": [
        "everyone"
    ],
    "e123": [
        "easy as one, two, three"
    ],
    "e2eg": [
        "ear to ear grin"
    ],
    "eak": [
        "eating at keyboard"
    ],
    "ebkac": [
        "error between keyboard and chair"
    ],
    "ed": [
        "erase display"
    ],
    "ef4t": [
        "effort"
    ],
    "eg": [
        "evil grin"
    ],
    "ei": [
        "eat it"
    ],
    "eip": [
        "editing in progress"
    ],
    "elsw": [
        "elsewhere"
    ],
    "eli5": [
        "explain like i'm 5"
    ],
    "em": [
        "e-mail"
    ],
    "ema": [
        "e-mail address"
    ],
    "embar": [
        "embarassing"
    ],
    "emfbi": [
        "excuse me for jumping in"
    ],
    "emsg": [
        "e-mail message"
    ],
    "enuf": [
        "enough"
    ],
    "eod": [
        "end of discussion"
    ],
    "eol": [
        "end of life"
    ],
    "eom": [
        "end of message"
    ],
    "eos": [
        "end of show"
    ],
    "eot": [
        "end of transmission"
    ],
    "eq": [
        "everquest"
    ],
    "erp": [
        "erotic role-play"
    ],
    "es": [
        "erase screen"
    ],
    "esad": [
        "eat *s* and die !"
    ],
    "eta": [
        "edited to add"
    ],
    "eva": [
        "ever"
    ],
    "evo": [
        "evolution"
    ],
    "ewg": [
        "evil wicked grin"
    ],
    "ewi": [
        "emailing while intoxicated"
    ],
    "ott": [
        "over the top"
    ],
    "eyc": [
        "excitable, yet calm"
    ],
    "ezy": [
        "easy"
    ],
    "f": [
        "female"
    ],
    "f2f": [
        "face to face"
    ],
    "f2p": [
        "free to play"
    ],
    "f4f": [
        "follow for follow"
    ],
    "faak": [
        "falling asleep at keyboard"
    ],
    "fab": [
        "fabulous"
    ],
    "facepalm": [
        "smacking your forehead with your palm"
    ],
    "faf": [
        "funny as freak"
    ],
    "fly": [
        "family"
    ],
    "faq": [
        "frequently asked questions"
    ],
    "fay": [
        "freak all you"
    ],
    "fb": [
        "facebook"
    ],
    "fbb": [
        "facebook bitch"
    ],
    "fbc": [
        "facebook chat"
    ],
    "fbf": [
        "fat boy food"
    ],
    "fbfr": [
        "facebook friend"
    ],
    "fbm": [
        "fine by me"
    ],
    "fbo": [
        "facebook official"
    ],
    "fbow": [
        "for better or worse"
    ],
    "fc": [
        "full card"
    ],
    "feelsbadman": [
        "a social meme that means to feel negative."
    ],
    "feelsbatman": [
        "a social meme taking “feelsbadman” to the extreme"
    ],
    "feelsgoodman": [
        "a social meme that means to feel positive"
    ],
    "feitctaj": [
        "freak 'em if they can't take a joke"
    ],
    "ff": [
        "follow friday"
    ],
    "ffa": [
        "free for all"
    ],
    "ffs": [
        "for freak'sakes"
    ],
    "ficcl": [
        "frankly i couldn't care a less"
    ],
    "fif": [
        "freak i'm funny"
    ],
    "fiik": [
        "freaked if i know"
    ],
    "fiiooh": [
        "forget it, i'm out of here"
    ],
    "fil": [
        "father in law"
    ],
    "fimh": [
        "forever in my heart"
    ],
    "finna": [
        "going to"
    ],
    "finsta": [
        "a second instagram account"
    ],
    "fish": [
        "first in, still here"
    ],
    "fitb": [
        "fill in the blank"
    ],
    "fml": [
        "freak my life"
    ],
    "fomc": [
        "falling off my chair"
    ],
    "fomo": [
        "fear of missing out"
    ],
    "foad": [
        "freak off and die"
    ],
    "foaf": [
        "friend of a friend"
    ],
    "fomcl": [
        "falling off my chair laughing"
    ],
    "frt": [
        "for real though"
    ],
    "ftbomh": [
        "from the bottom of my heart"
    ],
    "ftfy": [
        "fixed that for you"
    ],
    "ftl": [
        "for the loss"
    ],
    "ftw": [
        "for the win"
    ],
    "fu": [
        "freak you"
    ],
    "fubar": [
        "fouled up beyond all recognition"
    ],
    "fubb": [
        "fouled up beyond belief"
    ],
    "fud": [
        "face up deal"
    ],
    "futab": [
        "feet up, take a break"
    ],
    "fw": [
        "forward"
    ],
    "fwb": [
        "friend with benefits"
    ],
    "fwiw": [
        "for what it's worth"
    ],
    "fwm": [
        "fine with me"
    ],
    "fwp": [
        "first world problems"
    ],
    "fye": [
        "fire, something that is cool"
    ],
    "fyeo": [
        "for your eyes only"
    ],
    "fya": [
        "for your amusement"
    ],
    "fyi": [
        "for your information"
    ],
    "g": [
        "giggle"
    ],
    "g+": [
        "google+"
    ],
    "g/f": [
        "girlfriend"
    ],
    "gtsy": [
        "great to see you"
    ],
    "gtg": [
        "got to go"
    ],
    "g2gicyal8er": [
        "got to go i'll see you later"
    ],
    "g2r": [
        "got to run"
    ],
    "g2tu": [
        "got to tellg4c"
    ],
    "g9": [
        "genius"
    ],
    "ga": [
        "go ahead"
    ],
    "gac": [
        "get a clue"
    ],
    "gafc": [
        "get a freaking clue"
    ],
    "gal": [
        "get a life"
    ],
    "gank": [
        "unfair player kill"
    ],
    "gas": [
        "greetings and salutations"
    ],
    "gb": [
        "goodbye"
    ],
    "gbtw": [
        "get back to work"
    ],
    "gbu": [
        "god bless you"
    ],
    "gud": [
        "good"
    ],
    "gd/r": [
        "grinning, ducking, and running"
    ],
    "gfi": [
        "go for it"
    ],
    "gf": [
        "girl friend"
    ],
    "gfn": [
        "gone for now"
    ],
    "gg": [
        "brother"
    ],
    "gga": [
        "good game, all"
    ],
    "gge1": [
        "good game everyone"
    ],
    "ggu2": [
        "good game you too"
    ],
    "ggmsot": [
        "gotta get me some of that"
    ],
    "ggoh": [
        "gotta get outa here"
    ],
    "ggp": [
        "got to go pee"
    ],
    "gh": [
        "good hand"
    ],
    "giar": [
        "give it a rest"
    ],
    "gic": [
        "gift in crib"
    ],
    "gigo": [
        "garbage in, garbage out"
    ],
    "girl": [
        "guy in real life"
    ],
    "gj": [
        "good job"
    ],
    "gl": [
        "good luck"
    ],
    "gl2u": [
        "good luck to you"
    ],
    "gla": [
        "good luck all"
    ],
    "gl/hf": [
        "good luck, have fun"
    ],
    "gle1": [
        "good luck everyone"
    ],
    "glng": [
        "good luck next game"
    ],
    "gmba": [
        "giggling my butt off"
    ],
    "gmta": [
        "great minds think alike"
    ],
    "gmv": [
        "got my vote"
    ],
    "gnite": [
        "good night"
    ],
    "gna": [
        "good night all"
    ],
    "gne1": [
        "good night everyone"
    ],
    "gnsd": [
        "good night, sweet dreams"
    ],
    "goat": [
        "greatest of all times"
    ],
    "goi": [
        "get over it"
    ],
    "gol": [
        "giggling out loud"
    ],
    "gomb": [
        "get off my back"
    ],
    "gpoy": [
        "gratuitous picture of yourself"
    ],
    "gr8": [
        "great"
    ],
    "gr8est": [
        "greatest"
    ],
    "gratz": [
        "congratulations"
    ],
    "grl": [
        "girl"
    ],
    "grwg": [
        "get right with god"
    ],
    "gr&d": [
        "grinning, running and ducking"
    ],
    "gs": [
        "good split"
    ],
    "gt": [
        "good try"
    ],
    "gtfo": [
        "get the freak out"
    ],
    "gtfoh": [
        "get the freak outta here"
    ],
    "gtm": [
        "giggling to myself"
    ],
    "gtrm": [
        "going to read mail"
    ],
    "gwhtlc": [
        "glad we had this little chat"
    ],
    "h": [
        "hug"
    ],
    "h8": [
        "hate"
    ],
    "h8ttu": [
        "hate to be you"
    ],
    "hago": [
        "have a good one"
    ],
    "hak": [
        "hug and kiss"
    ],
    "halp": [
        "help"
    ],
    "hbu": [
        "how about you ?"
    ],
    "xoxoxo": [
        "hugs & kisses"
    ],
    "h2cus": [
        "hope to see you soon"
    ],
    "hagn": [
        "have a good night"
    ],
    "hand": [
        "have a nice day"
    ],
    "hb": [
        "hug back"
    ],
    "h-bday": [
        "happy birthday"
    ],
    "hf": [
        "have fun"
    ],
    "hfac": [
        "holy flipping animal crackers"
    ],
    "h-fday": [
        "happy father's day"
    ],
    "hhis": [
        "head hanging in shame"
    ],
    "hifw": [
        "how i felt when"
    ],
    "hl": [
        "half life"
    ],
    "h-mday": [
        "happy mother's day"
    ],
    "hmu": [
        "hit me up"
    ],
    "hnl": [
        "(w)hole another level"
    ],
    "hoas": [
        "hold on a second"
    ],
    "hp": [
        "hit points / health points"
    ],
    "hru": [
        "how are you ?"
    ],
    "hth": [
        "hope this helps"
    ],
    "hub": [
        "head up butt"
    ],
    "huya": [
        "head up your butt"
    ],
    "hv": [
        "have"
    ],
    "hvh": [
        "heroic violet hold"
    ],
    "hw": [
        "homework"
    ],
    "hyfr": [
        "hell yeah, freaking right !"
    ],
    "I2": [
        "i too"
    ],
    "i2": [
        "me too"
    ],
    "Ia8": [
        "i already ate"
    ],
    "Iaaa": [
        "i am an accountant"
    ],
    "Iaad": [
        "i am a doctor"
    ],
    "Iaal": [
        "i am a lawyer"
    ],
    "iac": [
        "in any case"
    ],
    "iae": [
        "in any event"
    ],
    "Ianac": [
        "i am not a crook"
    ],
    "Ianal": [
        "i am not a lawyer"
    ],
    "Iao": [
        "i am out"
    ],
    "ib": [
        "i'm back"
    ],
    "Ic": [
        "i see"
    ],
    "Icam": [
        "i couldn't agree more"
    ],
    "icbw": [
        "it could be worse"
    ],
    "Icedi": [
        "i can't even discuss it"
    ],
    "Icfilwu": [
        "i could fall in love with you"
    ],
    "icymi": [
        "in case you missed it"
    ],
    "Idbi": [
        "i don't believe it"
    ],
    "Idc": [
        "i don't care"
    ],
    "Idgaf": [
        "i don't give a freak"
    ],
    "Idts": [
        "i don't think so"
    ],
    "Ifyp": [
        "i feel your pain"
    ],
    "ig": [
        "instagram"
    ],
    "Ig2R": [
        "i got to run"
    ],
    "Ight": [
        "i got high tonight"
    ],
    "ign": [
        "i've got nothing"
    ],
    "Igp": [
        "i got to go pee"
    ],
    "Ihni": [
        "i have no idea"
    ],
    "iirc": [
        "if i remember correctly"
    ],
    "iiio": [
        "intel inside idiot outside"
    ],
    "Ik": [
        "i know"
    ],
    "ilbl8": [
        "i'll be late"
    ],
    "Ilum": [
        "i love you man"
    ],
    "Ilysm": [
        "i love you so much"
    ],
    "im": [
        "instant message"
    ],
    "imao": [
        "in my arrogant opinion"
    ],
    "imho": [
        "in my humble opinion"
    ],
    "imnsho": [
        "in my not so humble opinion"
    ],
    "imo": [
        "in my opinion"
    ],
    "Ims": [
        "i am sorry"
    ],
    "Imsb": [
        "i am so bored"
    ],
    "Imtm": [
        "i am the man"
    ],
    "Imu": [
        "i miss you"
    ],
    "inal": [
        "i'm not a lawyer"
    ],
    "inc": [
        "incoming"
    ],
    "inspoo": [
        "inspiration"
    ],
    "inv": [
        "invite"
    ],
    "iomh": [
        "in over my head"
    ],
    "iow": [
        "in other words"
    ],
    "irl": [
        "in real life"
    ],
    "Irmc": [
        "i rest my case"
    ],
    "Isly": [
        "i still love you"
    ],
    "iso": [
        "in search of"
    ],
    "itam": [
        "it's the accounting man"
    ],
    "itt": [
        "in this thread"
    ],
    "Ityk": [
        "i thought you knew"
    ],
    "iyss": [
        "if you say so"
    ],
    "Iwalu": [
        "i will always love you"
    ],
    "Iwawo": [
        "i want a way out"
    ],
    "iwiam": [
        "idiot wrapped in a moron"
    ],
    "Iwsn": [
        "i want sex now"
    ],
    "iykwim": [
        "if you know what i mean"
    ],
    "iyo": [
        "in your opinion"
    ],
    "Iyq": [
        "i like you"
    ],
    "yr": [
        "yeah right"
    ],
    "jas": [
        "just a second"
    ],
    "jam": [
        "just a minute"
    ],
    "jc": [
        "just checking"
    ],
    "jdi": [
        "just do it"
    ],
    "jelly": [
        "jealous"
    ],
    "jff": [
        "just for fun"
    ],
    "jfgi": [
        "just freaking google it"
    ],
    "jic": [
        "just in case"
    ],
    "jj": [
        "just joking"
    ],
    "jja": [
        "just joking around"
    ],
    "jkz": [
        "just kidding"
    ],
    "jlmk": [
        "just let me know"
    ],
    "jmo": [
        "just my opinion"
    ],
    "jp": [
        "jackpot"
    ],
    "jt": [
        "just teasing"
    ],
    "jtlyk": [
        "just to let you know"
    ],
    "jv": [
        "joint venture"
    ],
    "jw": [
        "just wondering"
    ],
    "ok": [
        "okay"
    ],
    "kk": [
        "knock knock"
    ],
    "kt": [
        "katie"
    ],
    "kb": [
        "kick butt"
    ],
    "kdfu": [
        "cracking the da freak up"
    ],
    "kewl": [
        "cool"
    ],
    "Keya": [
        "i will key you later"
    ],
    "keyme": [
        "key me when you get in"
    ],
    "kfy": [
        "kiss for you"
    ],
    "kia": [
        "know it all"
    ],
    "kir": [
        "keep it real"
    ],
    "kiss": [
        "keep it simple stupid"
    ],
    "kit": [
        "keep in touch"
    ],
    "kma": [
        "kiss my ass"
    ],
    "kmk": [
        "kiss my keister"
    ],
    "kms": [
        "killing myself"
    ],
    "kmt": [
        "kiss my tushie"
    ],
    "koc": [
        "kiss on cheek"
    ],
    "kol": [
        "key opinion leader"
    ],
    "koreaboo": [
        "obsessed with korean culture"
    ],
    "kos": [
        "kill on sight"
    ],
    "kow": [
        "knock on wood"
    ],
    "kotc": [
        "kiss on the cheek"
    ],
    "kotd": [
        "kicks of the day"
    ],
    "kotl": [
        "kiss on the lips"
    ],
    "knim": [
        "know what i mean ?"
    ],
    "nowl": [
        "knowledge"
    ],
    "kpc": [
        "keeping parents clueless"
    ],
    "ks": [
        "kill then steal"
    ],
    "ksc": [
        "kind of chuckle"
    ],
    "kutgw": [
        "keep up the good work"
    ],
    "kys": [
        "kill yourself"
    ],
    "l2g": [
        "love to go"
    ],
    "l2k": [
        "like to come"
    ],
    "l2p": [
        "learn to play"
    ],
    "l4l": [
        "like for like"
    ],
    "l8r": [
        "later"
    ],
    "l8rg8r": [
        "later gator"
    ],
    "lab": [
        "life's a bitch"
    ],
    "lbay": [
        "laughing back at you"
    ],
    "lbs": [
        "laughing but serious"
    ],
    "lbvs": [
        "laughing but very serious"
    ],
    "ld": [
        "long distance"
    ],
    "ldo": [
        "like duh obviously"
    ],
    "lerk": [
        "leaving easy reach of keyboard"
    ],
    "lfd": [
        "left for day"
    ],
    "lfg": [
        "looking for guard"
    ],
    "lfm": [
        "looking for more"
    ],
    "lhsx": [
        "lets have sex"
    ],
    "lhm": [
        "lord help me"
    ],
    "lho": [
        "laughing head off"
    ],
    "li": [
        "linkedin"
    ],
    "lic": [
        "like i care"
    ],
    "lik": [
        "liquor"
    ],
    "limt": [
        "laugh in my tummy"
    ],
    "lit": [
        "extremely intoxicated"
    ],
    "lls": [
        "laughing like silly"
    ],
    "lmao": [
        "laughing my ass off"
    ],
    "lmbo": [
        "laughing my butt off"
    ],
    "lmirl": [
        "lets meet in real life"
    ],
    "lmmfao": [
        "laughing my mother freaking ass off"
    ],
    "lmnk": [
        "leave my name out"
    ],
    "lms": [
        "like my status"
    ],
    "lnt": [
        "lost in translation"
    ],
    "loa": [
        "list of acronyms"
    ],
    "lol": [
        "laugh out loud"
    ],
    "lolo": [
        "lots of love"
    ],
    "lolh": [
        "laughing out loud hysterically"
    ],
    "lolwtf": [
        "laughing out loud (saying) what the freak ?"
    ],
    "loti": [
        "laughing on the inside"
    ],
    "lotr": [
        "lord of the rings"
    ],
    "lqtm": [
        "laughing quietly to myself"
    ],
    "lshmbh": [
        "laugh so hard my belly hurts"
    ],
    "lsv": [
        "language sex and violence"
    ],
    "ltd": [
        "living the dream"
    ],
    "ltlwdls": [
        "let's twist like we did last summer"
    ],
    "ltns": [
        "long time no see"
    ],
    "ltod": [
        "laptop of death"
    ],
    "lts": [
        "laughing to self"
    ],
    "lult": [
        "love you long time"
    ],
    "lulz": [
        "joke"
    ],
    "lvm": [
        "left voice mail"
    ],
    "lwos": [
        "laughing without smiling"
    ],
    "ly": [
        "love ya"
    ],
    "lylas": [
        "love you like a sis"
    ],
    "lylc": [
        "love you like crazy"
    ],
    "lysm": [
        "love you so much"
    ],
    "m$": [
        "microsoft"
    ],
    "m8": [
        "mate"
    ],
    "momboy": [
        "mamma's boy"
    ],
    "mbs": [
        "mom behind shoulder"
    ],
    "mc": [
        "merry christmas"
    ],
    "mdiac": [
        "my dad is a cop"
    ],
    "mego": [
        "my eyes glaze over"
    ],
    "meh": [
        "just okay"
    ],
    "mehh": [
        "sigh"
    ],
    "mez": [
        "mesmerize"
    ],
    "mfi": [
        "mad for it"
    ],
    "mfw": [
        "my face when"
    ],
    "mgb": [
        "may god bless"
    ],
    "mgmt": [
        "management"
    ],
    "mhoty": [
        "my hat is off to you"
    ],
    "mirl": [
        "meet in real life"
    ],
    "mkay": [
        "mmm okay"
    ],
    "mlm": [
        "give the middle finger"
    ],
    "sis": [
        "snickering in silence"
    ],
    "mmk": [
        "okay ?"
    ],
    "mnc": [
        "mother nature calls"
    ],
    "mnsg": [
        "mensaje"
    ],
    "mod": [
        "modification"
    ],
    "morf": [
        "male or female ?"
    ],
    "moo": [
        "my own opinion"
    ],
    "moos": [
        "member of the opposite sex"
    ],
    "mos": [
        "mother over shoulder"
    ],
    "moss": [
        "member of same sex"
    ],
    "mp": [
        "mana points"
    ],
    "mr.(number)": [
        "mr.3 would be a 3-year old son"
    ],
    "mrt": [
        "modified retweet"
    ],
    "mrw": [
        "my reaction when"
    ],
    "msg": [
        "message"
    ],
    "mtf": [
        "more to follow"
    ],
    "mtfbwu": [
        "may the force be with you"
    ],
    "mu": [
        "miss you"
    ],
    "muah": [
        "multiple unsuccessful attempts at humor"
    ],
    "musm": [
        "miss you so much"
    ],
    "x": [
        "kiss"
    ],
    "myo": [
        "mind your own"
    ],
    "myob": [
        "mind your own business"
    ],
    "n00b": [
        "newbie"
    ],
    "n1": [
        "nice one"
    ],
    "n2m": [
        "nothing too much"
    ],
    "nadt": [
        "not a darn thing"
    ],
    "nalopkt": [
        "not a lot of people know that"
    ],
    "nana": [
        "not now no need"
    ],
    "n/a": [
        "not applicable"
    ],
    "nbd": [
        "no big deal"
    ],
    "nbfab": [
        "no bad for a beginner"
    ],
    "nc": [
        "nice crib"
    ],
    "nd": [
        "nice double"
    ],
    "ne": [
        "any"
    ],
    "ne1": [
        "anyone"
    ],
    "nerf": [
        "changed and is now weaker"
    ],
    "nfm": [
        "not for me"
    ],
    "ngl": [
        "not gonna lie"
    ],
    "nfs": [
        "not for sale"
    ],
    "nfw": [
        "not for work"
    ],
    "nfws": [
        "not for work safe"
    ],
    "nh": [
        "nice hand"
    ],
    "nifoc": [
        "naked in front of computer"
    ],
    "nigi": [
        "now i get it"
    ],
    "nimby": [
        "not in my back yard"
    ],
    "nirok": [
        "not in reach of keyboard"
    ],
    "nlt": [
        "no later than"
    ],
    "nmh": [
        "not much here"
    ],
    "nmjc": [
        "nothing much just chilling"
    ],
    "nmu": [
        "not much you ?"
    ],
    "no1": [
        "no one"
    ],
    "noob": [
        "bad at games"
    ],
    "noyb": [
        "none of your business"
    ],
    "np": [
        "no problem"
    ],
    "npc": [
        "non-playing character"
    ],
    "nqt": [
        "newly qualified teacher"
    ],
    "nr": [
        "nice roll"
    ],
    "nrn": [
        "no reply necessary"
    ],
    "ns": [
        "nice split"
    ],
    "nsa": [
        "no strings attached"
    ],
    "nsfl": [
        "not safe for life"
    ],
    "nsfw": [
        "not safe for work"
    ],
    "nsisr": [
        "not sure if spelled right"
    ],
    "nt": [
        "nice try"
    ],
    "nthing": [
        "nothing"
    ],
    "nvr": [
        "never"
    ],
    "nw": [
        "no way"
    ],
    "nwo": [
        "no way out"
    ],
    "o4u": [
        "only for you"
    ],
    "o": [
        "hugs"
    ],
    "oa": [
        "online auctions"
    ],
    "oatus": [
        "on a totally unrelated subject"
    ],
    "ob": [
        "oh brother"
    ],
    "obv": [
        "obviously"
    ],
    "og": [
        "original gangster"
    ],
    "ogim": [
        "oh god, it's monday"
    ],
    "oh": [
        "overheard"
    ],
    "zomg": [
        "oh my god"
    ],
    "oi": [
        "operator indisposed"
    ],
    "oib": [
        "oh, i'm back"
    ],
    "oic": [
        "oh, i see"
    ],
    "oj": [
        "only joking"
    ],
    "ol": [
        "old lady"
    ],
    "oll": [
        "online love"
    ],
    "om": [
        "oh my"
    ],
    "omaa": [
        "oh my aching ass"
    ],
    "omdb": [
        "over my dead body"
    ],
    "omfg": [
        "oh my freaking god"
    ],
    "omg": [
        "oh my gosh"
    ],
    "omgyg2bk": [
        "oh my god, you got to be kidding"
    ],
    "omgys": [
        "oh my gosh you suck"
    ],
    "oms": [
        "on my soul"
    ],
    "omw": [
        "on my way"
    ],
    "onl": [
        "online"
    ],
    "oo": [
        "over and out"
    ],
    "ooc": [
        "out of character"
    ],
    "ooh": [
        "out of here"
    ],
    "oomf": [
        "one of my followers"
    ],
    "ootd": [
        "outfit of the day"
    ],
    "ooto": [
        "out of the office"
    ],
    "op": [
        "on phone"
    ],
    "orly": [
        "oh really ?"
    ],
    "os": [
        "operating system"
    ],
    "ot": [
        "off topic"
    ],
    "otb": [
        "off to bed"
    ],
    "otfl": [
        "on the floor laughing"
    ],
    "otl": [
        "out to lunch"
    ],
    "otoh": [
        "on the other hand"
    ],
    "otp": [
        "one true pairing; two people you would love to see as a couple"
    ],
    "ottomh": [
        "off the top of my head"
    ],
    "otw": [
        "off to work"
    ],
    "oyo": [
        "on your own"
    ],
    "p": [
        "partner"
    ],
    "p2p": [
        "pay to play"
    ],
    "p911": [
        "parents coming into room alert"
    ],
    "pap": [
        "post a picture"
    ],
    "pat": [
        "patrol"
    ],
    "prw": [
        "people are watching"
    ],
    "pbook": [
        "phonebook"
    ],
    "pc": [
        "player character"
    ],
    "pcm": [
        "please call me"
    ],
    "pda": [
        "personal display of affection"
    ],
    "pdh": [
        "pretty darn happy"
    ],
    "pds": [
        "please don't shoot"
    ],
    "pdq": [
        "pretty darn quick"
    ],
    "ppl": [
        "people"
    ],
    "pft": [
        "pretty freaking tight"
    ],
    "pic": [
        "picture"
    ],
    "pics": [
        "pictures"
    ],
    "pip": [
        "peeing in pants"
    ],
    "pir": [
        "parents in room"
    ],
    "piss": [
        "put in some sugar"
    ],
    "pita": [
        "pain in the ass"
    ],
    "pkmn": [
        "pokemon"
    ],
    "pl8": [
        "plate"
    ],
    "pld": [
        "played"
    ],
    "plmk": [
        "please let me know"
    ],
    "plz": [
        "please"
    ],
    "plu": [
        "people like us"
    ],
    "plztlme": [
        "please tell me"
    ],
    "pm": [
        "private message"
    ],
    "pmfi": [
        "pardon me for interrupting"
    ],
    "pmfji": [
        "pardon me for jumping in"
    ],
    "pmsl": [
        "pee myself laughing"
    ],
    "poahf": [
        "put on a happy face"
    ],
    "poidh": [
        "picture or it didn't happen"
    ],
    "pos": [
        "parent over shoulder"
    ],
    "pot": [
        "potion"
    ],
    "potd": [
        "photo of the day"
    ],
    "pov": [
        "privately owned vehicle"
    ],
    "ppu": [
        "pending pick-up"
    ],
    "presh": [
        "precious"
    ],
    "prolly": [
        "probably"
    ],
    "proggy": [
        "computer program"
    ],
    "porn": [
        "pornography"
    ],
    "prt": [
        "please retweet"
    ],
    "psa": [
        "public service announcement"
    ],
    "psos": [
        "parent standing over shoulder"
    ],
    "psp": [
        "playstation portable"
    ],
    "pst": [
        "please send tell"
    ],
    "ptfo": [
        "pass the freak out"
    ],
    "ptiypasi": [
        "put that in your pipe and smoke it"
    ],
    "ptl": [
        "praise the lord"
    ],
    "ptmm": [
        "please tell me more"
    ],
    "pto": [
        "parent teacher organization"
    ],
    "pug": [
        "pick up group"
    ],
    "pve": [
        "player vs enemy, player versus environment"
    ],
    "pvp": [
        "player versus player"
    ],
    "pwn": [
        "own"
    ],
    "pxt": [
        "please explain that"
    ],
    "pu": [
        "that stinks !"
    ],
    "puks": [
        "pick up kids"
    ],
    "pyt": [
        "pretty young thing"
    ],
    "pz": [
        "peace"
    ],
    "pza": [
        "pizza"
    ],
    "q": [
        "queue"
    ],
    "qc": [
        "quality control"
    ],
    "qfe": [
        "question for everyone"
    ],
    "qfi": [
        "quoted for irony"
    ],
    "qft": [
        "quoted for truth"
    ],
    "qik": [
        "quick"
    ],
    "ql": [
        "quit laughing"
    ],
    "qotd": [
        "quote of the day"
    ],
    "q_q": [
        "crying eyes"
    ],
    "qq": [
        "quick question"
    ],
    "qsl": [
        "reply"
    ],
    "qso": [
        "conversation"
    ],
    "qt": [
        "cutie"
    ],
    "qtpi": [
        "cutie pie"
    ],
    "r": [
        "are"
    ],
    "r8": [
        "rate"
    ],
    "rbay": [
        "right back at you"
    ],
    "rfn": [
        "right freaking now"
    ],
    "Rgr": [
        "i agree"
    ],
    "rhip": [
        "rank has its privileges"
    ],
    "rip": [
        "rest in peace"
    ],
    "rl": [
        "real life"
    ],
    "rly": [
        "really"
    ],
    "rme": [
        "rolling my eyes"
    ],
    "rmlb": [
        "read my lips baby"
    ],
    "rmmm": [
        "read my mail man"
    ],
    "roflcopter": [
        "rolling on floor laughing and spinning around"
    ],
    "roflmao": [
        "rolling on the floor, laughing my ass off"
    ],
    "rotfl": [
        "rolling on the floor laughing"
    ],
    "rotfluts": [
        "rolling on the floor laughing unable to speak"
    ],
    "rs": [
        "runescape"
    ],
    "rsn": [
        "real soon now"
    ],
    "rt": [
        "retweet"
    ],
    "rtbs": [
        "reason to be single"
    ],
    "rtfm": [
        "read the freaking manual"
    ],
    "rtfq": [
        "read the freaking question"
    ],
    "rthx": [
        "thanks for the rt"
    ],
    "rtms": [
        "read the manual, stupid"
    ],
    "rtntn": [
        "retention"
    ],
    "rtrctv": [
        "retroactive"
    ],
    "rtrmt": [
        "retirement"
    ],
    "rtsm": [
        "read the stupid manual"
    ],
    "rtwfq": [
        "read the whole freaking question"
    ],
    "ru": [
        "are you ?"
    ],
    "rumof": [
        "are you male or female ?"
    ],
    "ruok": [
        "are you okay ?"
    ],
    "rx": [
        "prescriptions"
    ],
    "rw": [
        "real world"
    ],
    "ryo": [
        "roll your own"
    ],
    "rys": [
        "are you single ?"
    ],
    "s2r": [
        "send to receive"
    ],
    "s2s": [
        "sorry to say"
    ],
    "s4l": [
        "spam for life"
    ],
    "sal": [
        "such a laugh"
    ],
    "sat": [
        "sorry about that"
    ],
    "savage": [
        "shockingly careless expression or response to an event or message"
    ],
    "sb": [
        "smiling back"
    ],
    "sbia": [
        "standing back in amazement"
    ],
    "sbt": [
        "sorry 'bout that"
    ],
    "sc": [
        "stay cool"
    ],
    "sd": [
        "sweet dreams"
    ],
    "sdmb": [
        "sweet dreams, my baby"
    ],
    "senpai": [
        "someone older than you"
    ],
    "seo": [
        "search engine optimization"
    ],
    "sete": [
        "smiling ear-to-ear"
    ],
    "selfie": [
        "a photo that is taken of oneself for social media sharing"
    ],
    "sfaik": [
        "so far as i know"
    ],
    "sh": [
        "same here"
    ],
    "su": [
        "shut up"
    ],
    "shid": [
        "slapping head in disgust"
    ],
    "ship": [
        "wishing two people were in a relationship"
    ],
    "sicnr": [
        "sorry, i could'nt resist"
    ],
    "sig2r": [
        "sorry, i got to run"
    ],
    "sihth": [
        "stupidity is hard to take"
    ],
    "simyc": [
        "sorry i missed your call"
    ],
    "sir": [
        "strike it rich"
    ],
    "sit": [
        "stay in touch"
    ],
    "sitd": [
        "still in the dark"
    ],
    "sjw": [
        "social justice warrior"
    ],
    "sk8": [
        "skate"
    ],
    "sk8ng": [
        "skating"
    ],
    "sk8r": [
        "skater"
    ],
    "sk8rboi": [
        "skater boy"
    ],
    "slap": [
        "sounds like a plan"
    ],
    "slay": [
        "to succeed at something"
    ],
    "sm": [
        "social media"
    ],
    "smazed": [
        "smoky haze"
    ],
    "smexi": [
        "sexy mexican"
    ],
    "smhid": [
        "scratching my head in disbelief"
    ],
    "snafu": [
        "situation normal all fouled up"
    ],
    "snert": [
        "snot nosed egotistical rude teenager"
    ],
    "snr": [
        "streaks and recents"
    ],
    "so": [
        "significant other"
    ],
    "soab": [
        "son of a bitch"
    ],
    "s’ok": [
        "it's okay"
    ],
    "sol": [
        "sooner or later"
    ],
    "somy": [
        "sick of me yet ?"
    ],
    "sorg": [
        "straight or gay ?"
    ],
    "Sos": [
        "i need help"
    ],
    "sos": [
        "son of sam"
    ],
    "sot": [
        "short of time"
    ],
    "sotmg": [
        "short of time, must go"
    ],
    "sowm": [
        "someone with me"
    ],
    "spk": [
        "speak"
    ],
    "srsly": [
        "seriously"
    ],
    "spst": [
        "same place, same time"
    ],
    "spto": [
        "spoke to"
    ],
    "sq": [
        "square"
    ],
    "sry": [
        "sorry"
    ],
    "ss": [
        "so sorry"
    ],
    "ssdd": [
        "same stuff, different day"
    ],
    "ssif": [
        "so stupid it's funny"
    ],
    "ssinf": [
        "so stupid it's not funny"
    ],
    "st&d": [
        "stop texting and drive"
    ],
    "stan": [
        "fan of someone"
    ],
    "str8": [
        "straight"
    ],
    "stw": [
        "search the web"
    ],
    "suitm": [
        "see you in the morning"
    ],
    "zup": [
        "what's up"
    ],
    "suth": [
        "so used to haters"
    ],
    "suyf": [
        "shut up you fool"
    ],
    "swag": [
        "scientific wild ass guess"
    ],
    "swak": [
        "sent with a kiss"
    ],
    "swalk": [
        "sealed with a loving kiss"
    ],
    "swat": [
        "scientific wild butt guess"
    ],
    "swl": [
        "screaming with laughter"
    ],
    "swmbo": [
        "she who must be obeyed"
    ],
    "sys": [
        "see you soon"
    ],
    "sux": [
        "it sucks"
    ],
    "syy": [
        "shut your yapper"
    ],
    "t+": [
        "think positive"
    ],
    "t4bu": [
        "thanks for being you"
    ],
    "tht": [
        "think happy thoughts"
    ],
    "ta": [
        "thanks a lot"
    ],
    "tafn": [
        "that's all for now"
    ],
    "tam": [
        "tomorro a.m."
    ],
    "tank": [
        "really strong"
    ],
    "tanked": [
        "owned"
    ],
    "tanking": [
        "owning"
    ],
    "tarfu": [
        "things are really fouled up"
    ],
    "tau": [
        "thinking about you"
    ],
    "taumualu": [
        "thinking about you miss you always love you"
    ],
    "tba": [
        "to be announced"
    ],
    "tbag": [
        "process of disgracing a corpse, taunting a fragged/killed player"
    ],
    "tbbh": [
        "to be brutally honest"
    ],
    "tbc": [
        "to be continued"
    ],
    "tbd": [
        "to be determined"
    ],
    "tbh": [
        "to be honest"
    ],
    "tbl": [
        "text back later"
    ],
    "tbt": [
        "throwback thursday"
    ],
    "tc": [
        "take care"
    ],
    "tcb": [
        "take care of business"
    ],
    "tcoy": [
        "take care of yourself"
    ],
    "td": [
        "tower defense"
    ],
    "tdtm": [
        "talk dirty to me"
    ],
    "tea": [
        "gossip"
    ],
    "tff": [
        "too freaking funny"
    ],
    "tfs": [
        "thanks for sharing"
    ],
    "tftf": [
        "thanks for the follow"
    ],
    "tfti": [
        "thanks for the invitation"
    ],
    "tftt": [
        "thanks for this tweet"
    ],
    "tg": [
        "thank goodness"
    ],
    "tgif": [
        "thank god it's friday"
    ],
    "thnq": [
        "thank-you"
    ],
    "thot": [
        "that whore over there"
    ],
    "tia": [
        "thanks in advance"
    ],
    "tiad": [
        "tomorrow is another day"
    ],
    "tic": [
        "tongue-in-cheek"
    ],
    "til": [
        "today i learned"
    ],
    "tilis": [
        "tell it like it is"
    ],
    "tir": [
        "teacher in room"
    ],
    "ttyl": [
        "talk to you later"
    ],
    "tl": [
        "too long"
    ],
    "tl;dr": [
        "too long; didn't read"
    ],
    "tm": [
        "trust me"
    ],
    "tma": [
        "take my advice"
    ],
    "tmb": [
        "tweet me back"
    ],
    "tmot": [
        "trust me on this"
    ],
    "tmyl": [
        "tell me your location"
    ],
    "tmwfi": [
        "take my word for it"
    ],
    "tnstaafl": [
        "there's no such thing as a free lunch"
    ],
    "tnt": [
        "til next time"
    ],
    "toj": [
        "tears of joy"
    ],
    "tos": [
        "terms of service"
    ],
    "ttly": [
        "totally"
    ],
    "toy": [
        "thinking of you"
    ],
    "tpm": [
        "tomorrow p.m."
    ],
    "tptb": [
        "the powers that be"
    ],
    "tsh": [
        "tripping so hard"
    ],
    "tsnf": [
        "that's so not fair"
    ],
    "tstb": [
        "the sooner, the better"
    ],
    "tt": [
        "trending topic"
    ],
    "ttfn": [
        "ta ta for now"
    ],
    "tttt": [
        "these things take time"
    ],
    "tui": [
        "turning you in"
    ],
    "yeet": [
        "excitement"
    ],
    "twss": [
        "that's what she said"
    ],
    "ttg": [
        "time to go"
    ],
    "ttyafn": [
        "talk to you awhile from now"
    ],
    "ttys": [
        "talk to you soon"
    ],
    "tyfc": [
        "thank you for charity"
    ],
    "tyfyc": [
        "thank you for your comment"
    ],
    "tys": [
        "told you so"
    ],
    "tyt": [
        "take your time"
    ],
    "tyso": [
        "thank you so much"
    ],
    "tyafy": [
        "thank you and freak you"
    ],
    "tyvm": [
        "thank you very much"
    ],
    "u": [
        "you"
    ],
    "^urs": [
        "up yours"
    ],
    "ycmu": [
        "you crack me up"
    ],
    "udi": [
        "unidentified drinking injury"
    ],
    "udm": [
        "you the man"
    ],
    "uds": [
        "ugly domestic scene"
    ],
    "ufb": [
        "un freaking believable"
    ],
    "ufn": [
        "until further notice"
    ],
    "ufwm": [
        "you freaking with me ?"
    ],
    "ugtbk": [
        "you've got to be kidding"
    ],
    "uhgtbsm": [
        "you have got to be s#$t*ing me !"
    ],
    "uktr": [
        "you know that's right"
    ],
    "ul": [
        "upload"
    ],
    "u-l": [
        "you will"
    ],
    "una": [
        "use no acronyms"
    ],
    "un4tun8": [
        "unfortunate"
    ],
    "unblefble": [
        "unbelievable"
    ],
    "uncrtn": [
        "uncertain"
    ],
    "unpc": [
        "not politically correct"
    ],
    "up2u": [
        "up to you"
    ],
    "uok": [
        "are you ok ?"
    ],
    "ur": [
        "you're"
    ],
    "ur2ys4me": [
        "you are too wise for me"
    ],
    "ura*": [
        "you are a star"
    ],
    "urh": [
        "you are hot"
    ],
    "ursktm": [
        "you are so kind to me"
    ],
    "urtm": [
        "you are the man"
    ],
    "urw": [
        "you are welcome"
    ],
    "usbca": [
        "until something better comes along"
    ],
    "usu": [
        "usually"
    ],
    "ut": [
        "unreal tournament"
    ],
    "yttl": [
        "you take too long"
    ],
    "utm": [
        "you tell me"
    ],
    "uv": [
        "unpleasant visual"
    ],
    "yw": [
        "you're welcome"
    ],
    "ux": [
        "user experience"
    ],
    "v": [
        "very"
    ],
    "veggie": [
        "vegetarian"
    ],
    "vat": [
        "value added tax"
    ],
    "vbl": [
        "visible bra line"
    ],
    "vbs": [
        "very big smile"
    ],
    "vc": [
        "voice chat"
    ],
    "veg": [
        "very evil grin"
    ],
    "vff": [
        "very freaking funny"
    ],
    "vfm": [
        "value for money"
    ],
    "vgc": [
        "very good condition"
    ],
    "vgg": [
        "very good game"
    ],
    "vgh": [
        "very good hand"
    ],
    "vip": [
        "very important person"
    ],
    "vm": [
        "voice mail"
    ],
    "vn": [
        "very nice"
    ],
    "vnh": [
        "very nice hand"
    ],
    "voip": [
        "voice over internet protocol"
    ],
    "vsc": [
        "very soft chuckle"
    ],
    "vsf": [
        "very sad face"
    ],
    "vwd": [
        "very well done"
    ],
    "vwp": [
        "very well played"
    ],
    "w@?": [
        "what ?"
    ],
    "wat": [
        "what"
    ],
    "wb": [
        "welcome back"
    ],
    "w/b": [
        "write back"
    ],
    "w3": [
        "www"
    ],
    "w8": [
        "wait"
    ],
    "wah": [
        "working at home"
    ],
    "waj": [
        "what a jerk"
    ],
    "wam": [
        "wait a minute"
    ],
    "wan2": [
        "want to ?"
    ],
    "wan2tlk": [
        "want to talk"
    ],
    "warez": [
        "pirated software"
    ],
    "was": [
        "wild ass guess"
    ],
    "wawa": [
        "where are we at ?"
    ],
    "wuf": [
        "where are you from ?"
    ],
    "wbs": [
        "write back soon"
    ],
    "wbu": [
        "what about you ?"
    ],
    "wc": [
        "who cares"
    ],
    "wca": [
        "who cares anyway"
    ],
    "whateves": [
        "whatever"
    ],
    "wkd": [
        "weekend"
    ],
    "webo": [
        "webopedia"
    ],
    "weebo": [
        "obsessed with of japanese culture"
    ],
    "wep": [
        "weapon"
    ],
    "wibni": [
        "wouldn't it be nice if"
    ],
    "wdalyic": [
        "who died and left you in charge"
    ],
    "wdyk": [
        "what do you know ?"
    ],
    "wgaca": [
        "what do you think ?"
    ],
    "wfm": [
        "works for me"
    ],
    "wiifm": [
        "what's in it for me ?"
    ],
    "wisp": [
        "winning is so pleasurable"
    ],
    "witp": [
        "what is the point ?"
    ],
    "witw": [
        "what in the world"
    ],
    "wiu": [
        "wrap it up"
    ],
    "wk": [
        "week"
    ],
    "wrt": [
        "with regard to"
    ],
    "wl": [
        "whatta loser"
    ],
    "w/o": [
        "without"
    ],
    "woa": [
        "work of art"
    ],
    "woke": [
        "people who are aware of current social issues and politics"
    ],
    "wombat": [
        "waste of money brains and time"
    ],
    "wrk": [
        "work"
    ],
    "wru": [
        "where are you ?"
    ],
    "wru@": [
        "where are you at ?"
    ],
    "wyd": [
        "what are you doing ?"
    ],
    "wtb": [
        "want to buy"
    ],
    "wtfe": [
        "what the freak ever"
    ],
    "wtfo": [
        "what the freak ? over."
    ],
    "wtg": [
        "way to go"
    ],
    "wtgp": [
        "want to go private"
    ],
    "wth": [
        "what the heck ?"
    ],
    "wtm": [
        "who's the man ?"
    ],
    "wts": [
        "want to sell ?"
    ],
    "wtt": [
        "want to trade ?"
    ],
    "wysiwyg": [
        "what you see is what you get"
    ],
    "wuw": [
        "what you want ?"
    ],
    "wuu2": [
        "what are you up to ?"
    ],
    "wuz": [
        "was"
    ],
    "wwjd": [
        "what would judd do ?"
    ],
    "wwnc": [
        "will wonders never cease"
    ],
    "wwyc": [
        "write when you can"
    ],
    "wycm": [
        "will you call me ?"
    ],
    "wygam": [
        "when you get a minute"
    ],
    "wyham": [
        "when you have a minute"
    ],
    "wylei": [
        "when you least expect it"
    ],
    "wywh": [
        "wish you were here"
    ],
    "x-1-10": [
        "exciting"
    ],
    "x!": [
        "a typical woman"
    ],
    "xd": [
        "devilish smile"
    ],
    "xme": [
        "excuse me"
    ],
    "xlnt": [
        "excellent"
    ],
    "xlr8": [
        "going faster"
    ],
    "xpost": [
        "cross-post"
    ],
    "xyl": [
        "ex-young lady"
    ],
    "yf": [
        "wife"
    ],
    "xyz": [
        "examine your zipper"
    ],
    "y?": [
        "why ?"
    ],
    "y": [
        "yawn"
    ],
    "y2k": [
        "you're too kind"
    ],
    "yaa": [
        "yet another acronym"
    ],
    "yaba": [
        "yet another bloody acronym"
    ],
    "yarly": [
        "ya, really ?"
    ],
    "yas": [
        "praise"
    ],
    "ybic": [
        "your brother in christ"
    ],
    "ybs": [
        "you'll be sorry"
    ],
    "ycdbwycid": [
        "you can't do business when your computer is down"
    ],
    "ycht": [
        "you can have them"
    ],
    "ycliu": [
        "you can look it up"
    ],
    "yct": [
        "your comment to"
    ],
    "yd": [
        "yesterday"
    ],
    "yg": [
        "young gentleman"
    ],
    "ygg": [
        "you go girl"
    ],
    "ygtbkm": [
        "you've got to be kidding me"
    ],
    "ygtr": [
        "you got that right"
    ],
    "yhbt": [
        "you have been trolled"
    ],
    "yhbw": [
        "you have been warned"
    ],
    "yhl": [
        "you have lost"
    ],
    "yiu": [
        "yes, i understand"
    ],
    "ykw": [
        "you know what"
    ],
    "ykwycd": [
        "you know what you can do"
    ],
    "yl": [
        "young lady"
    ],
    "ymmv": [
        "your mileage may vary"
    ],
    "ynk": [
        "you never know"
    ],
    "yryocc": [
        "you're running your own cuckoo clock"
    ],
    "ysic": [
        "your sister in christ"
    ],
    "ysyd": [
        "yeah sure you do"
    ],
    "yt": [
        "you there ?"
    ],
    "ytb": [
        "youth talk back"
    ],
    "ytg": [
        "you're the greatest"
    ],
    "ywhnb": [
        "yes, we have no bananas"
    ],
    "ywhol": [
        "yelling “woohoo” out loud"
    ],
    "ywsyls": [
        "you win some, you lose some"
    ],
    "z": [
        "said"
    ],
    "z%": [
        "zoo"
    ],
    "zh": [
        "sleeping hour"
    ],
    "zot": [
        "zero tolerance"
    ]
}
