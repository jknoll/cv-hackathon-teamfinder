#!/usr/bin/env python3
"""Normalize location strings in guests.jsonl to canonical forms.

Adds a `locationNormalized` field to each record while preserving the original `location`.
"""

import json
import sys
from collections import Counter

# Explicit mapping: raw location string (lowercased, stripped) -> canonical form
# None means "drop from dropdown" (joke/ambiguous entries)
LOCATION_MAP = {
    # San Francisco variants
    " san francisco": "San Francisco",
    "san francisco": "San Francisco",
    "san francisco, ca": "San Francisco",
    "san francisco, ca ": "San Francisco",
    "san francisco ca": "San Francisco",
    "san francisco, usa": "San Francisco",
    "san fransisco": "San Francisco",
    "sf": "San Francisco",
    "san francisco bay area": "San Francisco",
    "sf bay area": "San Francisco",
    "bay area": "San Francisco Bay Area",
    "bay area, ca": "San Francisco Bay Area",
    "silicon valley, ca": "San Francisco Bay Area",

    # Other SF Bay Area cities (keep distinct)
    "oakland, ca": "Oakland",
    "oakland, ca, usa": "Oakland",
    "palo alto, ca": "Palo Alto",
    "mountain view": "Mountain View",
    "sunnyvale": "Sunnyvale",
    "san jose": "San Jose",
    "san jose, ca": "San Jose",
    "santa clara": "Santa Clara",
    "santa clara, ca": "Santa Clara",

    # New York variants
    "new york": "New York",
    "new york city": "New York",
    "new york, ny": "New York",
    "new york, new york": "New York",
    "new york, usa": "New York",
    "brooklyn": "New York",
    "brooklyn, ny": "New York",
    "nyc (uni) / sf (work) / durham, nc (formerly) / princeton, nj (home)": "New York",

    # Los Angeles
    "los angeles, ca": "Los Angeles",
    "los angeles, california": "Los Angeles",
    "pasadena": "Pasadena",
    "irvine, california": "Irvine",
    "pomona, ca": "Pomona",

    # Boston
    "boston": "Boston",
    "boston, ma": "Boston",
    "boston, ma, usa": "Boston",
    "cambridge, ma": "Cambridge, MA",

    # Seattle
    "seattle": "Seattle",
    "seattle, wa, usa": "Seattle",

    # Austin
    "austin": "Austin",
    "austin, tx": "Austin",

    # Bangalore / Bengaluru
    "bangalore": "Bangalore",
    "bangalore, in": "Bangalore",
    "bangalore, india": "Bangalore",
    "bengaluru": "Bangalore",
    "bengaluru, india": "Bangalore",
    "bengaluru": "Bangalore",

    # Other Indian cities
    "delhi, india": "Delhi",
    "mumbai, india": "Mumbai",
    "pune": "Pune",
    "navi mumbai": "Mumbai",
    "vellore": "Vellore",
    "prayagraj, uttar pradesh, india": "Prayagraj",

    # India (generic)
    "india": "India",

    # London
    "london": "London",
    "london, uk": "London",
    "manchester": "Manchester",
    "oxford": "Oxford",
    "united kingdom": "United Kingdom",

    # Berlin
    "berlin": "Berlin",
    "berlin, germany": "Berlin",

    # Munich
    "munich": "Munich",
    "munich, germany": "Munich",

    # Paris
    "paris": "Paris",
    "paris, france": "Paris",

    # Toronto / Vancouver
    "toronto": "Toronto",
    "vancouver": "Vancouver",
    "vancouver, bc": "Vancouver",

    # Brazil
    "brazil": "Brazil",
    "brasil": "Brazil",
    "brasil ": "Brazil",
    "brasil, sp": "São Paulo",
    "sao paulo": "São Paulo",

    # Mexico
    "mexico": "Mexico",
    "méxico": "Mexico",

    # Sydney
    "sydney": "Sydney",
    "sydney, australia": "Sydney",
    "st lucia, qld, australia": "Brisbane",
    "melbourne": "Melbourne",

    # Tel Aviv
    "tel aviv": "Tel Aviv",

    # Tokyo
    "tokyo": "Tokyo",

    # Seoul
    "seoul, republic of korea": "Seoul",
    "south korea": "South Korea",

    # Singapore
    "singapore": "Singapore",

    # Dublin
    "dublin, ireland": "Dublin",

    # Lisbon / Portugal
    "lisbon": "Lisbon",
    "portugal": "Portugal",

    # Stockholm
    "stockholm": "Stockholm",

    # Estonia / Tallinn
    "estonia": "Estonia",
    "tallinn, estonia": "Tallinn",

    # Romania / Bucharest
    "romania": "Romania",
    "bucharest": "Bucharest",
    "timișoara, romania": "Timișoara",

    # Spain
    "barcelona, spain": "Barcelona",
    "madrid, spain": "Madrid",

    # Other European
    "gothenburg, sweden": "Gothenburg",
    "budapest, hungary": "Budapest",
    "brussels, belgium": "Brussels",
    "delft, the netherlands": "Delft",
    "reykjavík, iceland": "Reykjavík",

    # Middle East
    "dubai": "Dubai",
    "istanbul": "Istanbul",
    "riyadh, saudi arabia": "Riyadh",

    # South America
    "chile": "Chile",
    "santiago, chile": "Santiago",
    "colombia": "Colombia",
    "quito, ecuador": "Quito",

    # Asia
    "jakarta, indonesia": "Jakarta",
    "asia/indonesia": "Indonesia",
    "japan": "Japan",
    "karachi, pakistan": "Karachi",
    "samakhushi, kathmandu": "Kathmandu",
    "srilanka": "Sri Lanka",
    "maldives": "Maldives",

    # Africa
    "dakar": "Dakar",
    "edo state, ng": "Edo State, Nigeria",
    "egypt": "Egypt",

    # US states / generic US
    "ca": "California",
    "ca, usa": "California",
    "california": "California",
    "california, united states.": "California",
    "new jersey": "New Jersey",
    "florida, usa": "Florida",
    "us": "United States",
    "usa": "United States",
    "united states": "United States",
    "united states of america": "United States",

    # Specific US cities
    "atlanta": "Atlanta",
    "baltimore": "Baltimore",
    "alexandria, va": "Alexandria, VA",
    "hamilton": "Hamilton",
    "hanover, new hampshire": "Hanover, NH",
    "houston, tx": "Houston",
    "kansas city, missouri": "Kansas City",
    "miami, fl": "Miami",
    "minneapolis, us": "Minneapolis",
    "orlando, fl": "Orlando",
    "philadelphia, pa": "Philadelphia",
    "portland, or": "Portland",
    "sacramento, california": "Sacramento",
    "tempe, arizona, united states": "Tempe, AZ",
    "washington, dc": "Washington, DC",

    # Poland
    "poland": "Poland",
    "🇵🇱 / 🇺🇸": "Poland",

    # Remote / ambiguous / joke
    "remote": "Remote",
    "id": None,
    "127.0.0.1": None,
    "earth": None,
    "interweb worldwide": None,
    "outer space": None,
    "wandenreich": None,
}


