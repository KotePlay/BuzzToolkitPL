"""Host voices available on this machine, by pack language.

A trained voice lives in voice_models/<name>/ (written by voice_trainer.run from the user's own
game files): reference.wav + fine-tuned weights + info.json {"lang": "POL", "iso": "pl",
"base": "multilingual", ...}. A quick voice (make_host_reference.py) has only reference.wav.
Nothing here ships with the tool.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = os.path.join(ROOT, "voice_models")
SAME = {"GBR": "INE", "INE": "GBR"}         # UK / international English share the host


def list_voices():
    out = []
    for d in sorted(os.listdir(MODELS)) if os.path.isdir(MODELS) else []:
        info_path = os.path.join(MODELS, d, "info.json")
        if not os.path.exists(os.path.join(MODELS, d, "reference.wav")):
            continue
        info = json.load(open(info_path, encoding="utf-8")) if os.path.exists(info_path) else {}
        out.append({"name": d, "lang": info.get("lang", "GBR"), "trained": os.path.exists(os.path.join(MODELS, d, "s3gen_flow.pt")),
                    # voices trained before languages were recorded are English
                    "iso": info.get("iso", "en"), "base": info.get("base", "english"),
                    "engine": "clone:voice_models/%s/reference.wav" % d, "model": "voice_models/%s" % d})
    return out


def voice_for(lang):
    """Best voice for a pack language, or None (then the pack is built silent). A trained voice
    beats a quick one cloned from a short sample."""
    lang = lang.upper()
    hits = [v for v in list_voices() if v["lang"] == lang or v["lang"] == SAME.get(lang)]
    hits.sort(key=lambda v: not v["trained"])
    return hits[0] if hits else None


def voice_config(lang, base=None):
    """Pack "voice" settings using this language's voice (keeps rounds/vocab/warmth from base)."""
    v = voice_for(lang)
    if not v:
        return None
    cfg = dict(base or {})
    cfg.setdefault("rounds", ["standard", "picture", "all_that_apply", "point_stealer"])
    import build_pack
    iso = build_pack.LANGUAGES.get(lang, {}).get("whisper", "en")
    cfg["engine"] = v["engine"]
    clone = dict(cfg.get("clone") or {}, lang=iso)
    if v["trained"] and v["iso"] == iso:
        clone["model"] = v["model"]          # trained for this language, on its base model
    else:
        clone.pop("model", None)             # untrained: clone from the reference
    cfg["clone"] = clone
    cfg["language"] = lang
    if iso != "en":
        cfg.pop("vocab", None)               # English spelling hints don't apply
    return cfg
