#!/usr/bin/env python
import sys
import os
import shutil

NAMEMAP = { "Editra_be.po" : "Editra_be_BY.po",
            "Editra_bg.po" : "Editra_bg_BG.po",
            "Editra_ca.po" : "Editra_ca_ES.po",
            "Editra_ca@valencia.po" : "Editra_ca_ES@valencia.po",
            "Editra_cs.po" : "Editra_cs_CZ.po",
            "Editra_da.po" : "Editra_da_DK.po",
            "Editra_de.po" : "Editra_de_DE.po",
            "Editra_el.po" : "Editra_el_GR.po",
            "Editra_es.po" : "Editra_es_ES.po",
            "Editra_eu.po" : "Editra_eu_ES.po",
            "Editra_et.po" : "Editra_et_EE.po",
            "Editra_fa.po" : "Editra_fa_IR.po",
            "Editra_fi.po" : "Editra_fi_FI.po",
            "Editra_fr.po" : "Editra_fr_FR.po",
            "Editra_gl.po" : "Editra_gl_ES.po",
            "Editra_he.po" : "Editra_he_IL.po",
            "Editra_hr.po" : "Editra_hr_HR.po",
            "Editra_hu.po" : "Editra_hu_HU.po",
            "Editra_id.po" : "Editra_id_ID.po",
            "Editra_it.po" : "Editra_it_IT.po",
            "Editra_ja.po" : "Editra_ja_JP.po",
            "Editra_ka.po" : "Editra_ka_GE.po",
            "Editra_ko.po" : "Editra_ko_KR.po",
            "Editra_lt.po" : "Editra_lt_LT.po",
            "Editra_lv.po" : "Editra_lv_LV.po",
            "Editra_ms.po" : "Editra_ms_MY.po",
            "Editra_nb.po" : "Editra_nb_NO.po",
            "Editra_nl.po" : "Editra_nl_NL.po",
            "Editra_nn.po" : "Editra_nn_NO.po",
            "Editra_pl.po" : "Editra_pl_PL.po",
            "Editra_pt.po" : "Editra_pt_BR.po",
            "Editra_ro.po" : "Editra_ro_RO.po",
            "Editra_ru.po" : "Editra_ru_RU.po",
            "Editra_sk.po" : "Editra_sk_SK.po",
            "Editra_sl.po" : "Editra_sl_SI.po",
            "Editra_sr.po" : "Editra_sr_RS.po",
            "Editra_sv.po" : "Editra_sv_SE.po",
            "Editra_th.po" : "Editra_th_TH.po",
            "Editra_tr.po" : "Editra_tr_TR.po",
            "Editra_uk.po" : "Editra_uk_UA.po" }

def CopyLPFiles(dname):
    """Copies and renames launchpad files from given directory
    to the cwd.

    """
    for f in os.listdir(dname):
        if f.lower().startswith('editra') and f.endswith('.po'):
            newname = f.replace('editra', 'Editra')
            newname = newname.replace('-', '_')
            newname = NAMEMAP.get(newname, newname)
            source = os.path.join(dname, f)
            shutil.copy2(source, os.path.abspath("./%s" % newname))
        elif f.lower() == 'editra':
            p = os.path.join(dname, f)
            if os.path.isdir(p):
                CopyLPFiles(p) # recurse into subdir

if __name__ == '__main__':
    sdir = sys.argv[1]
    CopyLPFiles(sdir)
