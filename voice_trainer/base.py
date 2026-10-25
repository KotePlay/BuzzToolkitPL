"""Which Chatterbox model a voice is trained on, by language.

English voices fine-tune the English model (ChatterboxTTS). Every other language fine-tunes the
multilingual one (ChatterboxMultilingualTTS, 23 languages including Polish), whose text tokens
start with a language tag. The two have different text vocabularies and their own S3Gen weights,
so a work folder - and the voice exported from it - belongs to exactly one of them:
<work>/lang.json records which, and every step reads it from there.
"""
import json
import os

# pack (DLC) code -> (disc archive code, ISO code used by Chatterbox and Whisper). Czech and
# Croatian are missing because the multilingual model does not speak them.
LANGS = {"GBR": ("INE", "en"), "INE": ("INE", "en"), "ESP": ("ESP", "es"), "PRT": ("PRT", "pt"),
         "FRA": ("FRA", "fr"), "DEU": ("DEU", "de"), "ITA": ("ITA", "it"), "NLD": ("NLD", "nl"),
         "POL": ("POL", "pl"), "RUS": ("RUS", "ru"), "GRC": ("GRC", "el")}
ENGLISH = ("en", "", None)


def info(pack_lang):
    """'POL' -> {"lang": "POL", "disc": "POL", "iso": "pl", "base": "multilingual"}"""
    code = (pack_lang or "GBR").upper()
    if code == "INE":
        code = "GBR"
    if code not in LANGS:
        raise SystemExit("no trainable voice for language %r (known: %s)" % (code, ", ".join(sorted(LANGS))))
    disc, iso = LANGS[code]
    return {"lang": code, "disc": disc, "iso": iso,
            "base": "english" if iso in ENGLISH else "multilingual"}


def set_lang(work, pack_lang):
    """Record the work folder's language; refuses to switch a folder that already has another
    one, since its features and weights only fit the model they were made with."""
    want = info(pack_lang)
    path = os.path.join(work, "lang.json")
    if os.path.exists(path) or os.path.exists(os.path.join(work, "manifest.jsonl")):
        have = get_lang(work)                  # a folder from before languages were recorded is English
        if have["lang"] != want["lang"]:
            raise SystemExit("%s was made for %s, not %s - use a new --work folder per language"
                             % (work, have["lang"], want["lang"]))
        return have
    os.makedirs(work, exist_ok=True)
    json.dump(want, open(path, "w"), indent=1)
    return want


def get_lang(work):
    """The work folder's language (English for folders made before languages were recorded)."""
    path = os.path.join(work, "lang.json")
    return json.load(open(path)) if os.path.exists(path) else info("GBR")


def load(iso, device="cuda"):
    """The base model a voice in this language is trained on."""
    if iso in ENGLISH:
        from chatterbox.tts import ChatterboxTTS
        return ChatterboxTTS.from_pretrained(device=device)
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    return ChatterboxMultilingualTTS.from_pretrained(device=device)       # a string: see buzz_tts_clone.load


def text_tokens(model, text, iso):
    """T3 text tokens exactly as the model makes them at inference (language tag included)."""
    if iso in ENGLISH:
        return model.tokenizer.text_to_tokens(text)
    return model.tokenizer.text_to_tokens(text, language_id=iso)


def train_setup(max_frames):
    """How to train on this card -> (autocast dtype or None for fp32, speech tokens per
    micro-batch, micro-batches per optimiser step).

    The presets were sized for a 12 GB RTX 3060 in bfloat16. Cards before RTX 30xx have no fast
    bfloat16 (GTX 10xx emulates it, very slowly), so they train in fp32, which needs about twice
    the memory; cards with less memory split each batch into micro-batches whose gradients are
    added up before the step. The optimiser sees the same batch either way - only slower."""
    import torch
    props = torch.cuda.get_device_properties(0)
    dtype = torch.bfloat16 if props.major >= 8 else None
    budget = props.total_memory / 2 ** 30 / 12 * (1.0 if dtype else 0.5)
    accum = 1
    while budget * accum < 0.99 and accum < 8:
        accum *= 2
    return dtype, max(1, max_frames // accum), accum


def autocast(dtype):
    import contextlib
    import torch
    return torch.autocast("cuda", dtype=dtype) if dtype else contextlib.nullcontext()


def describe(dtype, micro, accum):
    import torch
    return "%s, %s: %d speech tokens x %d micro-batch%s per step" % (
        torch.cuda.get_device_name(0), "bf16" if dtype else "fp32", micro, accum, "" if accum == 1 else "es")
