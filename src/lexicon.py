"""Hand-written rules. Every term is matched as a whole word/phrase after normalisation.
Both Devanagari and romanised forms are listed because Prisma returns native script."""

TYPES = {
    "fire": ["आग", "धुआं", "धुआँ", "जल रहा", "जल रही", "aag", "dhuan", "fire", "smoke", "burning"],
    "medical": ["सीने", "दर्द", "साँस", "सांस", "बेहोश", "दिल का दौरा", "एम्बुलेंस", "chest", "pain", "breathing",
                "unconscious", "heart", "ambulance"],
    "accident": ["टक्कर", "एक्सीडेंट", "दुर्घटना", "बाइक", "ट्रक", "accident", "collision", "truck", "bike", "crash"],
    "dispute": ["पार्किंग", "पड़ोसी", "गाड़ी", "गेट", "gate", "झगड़ा", "parking", "neighbour", "neighbor"],
}

# life-threat evidence -> points. Urgency comes ONLY from this, never from tone / volume / exclamation marks.
THREAT = {
    "बेहोश": 5, "unconscious": 5, "जवाब नहीं": 3,
    "साँस": 4, "सांस": 4, "breathing": 4, "सीने": 4, "chest": 4,
    "फँसे": 4, "फंसे": 4, "trapped": 4,
    "खून": 3, "blood": 3, "bleeding": 3,
    "आग": 3, "fire": 3,
    "टक्कर": 2, "collision": 2, "तार": 2,
    "बचाओ": 1, "help": 1,
}
VULNERABLE = {"बच्चा": 2, "बच्चे": 2, "बच्ची": 2, "दादी": 2, "दादा": 2, "बुज़ुर्ग": 2, "बूढ़े": 2, "child": 2, "baby": 2}
COUNTS = {"दो लोग": 1, "तीन लोग": 1, "चार लोग": 1, "कई लोग": 1, "3 लोग": 1, "2 लोग": 1}

CRITICAL_AT, HIGH_AT = 8, 4   # score >= 8 critical, >= 4 high, else low

# FICTIONAL places only (so no real-world location claims). canonical name -> spoken/written variants
GAZETTEER = {
    "Neelkamal Colony": [
        "Neelkamal Colony", "नीलकमल कॉलोनी", "नीलकमल कालोनी", "नीलकमल colony",
        "नील कमल कॉलोनी", "नील कमल", "नीलकमल", "नीलकमाल कॉलोनी", "नीलकमाल", "new kamal colony"
    ],
    "Madhuvan Tower": [
        "Madhuvan Tower", "मधुवन टावर", "मधुवन टॉवर", "मधुबन tower", "मधुवन tower",
        "मधुबन", "मधुवन", "madhuhan tower", "madhuvan tower", "madhuvan"
    ],
    "Surajpur Highway": [
        "Surajpur Highway", "सूरजपुर हाईवे", "सूरजपुर हाइवे", "सूरजपुर highway", "सूरजपुर", "सुरजपुर", "सुराजपुर", "surajpur"
    ],
    "Hanuman Dhaba": [
        "Hanuman Dhaba", "हनुमान ढाबा", "हनुमान ढाबे", "हनुमान dhaba"
    ],
    "Lotus Apartments": [
        "Lotus Apartments", "लोटस अपार्टमेंट", "लोटस अपार्टमेंट्स", "लोटस apartment", "lotus apartments",
        "notice apartment"
    ],
}
