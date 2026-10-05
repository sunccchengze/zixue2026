"""Gentle entrance animations, written straight into the slide's <p:timing> tree.

Shape of it:
  * every slide gets a 0.5s cross-fade transition;
  * on ONE click, the slide builds itself in three beats -
    title block -> body -> takeaway band - each beat 420ms, 180ms apart.

Only one click is needed, so a speaker working from memory never has to
remember to click twice. Objects that must never flash (the full-bleed photo,
the top rule, the footer) are left out of the animation entirely.
"""
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Emu

EMU = 914400.0
DUR = 420          # ms, one fade
GAP = 180          # ms between beats
TRANSITION_MS = 500


def _e(tag):
    return OxmlElement("p:" + tag)


def _ctn(eid, dur=None, fill="hold", node_type=None, preset=None, preset_class=None):
    c = _e("cTn"); c.set("id", str(eid))
    if dur is not None:
        c.set("dur", str(dur))
    if fill:
        c.set("fill", fill)
    if node_type:
        c.set("nodeType", node_type)
    if preset is not None:
        c.set("presetID", str(preset))
    if preset_class is not None:
        c.set("presetClass", str(preset_class))
    c.set("presetSubtype", "0")
    c.set("grpId", "0")
    return c


def _fade_nodes(counter, sid, dur):
    """The two children PowerPoint writes for a Fade entrance."""
    kids = []

    g1 = _e("par"); c1 = _ctn(counter(), preset=10, preset_class=1, node_type="withGroup")
    st = _e("set")
    bh = _e("cBhvr")
    bh.append(_ctn(counter(), dur=1))
    tgt = _e("tgtEl"); sp = _e("spTgt"); sp.set("spid", str(sid)); tgt.append(sp)
    bh.append(tgt)
    an = _e("attrNameLst"); nm = _e("attrName"); nm.text = "style.visibility"; an.append(nm)
    bh.append(an)
    st.append(bh)
    to = _e("to"); sv = _e("strVal"); sv.set("val", "visible"); to.append(sv)
    st.append(to)
    _cl = _e("childTnLst"); _cl.append(st); c1.append(_cl)
    g1.append(c1); kids.append(g1)

    g2 = _e("par"); c2 = _ctn(counter(), preset=11, node_type="withGroup")
    am = _e("anim"); am.set("calcMode", "lin")
    bh2 = _e("cBhvr")
    bh2.append(_ctn(counter(), dur=dur))
    tgt2 = _e("tgtEl"); sp2 = _e("spTgt"); sp2.set("spid", str(sid)); tgt2.append(sp2)
    bh2.append(tgt2)
    an2 = _e("attrNameLst"); nm2 = _e("attrName"); nm2.text = "style.opacity"; an2.append(nm2)
    bh2.append(an2)
    am.append(bh2)
    tl = _e("tavLst")
    for tm, val in ((0, 0), (100000, 1)):
        tav = _e("tav"); tav.set("tm", str(tm))
        v = _e("val"); f = _e("fltVal"); f.set("val", str(val)); v.append(f)
        tav.append(v); tl.append(tav)
    am.append(tl)
    _cl = _e("childTnLst"); _cl.append(am); c2.append(_cl)
    g2.append(c2); kids.append(g2)
    return kids


def _beat_of(sh, slide_h):
    """-1 = never animate."""
    top = sh.top / EMU
    bot = (sh.top + sh.height) / EMU
    if sh.__class__.__name__ == "Picture" and (sh.width / EMU) > (slide_h * 1.3):
        return -1                       # full-bleed background
    if bot <= 0.12:
        return -1                       # top rule
    if top >= 6.90:
        return -1                       # footer
    if top < 2.10:
        return 1
    if top < 5.85:
        return 2
    return 3


def add_animation(slide, slide_h, start_id=1000):
    shapes = list(slide.shapes)
    plan = []
    for sh in shapes:
        sid = sh.shape_id
        if sid is None:
            continue
        b = _beat_of(sh, slide_h)
        if b < 0:
            continue
        plan.append((b, sh.top / EMU, sh.left / EMU, sid))
    if not plan:
        return 0
    plan.sort()

    n = [start_id]

    def nid():
        n[0] += 1
        return n[0]

    seq = []
    prev_beat = None
    for i, (beat, _t, _l, sid) in enumerate(plan):
        first_of_beat = (beat != prev_beat)
        if i == 0:
            node_type, delay = "clickEffect", "indefinite"
        elif first_of_beat:
            node_type, delay = "afterEffect", str(GAP)
        else:
            node_type, delay = "withEffect", "0"
        prev_beat = beat

        outer = _e("par")
        oc = _ctn(nid(), node_type=node_type)
        st = _e("stCondLst"); cond = _e("cond"); cond.set("delay", delay); st.append(cond)
        oc.append(st)
        inner = _e("par"); ic = _ctn(nid())
        kids = _e("childTnLst")
        for k in _fade_nodes(nid, sid, DUR):
            kids.append(k)
        ic.append(kids); inner.append(ic)
        _cl = _e("childTnLst"); _cl.append(inner); oc.append(_cl)
        outer.append(oc)
        seq.append(outer)

    main = _e("cTn"); main.set("id", str(nid())); main.set("dur", "indefinite")
    main.set("nodeType", "mainSeq")
    cl = _e("childTnLst")
    for s in seq:
        cl.append(s)
    main.append(cl)

    sq = _e("seq"); sq.set("concurrent", "1"); sq.set("nextAc", "seek")
    sq.append(main)
    for evt in ("onPrev", "onNext"):
        lst = _e("prevCondLst") if evt == "onPrev" else _e("nextCondLst")
        c = _e("cond"); c.set("evt", evt); c.set("delay", "0")
        te = _e("tgtEl"); te.append(_e("sldTgt")); c.append(te)
        lst.append(c); sq.append(lst)

    root_par = _e("par")
    rc = _ctn(nid(), dur="indefinite", node_type="tmRoot"); rc.set("restart", "never")
    _cl = _e("childTnLst"); _cl.append(sq); rc.append(_cl)
    root_par.append(rc)

    timing = _e("timing")
    _tl = _e("tnLst"); _tl.append(root_par); timing.append(_tl)

    trans = _e("transition")
    trans.set("spd", "med"); trans.set("advTm", "0")
    trans.append(_e("fade"))

    sl = slide._element
    anchor = sl.find("{http://schemas.openxmlformats.org/presentationml/2006/main}clrMapOvr")
    if anchor is not None:
        anchor.addnext(timing); anchor.addnext(trans)
    else:
        sl.append(trans); sl.append(timing)
    return len(plan)


def animate_presentation(prs):
    total = 0
    h = prs.slide_height / EMU
    for sl in prs.slides:
        total += add_animation(sl, h)
    return total
