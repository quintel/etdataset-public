import yaml
from graphviz import Digraph
import re
import html
import pandas as pd

# Excel-bestand voor ivar-kleuren (relatief pad vanaf de script locatie)
EXCEL_FILE = "etlocal_calculation_rules.xlsx"

# Kleurinformatie uit script A
prefix_styles = {
    "mq_": ("#7a3b1e", "ETM query (miscellaneous)", True),
    "dq_": ("#c96131", "ETM query (demand)", False),
    "eq_": ("#df9c7d", "ETM query (edge)", False),
    "tres_": ("#FFDA2D", "Transport research", False),
    "nl_": ("#5fafcb", "Klimaatmonitor (NL)", False),
}

km_color, km_label = "#e2b3a3", "Klimaatmonitor code (KM-var)"
const_color, const_label = "lightgray", "Constant"
num_re = re.compile(r"^-?\d+(?:\.\d+)?(?:e-?\d+)?$", re.I)
is_numeric = lambda x: isinstance(x, (int, float)) or (isinstance(x, str) and bool(num_re.match(x)))

# Operatie-mappings
simple_operations = {
    "sum": "+",
    "plus": "+", 
    "minus": "-",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
    "mul": "*",
    "div": "/"
}

# Binaire operatoren (hebben precies 2 componenten)
binary_operations = {"minus", "subtract", "divide", "div"}

# Complexere functies die als blokken moeten worden weergegeven
complex_functions = {"min", "max", "if", "iferror", "vlookup", "lookup", "round", "abs"}

# Globale teller om elke inline-expressie uniek te maken
_inline_counter = 0

def next_inline_id():
    global _inline_counter
    _inline_counter += 1
    return f"inline_op_{_inline_counter}"

def safe_str(x): 
    return str(x)

def prefix_info(var):
    """Haal prefix-informatie op voor een variabele."""
    if not isinstance(var, str): 
        return (None, None, None, False)
    for pre, (col, lbl, white_font) in prefix_styles.items():
        if var.startswith(pre):
            return pre, col, lbl, white_font
    return (None, None, None, False)

def load_ivar_colors():
    """Laad ivar-kleuren uit Excel-bestand."""
    import os
    
    # Probeer verschillende locaties voor het Excel-bestand
    possible_paths = [
        EXCEL_FILE,  # Huidige directory
        os.path.join("config", EXCEL_FILE),  # config subdirectory
        os.path.join("..", "config", EXCEL_FILE),  # parent/config directory
        os.path.join(os.path.dirname(__file__), EXCEL_FILE),  # script directory
    ]
    
    for excel_path in possible_paths:
        try:
            if os.path.exists(excel_path):
                xl = pd.ExcelFile(excel_path, engine="openpyxl")
                df_src = xl.parse("all_ivar_per_source")
                
                # Normaliseer kolommen
                df_src.columns = [str(c) for c in df_src.columns]
                
                # Zoek label-kolom
                label_col = [c for c in df_src.columns if c.lower().startswith("data derived")][0]
                
                # Maak kleur- en label-mappings
                ivar_color = {str(r["ivar"]).strip(): str(r["color"]).strip() for _, r in df_src.iterrows()}
                ivar_label = {str(r["ivar"]).strip(): str(r[label_col]).strip() for _, r in df_src.iterrows()}
                
                return ivar_color, ivar_label
        except Exception as e:
            continue
    
    print(f"Waarschuwing: Kon Excel-bestand niet laden op geen van de locaties: {possible_paths}")
    return {}, {}

