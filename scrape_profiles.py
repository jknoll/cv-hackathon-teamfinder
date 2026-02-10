#!/usr/bin/env python3
"""Scrape Cerebral Valley hackathon guest profiles and GitHub data."""

import asyncio
import aiohttp
import json
import re
import sys
import time
from pathlib import Path
from datetime import datetime

HANDLES = [
    "sebasalmeidam","eges","raymondyeh","parvathi96","JulianCrespi","doasfrancisco","manojmaheshwar","davewitwer","hannie","Pranavrevee","romirom11","abpraj","helloayushi","kerematam","jarm","naga-k","lucarso","tomyister","mian","KostyaV","niral28","matiszz","thegdsks","heyyfernanda","photoncat","namin","rashmi","brogers","gokul","nurpeiis","prabhakar","artemgetman","atemyipod","dankrieg","kevincollinsirl","mannad12","alissawu","wulfor","d3o","muhat","heysaik","leann86920","waleed_samouh","layonez","jpdias","degtrdg2","prerak","ser3ph","orangebite","timor",
    "yosun","incanspyder","eliozc","aryankeluskar","WaverAndrew","lionartmartins","xmens","ar813","dias-kh","adb","zzappa","emilzq","arjitmat","rmbk","kamathhrishi","hypercatcher","drewwasem","70lan7","Faouzielbakri","chrischarts8","lommyahon","anipotts","Alein","sureshbavisetti","avaliev","him2497","ytjo","manasdutta","utkarshm","hanshikag","bigadamknight","shaam","indoor47","alenjelco","aashwindev","rohitsingh017","nandini12396","roylin","ndegwajulius","Aman25m","affaanmustafa","saxenauts","pushpak","aakriti","dastin","ascender1729","madmecodes","ilhamfp","jordanjamesmedia","deepto98",
    "gauravjain14","fathiramm","udamliyanage","pranshuchourasia","gip","mnthnx64","shreya13050A","ansht","pushkalkatara","yacc","codefatherai","tonylim","louisojie","JackLau","Chiranjeevijoshi","fandika","vinyas","ath","saxenashobhit","jgheinz","idode_k","sangam","elviskahoro","nanddave","ksajan12","sarthology","aayushs","sydatf","akshitkhokhani","living_cool","brianluby","georgeck","hugoblanche","boristane","bingsu","kazu42","pedropaulovc","dekai","homeservicebase","ven","vineet","ventali","smalla","dioptre","sreeprasad","mrchang","And","diqi","organicnz","kashramli",
    "mxhd_rxshid","kimandrik","dhonam","bendechrai","MSGB","URCUTENEIGHBOR","surajp","TheFutureSandBox","nitesh","ravikant","karam1998","anasmjhd","moshesimon","meir","ardalan","hskendall","wpn10","allierays","moises","dmitry","himanshuVohra","mukur","roman_sevast","shashwatJain","qdee","hrishi","pmccaffrey6","abhi1223","yangshun","tarekbadrsh","sunit","nikiv","saicharank0608","zoid","kabadigitalinc","turo","nanas","jasone","remifran","mohsinss","djacobs","idmtr","Flareon","predictmax_ai","vichudo","bugatt","leocder","ivanleomk","kozak","vanditeztech",
    "jcolano","stanlyya","ryan-airguard","mchahed99","lucasiragusa","mostlovemusic","hatsuse","waddle","kholmirzaev","pomber","nives","dcx","trishan9","dannyscalant","brandtdev","gabimoncha","cmm","Allymahmoud","alikolahdoozan","ustunb","lokashrinav","LupuletiC","xfarooqi","giosakti","binhpham","ovis","raejin","karim_elgazar","ndesouki","nikx-vla","lgandecki","mnedo","krishhhg","Aaryan7","khosla","mufid","Ayushman","stnkvcs","ammon","nishantjosh","sanjay_sai","yungalgorithm","eddieliu","rahul2992","buyan14","hieudinh","voxmenthe","balajmarius","yigit","rohitverma007",
    "meleantonio","robcxyz","lukehutch","claudingash","gooduru","sankaku-desu","pastarita","mihirjadhav","iankiku","nightcrie","kayeezy","rohail","dmitrypyanov","oneilcyber","markfer","kazuumi","sahaib","allenleee","Shimayuz","pavancern","arjunkomath","femiositade","ob1","bottico","ansh714","pran-ker","mohsaad","nicholsonjf","dimaosipa","henkvaness","saranshgupta0107","xdotli","maximilien","neb","neelj23","Ishitaj","joshuajerin","shekkizh","tkimpson","michow","chrysilla","shawnd","cs4alhaider","13point5","kazukiyoda","himansh005","eggs","akodyn","jonatan","sinha",
    "AJSAI","hey_brb","atomsilverman","eflowers","yashalluri","lim","xbg","brz","brandonin","dataphysician","jmitch","sherbondy","tolatokuns","ryesmith","zakaria","joemiddie13","anshuldhawan","luongnv89","misbahsy","geoffreyyoung","jwh","astrobrez","jadengeller","arslnb","dev","maggiemcroskey","katie","abrinz","jarrodwatts","coreycole","aar","saptak","itsmesmarathe","dmanur","jairo","seflless","bme3412","aryanvichare","mukul","karthik_ragunath","aymuos","amogh10","javitsi","thierrydamiba","vinceovando","Eijun","spenceryang","inodb","dom1337","venkatacrc",
    "luke","tblt","aldojaja","jraad","abgup","wjf","derrick","YAB","maki","masterfung","rishik10","canitas","naama","awesomic","iss","suvasis","adi","kangjake","ramanfu","nahidalam","bart","svilupp","intabyu","KyeyuneKazibwe","skanador","nvganta","arhaan10sm","strickvl","barathwajanandan","michaelsparre","sumeetv","marot","rafacabrera7","jackzampolin","hamedmp","liviuolos","zyushg","augmentedmode","Chinat","tozdemir","blocksec","tirth8205","jmuncor","oalexsp","ceeeb","frg100","aaronbassett","juanpflores","balazs_nemethi","ishcodes",
    "tonynguyenvn17","javokhir","ankur","prathamesh","bxptr","adribarreda","boomer","jknoll","lilyzhng","vancuren","petroshong","rafaelobitten","fabiepenso","markokraemer","souptaco","tangenjm","ankitm","Healer","idon","stat-guy","psrth","HassamGani","Subramanya1997","vishalv97","Bayka","camin","michaelchomsky","seanx","Muz","anshu","puravpatel","magdaroni","al_from_koii","grabbou","yaambe_","stevederico","josephdib9","homo_ludens","sharon_shooky","carloslara","carpetxie","edwarddgao","bharat","dtran","karthikv2k","olegakbarov","tylergibbs","mmo","arnabgho","srgnunlu",
    "hkandala","danielmerja","leehanchung","ghatage","gpj","vaibhavp","tetraslam","vickijyz","demegire","SissiF","bneo","jedwhite","sfoscar","Claudius","bilalba","silv","mikeendale","nioralabs","kibaekr","AMichalski","garagon","charann","rmzlb","shawnbuilds","rickblalock","rogutkuba","joelwang","zacharyr0th","albertoomagno","iy3r","JulienCoulaud","agrim","koylanai","vibes","eddiebe","markmdev","legitamit","fant","danchou","chekos","0xthierry","vamsee","zruss","akeil","amichael","dorian","ghumare64","christianyun","rudrank","kaito",
]

