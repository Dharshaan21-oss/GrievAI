"""
GrievAI - Synthetic Grievance Dataset Generator
Generates realistic citizen grievance text labeled by category, for training
the DistilBERT classification model.

Categories:
1. Water Supply
2. Electricity
3. Roads & Infrastructure
4. Sanitation & Waste Management
5. Public Safety
6. Corruption
7. Health Services
8. Education

Design notes:
- Uses templated slot-filling with large randomized vocab pools (locations,
  durations, severity phrases, tone variants) so outputs are not repetitive.
- Mixes formal/informal register, includes occasional typos/casual grammar,
  varies length (short one-liners to multi-sentence complaints), and varies
  urgency/emotion, mirroring real citizen-submitted grievance text (CPGRAMS-style).
- Output: data/grievances_dataset.csv with columns [text, category]
"""

import random
import csv

random.seed(42)

# ---------- Shared vocab pools ----------
AREAS = [
    "Ward 7", "Sector 12", "Anna Nagar", "Gandhi Nagar", "MG Road area",
    "Block C", "the old bus stand area", "Rajiv Colony", "Nehru Street",
    "the market area", "Lakshmi Nagar", "Shanti Colony", "near the railway station",
    "Phase 2 layout", "the industrial estate road", "Kumaran Street",
    "behind the government school", "near the water tank", "Cross Street 4",
    "the housing board colony", "Ward 15", "Subramaniam Nagar"
]

DURATIONS = [
    "for the past 3 days", "for over a week now", "since last month",
    "for the last 2 weeks", "since yesterday", "for almost 10 days",
    "since the rains started", "for more than a month", "since Monday",
    "repeatedly over the last few weeks", "for the third time this month"
]

TONE_OPENERS_FORMAL = [
    "I would like to bring to your attention that",
    "This is to formally lodge a complaint regarding",
    "I am writing to report",
    "Kindly look into the following issue:",
    "I wish to file a grievance concerning",
    "Respected Sir/Madam, I would like to report",
]

TONE_OPENERS_INFORMAL = [
    "Hi, there is a serious problem with",
    "Sir this is very urgent,",
    "Please help, we are facing",
    "I want to complain about",
    "This is really frustrating,",
    "Since many days we are facing issue of",
    "Sir/madam pls check,",
]

CLOSERS = [
    "Please take immediate action.",
    "Kindly resolve this at the earliest.",
    "Requesting urgent intervention from the concerned department.",
    "This is causing a lot of inconvenience to residents.",
    "Please send someone to check as soon as possible.",
    "We have complained before but no action was taken.",
    "Hope for a quick resolution.",
    "This needs to be fixed before it gets worse.",
    "",  # sometimes no closer
    "Thank you for your attention to this matter.",
]

def maybe_typo(text):
    """Occasionally introduce mild informal/typo-like variation."""
    if random.random() < 0.12:
        text = text.replace("please", "pls").replace("Please", "Pls")
    if random.random() < 0.08:
        text = text.replace(" is ", " is  ")
    return text

def build(opener_pool, body, area=None, duration=None, closer=True):
    opener = random.choice(opener_pool)
    parts = [opener, body]
    if area and random.random() < 0.85:
        parts.append(f"in {area}")
    if duration and random.random() < 0.75:
        parts.append(duration)
    sentence = " ".join(parts).strip()
    if not sentence.endswith((".", "!", "?")):
        sentence += "."
    if closer and random.random() < 0.6:
        c = random.choice(CLOSERS)
        if c:
            sentence += " " + c
    return maybe_typo(sentence)


# ---------- Category-specific body templates ----------

WATER_BODIES = [
    "no water supply", "the water supply has been completely stopped",
    "we are getting extremely dirty and contaminated water",
    "there is a major water pipeline leakage wasting thousands of litres",
    "low water pressure making it impossible to fill even one bucket",
    "the water tanker has not come this week",
    "sewage water is mixing with our drinking water supply",
    "the bore well motor has broken down and nobody has repaired it",
    "water is supplied only for 10 minutes a day which is not enough",
    "the water tank in our area is leaking badly",
    "yellow colored water is coming from the tap",
]

ELECTRICITY_BODIES = [
    "frequent power cuts happening multiple times a day",
    "a transformer near our street is sparking dangerously",
    "the streetlights have not been working",
    "there has been no electricity since last night",
    "an exposed electric wire is hanging dangerously low on the road",
    "voltage fluctuation is damaging our home appliances",
    "the electricity pole is tilted and about to fall",
    "our new electricity connection application has been pending",
    "the meter reading shown is incorrect and bill is too high",
    "power supply keeps tripping every few hours",
]

