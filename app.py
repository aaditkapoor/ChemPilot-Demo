import streamlit as st
import os
import numpy as np
import requests
from rdkit.Chem.Draw import IPythonConsole
from rdkit.Chem import Draw
IPythonConsole.ipython_useSVG=True 
from rdkit.Chem import AllChem as Chem
#output = "CCC(=O)N(C1CCN(CC1)CCC2=CCCCCC2)C3=CC=CC=C3"
#human = "****(C1CCN(CC1)CCC2=CC=CC=C2)C3=CC=CC=C3"

def get_mol(m1, m2):
    mol = Chem.MolFromSmiles(m1)
    mol2 = Chem.MolFromSmiles(m2)
    return mol, mol2
def compare(mol1, mol2):
    x1 = np.array(Chem.GetMorganFingerprintAsBitVect(mol1, useChirality=True, radius=2, nBits=124))
    x2 = np.array(Chem.GetMorganFingerprintAsBitVect(mol2, useChirality=True, radius=2, nBits=124))
    return x1, x2
# ref: https://www.statology.org/jaccard-similarity-python/
def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def pipeline(output, human):
    mol1, mol2 = get_mol(output, human)   
    x1, x2 = compare(mol1, mol2)
    return mol1, mol2, x1, x2


st.title("ChemPilot Demo")


models = {
    "ChemPilot Model": "https://dashboard.scale.com/spellbook/api/app/upeo3udv",
}

# inputs
option = st.selectbox(
     'Select Model',
     ("ChemPilot Model", ))

st.info(models[option])

o_molecule = st.text_input(
        "Enter original molecule 👇",value='CCC(=O)N(C1CCN(CC1)CCC2=CC=CC=C2)C3=CC=CC=C3Nc1nc(Sc3ccccc3-c3ccccc3)n[nH]1')

mol = Chem.MolFromSmiles(o_molecule)
im=Draw.MolToImage(mol)
st.image(im)

replace = st.text_input(
        "What to replace 👇",value='biphenyl')

replace_with = st.text_input("Replace with 👇", 'Alkyne')

prompt = f"Replace {replace} with {replace_with}; Input Molecule: {o_molecule}; Output:"


# enter prompt here
print(prompt)


prompt_structure = prompt


headers = {"Authorization":"Basic cld6rkr80002bul19pwbxzeim"}

if option and o_molecule and replace and replace_with:
    data = {
        "input": prompt_structure
    }
    response = requests.post(
  "https://dashboard.scale.com/spellbook/api/app/upeo3udv",
  json=data,
  headers=headers)
   # )
    #print(prompt_structure)

    # draw
    #output = response.text # extract smiles here
    #s = Chem.MolFromSmiles(output)
    #im_s=Draw.MolToImage(mol)
    #st.image(im_s)
    #sim = jaccard_score(x1, x2)
    import json
    con = json.loads(response.text)

    print(con['text'])
    m1 = con['text']
    #st.info(con.decode("utf-8"))
    st.info(con['text'])

    try:
        mol = Chem.MolFromSmiles(m1)
        im2=Draw.MolToImage(mol)
        st.image(im2)
    except:
        pass

    #st.info(f"Model output: {response.text}")
    #st.info(f"Similarity: {sim}")
else:
    st.error("Please enter input")