TIMEZONE_MAP = {
    "san francisco": "America/Los_Angeles", "sf": "America/Los_Angeles", "bay area": "America/Los_Angeles",
    "los angeles": "America/Los_Angeles", "seattle": "America/Los_Angeles",
    "portland": "America/Los_Angeles", "california": "America/Los_Angeles", "palo alto": "America/Los_Angeles",
    "mountain view": "America/Los_Angeles", "sunnyvale": "America/Los_Angeles", "oakland": "America/Los_Angeles",
    "new york": "America/New_York", "nyc": "America/New_York", "brooklyn": "America/New_York",
    "boston": "America/New_York", "miami": "America/New_York", "washington": "America/New_York",
    "chicago": "America/Chicago", "austin": "America/Chicago", "dallas": "America/Chicago",
    "denver": "America/Denver", "boulder": "America/Denver",
    "london": "Europe/London", "uk": "Europe/London",
    "berlin": "Europe/Berlin", "germany": "Europe/Berlin", "munich": "Europe/Berlin",
    "paris": "Europe/Paris", "france": "Europe/Paris",
    "amsterdam": "Europe/Amsterdam", "netherlands": "Europe/Amsterdam",
    "singapore": "Asia/Singapore",
    "tokyo": "Asia/Tokyo", "japan": "Asia/Tokyo",
    "bangalore": "Asia/Kolkata", "bengaluru": "Asia/Kolkata", "mumbai": "Asia/Kolkata",
    "india": "Asia/Kolkata", "delhi": "Asia/Kolkata", "hyderabad": "Asia/Kolkata",
    "toronto": "America/Toronto", "canada": "America/Toronto", "vancouver": "America/Vancouver",
    "sydney": "Australia/Sydney", "melbourne": "Australia/Sydney", "australia": "Australia/Sydney",
    "dubai": "Asia/Dubai", "uae": "Asia/Dubai",
    "tel aviv": "Asia/Jerusalem", "israel": "Asia/Jerusalem",
    "lisbon": "Europe/Lisbon", "portugal": "Europe/Lisbon",
    "brazil": "America/Sao_Paulo", "são paulo": "America/Sao_Paulo",
    "nairobi": "Africa/Nairobi", "kenya": "Africa/Nairobi",
    "seoul": "Asia/Seoul", "korea": "Asia/Seoul",
    "zurich": "Europe/Zurich", "switzerland": "Europe/Zurich",
    "stockholm": "Europe/Stockholm", "sweden": "Europe/Stockholm",
    "barcelona": "Europe/Madrid", "madrid": "Europe/Madrid", "spain": "Europe/Madrid",
}


