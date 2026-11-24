"""Ridiculous at first glance, real by the second: one sentence, one pitch.

A local tournament decides the entry. Ten original one-sentence startup
pitches compete, each naming a bizarre thing being sold, the people who
pay for it, and the reason the money holds together. Every pitch carries
one hand-set score per axis on a 0-5 scale: how genuinely bizarre the
idea is, whether the business logic survives a second look, how cleanly
the sentence lands as a pitch, and how concrete and vivid the writing
is. Axis weights follow the house judge brief, with bizarre and logic
heaviest because the laugh must come from the idea itself and the money
must survive the second glance. The champion is the highest weighted
total; ties break on bizarre first, then on shorter text, then on tag.
Before the champion is written, two guards run: the sealed-scorer gate
(1-200 characters, one sentence, not blank) and a structure check (a
named invention, an absurd mechanism, and a payoff clause naming the
payer and the payment), plus a minimum-total bar so a weak field never
ships. The run is fully deterministic, so two runs write byte-identical
output to /output/entry.txt.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")
MAX_CHARS = 200
MIN_CHARS = 1
CHAMPION_MIN_TOTAL = 40

AXIS_WEIGHTS = {
    "bizarre": 3,
    "logic": 3,
    "landing": 2,
    "concrete": 2,
}
AXIS_KEYS = ("bizarre", "logic", "landing", "concrete")


def build_candidates():
    """Return the ten tournament pitches as plain record dicts.

    Each record holds the pitch text, one score per axis, and a short
    note on how the absurd premise turns into a real market. Scores
    were set by hand against the judge brief before the tournament
    ran, never tuned to favour a pre-chosen winner. No two records
    share a theme, so the field tests ten different kinds of strange.
    """
    records = [
        {
            "tag": "snore-translator",
            "text": (
                "The Snore Translator, an app that turns your "
                "partner's snoring into nightly subtitles, so "
                "sleep-deprived spouses pay monthly to finally read "
                "what the snoring meant."
            ),
            "bizarre": 5,
            "logic": 5,
            "landing": 5,
            "concrete": 5,
            "fix_note": "subtitles turn a nightly annoyance into a subscription spouses renew",
        },
        {
            "tag": "scent-bank",
            "text": (
                "The Scent Bank, a vault that bottles your "
                "grandmother's kitchen smell before she moves house, "
                "so nostalgic families pay per jar to reopen "
                "childhood on demand."
            ),
            "bizarre": 5,
            "logic": 4,
            "landing": 4,
            "concrete": 5,
            "fix_note": "one jar per memory turns nostalgia into a repeat purchase",
        },
        {
            "tag": "expiry-tattoo",
            "text": (
                "The Expiry Tattoo Parlour, a studio that tattoos "
                "your food's expiry dates onto your forearm, so "
                "forgetful shoppers pay per tattoo to never eat "
                "expired yoghurt again."
            ),
            "bizarre": 5,
            "logic": 4,
            "landing": 4,
            "concrete": 4,
            "fix_note": "ink on skin replaces the label nobody reads before eating",
        },
        {
            "tag": "breakup-confetti",
            "text": (
                "The Breakup Confetti Cannon, a service that fires "
                "biodegradable confetti through your ex's window at "
                "midnight, so heartbroken clients pay per launch to "
                "feel avenged without a lawsuit."
            ),
            "bizarre": 4,
            "logic": 4,
            "landing": 4,
            "concrete": 4,
            "fix_note": "a paid launch sells revenge with no court date attached",
        },
        {
            "tag": "plant-therapist",
            "text": (
                "The Plant Therapist, a counsellor who mediates "
                "disputes between stressed workers and their desk "
                "plants, so guilty plant-killers pay per session to "
                "keep their ferns alive."
            ),
            "bizarre": 4,
            "logic": 4,
            "landing": 4,
            "concrete": 4,
            "fix_note": "a session fee buys absolution plus a living fern",
        },
        {
            "tag": "goldfish-funeral",
            "text": (
                "The Goldfish Funeral Director, a service that "
                "stages tiny riverside funerals for dead goldfish, "
                "so grieving children pay per ceremony to say a "
                "proper goodbye."
            ),
            "bizarre": 4,
            "logic": 3,
            "landing": 4,
            "concrete": 4,
            "fix_note": "a ceremony sells closure to families with small mourners",
        },
        {
            "tag": "apology-hotline",
            "text": (
                "The Apology Hotline for Houseplants, a phone line "
                "where botanists apologise to your plants on your "
                "behalf, so neglectful owners pay per call to ease "
                "their guilt."
            ),
            "bizarre": 4,
            "logic": 3,
            "landing": 4,
            "concrete": 4,
            "fix_note": "a paid call turns plant guilt into a conversation",
        },
        {
            "tag": "tooth-fairy-insurance",
            "text": (
                "The Tooth Fairy Insurance, a policy that pays "
                "parents when the tooth fairy forgets a visit, so "
                "panicked mums pay monthly to never explain a "
                "missing coin again."
            ),
            "bizarre": 3,
            "logic": 4,
            "landing": 4,
            "concrete": 4,
            "fix_note": "a premium buys a cover story for every forgotten visit",
        },
        {
            "tag": "cancelled-plans-mourner",
            "text": (
                "The Professional Mourner for Cancelled Plans, a "
                "service that stages a tiny funeral for your ruined "
                "weekend plans, so disappointed friends pay per "
                "ceremony to grieve their brunch properly."
            ),
            "bizarre": 4,
            "logic": 3,
            "landing": 4,
            "concrete": 4,
            "fix_note": "a paid ceremony sells closure for a brunch that never happened",
        },
        {
            "tag": "queue-witness",
            "text": (
                "The Queue Witness, a service that stands in line "
                "for you and livestreams your place in it, so "
                "impatient shoppers pay per hour to skip waiting "
                "without losing their spot."
            ),
            "bizarre": 3,
            "logic": 4,
            "landing": 3,
            "concrete": 3,
            "fix_note": "an hourly fee sells waiting time back to shoppers",
        },
    ]
    return records


def score_record(record):
    """Return the weighted tournament total for one candidate record."""
    total = 0
    for axis in AXIS_KEYS:
        total += record[axis] * AXIS_WEIGHTS[axis]
    return total


def rank_records(records):
    """Return records ordered best first, with deterministic tie-breaks.

    Ties break on bizarre first, then on shorter text, then on tag, so
    the ordering never depends on input order or on anything random.
    """
    scored = []
    for record in records:
        entry = dict(record)
        entry["total"] = score_record(record)
        scored.append(entry)
    ranked = sorted(
        scored,
        key=lambda item: (
            -item["total"],
            -item["bizarre"],
            len(item["text"]),
            item["tag"],
        ),
    )
    return ranked


def check_pitch(text):
    """Return a list of gate problems for a pitch, empty when it passes.

    The gate mirrors the sealed scorer: UTF-8 text of 1 to 200
    characters, not only white space, and exactly one sentence.
    """
    problems = []
    stripped = text.strip()
    if len(text) < MIN_CHARS:
        problems.append("pitch is empty")
    if len(text) > MAX_CHARS:
        problems.append("pitch exceeds 200 characters")
    if stripped == "":
        problems.append("pitch is only white space")
    if "\n" in text:
        problems.append("pitch spans more than one line")
    if text.count(".") != 1:
        problems.append("pitch must hold exactly one sentence")
    if not stripped.endswith("."):
        problems.append("pitch must end with a full stop")
    return problems


def check_structure(text):
    """Return structure problems: named invention, mechanism, payoff.

    A valid pitch opens with a named invention, carries an absurd
    mechanism in the middle, and closes with a payoff clause that
    names the payer and the payment.
    """
    problems = []
    if not text.startswith("The "):
        problems.append("pitch must open with a named invention")
    if ", a " not in text and ", an " not in text:
        problems.append("pitch must introduce the invention after its name")
    if ", so " not in text:
        problems.append("pitch must close with a payoff clause")
    if " pay " not in text and " pays " not in text:
        problems.append("pitch must name who pays")
    return problems


def write_pitch(text, destination):
    """Write the pitch to destination, creating its parent directory."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        destination.write_text(text, encoding="utf-8")
    except OSError as write_err:
        raise RuntimeError(
            f"failed to write {destination}: {write_err}"
        ) from write_err
    return destination


