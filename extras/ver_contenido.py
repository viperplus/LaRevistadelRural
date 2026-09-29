#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\Users\black\Desktop\opencode archivos\clase n°4\revista\datos\importados.json', encoding='utf-8') as f:
    data = json.load(f)

targets = [
    'cient_fica_y_tecnol_gica_clase_n°9_4to_a_o_saira_linare',
    'clase_9_educacion_cintifica_y_tecnologica_4to_a_o_leone',
    'clase_9_cientifica_y_tecnologica_guadalupe_centeno_lago',
    'clase_n°9_cientifica_y_tecnologica_rio_chico_gaminao_aa',
    'marrone_e_rosso_vintage_tecnologia_infografica_1_compre',
    'medrano_julieta_4to_a_o_clase_9_cientifica_y_tecnologic',
    'secogabriela_sedeaguadadeguerra_4toa_o_la_revista_rural',
]

for slug_part in targets:
    for a in data:
        if slug_part in a['slug']:
            print(f'\n===== {a.get("titulo","")[:70]} =====')
            print(f'Slug: {a["slug"]}')
            paras = a.get('parrafos', [])
            for i, p in enumerate(paras[:10]):
                print(f'  [{i}] {p[:120]}')
            if len(paras) > 10:
                print(f'  ... ({len(paras)} total)')
            break