def guess_timezone(location):
    if not location:
        return None
    loc_lower = location.lower()
    for keyword, tz in TIMEZONE_MAP.items():
        if keyword in loc_lower:
            return tz
    return None


def parse_profile(html):
    """Extract user profile by unescaping RSC flight data and parsing JSON."""
    idx = html.find('"userId"')
    if idx == -1:
        idx = html.find('\\"userId\\"')
    if idx == -1:
        return None

    # Get a chunk around the userId
    start = max(0, idx - 10)
    chunk = html[start:start + 3000]

    # Unescape the RSC flight data: \\\" -> "
    unescaped = chunk.replace('\\"', '"')

    # Find the JSON object boundaries
    obj_start = unescaped.rfind('{', 0, 15)
    if obj_start == -1:
        obj_start = 0

    # Find the closing brace after location field
    loc_idx = unescaped.find('"location"', obj_start)
    if loc_idx == -1:
        return None

    # Find the end of the location value and the closing brace
    end = unescaped.find('}', loc_idx)
    if end == -1:
        return None

    json_str = unescaped[obj_start:end + 1]

    try:
        obj = json.loads(json_str)
        return {
            "userId": obj.get("userId"),
            "firstName": obj.get("firstName"),
            "lastName": obj.get("lastName"),
            "avatarUrl": obj.get("avatarUrl"),
            "handle": obj.get("handle"),
            "description": obj.get("description"),
            "linkedinUsername": obj.get("linkedinUsername"),
            "githubUsername": obj.get("githubUsername"),
            "xHandle": obj.get("xHandle"),
            "siteUrl": obj.get("siteUrl"),
            "location": obj.get("location"),
        }
    except json.JSONDecodeError:
        return None


async def fetch_profile(session, handle, semaphore):
    async with semaphore:
        url = f"https://cerebralvalley.ai/u/{handle}"
        try:
            headers = {"Accept-Encoding": "gzip, deflate"}
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15), headers=headers) as resp:
                if resp.status != 200:
                    return {"handle": handle, "error": f"status_{resp.status}"}
                html = await resp.text()
                profile = parse_profile(html)
                if profile:
                    return profile
                return {"handle": handle, "error": "no_match"}
        except Exception as e:
            return {"handle": handle, "error": str(e)}


GITHUB_TOKEN = None  # Set via env or command line