def ensure_var_node(graph: Digraph, var_name: str, legends: set, ivar_color: dict, ivar_label: dict, is_etlocal_key: bool = False) -> str:
    """
    Zorgt dat er voor `var_name` een variabele-node bestaat in de GraphViz-graaf.
    Als de node nog niet bestaat, wordt hij aangemaakt met de juiste kleuren.
    """
    node_id = f"var_{var_name}"
    # Controleer of de node al in de graph body voorkomt
    existing_ids = {line.split()[0] for line in graph.body if line.strip().startswith(node_id)}
    if node_id not in existing_ids:
        label = safe_str(var_name)
        pre, col_pref, lbl_pref, white_font = prefix_info(var_name)
        fontcolor = "white" if white_font else "black"
        
        if is_etlocal_key:
            # ETLocal key: witte rechthoek
            graph.node(node_id, label=label, shape="box", style="filled", fillcolor="white")
        elif pre:
            # Behoud de prefix in het label voor duidelijkheid
            legends.add((col_pref, lbl_pref))
            graph.node(node_id, label=label, shape="ellipse", style="filled", fillcolor=col_pref, fontcolor=fontcolor)
        elif var_name in ivar_color:
            col = ivar_color[var_name]
            legends.add((col, ivar_label.get(var_name, "Other source")))
            graph.node(node_id, label=label, shape="ellipse", style="filled", fillcolor=col, fontcolor=fontcolor)
        elif is_numeric(var_name):
            legends.add((const_color, const_label))
            graph.node(node_id, label=label, shape="ellipse", style="filled", fillcolor=const_color)
        else:
            # Tussentijdse variabelen zijn wit
            graph.node(node_id, label=label, shape="ellipse", style="filled", fillcolor="white")
    return node_id

def process_expression(graph: Digraph, expr_def: dict, legends: set, ivar_color: dict, ivar_label: dict, target_node: str) -> None:
    """
    Verwerkt een inline expressie-structuur.
    Eenvoudige operatoren worden als pijllabels weergegeven.
    Complexere functies krijgen een rechthoekig tussenblok.
    """
    expr_name = expr_def.get("expression", "expr")
    
    # Bepaal of dit een eenvoudige operator of complexere functie is
    if expr_name in simple_operations:
        # Eenvoudige operator: gebruik symbool als pijllabel
        symbol = simple_operations[expr_name]
        components = expr_def.get("components", [])
        
        for i, comp in enumerate(components):
            # Voor binaire operatoren: eerste component +, tweede component het symbool
            if expr_name in binary_operations and len(components) == 2:
                label = "+" if i == 0 else symbol
            else:
                label = symbol
                
            if "variable" in comp:
                child_var = comp["variable"]
                child_node = ensure_var_node(graph, child_var, legends, ivar_color, ivar_label, False)
                graph.edge(child_node, target_node, label=label)
            elif "expression" in comp:
                process_expression(graph, comp, legends, ivar_color, ivar_label, target_node)
            else:
                raise ValueError(f"Component heeft geen 'variable' of 'expression': {comp}")
    
    elif expr_name in complex_functions:
        # Complexere functie: maak ruit-vormig tussenblok
        expr_id = next_inline_id()
        graph.node(expr_id, label=expr_name, shape="diamond", style="filled", fillcolor="white")
        
        for comp in expr_def.get("components", []):
            if "variable" in comp:
                child_var = comp["variable"]
                child_node = ensure_var_node(graph, child_var, legends, ivar_color, ivar_label, False)
                graph.edge(child_node, expr_id)
            elif "expression" in comp:
                process_expression(graph, comp, legends, ivar_color, ivar_label, expr_id)
            else:
                raise ValueError(f"Component heeft geen 'variable' of 'expression': {comp}")
        
        graph.edge(expr_id, target_node)
    
    else:
        # Onbekende expressie: behandel als complexe functie
        expr_id = next_inline_id()
        graph.node(expr_id, label=expr_name, shape="diamond", style="filled", fillcolor="white")
        
        for comp in expr_def.get("components", []):
            if "variable" in comp:
                child_var = comp["variable"]
                child_node = ensure_var_node(graph, child_var, legends, ivar_color, ivar_label, False)
                graph.edge(child_node, expr_id)
            elif "expression" in comp:
                process_expression(graph, comp, legends, ivar_color, ivar_label, expr_id)
            else:
                raise ValueError(f"Component heeft geen 'variable' of 'expression': {comp}")
        
        graph.edge(expr_id, target_node)

