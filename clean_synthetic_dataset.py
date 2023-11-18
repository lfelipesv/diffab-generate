import json
import os

from Bio.PDB import Select, PDBIO
from Bio.PDB.PDBParser import PDBParser

generated_json_file = 'data/sabdab_all_generated.json'
output_json_file = 'data/sabdab_all_generated_clean.json'
output_folder = 'results/dataset/synthetic_data_clean'

class ChainSelect(Select):
    def __init__(self, chains):
        self.chains = chains

    def accept_chain(self, chain):
        if chain.get_id() in self.chains:
            return 1
        else:          
            return 0

# Loop each line in the generated json file
filtered_json_lines = []
i = 1
with open(generated_json_file, 'r') as f:
    for line in f:
        print(i)
        json_data = json.loads(line)
        pdb_id = json_data['pdb']
        if pdb_id.endswith('_REF') or pdb_id.endswith('_0') or pdb_id.endswith('_2'):
            filtered_json_lines.append(line)
            heavy_chain = json_data['heavy_chain']
            light_chain = json_data['light_chain']
            antigen_chains = json_data['antigen_chains']
            chains = [heavy_chain, light_chain] + antigen_chains
            pdb_data_path = json_data['pdb_data_path']
            p = PDBParser(PERMISSIVE=1)
            structure = p.get_structure(pdb_data_path, pdb_data_path)
            pdb_clean_file = os.path.join(output_folder, '{}.pdb'.format(pdb_id))                         
            io_w_no_h = PDBIO()               
            io_w_no_h.set_structure(structure)
            io_w_no_h.save('{}'.format(pdb_clean_file), ChainSelect(chains))
        i = i+1

# save filtered_json_lines to output_json_file
with open(output_json_file, 'w') as f:
    for line in filtered_json_lines:
        f.write(line)