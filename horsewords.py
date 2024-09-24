import gsorter as gs
import json
import re

# Baseline normalizer for arpabet.
def arpabet_normalizer(arpabet_string):
    single_map = {
        '@': 'AA', 'a': 'AE', 'A': 'AH', 'c': 'AO', 'W': 'AW', 'x': 'AX',
        'Y': 'AY', 'E': 'EH', 'R': 'ER', 'e': 'EY', 'I': 'IH', 'X': 'IX',
        'i': 'IY', 'o': 'OW', 'O': 'OY', 'U': 'UH', 'u': 'UW',
        'b': 'B', 'C': 'CH', 'd': 'D', 'D': 'DH', 'F': 'DX',
        'L': 'EL', 'M': 'EM', 'N': 'EN', 'f': 'F', 'g': 'G', 'h': 'HH',
        'J': 'JH', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'G': 'NG',
        'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 'S': 'SH', 't': 'T',
        'T': 'TH', 'v': 'V', 'w': 'W', 'H': 'WH', 'y': 'Y', 'z': 'Z',
        'Z': 'ZH'
    }
    doubles = set(v for k,v in single_map.items()).union({'AXR',
        'UX', 'NX', 'H'})
    vowels = {
        'AA', 'AE', 'AH', 'AO', 'AW', 'AX', 'AXR', 'AY', 'EH', 'ER',
        'EY', 'IH', 'IX', 'IY', 'OW', 'OY', 'UH', 'UW', 'UX'
    }

    tokens = arpabet_string.split()
    out = []
    for tok in tokens:
        match = re.match(r'([a-zA-Z@]+)(\d)?', tok)
        # Can't fix this
        if match is None:
            out.append(tok)
            continue
        phoneme = match.group(1)
        stress = match.group(2)

        # 1. Identifies everything that isn't proper double ARPAbet token
        if phoneme not in doubles:
            if phoneme not in single_map:
                pass
            # 2. Try to fix improper single-letter ARPAbet tokens
            else:
                phoneme = single_map[phoneme]
            
        # 3. Fix missing stresses on vowels
        if phoneme in vowels and stress is None:
            stress = '0'
        elif phoneme not in vowels:
            stress = ''
        tok = phoneme + stress
        out.append(tok)
    return ' '.join(out)

def arpabet_normalize_data(data):
    # That occasional 1 in 6000 JSON hallucination...
    if not 'transcription' in data:
        return data
    data['transcription'] = arpabet_normalizer(data['transcription'])
    return data

def horsemain():
    # Step 1. Define a file function that produces list[Item]
    def horse_file_fn(filepath : str) -> list[gs.Item]:
        ret = []
        if filepath.endswith('.json'):
            with open(filepath, encoding='utf-8') as f:
                obj = json.load(f)
                for baseword, data in obj.items():
                    ret.append(gs.Item(comparison_id=baseword,
                        data=arpabet_normalize_data(data)))
        else: # handle non-json
            with open(filepath, encoding='utf-8') as f:
                while line := f.readline():
                    baseword, transcription = line.split('  ')
                    ret.append(gs.Item(comparison_id=baseword.lower(),
                        data={'transcription':
                         arpabet_normalizer(transcription)}))
        return ret

    # Step 2. Use Groupers to create your groups 
    grouper = gs.MultiFile(file_fn=horse_file_fn, name='horsewords')
    group = grouper([
        r'D:\Code\PPPDataset\horsewords.clean',
        r'D:\Code\PPPDataset\horsewords_raw_output.json',
        r'D:\Code\PPPDataset\horsewords_raw_output_thinking.json',
        ])

    # (or just skip step 1 and 2 and manually create the groups yourself)

    # Step 3. Define fields
    fields = {
        'transcription': gs.FieldSpec(field_type='line'),
        'confidence': gs.FieldSpec(
            field_type='line', optional=True, editable=False),
        'thinking': gs.FieldSpec(
            field_type='multiline', optional=True, editable=False),
    }

    # Step 4. Create a Project from your groups
    project = gs.Project(groups=[group], name='horsewords_project')
    #print(project.model_dump_json())

    # Step 5. ???
    # Step 6. Profit!
    sorter = gs.GSorter(project, fields=fields)
    sorter.ui_run()

if __name__ == '__main__':
    horsemain()