def build_flow_from_yaml(yaml_data: dict, etlocal_key: str) -> Digraph:
    """
    Loopt over de top-level keys in de YAML en bouwt de stroomdiagram-graaf:
    - Voor elk key=variabele (bv. tp_road_total_diesel_tj):
      - Als er een 'expression' is: verbind componenten direct met de variabele-node,
        met bewerkingen als pijllabels.
      - Als er alleen 'variable' staat (alias): verbind var_source → var_key.
    """
    graph = Digraph(format="png")
    graph.attr(rankdir="LR")
    
    legends = set()
    
    # Laad ivar-kleuren uit Excel
    ivar_color, ivar_label = load_ivar_colors()
    
    for var_name, definition in yaml_data.items():
        # Controleer of dit de ETLocal key is
        is_etlocal_key_var = (var_name == etlocal_key)
        result_node = ensure_var_node(graph, var_name, legends, ivar_color, ivar_label, is_etlocal_key_var)

        if "expression" in definition:
            # Verwerk expressie en verbind componenten direct met result_node
            process_expression(graph, definition, legends, ivar_color, ivar_label, result_node)

        elif "variable" in definition:
            src_var = definition["variable"]
            src_node = ensure_var_node(graph, src_var, legends, ivar_color, ivar_label, False)
            graph.edge(src_node, result_node)

        else:
            # Alleen de variabele-node is nodig; al gecreëerd via ensure_var_node
            pass

    # Voeg legend toe
    if legends:
        rows_html = "".join(f"<TR><TD BGCOLOR=\"{c}\" WIDTH=\"30\"></TD><TD>{html.escape(l)}</TD></TR>" for c, l in sorted(legends, key=lambda x: x[1]))
        graph.node("legend", label=f"<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\">{rows_html}</TABLE>>", shape="plaintext")
        # Verbind legend onzichtbaar met een willekeurige node
        if yaml_data:
            first_var = next(iter(yaml_data.keys()))
            first_node = f"var_{first_var}"
            graph.edge("legend", first_node, style="invis")

    return graph

def create_dependency_diagram(etlocal_key: str, yaml_dir: str = "./yaml_files_for_etlocal_key_calculation", 
                             save_files: bool = True, output_dir: str = ".") -> Digraph:
    """
    Creëert een dependency diagram voor een gegeven ETLocal key.
    
    Parameters:
    -----------
    etlocal_key : str
        De ETLocal key waarvoor het diagram gemaakt wordt
    yaml_dir : str
        Directory waar de YAML bestanden staan (default: "./yaml_files_for_etlocal_key_calculation")
    save_files : bool
        Of .dot en .png bestanden opgeslagen moeten worden (default: True)
    output_dir : str
        Directory voor output bestanden (default: ".")
    
    Returns:
    --------
    Digraph
        Het Graphviz diagram object (kan direct in Jupyter worden getoond)
    """
    import os
    
    # Construeer YAML pad
    yaml_path = os.path.join(yaml_dir, f"{etlocal_key}_dependency.yaml")
    
    # Controleer of YAML bestand bestaat
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"YAML bestand niet gevonden: {yaml_path}")
    
    # Lees YAML data
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)
    
    # Bouw het diagram
    graph = build_flow_from_yaml(yaml_data, etlocal_key)
    
    # Sla bestanden op als gewenst
    if save_files:
        output_basename = f"{etlocal_key}_dependency_graph"
        
        # Sla .dot bestand op
        dot_path = os.path.join(output_dir, f"{output_basename}.dot")
        graph.save(dot_path)
        print(f"Graphviz .dot-bestand opgeslagen als: {dot_path}")
        
        # Probeer PNG te renderen
        try:
            png_path = graph.render(filename=os.path.join(output_dir, output_basename), cleanup=True)
            print(f"Diagram gerenderd naar PNG: {png_path}")
        except Exception as e:
            print("Fout bij renderen naar PNG (controleer Graphviz-installatie):", e)
            print(f"Renderhandmatig met:\n  dot -Tpng {dot_path} -o {output_basename}.png")
    
    return graph

# === Voor direct gebruik als script ===
if __name__ == "__main__":
    # Standaard ETLocal key voor testen
    etlocal_key = 'input_industry_food_electricity_demand'
    
    # Maak het diagram
    graph = create_dependency_diagram(etlocal_key)
    
    # Toon het diagram (werkt alleen in Jupyter)
    graph