def normalize(raw_location: str | None) -> str | None:
    """Return canonical location, or None for joke/ambiguous entries."""
    if not raw_location:
        return None
    key = raw_location.lower().strip()
    if key in LOCATION_MAP:
        return LOCATION_MAP[key]
    # Fallback: title-case the trimmed original
    return raw_location.strip().title()


def main():
    input_path = "/Users/justinknoll/git/tmp/cv-hackathon/guests.jsonl"

    with open(input_path, "r") as f:
        records = [json.loads(line) for line in f if line.strip()]

    for rec in records:
        rec["locationNormalized"] = normalize(rec.get("location"))

    with open(input_path, "w") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # Summary
    raw_locs = [r.get("location") for r in records if r.get("location")]
    norm_locs = [r["locationNormalized"] for r in records if r["locationNormalized"]]
    raw_unique = len(set(raw_locs))
    norm_unique = len(set(norm_locs))

    print(f"Total records: {len(records)}")
    print(f"Records with location: {len(raw_locs)}")
    print(f"Unique raw locations: {raw_unique}")
    print(f"Unique normalized locations: {norm_unique}")
    print(f"Reduction: {raw_unique} → {norm_unique} ({raw_unique - norm_unique} merged)")
    print()

    # Show normalized location counts
    counter = Counter(norm_locs)
    print("Normalized locations (by count):")
    for loc, count in counter.most_common():
        print(f"  {count:3d}  {loc}")

    # Check for unmapped locations (fallback path)
    unmapped = []
    for r in records:
        raw = r.get("location")
        if raw and raw.lower().strip() not in LOCATION_MAP:
            unmapped.append(raw)
    if unmapped:
        print(f"\n⚠️  {len(unmapped)} records used fallback normalization:")
        for u in sorted(set(unmapped)):
            print(f"  {u!r}")
    else:
        print("\n✓ All locations mapped explicitly.")


if __name__ == "__main__":
    main()
