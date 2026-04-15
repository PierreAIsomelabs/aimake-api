SYSTEM_CADQUERY = """Tu es un expert CadQuery. Génère UNIQUEMENT du code Python CadQuery valide, sans markdown, sans backticks. Les variables step_path et stl_path sont déjà définies. Exporte toujours avec result.val().exportStep(step_path) et cq.exporters.export(result, stl_path)."""

def build_generate_prompt(dimensions, description, photos_analysis):
    dims = "\n".join(["- {}: {}".format(k,v) for k,v in dimensions.items()])
    return "Génère CadQuery pour:\nDIMENSIONS:\n{}\nDESCRIPTION: {}\nANALYSE: {}".format(dims, description, photos_analysis)

def build_repair_prompt(dimensions, description, damage, photos_analysis):
    dims = "\n".join(["- {}: {}".format(k,v) for k,v in dimensions.items()])
    return "Reconstruis cette pièce cassée comme neuve:\nDIMENSIONS:\n{}\nDESCRIPTION: {}\nDOMMAGES: {}\nANALYSE: {}".format(dims, description, damage, photos_analysis)

def build_modify_prompt(dimensions, modification, photos_analysis, existing_code=""):
    dims = "\n".join(["- {}: {}".format(k,v) for k,v in dimensions.items()])
    existing = "\nCODE EXISTANT:\n{}".format(existing_code) if existing_code else ""
    return "Modifie cette pièce:\nDIMENSIONS:\n{}\nMODIFICATION: {}\nANALYSE: {}{}".format(dims, modification, photos_analysis, existing)

def build_vision_prompt(description):
    return 'Analyse cette pièce mécanique. Description: "{}". Réponds UNIQUEMENT en JSON: {{"piece_type":"arbre|bride|boitier|plaque|autre","geometry":"revolution|prismatique|complexe","process":"tournage|fraisage|mixte","material_guess":"acier|inox|aluminium|laiton|plastique|inconnu","features":[],"damage":"aucun|casse|fissure|usure","damage_description":"","confidence":0.85}}'.format(description)