ROADS_BODIES = [
    "a huge pothole has formed in the middle of the road",
    "the road has not been repaired despite being completely broken",
    "construction debris has been dumped on the road blocking traffic",
    "there is no streetlight making the road unsafe at night",
    "the footpath is completely damaged and unusable",
    "a speed breaker was built without any warning signs causing accidents",
    "the bridge has developed cracks and looks unsafe",
    "waterlogging happens on this road every time it rains",
    "the newly laid road has already started breaking apart",
    "an open manhole on the road is a serious accident risk",
]

SANITATION_BODIES = [
    "garbage has not been collected for many days",
    "a huge pile of waste has accumulated near the community bin",
    "the public toilet is in an extremely unhygienic condition",
    "drainage water is overflowing onto the street",
    "dead animals have been lying on the road uncollected",
    "the drainage system near our house is completely blocked",
    "mosquito breeding is increasing due to stagnant dirty water",
    "waste is being burned openly causing air pollution",
    "the sewage line has burst and is flowing onto the road",
    "stray animals are rummaging through uncollected garbage bags",
]

SAFETY_BODIES = [
    "there has been an increase in chain snatching incidents",
    "a group of people gather and create nuisance every night",
    "there is no police patrolling in our area at night",
    "eve teasing has been happening near the girls school",
    "an abandoned building has become a hub for illegal activities",
    "streetlights are broken making the area unsafe for women",
    "illegal liquor is being sold openly near the park",
    "stray dogs have been attacking children in the colony",
    "there was a fight/altercation that turned violent near the market",
    "unauthorized construction is blocking the emergency exit route",
]

CORRUPTION_BODIES = [
    "an official is demanding a bribe to process my application",
    "money was taken for a certificate that was never issued",
    "the contractor has clearly used substandard material and pocketed the difference",
    "funds allocated for the road project seem to have been misused",
    "I was asked to pay extra unofficial charges for a routine government service",
    "the ration shop dealer is selling allotted grains in the black market",
    "an inspector demanded money to pass a report that should be free",
    "the panchayat member is favoring certain families for scheme benefits unfairly",
    "documents are being delayed intentionally unless a bribe is paid",
    "public funds meant for street lighting were diverted without any work done",
]

HEALTH_BODIES = [
    "the primary health center has no doctor available most days",
    "essential medicines are out of stock at the government hospital",
    "the ambulance took over an hour to arrive during an emergency",
    "the hospital staff behaved very rudely with patients",
    "there is no cleanliness maintained inside the government hospital",
    "the vaccination camp promised for this week has not been organized",
    "we have been waiting for hours without any doctor attending patients",
    "the health center lacks basic equipment for even minor treatments",
    "expired medicines were allegedly given at the local dispensary",
    "there is no ambulance service available in our rural area",
]

EDUCATION_BODIES = [
    "the government school has not had a teacher for the past two months",
    "the school building's roof is leaking and unsafe for children",
    "midday meal quality has drastically deteriorated",
    "textbooks have still not been distributed despite the term starting",
    "the school toilets are in an unusable and unhygienic state",
    "there are no proper desks and children are made to sit on the floor",
    "the promised scholarship amount has not been credited for months",
    "the school has no drinking water facility for students",
    "classes are being held in an overcrowded single room",
    "the newly appointed teacher has not shown up since being assigned",
]

CATEGORY_MAP = {
    "Water Supply": WATER_BODIES,
    "Electricity": ELECTRICITY_BODIES,
    "Roads & Infrastructure": ROADS_BODIES,
    "Sanitation & Waste Management": SANITATION_BODIES,
    "Public Safety": SAFETY_BODIES,
    "Corruption": CORRUPTION_BODIES,
    "Health Services": HEALTH_BODIES,
    "Education": EDUCATION_BODIES,
}

TARGET_PER_CATEGORY = 150

def generate_rows():
    rows = []
    for category, bodies in CATEGORY_MAP.items():
        count = 0
        attempts = 0
        seen = set()
        while count < TARGET_PER_CATEGORY and attempts < TARGET_PER_CATEGORY * 20:
            attempts += 1
            body = random.choice(bodies)
            opener_pool = TONE_OPENERS_FORMAL if random.random() < 0.55 else TONE_OPENERS_INFORMAL
            area = random.choice(AREAS) if random.random() < 0.8 else None
            duration = random.choice(DURATIONS) if random.random() < 0.7 else None
            text = build(opener_pool, body, area, duration)
            key = text.lower()
            if key in seen:
                continue
            seen.add(key)
            rows.append((text, category))
            count += 1
    random.shuffle(rows)
    return rows

def main():
    rows = generate_rows()
    out_path = "/home/claude/ml_pipeline/data/grievances_dataset.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "category"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows -> {out_path}")

    # quick class balance check
    from collections import Counter
    counts = Counter(c for _, c in rows)
    for cat, cnt in counts.items():
        print(f"  {cat}: {cnt}")

if __name__ == "__main__":
    main()