def report_table(ranked):
    """Build the human-readable tournament table lines."""
    lines = [
        "tournament standings "
        "(total / bizarre / logic / landing / concrete):"
    ]
    for position, item in enumerate(ranked, start=1):
        line = (
            f"{position}. {item['tag']}: {item['total']} "
            f"({item['bizarre']}/{item['logic']}/"
            f"{item['landing']}/{item['concrete']}) "
            f"{len(item['text'])} chars"
        )
        lines.append(line)
    top_three = ranked[:3]
    lines.append("top three fixes:")
    for item in top_three:
        lines.append(f"- {item['tag']}: {item['fix_note']}")
    return lines


def main():
    """Run the tournament, gate the champion, and write the output file."""
    outcome = 0
    records = build_candidates()
    ranked = []
    champion = {"tag": "", "text": "", "total": 0, "fix_note": ""}
    if len(records) > 0:
        ranked = rank_records(records)
        champion = ranked[0]
    if len(records) == 0:
        print("gate failure: candidate list is empty")
        outcome = 2
    if len(records) > 0 and champion["total"] < CHAMPION_MIN_TOTAL:
        print(
            f"gate failure: champion total {champion['total']} "
            f"below bar {CHAMPION_MIN_TOTAL}"
        )
        outcome = 3
    problems = check_pitch(champion["text"])
    problems.extend(check_structure(champion["text"]))
    if len(records) > 0 and problems:
        for problem in problems:
            print(f"gate failure: {problem}")
        outcome = 1
    if outcome == 0:
        for line in report_table(ranked):
            print(line)
        print(f"champion: {champion['tag']} ({len(champion['text'])} chars)")
        print(f"champion fix: {champion['fix_note']}")
        write_pitch(champion["text"], OUTPUT_PATH)
        print(f"wrote {OUTPUT_PATH}")
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())