async def fetch_github_user(session, username, semaphore):
    """Fetch GitHub user profile and recent activity."""
    async with semaphore:
        headers = {"Accept": "application/vnd.github.v3+json"}
        if GITHUB_TOKEN:
            headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
        try:
            async with session.get(
                f"https://api.github.com/users/{username}",
                headers=headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                if resp.status == 403:
                    return {"username": username, "error": "rate_limited"}
                if resp.status != 200:
                    return {"username": username, "error": f"status_{resp.status}"}
                user = await resp.json()

            async with session.get(
                f"https://api.github.com/users/{username}/repos?sort=stars&per_page=10",
                headers=headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                repos = await resp.json() if resp.status == 200 else []

            async with session.get(
                f"https://api.github.com/users/{username}/events?per_page=30",
                headers=headers, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                events = await resp.json() if resp.status == 200 else []

            return {
                "username": username,
                "bio": user.get("bio"),
                "location": user.get("location"),
                "company": user.get("company"),
                "blog": user.get("blog"),
                "public_repos": user.get("public_repos", 0),
                "followers": user.get("followers", 0),
                "following": user.get("following", 0),
                "created_at": user.get("created_at"),
                "repos": [
                    {
                        "name": r.get("name"),
                        "description": (r.get("description") or "")[:200],
                        "stars": r.get("stargazers_count", 0),
                        "forks": r.get("forks_count", 0),
                        "language": r.get("language"),
                        "updated_at": r.get("updated_at"),
                    }
                    for r in (repos if isinstance(repos, list) else [])
                ],
                "recent_event_count": len(events) if isinstance(events, list) else 0,
                "recent_event_types": list(set(
                    e.get("type", "") for e in (events if isinstance(events, list) else [])
                )),
            }
        except Exception as e:
            return {"username": username, "error": str(e)}


def score_github(gh):
    if not gh or gh.get("error"):
        return 0
    score = 0
    score += min(gh.get("public_repos", 0), 30) * 0.5
    score += min(gh.get("followers", 0), 300) * 0.05
    total_stars = sum(r.get("stars", 0) for r in gh.get("repos", []))
    score += min(total_stars, 500) * 0.05
    score += min(gh.get("recent_event_count", 0), 30) * 0.5
    score += min(len(gh.get("recent_event_types", [])), 5) * 2
    created = gh.get("created_at", "")
    if created:
        try:
            age_years = (datetime.now() - datetime.fromisoformat(created.replace("Z", "+00:00")).replace(tzinfo=None)).days / 365
            score += min(age_years, 10)
        except Exception:
            pass
    if gh.get("bio"):
        score += 5
    return min(round(score), 100)


def assess_claude_code_proficiency(gh):
    if not gh or gh.get("error"):
        return {"score": 0, "signals": []}
    signals = []
    score = 0
    for r in gh.get("repos", []):
        name = (r.get("name") or "").lower()
        desc = (r.get("description") or "").lower()
        if any(kw in name or kw in desc for kw in ["claude", "anthropic", "mcp", "model-context-protocol"]):
            signals.append(f"claude-related repo: {r.get('name')}")
            score += 20
        if any(kw in name or kw in desc for kw in ["llm", "ai-agent", "langchain", "openai", "gpt", "chatbot"]):
            signals.append(f"AI/LLM repo: {r.get('name')}")
            score += 10
        if any(kw in name or kw in desc for kw in ["cli", "terminal", "command-line"]):
            signals.append(f"CLI tool: {r.get('name')}")
            score += 5
    event_types = gh.get("recent_event_types", [])
    if "PushEvent" in event_types:
        score += 10
        signals.append("active pusher")
    if "CreateEvent" in event_types:
        score += 5
        signals.append("creates repos/branches")
    return {"score": min(score, 100), "signals": signals}


def assess_hackathon_history(gh):
    if not gh or gh.get("error"):
        return {"score": 0, "signals": []}
    signals = []
    score = 0
    for r in gh.get("repos", []):
        name = (r.get("name") or "").lower()
        desc = (r.get("description") or "").lower()
        if any(kw in name or kw in desc for kw in ["hackathon", "hack", "devpost", "ethglobal", "treehacks", "calhacks", "hackmit"]):
            signals.append(f"hackathon repo: {r.get('name')}")
            score += 20
    return {"score": min(score, 100), "signals": signals}


async def main():
    out_path = Path(__file__).parent / "guests.jsonl"
    profiles = []
    errors = []

    print(f"Phase 1: Fetching {len(HANDLES)} CV profiles...")
    sem = asyncio.Semaphore(20)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_profile(session, h, sem) for h in HANDLES]
        for i, coro in enumerate(asyncio.as_completed(tasks)):
            result = await coro
            if result.get("error"):
                errors.append(result)
            else:
                profiles.append(result)
            done = i + 1
            if done % 50 == 0 or done == len(HANDLES):
                print(f"  CV profiles: {done}/{len(HANDLES)} ({len(profiles)} ok, {len(errors)} errors)")

    print(f"\nPhase 1 complete: {len(profiles)} profiles, {len(errors)} errors")
    if errors:
        print(f"  Failed handles: {[e.get('handle','?') for e in errors[:20]]}{'...' if len(errors) > 20 else ''}")

    # Phase 2: GitHub data
    github_users = [p for p in profiles if p.get("githubUsername")]
    print(f"\nPhase 2: Fetching {len(github_users)} GitHub profiles (unauthenticated, may hit rate limits)...")
    gh_sem = asyncio.Semaphore(15 if GITHUB_TOKEN else 3)
    gh_data = {}
    async with aiohttp.ClientSession() as session:
        gh_tasks = []
        seen_usernames = set()
        for p in github_users:
            u = p["githubUsername"]
            if u not in seen_usernames:
                seen_usernames.add(u)
                gh_tasks.append(fetch_github_user(session, u, gh_sem))

        for i, coro in enumerate(asyncio.as_completed(gh_tasks)):
            result = await coro
            username = result.get("username", "")
            gh_data[username] = result
            done = i + 1
            if done % 50 == 0 or done == len(gh_tasks):
                rl = sum(1 for v in gh_data.values() if v.get("error") == "rate_limited")
                ok = sum(1 for v in gh_data.values() if not v.get("error"))
                print(f"  GitHub: {done}/{len(gh_tasks)} ({ok} ok, {rl} rate_limited)")

    print(f"\nPhase 2 complete: {len(gh_data)} GitHub profiles")

    # Phase 3: Assemble JSONL
    print(f"\nPhase 3: Assembling JSONL...")
    with open(out_path, "w") as f:
        for p in profiles:
            gh_username = p.get("githubUsername")
            gh = gh_data.get(gh_username, {}) if gh_username else {}

            location = p.get("location")
            location_source = "cerebralvalley" if location else None
            gh_location = gh.get("location") if not gh.get("error") else None
            contradictions = []
            if location and gh_location and location.lower().strip() != gh_location.lower().strip():
                contradictions.append(f"location: CV='{location}' vs GitHub='{gh_location}'")
            if not location and gh_location:
                location = gh_location
                location_source = "github"

            timezone = guess_timezone(location)

            record = {
                "name": f"{p.get('firstName', '')} {p.get('lastName', '')}".strip(),
                "handle": p.get("handle"),
                "cvProfileUrl": f"https://cerebralvalley.ai/u/{p.get('handle')}",
                "avatarUrl": p.get("avatarUrl"),
                "location": location,
                "locationSource": location_source,
                "timezone": timezone,
                "description": p.get("description"),
                "socialAccounts": {
                    "linkedin": f"https://linkedin.com/in/{p['linkedinUsername']}" if p.get("linkedinUsername") else None,
                    "github": f"https://github.com/{p['githubUsername']}" if p.get("githubUsername") else None,
                    "x": f"https://x.com/{p['xHandle']}" if p.get("xHandle") else None,
                    "website": p.get("siteUrl"),
                },
                "githubScore": score_github(gh) if gh_username else None,
                "githubData": {
                    "bio": gh.get("bio"),
                    "company": gh.get("company"),
                    "publicRepos": gh.get("public_repos"),
                    "followers": gh.get("followers"),
                    "topRepos": gh.get("repos", [])[:5],
                    "recentEventCount": gh.get("recent_event_count"),
                    "error": gh.get("error"),
                } if gh_username else None,
                "claudeCodeProficiency": assess_claude_code_proficiency(gh) if gh_username else {"score": 0, "signals": []},
                "hackathonHistory": assess_hackathon_history(gh) if gh_username else {"score": 0, "signals": []},
                "contradictions": contradictions,
            }
            f.write(json.dumps(record) + "\n")

    print(f"\nDone! Wrote {len(profiles)} records to {out_path}")
    ok_gh = sum(1 for v in gh_data.values() if not v.get("error"))
    with_loc = sum(1 for p in profiles if p.get("location") or (p.get("githubUsername") and gh_data.get(p["githubUsername"], {}).get("location")))
    print(f"  With GitHub data: {ok_gh}")
    print(f"  With location: {with_loc}")


if __name__ == "__main__":
    import os
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not GITHUB_TOKEN:
        # Try gh cli
        import subprocess
        try:
            GITHUB_TOKEN = subprocess.check_output(["gh", "auth", "token"], text=True).strip()
        except Exception:
            pass
    if GITHUB_TOKEN:
        print(f"Using GitHub token: {GITHUB_TOKEN[:10]}...")
    else:
        print("WARNING: No GitHub token found. Will be rate-limited to 60 req/hour.")
    asyncio.run(main())
